import argparse
import json

import bucket_utils
import dorothea_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from tqdm import tqdm

np.random.seed(42)

# Plotting Style
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

# Min DF Sweep Range
min_dfs = [
    1,
    2,
    5,
    12,
    19,
    26,
    34,
    43,
    55,
    69,
    82,
    90,
    97,
    114,
    128,
    143,
    164,
    197,
    226,
    240,
    308,
]
bucket_n_features = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
jl_n_features = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
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
    # 1. Load Data
    print("Loading Dorothea data...")
    try:
        X_full, _ = dorothea_utils.load_dorothea_data(valid=True)
    except FileNotFoundError:
        print("Valid set issues, loading only train")
        X_full, _ = dorothea_utils.load_dorothea_data(valid=False)

    X_full = X_full.astype(np.float64)

    # 2. Compute "Ground Truth" (Full Dimension)
    print("Computing Top Singular Vector (Ground Truth)...")
    # Dorothea is 1150 x 100000. SVD is feasible.
    try:
        _, _, vt_full = svds(X_full, k=1)
        v_full = vt_full[0]  # type: ignore # Shape (D,)
    except Exception as e:
        print(f"SVD failed: {e}")
        raise e

    # Max Norm Squared
    var_max = np.linalg.norm(X_full @ v_full) ** 2

    # Pre-compute document frequencies
    print("Computing document frequencies...")
    X_bin = X_full.copy()
    X_bin.data[:] = 1
    doc_freqs = np.array(X_bin.sum(axis=0)).flatten()
    del X_bin

    results = {
        "min_dfs": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "variance_recovery": [],
    }

    tqdm.write("Sweeping min_df for Dorothea...")

    for mdf in tqdm(min_dfs, desc="min_df Sweep"):
        keep_mask = doc_freqs >= mdf
        keep_indices = np.where(keep_mask)[0]

        if len(keep_indices) == 0:
            print(f"Skipping min_df={mdf} (0 features kept)")
            continue

        X_trunc = X_full[:, keep_indices]  # type: ignore

        shape = X_trunc.shape
        feature_dim = shape[1]
        num_samples = shape[0]

        row_sparsity = int(X_trunc.getnnz(axis=1).max()) if shape[0] > 0 else 0
        col_sparsity = int(X_trunc.getnnz(axis=0).max()) if shape[1] > 0 else 0
        sparsity = max(row_sparsity, col_sparsity)

        space_stream = feature_dim
        space_sparse = X_trunc.getnnz()
        space_quantum = (
            2 * np.ceil(np.log2(num_samples + feature_dim + 1))
            + np.ceil(np.log2(sparsity + 1))
            + 4
        )

        if min(shape) <= 1:
            if shape[1] == 1:
                # 1 feature: direction is [1.0]
                v_trunc = np.array([1.0])
            else:
                print(f"Skipping min_df={mdf} (Dimensions too small: {shape})")
                continue
        else:
            try:
                _, _, vt_trunc = svds(X_trunc, k=1)
                v_trunc = vt_trunc[0]  # type: ignore
            except Exception as e:
                print(f"SVD failed for shape {shape}: {e}")
                continue

        v_lifted = np.zeros(X_full.shape[1])  # type: ignore
        v_lifted[keep_indices] = v_trunc
        norm = np.linalg.norm(v_lifted)
        v_lifted = v_lifted / norm

        var_captured = np.linalg.norm(X_full @ v_lifted) ** 2
        recovery = var_captured / var_max

        results["min_dfs"].append(mdf)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["variance_recovery"].append(recovery)

    return results


