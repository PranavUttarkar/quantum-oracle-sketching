import argparse
import json

import bucket_utils
import dorothea_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import cross_val_score
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

# Min DF Sweep Range (Same as PCA)
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


def get_svm_results_full():
    # 1. Load Data
    print("Loading Dorothea data...")
    X_full, y_full = dorothea_utils.load_dorothea_data(valid=True)
    tqdm.write(f"Dataset shape: {X_full.shape}")
    row_sparsity = int(X_full.getnnz(axis=1).max())
    col_sparsity = int(X_full.getnnz(axis=0).max())
    sparsity = max(row_sparsity, col_sparsity)
    tqdm.write(
        f"Max row sparsity: {row_sparsity}, Max col sparsity: {col_sparsity}, Overall sparsity: {sparsity}"
    )

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
        "accuracies_mean": [],
        "accuracies_std": [],
        "accuracy_scores": [],
    }

    tqdm.write("Sweeping min_df for Dorothea (SVM)...")

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

        # Space metrics
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

        clf = RidgeClassifier(
            random_state=42, alpha=200, solver="auto", class_weight="balanced"
        )

        # 5-Fold Cross Validation
        scores = cross_val_score(clf, X_trunc, y_full, cv=5)

        results["min_dfs"].append(mdf)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["accuracies_mean"].append(scores.mean())
        results["accuracies_std"].append(scores.std() / np.sqrt(len(scores)))
        results["accuracy_scores"].append([float(s) for s in scores])

    return results


def get_svm_results_bucket(bucket_seeds):
    print("Loading Dorothea data...")
    X_full, y_full = dorothea_utils.load_dorothea_data(valid=True)
    tqdm.write(f"Dataset shape: {X_full.shape}")

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
        "accuracies_mean": [],
        "accuracies_std": [],
        "accuracy_scores_by_seed": [],
    }

    tqdm.write("Sweeping bucket dimension for Dorothea (SVM)...")

    for n_features in tqdm(n_features_list, desc="bucket Sweep"):
        seed_space_streaming = []
        seed_space_sparse = []
        seed_space_quantum = []
        seed_accuracy_scores = []

        for seed in bucket_seeds:
            X_bucket, _ = bucket_utils.bucket_features(X_full, n_features, seed=seed)

            feature_dim = X_bucket.shape[1]
            num_samples = X_bucket.shape[0]
            sparsity = bucket_utils.max_sparsity(X_bucket)

            # Same machine-size formulas as the rare-feature path; bucket only changes X.
            seed_space_streaming.append(feature_dim)
            seed_space_sparse.append(X_bucket.getnnz())
            seed_space_quantum.append(
                2 * np.ceil(np.log2(num_samples + feature_dim + 1))
                + np.ceil(np.log2(sparsity + 1))
                + 4
            )

            clf = RidgeClassifier(
                random_state=42, alpha=200, solver="auto", class_weight="balanced"
            )
            scores = cross_val_score(clf, X_bucket, y_full, cv=5)
            seed_accuracy_scores.append([float(s) for s in scores])

        acc_mean, acc_sem = bucket_utils.mean_and_sem(seed_accuracy_scores)

        results["n_features"].append(n_features)
        results["space_streaming"].append(np.mean(seed_space_streaming))
        results["space_sparse"].append(np.mean(seed_space_sparse))
        results["space_quantum"].append(np.mean(seed_space_quantum))
        results["space_streaming_by_seed"].append(seed_space_streaming)
        results["space_sparse_by_seed"].append(seed_space_sparse)
        results["space_quantum_by_seed"].append(seed_space_quantum)
        results["accuracies_mean"].append(acc_mean)
        results["accuracies_std"].append(acc_sem)
        results["accuracy_scores_by_seed"].append(seed_accuracy_scores)

    return results


def plot_parametric_hybrid(
    x_mean, x_std, y_mean, color, marker, label, linewidth, marker_size
):
    # 1. Horizontal Tube (Accuracy SEM/STD)
    y_vals = np.array(y_mean)
    x_vals = np.array(x_mean)
    x_errs = np.array(x_std) if x_std is not None else np.zeros_like(x_vals)

    plt.fill_betweenx(
        y_vals,
        x_vals - x_errs,
        x_vals + x_errs,
        color=color,
        alpha=0.2,
        edgecolor="none",
    )

    # 2. Line
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


def get_sorted_arrays(x_mean, x_std, y_mean):
    data = sorted(zip(x_mean, x_std, y_mean), key=lambda x: x[2])
    return (
        np.array([d[0] for d in data]),
        np.array([d[1] for d in data]),
        np.array([d[2] for d in data]),
    )


