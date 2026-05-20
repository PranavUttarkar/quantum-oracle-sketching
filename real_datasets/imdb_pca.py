import argparse
import json

import bucket_utils
import imdb_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

np.random.seed(42)

# Same Plotting Style as 20NG
plt.rcParams.update(
    {
        "font.family": "sans",
        "font.serif": ["Google Sans"],
        "mathtext.fontset": "stix",
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "figure.figsize": (3.5, 2.5),
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
        "legend.frameon": True,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 3,
        "ytick.major.size": 3,
    }
)

# Min DF Sweep Range - Optimized for even spacing
min_dfs = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    11,
    12,
    14,
    16,
    19,
    21,
    24,
    28,
    32,
    36,
    42,
    48,
    55,
    62,
    71,
    81,
    93,
    106,
    122,
    139,
    159,
    181,
    207,
    236,
    270,
    308,
    352,
    402,
    459,
    524,
    599,
    684,
    781,
    891,
    1018,
    1162,
    1327,
    1515,
    1730,
    1976,
    2256,
    2576,
    2941,
    3358,
    3835,
    4379,
    5000,
]
bucket_n_features = [
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    49152,
    65536,
    81000,
]
n_bucket_seeds = 5
num_markers = 40

colors = {
    "quantum": "#CD591A",
    "streaming": "#2657AF",
    "sparse": "#606060",
}
labels = {
    "streaming": "Classical streaming",
    "sparse": "Classical sparse / QRAM",
    "quantum": "Quantum oracle sketching",
}
markers = {"streaming": "P", "sparse": "X", "quantum": "D"}
figsize = (3.5, 3.5)
markersize = {"streaming": 50, "sparse": 50, "quantum": 30}
linewidth_marker = {"streaming": 0, "sparse": 0, "quantum": 0}


def get_pca_results_full():
    # 1. Load Data (Full IMDB)
    raw_documents, _ = imdb_utils.load_imdb_data()

    # 2. Compute "Ground Truth" (Full Dimension)
    print("Vectorizing Full Dimension Reference (min_df=1)...")
    full_vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
    X_full = full_vectorizer.fit_transform(raw_documents)
    # X_full.eliminate_zeros() # Often slower for very large matrices if not needed

    print("Computing Top Singular Vector (Ground Truth)...")
    # Note: We use X_full.asfptype() to ensure float compatibility for svds
    _, _, vt_full = svds(X_full.asfptype(), k=1)
    v_full = vt_full[0]  # type: ignore # Shape (D,)

    # Max Norm Squared (energy of the top component)
    var_max = np.linalg.norm(X_full @ v_full) ** 2

    # Vocabulary map
    vocab_full = full_vectorizer.vocabulary_
    D_full = X_full.shape[1]

    # Storage
    results = {
        "min_dfs": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "variance_recovery": [],
    }

    tqdm.write("Sweeping min_df for Full IMDB...")

    for mdf in tqdm(min_dfs, desc="min_df Sweep"):
        vectorizer = TfidfVectorizer(min_df=mdf, stop_words="english")
        X_trunc = vectorizer.fit_transform(raw_documents)
        # X_trunc.eliminate_zeros()

        shape = X_trunc.get_shape()
        feature_dim = shape[1]
        num_samples = shape[0]

        # Sparsity calculation
        row_sparsity = int(X_trunc.getnnz(axis=1).max())
        col_sparsity = int(X_trunc.getnnz(axis=0).max())
        sparsity = max(row_sparsity, col_sparsity)

        # --- Space Calculations ---
        space_stream = feature_dim
        space_sparse = X_trunc.getnnz()

        # Quantum Space Calculation
        space_quantum = (
            2 * np.ceil(np.log2(num_samples + feature_dim))
            + np.ceil(np.log2(sparsity))
            + 4
        )

        # --- SVD Calculation (Sparse) ---
        # Compute Top Singular Vector in Truncated Space
        _, _, vt_trunc = svds(X_trunc.asfptype(), k=1)
        v_trunc = vt_trunc[0]  # type: ignore # Shape (D,)

        # --- Variance Recovery Calculation ---
        # Lift to Full Space
        v_lifted = np.zeros(D_full)  # type: ignore

        # Fast Lifting
        # 1. Get feature names of truncated
        trunc_feature_names = vectorizer.get_feature_names_out()
        # 2. Get corresponding indices in full vocab
        #    Many words will be present since min_df > 1 implies present in min_df=1
        full_indices = []
        trunc_indices = []

        for i, word in enumerate(trunc_feature_names):
            if word in vocab_full:
                full_indices.append(vocab_full[word])
                trunc_indices.append(i)

        v_lifted[full_indices] = v_trunc[trunc_indices]

        # Normalize lifted vector (unit direction)
        norm = np.linalg.norm(v_lifted)
        v_lifted = v_lifted / norm

        # Variance (Energy) Captured
        var_captured = np.linalg.norm(X_full @ v_lifted) ** 2  # type: ignore
        recovery = var_captured / var_max

        results["min_dfs"].append(mdf)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["variance_recovery"].append(recovery)

    return results