def get_pca_results_bucket(bucket_seeds, truncation_mode="bucket"):
    print("Loading Dorothea data...")
    try:
        X_full, _ = dorothea_utils.load_dorothea_data(valid=True)
    except FileNotFoundError:
        print("Valid set issues, loading only train")
        X_full, _ = dorothea_utils.load_dorothea_data(valid=False)

    X_full = X_full.astype(np.float64)

    print("Computing Top Singular Vector (Ground Truth)...")
    _, _, vt_full = svds(X_full, k=1)
    v_full = vt_full[0]  # type: ignore
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

    tqdm.write(f"Sweeping {truncation_mode} dimension for Dorothea...")

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
                2 * np.ceil(np.log2(num_samples + feature_dim + 1))
                + np.ceil(np.log2(sparsity + 1))
                + 4
            )

            if truncation_info is None:
                seed_recoveries.append(1.0)
            else:
                _, _, vt_bucket = svds(bucket_utils.svds_input(X_bucket), k=1)
                v_bucket = vt_bucket[0]  # type: ignore
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

    plt.scatter(
        x_vals,
        y_vals,
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

    if load_file:
        print(f"Loading analysis from {load_file}...")
        with open(load_file, "r") as f:
            data_to_save = json.load(f)
        bucket_utils.validate_truncation_data(data_to_save, mode, load_file)
        raw_key = (
            "raw_data_by_n_features"
            if mode in ("bucket", "jl")
            else "raw_data_by_min_df"
        )
        raw_data = data_to_save[raw_key]
        params = sorted([int(k) for k in raw_data.keys()])

        final_stats = {
            k: {"mean_space": [], "mean_var": [], "sem_var": []} for k in keys
        }
        for param in params:
            entry = raw_data[str(param)]
            for k in keys:
                method_entry = entry[k]

                final_stats[k]["mean_space"].append(method_entry["space"])
                if "variance_recovery_by_seed" in method_entry:
                    rec_mean, rec_sem = bucket_utils.mean_and_sem(
                        method_entry["variance_recovery_by_seed"]
                    )
                else:
                    rec_mean = method_entry["variance_recovery"]
                    rec_sem = method_entry.get("variance_recovery_sem", 0.0)
                final_stats[k]["mean_var"].append(rec_mean)
                final_stats[k]["sem_var"].append(rec_sem)

    else:
        if mode in ("bucket", "jl"):
            if mode == "bucket":
                print("Running PCA Analysis on bucketed Dorothea Dataset...")
                feature_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
                output_json = "dorothea_bucket_size_vs_variance.json"
                dataset_name = "Dorothea (bucket)"
            else:
                print("Running PCA Analysis on Sparse-JL-projected Dorothea Dataset...")
                feature_seeds = bucket_utils.sample_jl_seeds(n_bucket_seeds)
                output_json = "dorothea_jl_size_vs_variance.json"
                dataset_name = "Dorothea (sparse JL)"
            print(f"Averaging over random feature seeds: {feature_seeds}")
            results = get_pca_results_bucket(
                bucket_seeds=feature_seeds, truncation_mode=mode
            )
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
        else:
            print("Running Analysis on Dorothea Dataset...")
            results = get_pca_results_full()
            param_name = "min_dfs"
            raw_key = "raw_data_by_min_df"
            output_json = "dorothea_size_vs_variance.json"
            dataset_name = "Dorothea"

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

        final_stats = {
            k: {"mean_space": [], "mean_var": [], "sem_var": []} for k in keys
        }

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
                    data_to_save[raw_key][param_str][k][
                        "variance_recovery_by_seed"
                    ] = results["variance_recovery_by_seed"][i]

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
        ind = (xm >= 0.1) * (xm <= 1)
        xm = xm[ind]
        xs = xs[ind]
        ym = ym[ind]
        plot_parametric_hybrid(
            xm,
            xs,
            ym,
            colors[k],
            markers[k],
            (streaming_label_for_mode(mode) if k == "streaming" else labels[k]),
            linewidth_marker[k],
            markersize[k],
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]
    ax = plt.gca()
    if mode in ("bucket", "jl"):
        streaming_label_x, streaming_label_y, streaming_label_ha = (
            (0.7, 0.76, "right") if mode == "jl" else (0.22, 0.5, "left")
        )
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
            0.035,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
    else:
        plt.text(
            0.15,
            8e5,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.9,
            4e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            1,
            1.4e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.ylim(1e1, 2e6)
    plt.xlabel("Relative explained variance")
    if mode in ("bucket", "jl"):
        plt.xlim(0.35, 1.05)
        plt.xticks([0.4, 0.6, 0.8, 1.0], ["40%", "60%", "80%", "100%"])
    else:
        plt.xticks(
            [0.2, 0.4, 0.6, 0.8, 1.0],
            ["20%", "40%", "60%", "80%", "100%"],
        )
        plt.xlim(0.08, 1.05)
    plt.tick_params(direction="in", which="both", top=False, right=True)
    ax.set_ylabel("Machine size")
    ax.tick_params(axis="y")

    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Dimension reduction")
    plt.tight_layout()
    if mode == "bucket":
        output_pdf = "dorothea_bucket_size_vs_variance.pdf"
    elif mode == "jl":
        output_pdf = "dorothea_jl_size_vs_variance.pdf"
    else:
        output_pdf = "dorothea_size_vs_variance.pdf"
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dorothea Machine Size vs Variance Analysis"
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
