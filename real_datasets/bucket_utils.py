import numpy as np
import scipy.sparse as sp


DEFAULT_BUCKET_SEED_SAMPLE_SEED = 42
DEFAULT_JL_SEED_SAMPLE_SEED = DEFAULT_BUCKET_SEED_SAMPLE_SEED
SPARSE_JL_TRANSFORM = "balanced_signed_bucket"


def sample_bucket_seeds(n_seeds=5, sample_seed=DEFAULT_BUCKET_SEED_SAMPLE_SEED):
    """Sample bucket seeds reproducibly from a fixed RNG seed."""
    rng = np.random.default_rng(sample_seed)
    return [int(seed) for seed in rng.integers(0, 2**32 - 1, size=n_seeds)]


def sample_jl_seeds(n_seeds=5, sample_seed=DEFAULT_JL_SEED_SAMPLE_SEED):
    """Sample JL projection seeds reproducibly from a fixed RNG seed."""
    rng = np.random.default_rng(sample_seed)
    return [int(seed) for seed in rng.integers(0, 2**32 - 1, size=n_seeds)]


def mean_and_sem(values):
    """Mean and SEM over all scalar values in a nested list/array."""
    vals = np.array(values, dtype=float).reshape(-1)
    return float(np.mean(vals)), float(np.std(vals) / np.sqrt(vals.size))


def bucket_features(X, n_buckets, seed=42):
    """Merge D original features into n_buckets random balanced buckets.

    The bucketed feature is the normalized sum of features in that bucket:

        z_b = (1 / sqrt(|B_b|)) * sum_{j in B_b} x_j.

    Equivalently, X_bucket = X P, where P has one nonzero entry per row.
    With the 1/sqrt(|B_b|) normalization, the columns of P are orthonormal
    (P.T @ P = I). For PCA, lift_bucket_vector(v, info) returns P v.

    If n_buckets >= D, no approximation is made and the original matrix is
    returned. This makes the full-dimension endpoint exactly the original data.
    """
    X = sp.csr_matrix(X)
    n_features = X.shape[1]
    n_buckets = min(int(n_buckets), n_features)

    if n_buckets >= n_features:
        return X, None

    rng = np.random.default_rng(seed)
    perm = rng.permutation(n_features)

    bucket_of_feature = np.empty(n_features, dtype=np.int64)
    bucket_sizes = np.zeros(n_buckets, dtype=np.float64)
    for rank, feature in enumerate(perm):
        bucket = rank * n_buckets // n_features
        bucket_of_feature[feature] = bucket
        bucket_sizes[bucket] += 1.0

    weights = 1.0 / np.sqrt(bucket_sizes[bucket_of_feature])
    projection = sp.csr_matrix(
        (weights, (np.arange(n_features), bucket_of_feature)),
        shape=(n_features, n_buckets),
    )

    X_bucket = (X @ projection).tocsr()
    X_bucket.eliminate_zeros()
    return X_bucket, (bucket_of_feature, bucket_sizes)


def sparse_jl_features(X, n_buckets, seed=42):
    """Balanced signed one-sparse JL projection.

    This is the signed version of bucket_features: each original feature is
    assigned to one balanced bucket and multiplied by an independent random
    sign before the bucket sum. The 1/sqrt(bucket size) normalization keeps
    the projection columns orthonormal. If k >= D, the original matrix is
    returned exactly, so the full-dimension endpoint is unchanged.
    """
    X = sp.csr_matrix(X)
    n_features = X.shape[1]
    n_buckets = min(int(n_buckets), n_features)

    if n_buckets >= n_features:
        return X, None

    rng = np.random.default_rng(seed)
    perm = rng.permutation(n_features)
    signs = rng.choice([-1.0, 1.0], size=n_features)

    bucket_of_feature = np.empty(n_features, dtype=np.int64)
    bucket_sizes = np.zeros(n_buckets, dtype=np.float64)
    for rank, feature in enumerate(perm):
        bucket = rank * n_buckets // n_features
        bucket_of_feature[feature] = bucket
        bucket_sizes[bucket] += 1.0

    weights = signs / np.sqrt(bucket_sizes[bucket_of_feature])
    projection = sp.csr_matrix(
        (weights, (np.arange(n_features), bucket_of_feature)),
        shape=(n_features, n_buckets),
    )

    X_jl = (X @ projection).tocsr()
    X_jl.eliminate_zeros()
    return X_jl, (bucket_of_feature, bucket_sizes, signs)