def get_pca_results_bucket(bucket_seeds):
    # 1. Load and vectorize the full min_df=1 data once.
    raw_documents, _ = imdb_utils.load_imdb_data()

    print("Vectorizing Full Dimension Reference (min_df=1)...")
    vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
    X_full = vectorizer.fit_transform(raw_documents)

    print("Computing Top Singular Vector (Ground Truth)...")
    _, _, vt_full = svds(X_full.asfptype(), k=1)
    v_full = vt_full[0]  # type: ignore
    var_max = np.linalg.norm(X_full @ v_full) ** 2

    full_dim = X_full.shape[1]
    n_features_list = [k for k in bucket_n_features if k < full_dim] + [full_dim]

    results = {
        "n_features": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "space_streaming_by_seed": [],
        "space_sparse_by_seed": [],
        "space_quantum_by_seed": [],
        "variance_recovery": [],
        "variance_recovery_sem": [],
        "variance_recovery_by_seed": [],
    }

    tqdm.write("Sweeping bucket dimension for Full IMDB...")

    for n_features in tqdm(n_features_list, desc="bucket Sweep"):
        seed_space_streaming = []
        seed_space_sparse = []
        seed_space_quantum = []
        seed_recoveries = []

        for seed in bucket_seeds:
            X_bucket, bucket_info = bucket_utils.bucket_features(
                X_full, n_features, seed=seed
            )

            feature_dim = X_bucket.shape[1]
            num_samples = X_bucket.shape[0]
            sparsity = bucket_utils.max_sparsity(X_bucket)

            # Same machine-size formulas as the rare-feature path; bucket only changes X.
            seed_space_streaming.append(feature_dim)
            seed_space_sparse.append(X_bucket.getnnz())
            seed_space_quantum.append(
                2 * np.ceil(np.log2(num_samples + feature_dim))
                + np.ceil(np.log2(sparsity))
                + 4
            )

            if bucket_info is None:
                seed_recoveries.append(1.0)
            else:
                _, _, vt_bucket = svds(X_bucket.asfptype(), k=1)
                v_bucket = vt_bucket[0]  # type: ignore
                v_lifted = bucket_utils.lift_bucket_vector(v_bucket, bucket_info)
                v_lifted = v_lifted / np.linalg.norm(v_lifted)
                var_captured = np.linalg.norm(X_full @ v_lifted) ** 2
                seed_recoveries.append(var_captured / var_max)

        results["n_features"].append(n_features)
        results["space_streaming"].append(np.mean(seed_space_streaming))
        results["space_sparse"].append(np.mean(seed_space_sparse))
        results["space_quantum"].append(np.mean(seed_space_quantum))
        results["space_streaming_by_seed"].append(seed_space_streaming)
        results["space_sparse_by_seed"].append(seed_space_sparse)
        results["space_quantum_by_seed"].append(seed_space_quantum)
        rec_mean, rec_sem = bucket_utils.mean_and_sem(seed_recoveries)
        results["variance_recovery"].append(rec_mean)
        results["variance_recovery_sem"].append(rec_sem)
        results["variance_recovery_by_seed"].append(seed_recoveries)

    return results


