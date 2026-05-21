import argparse
import json
from itertools import combinations

import bucket_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pbmc68k_utils
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import cross_val_score
from tqdm import tqdm

np.random.seed(42)
N_PAIRS = 100  # Number of random pairs to average over

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
bucket_n_features = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
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


def get_random_pairs(n_classes, n_pairs, rng):
    """Generate n_pairs random pairs from n_classes."""
    all_pairs = list(combinations(range(n_classes), 2))
    indices = rng.choice(len(all_pairs), size=n_pairs, replace=True)
    return [all_pairs[i] for i in indices]


def get_ridge_results_full():
    # 1. Load Full Data (normalized, all genes, all classes)
    tqdm.write("Loading PBMC68k dataset (all classes)...")
    X_full, y_full, label_names = pbmc68k_utils.load_pbmc68k_data(
        min_samples=1, normalize=True, binary=False
    )
    tqdm.write(f"Dataset shape: {X_full.shape}, Classes: {label_names}")

    # 2. Generate random pairs of cell types
    rng = np.random.default_rng(42)
    n_classes = len(label_names)
    pairs = get_random_pairs(n_classes, N_PAIRS, rng)
    tqdm.write(f"Using {len(pairs)} random class pairs for binary classification")
    for i, (c1, c2) in enumerate(pairs):
        tqdm.write(f"  Pair {i + 1}: {label_names[c1]} vs {label_names[c2]}")

    # 3. Sweep min_samples
    results = {
        "min_samples": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "accuracies_mean": [],
        "accuracies_std": [],
        "accuracy_scores_by_pair": [],
        "pairs": [(label_names[c1], label_names[c2]) for c1, c2 in pairs],
    }

    tqdm.write("Sweeping min_samples for PBMC68k (averaged over random pairs)...")

    for min_samp in tqdm(min_samples_list, desc="min_samples Sweep"):
        # Filter genes by min_samples on full data
        X_filtered, gene_indices = pbmc68k_utils.filter_genes_by_frequency(
            X_full, min_samp
        )

        # Skip if no genes remain
        if X_filtered.shape[1] == 0:
            continue

        # Collect results across all pairs
        pair_accuracies = []
        pair_accuracy_scores = []
        pair_space_streaming = []
        pair_space_sparse = []
        pair_space_quantum = []

        for c1, c2 in pairs:
            # Create binary subset for this pair
            mask = (y_full == c1) | (y_full == c2)
            X_pair = X_filtered[mask]
            y_pair = (y_full[mask] == c2).astype(
                int
            )  # Binary labels: 0 for c1, 1 for c2

            shape = X_pair.get_shape()
            feature_dim = shape[1]
            num_samples = shape[0]

            # Sparsity calculation
            row_sparsity = int(X_pair.getnnz(axis=1).max())
            col_sparsity = int(X_pair.getnnz(axis=0).max())
            sparsity = max(row_sparsity, col_sparsity)

            # --- Space Calculations ---
            space_stream = feature_dim
            space_sparse = X_pair.getnnz()
            space_quantum = (
                2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
                + np.ceil(np.log2(sparsity + 1))
                + 4
            )

            # --- Ridge Training & Eval (CV) ---
            clf = RidgeClassifier(
                random_state=42, alpha=200.0, solver="auto", class_weight="balanced"
            )
            # 5-Fold Cross Validation
            scores = cross_val_score(clf, X_pair, y_pair, cv=5)

            pair_accuracies.append(scores.mean())
            pair_accuracy_scores.append([float(s) for s in scores])
            pair_space_streaming.append(space_stream)
            pair_space_sparse.append(space_sparse)
            pair_space_quantum.append(space_quantum)

        # Average across pairs
        acc_mean = np.mean(pair_accuracies)
        # Standard error across pairs (variation between pairs)
        acc_sem = np.std(pair_accuracies) / np.sqrt(len(pair_accuracies))

        # Average space metrics (they vary slightly due to different sample sizes per pair)
        space_streaming_mean = np.mean(pair_space_streaming)
        space_sparse_mean = np.mean(pair_space_sparse)
        space_quantum_mean = np.mean(pair_space_quantum)

        results["min_samples"].append(min_samp)
        results["space_streaming"].append(space_streaming_mean)
        results["space_sparse"].append(space_sparse_mean)
        results["space_quantum"].append(space_quantum_mean)
        results["accuracies_mean"].append(acc_mean)
        results["accuracies_std"].append(acc_sem)
        results["accuracy_scores_by_pair"].append(pair_accuracy_scores)

    return results


