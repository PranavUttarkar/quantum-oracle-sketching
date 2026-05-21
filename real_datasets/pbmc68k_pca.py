import argparse
import json

import bucket_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pbmc68k_utils
from scipy.sparse.linalg import svds
from tqdm import tqdm

np.random.seed(42)

# Same Plotting Style
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

# min_samples sweep - similar to min_df
min_samples_list = pbmc68k_utils.get_min_samples_sweep()
bucket_n_features = [
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    12288,
    16384,
    20000,
    24576,
    29491,
]
jl_n_features = bucket_n_features
n_bucket_seeds = 5
n_jl_seeds = 5
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


def streaming_label_for_mode(mode):
    if mode == "bucket":
        return "Classical feature hashing"
    if mode == "jl":
        return "Classical sparse JL"
    return labels["streaming"]


def get_pca_results_full():
    # 1. Load Full Data (binary classification)
    tqdm.write("Loading PBMC68k dataset (binary classification)...")
    X_full, y, label_names = pbmc68k_utils.load_pbmc68k_data(
        min_samples=1, normalize=True, binary=False
    )
    tqdm.write(f"Dataset shape: {X_full.shape}, Classes: {label_names}")

    # Compute "Ground Truth" (Full Dimension)
    tqdm.write("Computing Top Singular Vector (Ground Truth)...")
    _, _, vt_full = svds(X_full.asfptype(), k=1)
    v_full = vt_full[0]

    # Max Norm Squared (energy of the top component)
    var_max = np.linalg.norm(X_full @ v_full) ** 2
    D_full = X_full.shape[1]

    # Storage
    results = {
        "min_samples": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "variance_recovery": [],
    }

    tqdm.write("Sweeping min_samples for PBMC68k...")

    for min_samp in tqdm(min_samples_list, desc="min_samples Sweep"):
        # Filter genes by min_samples
        X_trunc, gene_indices = pbmc68k_utils.filter_genes_by_frequency(
            X_full, min_samp
        )

        # Skip if no genes remain
        if X_trunc.shape[1] == 0:
            continue

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

        space_quantum = (
            2 * np.ceil(np.log2(num_samples + feature_dim))
            + np.ceil(np.log2(sparsity))
            + 4
        )

        # --- SVD Calculation (Sparse) ---
        _, _, vt_trunc = svds(X_trunc.asfptype(), k=1)
        v_trunc = vt_trunc[0]

        # --- Variance Recovery Calculation ---
        # Lift to Full Space
        v_lifted = np.zeros(D_full)
        v_lifted[gene_indices] = v_trunc

        # Normalize lifted vector
        norm = np.linalg.norm(v_lifted)
        v_lifted = v_lifted / norm

        # Variance (Energy) Captured
        var_captured = np.linalg.norm(X_full @ v_lifted) ** 2
        recovery = var_captured / var_max

        results["min_samples"].append(min_samp)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["variance_recovery"].append(recovery)

    return results


