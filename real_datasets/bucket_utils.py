import numpy as np
import scipy.sparse as sp


DEFAULT_BUCKET_SEED_SAMPLE_SEED = 42


def sample_bucket_seeds(n_seeds=5, sample_seed=DEFAULT_BUCKET_SEED_SAMPLE_SEED):
    """Sample bucket seeds reproducibly from a fixed RNG seed."""
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


def lift_bucket_vector(v_bucket, bucket_info):
    """Lift a vector from bucket space back to the original feature space."""
    if bucket_info is None:
        return np.asarray(v_bucket)

    bucket_of_feature, bucket_sizes = bucket_info
    return np.asarray(v_bucket)[bucket_of_feature] / np.sqrt(
        bucket_sizes[bucket_of_feature]
    )


def max_sparsity(X):
    """Maximum row/column sparsity used by the existing space formulas."""
    X = sp.csr_matrix(X)
    row_sparsity = int(X.getnnz(axis=1).max()) if X.shape[0] else 0
    col_sparsity = int(X.getnnz(axis=0).max()) if X.shape[1] else 0
    return max(row_sparsity, col_sparsity)