def get_ridge_results_bucket(bucket_seeds, truncation_mode="bucket"):
    tqdm.write("Loading PBMC68k dataset (all classes)...")
    X_full, y_full, label_names = pbmc68k_utils.load_pbmc68k_data(
        min_samples=1, normalize=True, binary=False
    )
    tqdm.write(f"Dataset shape: {X_full.shape}, Classes: {label_names}")

    rng = np.random.default_rng(42)
    n_classes = len(label_names)
    pairs = get_random_pairs(n_classes, N_PAIRS, rng)

    full_dim = X_full.shape[1]
    feature_grid = jl_n_features if truncation_mode == "jl" else bucket_n_features
    n_features_list = [k for k in feature_grid if k < full_dim] + [full_dim]

    results = {
        "n_features": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "space_streaming_by_seed_pair": [],
        "space_sparse_by_seed_pair": [],
        "space_quantum_by_seed_pair": [],
        "accuracies_mean": [],
        "accuracies_std": [],
        "accuracy_scores_by_seed_pair": [],
        "pairs": [(label_names[c1], label_names[c2]) for c1, c2 in pairs],
    }

    tqdm.write(f"Sweeping {truncation_mode} dimension for PBMC68k...")

    for n_features in tqdm(n_features_list, desc=f"{truncation_mode} Sweep"):
        seed_pair_accuracy_scores = []
        seed_pair_space_streaming = []
        seed_pair_space_sparse = []
        seed_pair_space_quantum = []

        for seed in bucket_seeds:
            X_bucket_full, _ = bucket_utils.random_truncated_features(
                X_full, n_features, seed=seed, mode=truncation_mode
            )

            this_seed_scores = []
            this_seed_space_streaming = []
            this_seed_space_sparse = []
            this_seed_space_quantum = []

            for c1, c2 in pairs:
                mask = (y_full == c1) | (y_full == c2)
                X_pair = X_bucket_full[mask]
                y_pair = (y_full[mask] == c2).astype(int)

                feature_dim = X_pair.shape[1]
                num_samples = X_pair.shape[0]
                sparsity = bucket_utils.max_sparsity(X_pair)

                # Same machine-size formulas as the rare-feature path, applied to X_pair.
                space_stream = feature_dim
                space_sparse = bucket_utils.matrix_nnz(X_pair)
                space_quantum = (
                    2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
                    + np.ceil(np.log2(sparsity + 1))
                    + 4
                )

                clf = RidgeClassifier(
                    random_state=42, alpha=200.0, solver="auto", class_weight="balanced"
                )
                scores = cross_val_score(clf, X_pair, y_pair, cv=5)

                this_seed_scores.append([float(s) for s in scores])
                this_seed_space_streaming.append(space_stream)
                this_seed_space_sparse.append(space_sparse)
                this_seed_space_quantum.append(space_quantum)

            seed_pair_accuracy_scores.append(this_seed_scores)
            seed_pair_space_streaming.append(this_seed_space_streaming)
            seed_pair_space_sparse.append(this_seed_space_sparse)
            seed_pair_space_quantum.append(this_seed_space_quantum)

        acc_mean, acc_sem = bucket_utils.mean_and_sem(seed_pair_accuracy_scores)

        results["n_features"].append(n_features)
        results["space_streaming"].append(np.mean(seed_pair_space_streaming))
        results["space_sparse"].append(np.mean(seed_pair_space_sparse))
        results["space_quantum"].append(np.mean(seed_pair_space_quantum))
        results["space_streaming_by_seed_pair"].append(seed_pair_space_streaming)
        results["space_sparse_by_seed_pair"].append(seed_pair_space_sparse)
        results["space_quantum_by_seed_pair"].append(seed_pair_space_quantum)
        results["accuracies_mean"].append(acc_mean)
        results["accuracies_std"].append(acc_sem)
        results["accuracy_scores_by_seed_pair"].append(seed_pair_accuracy_scores)

    return results