def get_pca_results_bucket(bucket_seeds, truncation_mode="bucket"):
    tqdm.write("Loading PBMC68k dataset...")
    X_full, y, label_names = pbmc68k_utils.load_pbmc68k_data(
        min_samples=1, normalize=True, binary=False
    )
    tqdm.write(f"Dataset shape: {X_full.shape}, Classes: {label_names}")

    tqdm.write("Computing Top Singular Vector (Ground Truth)...")
    _, _, vt_full = svds(X_full.asfptype(), k=1)
    v_full = vt_full[0]
    var_max = np.linalg.norm(X_full @ v_full) ** 2

    full_dim = X_full.shape[1]
    feature_grid = jl_n_features if truncation_mode == "jl" else bucket_n_features
    n_features_list = [k for k in feature_grid if k < full_dim] + [full_dim]

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

    tqdm.write(f"Sweeping {truncation_mode} dimension for PBMC68k...")

    for n_features in tqdm(n_features_list, desc=f"{truncation_mode} Sweep"):
        seed_space_streaming = []
        seed_space_sparse = []
        seed_space_quantum = []
        seed_recoveries = []

        for seed in bucket_seeds:
            X_bucket, truncation_info = bucket_utils.random_truncated_features(
                X_full, n_features, seed=seed, mode=truncation_mode
            )

            feature_dim = X_bucket.shape[1]
            num_samples = X_bucket.shape[0]
            sparsity = bucket_utils.max_sparsity(X_bucket)

            # Same machine-size formulas as the rare-feature path, applied to X_bucket.
            seed_space_streaming.append(feature_dim)
            seed_space_sparse.append(bucket_utils.matrix_nnz(X_bucket))
            seed_space_quantum.append(
                2 * np.ceil(np.log2(num_samples + feature_dim))
                + np.ceil(np.log2(sparsity))
                + 4
            )

            if truncation_info is None:
                seed_recoveries.append(1.0)
            else:
                _, _, vt_bucket = svds(bucket_utils.svds_input(X_bucket), k=1)
                v_bucket = vt_bucket[0]
                v_lifted = bucket_utils.lift_truncated_vector(
                    v_bucket, truncation_info, mode=truncation_mode
                )
                lifted_norm = bucket_utils.lifted_vector_norm(
                    v_lifted
                )
                v_lifted = v_lifted / lifted_norm
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
        marker_indices += [-5, -10, -15, -20]

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
    if mode not in ("rare", "bucket", "jl"):
        raise ValueError("mode must be 'rare', 'bucket', or 'jl'")

    keys = ["streaming", "sparse", "quantum"]

    if load_file is not None:
        print(f"Loading analysis from {load_file}...")
        with open(load_file, "r") as f:
            data = json.load(f)
        bucket_utils.validate_truncation_data(data, mode, load_file)
        raw_key = (
            "raw_data_by_n_features"
            if mode in ("bucket", "jl")
            else "raw_data_by_min_samples"
        )
        raw_data = data[raw_key]
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
        if mode in ("bucket", "jl"):
            if mode == "bucket":
                print("Running PCA Analysis on bucketed PBMC68k Dataset...")
                feature_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
                output_json = "pbmc68k_bucket_size_vs_variance.json"
                dataset_name = "PBMC68k (bucket)"
            else:
                print("Running PCA Analysis on Sparse-JL-projected PBMC68k Dataset...")
                feature_seeds = bucket_utils.sample_jl_seeds(n_bucket_seeds)
                output_json = "pbmc68k_jl_size_vs_variance.json"
                dataset_name = "PBMC68k (sparse JL)"
            print(f"Averaging over random feature seeds: {feature_seeds}")
            results = get_pca_results_bucket(
                bucket_seeds=feature_seeds, truncation_mode=mode
            )
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
        else:
            print("Running PCA Analysis on PBMC68k Dataset (Binary Classification)...")
            results = get_pca_results_full()
            param_name = "min_samples"
            raw_key = "raw_data_by_min_samples"
            output_json = "pbmc68k_size_vs_variance.json"
            dataset_name = "PBMC68k (Binary)"

        final_stats = {
            k: {"mean_space": [], "mean_var": [], "sem_var": []} for k in keys
        }

        data_to_save = {"dataset": dataset_name, raw_key: {}}
        if mode == "bucket":
            data_to_save["truncation_mode"] = "bucket"
            data_to_save["bucket_seeds"] = feature_seeds
            data_to_save["bucket_n_features"] = results["n_features"]
            data_to_save["bucket_seed_sample_seed"] = (
                bucket_utils.DEFAULT_BUCKET_SEED_SAMPLE_SEED
            )
        elif mode == "jl":
            data_to_save["truncation_mode"] = "jl"
            data_to_save["jl_seeds"] = feature_seeds
            data_to_save["jl_n_features"] = results["n_features"]
            data_to_save["jl_seed_sample_seed"] = (
                bucket_utils.DEFAULT_JL_SEED_SAMPLE_SEED
            )
            data_to_save["jl_transform"] = bucket_utils.SPARSE_JL_TRANSFORM

        for i, param in enumerate(results[param_name]):
            param_str = str(param)
            data_to_save[raw_key][param_str] = {}

            for k in keys:
                space = results[f"space_{k}"][i]
                rec = results["variance_recovery"][i]
                rec_sem = (
                    results["variance_recovery_sem"][i]
                    if mode in ("bucket", "jl")
                    else 0.0
                )

                final_stats[k]["mean_space"].append(space)
                final_stats[k]["mean_var"].append(rec)
                final_stats[k]["sem_var"].append(rec_sem)

                data_to_save[raw_key][param_str][k] = {
                    "space": space,
                    "variance_recovery": rec,
                    "variance_recovery_sem": rec_sem,
                }
                if mode in ("bucket", "jl"):
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
            (streaming_label_for_mode(mode) if k == "streaming" else labels[k]),
            linewidth_marker[k],
            markersize[k],
            show_all_markers=(mode in ("bucket", "jl")),
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]

    ax = plt.gca()
    if mode in ("bucket", "jl"):
        streaming_label_x, streaming_label_y, streaming_label_ha = (
            (0.9, 0.45, "right") if mode == "jl" else (0.9, 0.62, "right")
        )
        plt.text(
            0.2,
            0.9,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        plt.text(
            streaming_label_x,
            streaming_label_y,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha=streaming_label_ha,
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
            1,
            1e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            0.996,
            1.2e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            1,
            1.7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.ylim(1e1, 1e7)
    plt.xlabel("Relative explained variance")

    if mode in ("bucket", "jl"):
        plt.xticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
        plt.xlim(-0.1, 1.1)
    else:
        plt.xticks(
            [0.92, 0.94, 0.96, 0.98, 1],
            ["92%", "94%", "96%", "98%", "100%"],
        )
        plt.xlim(0.915, 1.005)

    plt.tick_params(direction="in", which="both", top=False, right=True)
    ax.set_ylabel("Machine size")
    ax.tick_params(axis="y")
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Dimension reduction")
    plt.tight_layout()
    if mode == "bucket":
        output_pdf = "pbmc68k_bucket_size_vs_variance.pdf"
    elif mode == "jl":
        output_pdf = "pbmc68k_jl_size_vs_variance.pdf"
    else:
        output_pdf = "pbmc68k_size_vs_variance.pdf"
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PBMC68k Machine Size vs Variance Analysis"
    )
    parser.add_argument(
        "--load", type=str, default=None, help="Load analysis data from JSON file"
    )
    parser.add_argument(
        "--mode",
        choices=["rare", "bucket", "jl"],
        required=True,
        help=(
            "rare: original rare-feature truncation; "
            "bucket: random feature buckets; "
            "jl: balanced signed sparse JL projection"
        ),
    )
    parser.add_argument("--n-bucket-seeds", type=int, default=n_bucket_seeds)
    parser.add_argument("--n-jl-seeds", type=int, default=n_jl_seeds)
    args = parser.parse_args()
    if args.mode == "jl":
        n_random_seeds = args.n_jl_seeds
    else:
        n_random_seeds = args.n_bucket_seeds
    run_analysis(
        load_file=args.load, mode=args.mode, n_bucket_seeds=n_random_seeds
    )