def run_analysis(load_file=None, mode=None, n_bucket_seeds=n_bucket_seeds):
    if mode not in ("rare", "bucket"):
        raise ValueError("mode must be 'rare' or 'bucket'")

    keys = ["streaming", "sparse", "quantum"]

    if load_file:
        print(f"Loading analysis from {load_file}...")
        with open(load_file, "r") as f:
            data_to_save = json.load(f)
        raw_key = "raw_data_by_n_features" if mode == "bucket" else "raw_data_by_min_df"
        raw_data = data_to_save[raw_key]
        params = sorted([int(k) for k in raw_data.keys()])

        final_stats = {
            k: {"mean_space": [], "mean_acc": [], "sem_acc": []} for k in keys
        }
        for param in params:
            entry = raw_data[str(param)]
            for k in keys:
                method_entry = entry[k]
                final_stats[k]["mean_space"].append(method_entry["space"])
                if "accuracy_scores_by_seed" in method_entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        method_entry["accuracy_scores_by_seed"]
                    )
                elif "accuracy_scores" in method_entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        method_entry["accuracy_scores"]
                    )
                else:
                    if "accuracy_mean" in method_entry:
                        acc_mean = method_entry["accuracy_mean"]
                        acc_sem = method_entry["accuracy_sem"]
                    else:
                        acc_mean = method_entry["accuracy"]
                        acc_sem = method_entry["accuracy_std"]
                final_stats[k]["mean_acc"].append(acc_mean)
                final_stats[k]["sem_acc"].append(acc_sem)

    else:
        if mode == "bucket":
            print("Running SVM Analysis on bucketed Dorothea Dataset...")
            bucket_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
            print(f"Averaging over bucket seeds: {bucket_seeds}")
            results = get_svm_results_bucket(bucket_seeds=bucket_seeds)
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
            output_json = "dorothea_bucket_size_vs_accuracy.json"
            dataset_name = "Dorothea (bucket)"
        else:
            print("Running SVM Analysis on Dorothea Dataset...")
            results = get_svm_results_full()
            param_name = "min_dfs"
            raw_key = "raw_data_by_min_df"
            output_json = "dorothea_size_vs_accuracy.json"
            dataset_name = "Dorothea"

        data_to_save = {"dataset": dataset_name, raw_key: {}}
        if mode == "bucket":
            data_to_save["bucket_seeds"] = bucket_seeds
            data_to_save["bucket_n_features"] = bucket_n_features
            data_to_save["bucket_seed_sample_seed"] = (
                bucket_utils.DEFAULT_BUCKET_SEED_SAMPLE_SEED
            )

        final_stats = {
            k: {"mean_space": [], "mean_acc": [], "sem_acc": []} for k in keys
        }

        for i, param in enumerate(results[param_name]):
            param_str = str(param)
            data_to_save[raw_key][param_str] = {}

            for k in keys:
                space = results[f"space_{k}"][i]
                acc = results["accuracies_mean"][i]
                sem = results["accuracies_std"][i]

                final_stats[k]["mean_space"].append(space)
                final_stats[k]["mean_acc"].append(acc)
                final_stats[k]["sem_acc"].append(sem)

                data_to_save[raw_key][param_str][k] = {
                    "space": space,
                    "accuracy_mean": acc,
                    "accuracy_sem": sem,
                }
                if mode == "bucket":
                    data_to_save[raw_key][param_str][k]["space_by_seed"] = results[
                        f"space_{k}_by_seed"
                    ][i]
                    data_to_save[raw_key][param_str][k][
                        "accuracy_scores_by_seed"
                    ] = results["accuracy_scores_by_seed"][i]
                else:
                    data_to_save[raw_key][param_str][k]["accuracy_scores"] = results[
                        "accuracy_scores"
                    ][i]

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
        ind = xm >= 0.6
        plot_parametric_hybrid(
            xm[ind],
            xs[ind],
            ym[ind],
            colors[k],
            markers[k],
            labels[k],
            linewidth_marker[k],
            markersize[k],
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]
    ax = plt.gca()
    if mode == "bucket":
        plt.text(
            0.05,
            0.92,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        plt.text(
            0.85,
            0.58,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
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
            0.9,
            6e5,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            0.9,
            4e3,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            0.95,
            1.4e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.xlabel("Accuracy")
    plt.ylabel("Machine size")
    plt.ylim(1e1, 2e6)
    if mode == "bucket":
        plt.xlim(0.79, 0.95)
        plt.xticks([0.80, 0.84, 0.88, 0.92], ["80%", "84%", "88%", "92%"])
    else:
        plt.xlim(0.58, 0.97)
        plt.xticks([0.60, 0.70, 0.80, 0.90], ["60%", "70%", "80%", "90%"])
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Binary classification")
    plt.tight_layout()
    output_pdf = (
        "dorothea_bucket_size_vs_accuracy.pdf"
        if mode == "bucket"
        else "dorothea_size_vs_accuracy.pdf"
    )
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dorothea Machine Size vs Accuracy Analysis"
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
