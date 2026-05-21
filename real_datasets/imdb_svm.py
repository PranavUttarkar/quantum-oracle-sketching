import argparse
import json

import bucket_utils
import imdb_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import cross_val_score
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
bucket_n_features = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
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


def get_ridge_results_full():
    # 1. Load Data
    X_all_raw, y_all = imdb_utils.load_imdb_data()

    # 2. Sweep min_df
    results = {
        "min_dfs": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "accuracies_mean": [],
        "accuracies_std": [],  # For error bars (SEM)
        "accuracy_scores": [],
    }

    tqdm.write("Sweeping min_df for Full IMDB...")

    for mdf in tqdm(min_dfs, desc="min_df Sweep"):
        vectorizer = TfidfVectorizer(
            min_df=mdf, stop_words="english", dtype=np.float32
        )
        X_all = vectorizer.fit_transform(X_all_raw)
        X_all.eliminate_zeros()

        shape = X_all.get_shape()
        feature_dim = shape[1]
        num_samples = shape[0]

        # Sparsity calculation
        row_sparsity = int(X_all.getnnz(axis=1).max())
        col_sparsity = int(X_all.getnnz(axis=0).max())
        sparsity = max(row_sparsity, col_sparsity)

        # --- Space Calculations ---
        space_stream = feature_dim
        space_sparse = X_all.getnnz()

        space_quantum = (
            2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
            + np.ceil(np.log2(sparsity + 1))
            + 4
        )

        # --- Ridge Training & Eval (CV) ---
        clf = RidgeClassifier(random_state=42, alpha=10, solver="auto")
        # 5-Fold Cross Validation
        scores = cross_val_score(clf, X_all, y_all, cv=5)

        acc_mean = scores.mean()
        # Calculate Standard Error of the Mean (SEM) = std / sqrt(n)
        acc_sem = scores.std() / np.sqrt(len(scores))

        results["min_dfs"].append(mdf)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["accuracies_mean"].append(acc_mean)
        results["accuracies_std"].append(acc_sem)
        results["accuracy_scores"].append([float(s) for s in scores])

    return results