def plot_parametric_hybrid(
    x_mean,
    x_std,
    y_mean,
    color,
    marker,
    label,
    linewidth,
    marker_size,
):
    y_vals = np.array(y_mean)
    x_vals = np.array(x_mean)
    x_errs = np.array(x_std)

    plt.fill_betweenx(
        y_vals,
        x_vals - x_errs,
        x_vals + x_errs,
        color=color,
        alpha=0.2,
        edgecolor="none",
    )

    # Line
    plt.plot(x_vals, y_vals, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    # # Markers
    # x_min, x_max = np.min(x_vals), np.max(x_vals)
    # target_x = np.linspace(x_min, x_max, num=num_markers)
    # marker_indices = []
    # for tx in target_x:
    #     idx = (np.abs(x_vals - tx)).argmin()
    #     if idx not in marker_indices:
    #         marker_indices.append(idx)

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


def get_sorted_arrays(x_mean, x_std, y_mean):
    data = sorted(zip(x_mean, x_std, y_mean), key=lambda x: x[2])
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
            k: {"mean_space": [], "mean_acc": [], "sem_acc": []} for k in keys
        }
        for param in params:
            for k in keys:
                entry = raw_data[str(param)][k]

                final_stats[k]["mean_space"].append(entry["space"])
                if "accuracy_scores_by_seed_pair" in entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        entry["accuracy_scores_by_seed_pair"]
                    )
                elif "accuracy_scores_by_pair" in entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        entry["accuracy_scores_by_pair"]
                    )
                else:
                    acc_mean = entry["accuracy_mean"]
                    acc_sem = entry["accuracy_sem"]
                final_stats[k]["mean_acc"].append(acc_mean)
                final_stats[k]["sem_acc"].append(acc_sem)

    else:
        if mode in ("bucket", "jl"):
            if mode == "bucket":
                print("Running Ridge Analysis on bucketed PBMC68k Dataset...")
                feature_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
                output_json = "pbmc68k_bucket_size_vs_accuracy.json"
                dataset_name = "PBMC68k (bucket, averaged over random pairs)"
            else:
                print("Running Ridge Analysis on Sparse-JL-projected PBMC68k Dataset...")
                feature_seeds = bucket_utils.sample_jl_seeds(n_bucket_seeds)
                output_json = "pbmc68k_jl_size_vs_accuracy.json"
                dataset_name = "PBMC68k (JL, averaged over random pairs)"
            print(f"Averaging over random feature seeds: {feature_seeds}")
            results = get_ridge_results_bucket(
                bucket_seeds=feature_seeds, truncation_mode=mode
            )
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
        else:
            print(
                "Running Ridge Analysis on PBMC68k Dataset (Binary Classification)..."
            )
            results = get_ridge_results_full()
            param_name = "min_samples"
            raw_key = "raw_data_by_min_samples"
            output_json = "pbmc68k_size_vs_accuracy.json"
            dataset_name = "PBMC68k (Binary, averaged over random pairs)"

        final_stats = {
            k: {"mean_space": [], "mean_acc": [], "sem_acc": []} for k in keys
        }

        data_to_save = {
            "dataset": dataset_name,
            "pairs": results.get("pairs", []),
            "n_pairs": len(results.get("pairs", [])),
            raw_key: {},
        }
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
                if mode in ("bucket", "jl"):
                    acc_mean = results["accuracies_mean"][i]
                    acc_sem = results["accuracies_std"][i]
                else:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        results["accuracy_scores_by_pair"][i]
                    )

                final_stats[k]["mean_space"].append(space)
                final_stats[k]["mean_acc"].append(acc_mean)
                final_stats[k]["sem_acc"].append(acc_sem)

                data_to_save[raw_key][param_str][k] = {
                    "space": space,
                    "accuracy_mean": acc_mean,
                    "accuracy_sem": acc_sem,
                }
                if mode in ("bucket", "jl"):
                    data_to_save[raw_key][param_str][k]["space_by_seed_pair"] = results[
                        f"space_{k}_by_seed_pair"
                    ][i]
                    data_to_save[raw_key][param_str][k][
                        "accuracy_scores_by_seed_pair"
                    ] = results["accuracy_scores_by_seed_pair"][i]
                else:
                    data_to_save[raw_key][param_str][k]["accuracy_scores_by_pair"] = (
                        results["accuracy_scores_by_pair"][i]
                    )

        with open(output_json, "w") as f:
            json.dump(data_to_save, f, indent=2)
        print(f"Saved raw data to {output_json}")

    # Plot
    plt.figure(figsize=figsize)
    for k in keys:
        xm, xs, ym = get_sorted_arrays(
            final_stats[k]["mean_acc"],
            final_stats[k]["sem_acc"],
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
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]

    ax = plt.gca()
    if mode in ("bucket", "jl"):
        streaming_label_x, streaming_label_y, streaming_label_ha = (
            (0.7, 0.45, "right") if mode == "jl" else (0.9, 0.62, "right")
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
            0.81,
            2e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.888,
            1.2e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            0.90,
            1.7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.xlabel("Accuracy")

    plt.xticks(
        [0.80, 0.82, 0.84, 0.86, 0.88, 0.90],
        ["80%", "82%", "84%", "86%", "88%", "90%"],
    )
    if mode == "bucket":
        plt.xlim(0.795, 0.91)
    else:
        plt.xlim(0.795, 0.915)

    plt.tick_params(direction="in", which="both", top=False, right=True)
    plt.ylabel("Machine size")
    plt.ylim(1e1, 1e7)
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Binary classification")
    plt.tight_layout()
    if mode == "bucket":
        output_pdf = "pbmc68k_bucket_size_vs_accuracy.pdf"
    elif mode == "jl":
        output_pdf = "pbmc68k_jl_size_vs_accuracy.pdf"
    else:
        output_pdf = "pbmc68k_size_vs_accuracy.pdf"
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PBMC68k Machine Size vs Accuracy Analysis"
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