def plot_parametric_hybrid(
    x_mean,
    x_sem,
    y_mean,
    color,
    marker,
    label,
    linewidth,
    marker_size,
    show_all_markers=False,
):
    x_vals = np.array(x_mean)
    y_vals = np.array(y_mean)
    x_errs = np.array(x_sem)

    if np.any(x_errs > 0):
        plt.fill_betweenx(
            y_vals,
            x_vals - x_errs,
            x_vals + x_errs,
            color=color,
            alpha=0.2,
            edgecolor="none",
        )

    plt.plot(x_vals, y_vals, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    if show_all_markers:
        marker_indices = np.arange(len(x_vals))
    else:
        x_min, x_max = np.min(x_vals), np.max(x_vals)
        target_x = np.linspace(x_min, x_max, num=num_markers)
        marker_indices = []
        for tx in target_x:
            idx = (np.abs(x_vals - tx)).argmin()
            if idx not in marker_indices:
                marker_indices.append(idx)
        marker_indices += [-2, -5, -10, -15, -19, -24]

    plt.scatter(
        x_vals[marker_indices],
        y_vals[marker_indices],
        marker=marker,
        color=color,
        label=label,
        alpha=0.9,
        s=marker_size,
        linewidth=linewidth,
    )


def get_sorted_arrays_with_sem(x_mean, x_sem, y_mean):
    data = sorted(zip(x_mean, x_sem, y_mean), key=lambda x: x[2])
    return (
        np.array([d[0] for d in data]),
        np.array([d[1] for d in data]),
        np.array([d[2] for d in data]),
    )


def run_analysis(load_file=None, mode=None, n_bucket_seeds=n_bucket_seeds):
    if mode not in ("rare", "bucket"):
        raise ValueError("mode must be 'rare' or 'bucket'")

    keys = ["streaming", "sparse", "quantum"]

    if load_file is not None:
        print(f"Loading analysis from {load_file}...")
        with open(load_file, "r") as f:
            data = json.load(f)
        # Extract data directly
        raw_key = "raw_data_by_n_features" if mode == "bucket" else "raw_data_by_min_df"
        raw_data = data[raw_key]
        # Convert keys to int and sort
        params = sorted([int(k) for k in raw_data.keys()])

        final_stats = {
            k: {"mean_space": [], "mean_var": [], "sem_var": []} for k in keys
        }

        for param in params:
            for k in keys:
                entry = raw_data[str(param)][k]
                final_stats[k]["mean_space"].append(entry["space"])
                if "variance_recovery_by_seed" in entry:
                    rec_mean, rec_sem = bucket_utils.mean_and_sem(
                        entry["variance_recovery_by_seed"]
                    )
                else:
                    rec_mean = entry["variance_recovery"]
                    rec_sem = entry.get("variance_recovery_sem", 0.0)
                final_stats[k]["mean_var"].append(rec_mean)
                final_stats[k]["sem_var"].append(rec_sem)

    else:
        if mode == "bucket":
            print("Running PCA Analysis on bucketed IMDB Dataset...")
            bucket_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
            print(f"Averaging over bucket seeds: {bucket_seeds}")
            results = get_pca_results_bucket(bucket_seeds=bucket_seeds)
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
            output_json = "imdb_bucket_size_vs_variance.json"
            dataset_name = "IMDB Full (bucket)"
        else:
            print("Running Analysis on Full IMDB Dataset...")
            results = get_pca_results_full()
            param_name = "min_dfs"
            raw_key = "raw_data_by_min_df"
            output_json = "imdb_size_vs_variance.json"
            dataset_name = "IMDB Full"

        # Reshape into final_stats format for plotting and saving
        final_stats = {
            k: {"mean_space": [], "mean_var": [], "sem_var": []} for k in keys
        }

        data_to_save = {"dataset": dataset_name, raw_key: {}}
        if mode == "bucket":
            data_to_save["bucket_seeds"] = bucket_seeds
            data_to_save["bucket_n_features"] = bucket_n_features
            data_to_save["bucket_seed_sample_seed"] = (
                bucket_utils.DEFAULT_BUCKET_SEED_SAMPLE_SEED
            )

        for i, param in enumerate(results[param_name]):
            param_str = str(param)
            data_to_save[raw_key][param_str] = {}

            for k in keys:
                space = results[f"space_{k}"][i]
                rec = results["variance_recovery"][i]
                rec_sem = (
                    results["variance_recovery_sem"][i] if mode == "bucket" else 0.0
                )

                final_stats[k]["mean_space"].append(space)
                final_stats[k]["mean_var"].append(rec)
                final_stats[k]["sem_var"].append(rec_sem)

                data_to_save[raw_key][param_str][k] = {
                    "space": space,
                    "variance_recovery": rec,
                    "variance_recovery_sem": rec_sem,
                }
                if mode == "bucket":
                    data_to_save[raw_key][param_str][k]["space_by_seed"] = results[
                        f"space_{k}_by_seed"
                    ][i]
                    data_to_save[raw_key][param_str][k]["variance_recovery_by_seed"] = (
                        results["variance_recovery_by_seed"][i]
                    )

        with open(output_json, "w") as f:
            json.dump(data_to_save, f, indent=2)
        print(f"Saved raw data to {output_json}")

    # Plot
    plt.figure(figsize=figsize)
    for k in keys:
        xm, xs, ym = get_sorted_arrays_with_sem(
            final_stats[k]["mean_var"],
            final_stats[k]["sem_var"],
            final_stats[k]["mean_space"],
        )
        plot_parametric_hybrid(
            xm,
            xs,
            ym,
            colors[k],
            markers[k],
            labels[k],
            linewidth_marker[k],
            markersize[k],
            show_all_markers=(mode == "bucket"),
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]
    ax = plt.gca()
    if mode == "bucket":
        plt.text(
            0.2,
            0.85,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        plt.text(
            0.9,
            0.70,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
        )
        plt.text(
            0.15,
            0.04,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
    else:
        plt.text(
            0.75,
            4e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.99,
            9e4,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            1,
            1.9e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.ylim(1e1, 1e7)
    plt.xlabel("Relative explained variance")
    if mode == "bucket":
        plt.xticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
        plt.xlim(-0.1, 1.1)
    else:
        plt.xticks(
            [0.75, 0.8, 0.85, 0.9, 0.95, 1.0],
            ["75%", "80%", "85%", "90%", "95%", "100%"],
        )
        plt.xlim(0.73, 1.03)
    plt.tick_params(direction="in", which="both", top=False, right=True)
    ax.set_ylabel("Machine size")
    ax.tick_params(axis="y")
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Dimension reduction")
    plt.tight_layout()
    output_pdf = (
        "imdb_bucket_size_vs_variance.pdf"
        if mode == "bucket"
        else "imdb_size_vs_variance.pdf"
    )
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="IMDB Machine Size vs Variance Analysis"
    )
    parser.add_argument(
        "--load", type=str, default=None, help="Load analysis data from JSON file"
    )
    parser.add_argument(
        "--mode",
        choices=["rare", "bucket"],
        required=True,
        help="rare: original rare-feature truncation; bucket: random feature buckets",
    )
    parser.add_argument("--n-bucket-seeds", type=int, default=n_bucket_seeds)
    args = parser.parse_args()

    run_analysis(
        load_file=args.load, mode=args.mode, n_bucket_seeds=args.n_bucket_seeds
    )