def random_truncated_features(X, n_features, seed=42, mode="bucket"):
    """Apply one of the random feature truncations used in the experiments."""
    if mode == "bucket":
        return bucket_features(X, n_features, seed=seed)
    if mode == "jl":
        return sparse_jl_features(X, n_features, seed=seed)
    raise ValueError("mode must be 'bucket' or 'jl'")


def lift_bucket_vector(v_bucket, bucket_info):
    """Lift a vector from bucket space back to the original feature space."""
    if bucket_info is None:
        return np.asarray(v_bucket)

    bucket_of_feature, bucket_sizes = bucket_info
    return np.asarray(v_bucket)[bucket_of_feature] / np.sqrt(
        bucket_sizes[bucket_of_feature]
    )


def lift_sparse_jl_vector(v_jl, sparse_jl_info):
    """Lift a balanced signed sparse JL vector to original feature space."""
    if sparse_jl_info is None:
        return np.asarray(v_jl)

    bucket_of_feature, bucket_sizes, signs = sparse_jl_info
    return (
        signs
        * np.asarray(v_jl)[bucket_of_feature]
        / np.sqrt(bucket_sizes[bucket_of_feature])
    )


def lift_truncated_vector(v_truncated, truncation_info, mode="bucket"):
    """Lift a vector produced by a random feature truncation."""
    if mode == "bucket":
        return lift_bucket_vector(v_truncated, truncation_info)
    if mode == "jl":
        return lift_sparse_jl_vector(v_truncated, truncation_info)
    raise ValueError("mode must be 'bucket' or 'jl'")


def lifted_vector_norm(v_lifted):
    """Norm used when evaluating a lifted PCA direction.

    All current lifts live directly in the original feature space. For sparse
    JL, lift_sparse_jl_vector applies the same signed projection used to form
    the bucketed matrix.
    """
    return np.linalg.norm(v_lifted)


def validate_truncation_data(data, mode, path="loaded JSON"):
    """Reject stale or mismatched cached numerics before plotting."""
    feature_mode = mode in ("bucket", "jl")
    has_feature_sweep = "raw_data_by_n_features" in data
    if has_feature_sweep != feature_mode:
        raise ValueError(f"{path} does not match --mode {mode}")

    if not feature_mode:
        return

    legacy_nonbucket_keys = {
        "jl_transform",
        "jl_seeds",
    }
    if (
        mode == "bucket"
        and data.get("truncation_mode") in (None, "bucket")
        and not any(k in data for k in legacy_nonbucket_keys)
    ):
        return
    if data.get("truncation_mode") != mode:
        raise ValueError(f"{path} has truncation_mode={data.get('truncation_mode')!r}")
    if mode == "jl" and data.get("jl_transform") != SPARSE_JL_TRANSFORM:
        raise ValueError(f"{path} was not generated with balanced signed sparse JL")


def matrix_nnz(X):
    """Number of stored/nonzero entries for space accounting."""
    if sp.issparse(X):
        return int(X.getnnz())
    return int(np.size(X))


def svds_input(X):
    """Return a float matrix accepted by scipy.sparse.linalg.svds."""
    if sp.issparse(X):
        return X.asfptype()
    X = np.asarray(X)
    if np.issubdtype(X.dtype, np.floating):
        return X
    return X.astype(np.float32)


def max_sparsity(X):
    """Maximum row/column sparsity used by the existing space formulas."""
    if not sp.issparse(X):
        return max(X.shape) if np.size(X) else 0

    X = sp.csr_matrix(X)
    row_sparsity = int(X.getnnz(axis=1).max()) if X.shape[0] else 0
    col_sparsity = int(X.getnnz(axis=0).max()) if X.shape[1] else 0
    return max(row_sparsity, col_sparsity)