def get_ridge_results_bucket(bucket_seeds, truncation_mode="bucket"):
    # 1. Load and vectorize the full min_df=1 data once.
    X_all_raw, y_all = imdb_utils.load_imdb_data()

    vectorizer = TfidfVectorizer(min_df=1, stop_words="english", dtype=np.float32)
    X_full = vectorizer.fit_transform(X_all_raw)
    X_full.eliminate_zeros()

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
        "accuracies_mean": [],
        "accuracies_std": [],
        "accuracy_scores_by_seed": [],
    }

    tqdm.write(f"Sweeping {truncation_mode} dimension for Full IMDB...")

    for n_features in tqdm(n_features_list, desc=f"{truncation_mode} Sweep"):
        seed_space_streaming = []
        seed_space_sparse = []
        seed_space_quantum = []
        seed_accuracy_scores = []

        for seed in bucket_seeds:
            X_bucket, _ = bucket_utils.random_truncated_features(
                X_full, n_features, seed=seed, mode=truncation_mode
            )

            feature_dim = X_bucket.shape[1]
            num_samples = X_bucket.shape[0]
            sparsity = bucket_utils.max_sparsity(X_bucket)

            # Same machine-size formulas as the rare-feature path, applied to X_bucket.
            seed_space_streaming.append(feature_dim)
            seed_space_sparse.append(bucket_utils.matrix_nnz(X_bucket))
            seed_space_quantum.append(
                2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
                + np.ceil(np.log2(sparsity + 1))
                + 4
            )

            clf = RidgeClassifier(random_state=42, alpha=10, solver="auto")
            scores = cross_val_score(clf, X_bucket, y_all, cv=5)
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
    x_mean,
    x_std,
    y_mean,
    color,
    marker,
    label,
    linewidth,
    marker_size,
    show_all_markers=False,
):
    # 1. Horizontal Tube (Accuracy SEM)
    # y_mean is Space (Log scale), which doesn't have variance here (single run)
    # x_mean is Accuracy, which has SEM

    # We want shade around x_mean defined by x_std
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

    # 2. Line
    plt.plot(x_vals, y_vals, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    # 3. Markers
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
        marker_indices += [-1, -3, -9, -13, -18, -21, -28]

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


def get_sorted_arrays(x_mean, x_std, y_mean):
    # Sort by Y-axis metric (Space)
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
            else "raw_data_by_min_df"
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
                if "accuracy_scores_by_seed" in entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        entry["accuracy_scores_by_seed"]
                    )
                elif "accuracy_scores" in entry:
                    acc_mean, acc_sem = bucket_utils.mean_and_sem(
                        entry["accuracy_scores"]
                    )
                else:
                    acc_mean = entry["accuracy_mean"]
                    acc_sem = entry["accuracy_sem"]
                final_stats[k]["mean_acc"].append(acc_mean)
                final_stats[k]["sem_acc"].append(acc_sem)

    else:
        if mode in ("bucket", "jl"):
            if mode == "bucket":
                print("Running Ridge Analysis on bucketed IMDB Dataset...")
                feature_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
                output_json = "imdb_bucket_size_vs_accuracy.json"
                dataset_name = "IMDB Full (bucket)"
            else:
                print("Running Ridge Analysis on Sparse-JL-projected IMDB Dataset...")
                feature_seeds = bucket_utils.sample_jl_seeds(n_bucket_seeds)
                output_json = "imdb_jl_size_vs_accuracy.json"
                dataset_name = "IMDB Full (sparse JL)"
            print(f"Averaging over random feature seeds: {feature_seeds}")
            results = get_ridge_results_bucket(
                bucket_seeds=feature_seeds, truncation_mode=mode
            )
            param_name = "n_features"
            raw_key = "raw_data_by_n_features"
        else:
            print("Running Ridge Analysis on Full IMDB Dataset...")
            results = get_ridge_results_full()
            param_name = "min_dfs"
            raw_key = "raw_data_by_min_df"
            output_json = "imdb_size_vs_accuracy.json"
            dataset_name = "IMDB Full"

        final_stats = {
            k: {"mean_space": [], "mean_acc": [], "sem_acc": []} for k in keys
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
                acc_mean = results["accuracies_mean"][i]
                acc_sem = results["accuracies_std"][i]

                final_stats[k]["mean_space"].append(space)
                final_stats[k]["mean_acc"].append(acc_mean)
                final_stats[k]["sem_acc"].append(acc_sem)

                data_to_save[raw_key][param_str][k] = {
                    "space": space,
                    "accuracy_mean": acc_mean,
                    "accuracy_sem": acc_sem,
                }
                if mode in ("bucket", "jl"):
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
            (0.7, 0.5, "right") if mode == "jl" else (0.9, 0.7, "right")
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
            0.04,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        plt.xticks([0.60, 0.70, 0.80, 0.90], ["60%", "70%", "80%", "90%"])
        plt.xlim(0.57, 0.92)
    else:
        plt.text(
            0.70,
            4e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.88,
            9e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.text(
            0.90,
            1.9e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        plt.xticks(
            [0.70, 0.75, 0.80, 0.85, 0.90],
            ["70%", "75%", "80%", "85%", "90%"],
        )
        plt.xlim(0.69, 0.91)

    plt.yscale("log")
    plt.xlabel("Accuracy")
    plt.tick_params(direction="in", which="both", top=False, right=True)
    plt.ylabel("Machine size")
    plt.ylim(1e1, 1e7)
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Binary classification")
    plt.tight_layout()
    if mode == "bucket":
        output_pdf = "imdb_bucket_size_vs_accuracy.pdf"
    elif mode == "jl":
        output_pdf = "imdb_jl_size_vs_accuracy.pdf"
    else:
        output_pdf = "imdb_size_vs_accuracy.pdf"
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="IMDB Machine Size vs Accuracy Analysis"
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
