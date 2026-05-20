import argparse
import json
import random
from collections import defaultdict

import bucket_utils
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import cross_val_score
from tqdm import tqdm

np.random.seed(42)
random.seed(42)

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

min_dfs = list(range(2, 21)) + list(range(25, 105, 5))
bucket_n_features = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
n_bucket_seeds = 5
num_markers = 20

# --- Plotting ---
colors = {
    "quantum": "#CD591A",  # Quantum curve color
    "streaming": "#2657AF",  # Strong Blue
    "sparse": "#606060",  # Dark Grey (De-emphasized)
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


def load_data(categories=None):
    tqdm.write(f"Loading 20Newsgroups {categories}...")
    data_train = fetch_20newsgroups(
        subset="train",
        categories=categories,
        remove=("headers", "footers", "quotes"),
        return_X_y=True,
    )
    data_test = fetch_20newsgroups(
        subset="test",
        categories=categories,
        remove=("headers", "footers", "quotes"),
        return_X_y=True,
    )
    return data_train[0], data_train[1], data_test[0], data_test[1]


def get_ridge_results(categories):
    # 1. Load Data
    X_train_raw, y_train, X_test_raw, y_test = load_data(categories)

    # Combine for Cross Validation
    X_all_raw = list(X_train_raw) + list(X_test_raw)
    y_all = np.concatenate([y_train, y_test])

    # 2. Sweep min_df (Sparse Range for Smooth Plots)

    # Storage
    results = {
        "min_dfs": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "accuracies": [],
        "error_rates": [],
    }

    tqdm.write(f"Sweeping min_df for categories {categories}...")

    for mdf in tqdm(min_dfs, desc="min_df Sweep", leave=False):
        vectorizer = TfidfVectorizer(min_df=mdf, stop_words="english")
        X_all = vectorizer.fit_transform(X_all_raw)
        X_all.eliminate_zeros()  # type: ignore

        shape = X_all.get_shape()
        feature_dim = shape[1]
        num_samples = shape[0]

        # Sparsity calculation
        row_sparsity = int(X_all.getnnz(axis=1).max())
        col_sparsity = int(X_all.getnnz(axis=0).max())
        sparsity = max(row_sparsity, col_sparsity)

        # --- Space Calculations ---
        # Any classical streaming algorithm must at least store the weight vector,
        #    which is of size d. So classical streaming space is d floats.
        # Any classical standard algorithm that stores the whole sparse matrix
        #    must at least store all non-zero entries, so classical sparse space is nnz.
        space_stream = feature_dim  # Classical Streaming Space: d
        space_sparse = X_all.getnnz()  # Classical Sparse Space: nnz

        # We use quantum oracle sketching to build:
        # 1. The block encoding of the augmented data matrix [X; \lambda I] in R^{(n+d) x d},
        #    Its Hermitian dilation is in R^{(n+2d) x (n+2d)}. This requires building the
        #    sparse index/element oracle for the augmented matrix, which has sparsity = sparsity + 1.
        #    Hence, building index oracle requires 2log2(n+2d) + log2(sparsity + 1) + 2 (QSVT & binary search output) qubits.
        #    Building element oracle can reuse the same qubits, so no extra qubits needed.
        # 2. The state preparation unitary block encoding of the label vector y in R^n, which
        #    requires log2(n) + 2 (first LCU+QSVT and second LCU) qubits. These qubits are contained
        #    in the previous count and they can be reused.
        # Then we perform quantum ridge regression with amplitude amplification using QSVT-based quantum linear system solver,
        #    which requires 1 ancilla qubit for the QSVT, contained in the previous count because we can reuse
        #    the ancilla qubit from quantum oracle sketching.
        # Finally, we need to perform interferometric measurement to calculate the signed overlap with test state,
        #    which requires 1 extra ancilla qubit.
        # The final estimate of the label is stored classically on a running average, so only 1 extra float is needed.
        # Therefore, total quantum space is:
        #   (2log2(n + 2d) + log2(sparsity + 1) + 3) qubits + 1 float
        space_quantum = (
            2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
            + np.ceil(np.log2(sparsity + 1))
            + 4  # + 3 qubits + 1 float
        )

        # --- Ridge Training & Eval (CV) ---
        clf = RidgeClassifier(random_state=42, alpha=1.0, solver="auto")
        # 5-Fold Cross Validation
        # That means in each fold, we train on 80% data and test on 20% data
        scores = cross_val_score(clf, X_all, y_all, cv=5)

        results["min_dfs"].append(mdf)
        results["space_streaming"].append(space_stream)
        results["space_sparse"].append(space_sparse)
        results["space_quantum"].append(space_quantum)
        results["accuracies"].append([float(s) for s in scores])
        results["error_rates"].append([float(1.0 - s) for s in scores])

    return results


def get_ridge_results_bucket(categories, bucket_seeds):
    X_train_raw, y_train, X_test_raw, y_test = load_data(categories)

    X_all_raw = list(X_train_raw) + list(X_test_raw)
    y_all = np.concatenate([y_train, y_test])

    vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
    X_full = vectorizer.fit_transform(X_all_raw)
    X_full.eliminate_zeros()  # type: ignore

    results = {
        "n_features": [],
        "space_streaming": [],
        "space_sparse": [],
        "space_quantum": [],
        "accuracies": [],
        "error_rates": [],
    }

    tqdm.write(f"Sweeping bucket dimension for categories {categories}...")

    for n_features in tqdm(bucket_n_features, desc="bucket Sweep", leave=False):
        seed_space_streaming = []
        seed_space_sparse = []
        seed_space_quantum = []
        seed_accuracy_scores = []
        seed_error_scores = []

        for seed in bucket_seeds:
            X_bucket, _ = bucket_utils.bucket_features(X_full, n_features, seed=seed)

            feature_dim = X_bucket.shape[1]
            num_samples = X_bucket.shape[0]
            sparsity = bucket_utils.max_sparsity(X_bucket)

            # Same machine-size formulas as the rare-feature path; bucket only changes X.
            seed_space_streaming.append(feature_dim)
            seed_space_sparse.append(X_bucket.getnnz())
            seed_space_quantum.append(
                2 * np.ceil(np.log2(num_samples + 2 * feature_dim))
                + np.ceil(np.log2(sparsity + 1))
                + 4
            )

            clf = RidgeClassifier(random_state=42, alpha=1.0, solver="auto")
            scores = cross_val_score(clf, X_bucket, y_all, cv=5)
            seed_accuracy_scores.append([float(s) for s in scores])
            seed_error_scores.append([float(1.0 - s) for s in scores])

        results["n_features"].append(n_features)
        results["space_streaming"].append(seed_space_streaming)
        results["space_sparse"].append(seed_space_sparse)
        results["space_quantum"].append(seed_space_quantum)
        results["accuracies"].append(seed_accuracy_scores)
        results["error_rates"].append(seed_error_scores)

    return results


def plot_parametric_hybrid(
    x_mean,
    x_std,
    y_mean,
    y_std,
    color,
    marker,
    label,
    linewidth,
    marker_size,
    ax=None,
    show_all_markers=False,
):
    # 1. Horizontal Tube (Accuracy/Error Variance)
    plt.fill_betweenx(
        y_mean, x_mean - x_std, x_mean + x_std, color=color, alpha=0.2, edgecolor="none"
    )

    # 2. Line (Full data)
    plt.plot(x_mean, y_mean, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    # 3. Markers
    # only display markers for evenly spaced points over accuracy to avoid clutter
    # calculate marker indices based on x_mean, note that x_mean is not necessarily evenly spaced
    if show_all_markers:
        marker_indices = np.arange(len(x_mean))
    else:
        x_min, x_max = np.min(x_mean), np.max(x_mean)
        target_x = np.linspace(x_min, x_max, num=num_markers)
        marker_indices = []
        for tx in target_x:
            idx = (np.abs(x_mean - tx)).argmin()
            if idx not in marker_indices:
                marker_indices.append(idx)
        marker_indices.append(-3)

    plt.scatter(
        x_mean[marker_indices],
        y_mean[marker_indices],
        marker=marker,
        color=color,
        label=label,
        alpha=0.9,
        s=marker_size,
        linewidth=linewidth,
    )


def get_sorted_arrays(x_mean, x_std, y_mean, y_std):
    # Sort by Y-axis metric (Space) to ensure clean trajectories
    data = sorted(zip(x_mean, x_std, y_mean, y_std), key=lambda x: x[2])
    return (
        np.array([d[0] for d in data]),
        np.array([d[1] for d in data]),
        np.array([d[2] for d in data]),
        np.array([d[3] for d in data]),
    )


def run_analysis(
    n_pairs=10, from_json_data=None, mode=None, n_bucket_seeds=n_bucket_seeds
):
    if mode not in ("rare", "bucket"):
        raise ValueError("mode must be 'rare' or 'bucket'")

    keys = ["streaming", "sparse", "quantum"]
    final_stats = {
        k: {
            "mean_space": [],
            "std_space": [],
            "mean_acc": [],
            "std_acc": [],
            "mean_err": [],
            "std_err": [],
        }
        for k in keys
    }

    if from_json_data is not None:
        print("Restoring analysis from JSON data...")
        n_pairs = from_json_data["n_pairs"]
        raw_key = "raw_data_by_n_features" if mode == "bucket" else "raw_data_by_min_df"
        raw_data = from_json_data[raw_key]
        by_param = {int(k): v for k, v in raw_data.items()}

        # Re-compute stats
        for param in sorted(by_param.keys()):
            for k in keys:
                entry = by_param[param][k]
                if "space_by_seed_pair" in entry:
                    spaces = np.array(entry["space_by_seed_pair"], dtype=float).reshape(
                        -1
                    )
                elif "space_by_pair" in entry:
                    spaces = np.array(entry["space_by_pair"], dtype=float).reshape(-1)
                else:
                    spaces = np.array(entry["space"], dtype=float).reshape(-1)

                if "accuracy_scores_by_seed_pair" in entry:
                    accs = np.array(
                        entry["accuracy_scores_by_seed_pair"], dtype=float
                    ).reshape(-1)
                elif "accuracy_scores_by_pair" in entry:
                    accs = np.array(
                        entry["accuracy_scores_by_pair"], dtype=float
                    ).reshape(-1)
                else:
                    accs = np.array(entry["accuracy"], dtype=float).reshape(-1)

                if "error_scores_by_seed_pair" in entry:
                    errs = np.array(
                        entry["error_scores_by_seed_pair"], dtype=float
                    ).reshape(-1)
                elif "error_scores_by_pair" in entry:
                    errs = np.array(entry["error_scores_by_pair"], dtype=float).reshape(
                        -1
                    )
                else:
                    errs = np.array(entry["error"], dtype=float).reshape(-1)

                if len(spaces) > 0:
                    # calculate mean and std error of the mean
                    sqrt_space_n = np.sqrt(spaces.size)
                    sqrt_acc_n = np.sqrt(accs.size)
                    sqrt_err_n = np.sqrt(errs.size)
                    final_stats[k]["mean_space"].append(np.mean(spaces))
                    final_stats[k]["std_space"].append(np.std(spaces) / sqrt_space_n)
                    final_stats[k]["mean_acc"].append(np.mean(accs))
                    final_stats[k]["std_acc"].append(np.std(accs) / sqrt_acc_n)
                    final_stats[k]["mean_err"].append(np.mean(errs))
                    final_stats[k]["std_err"].append(np.std(errs) / sqrt_err_n)

    else:
        print(f"Running Analysis over {n_pairs} random sets of 1v1 categories...")
        if mode == "bucket":
            bucket_seeds = bucket_utils.sample_bucket_seeds(n_bucket_seeds)
            print(f"Averaging over bucket seeds: {bucket_seeds}")
        all_cats = fetch_20newsgroups(
            subset="train", remove=("headers", "footers", "quotes")
        ).target_names  # type: ignore

        by_param = defaultdict(
            lambda: {k: {"space": [], "error": [], "accuracy": []} for k in keys}
        )

        for i in tqdm(range(n_pairs), desc="Category Pairs", leave=True):
            # Randomly select 2 categories
            cats = random.sample(all_cats, 2)

            tqdm.write(f"[{i + 1}/{n_pairs}] Group: {cats}")

            # Calculate Ridge accuracy and space.
            if mode == "bucket":
                res = get_ridge_results_bucket(cats, bucket_seeds=bucket_seeds)
                params = res["n_features"]
            else:
                res = get_ridge_results(cats)
                params = res["min_dfs"]

            for j, param in enumerate(params):
                for k in keys:
                    by_param[param][k]["space"].append(res[f"space_{k}"][j])
                    by_param[param][k]["error"].append(res["error_rates"][j])
                    by_param[param][k]["accuracy"].append(res["accuracies"][j])

        # Compute Stats
        for param in sorted(by_param.keys()):
            for k in keys:
                spaces = np.array(by_param[param][k]["space"], dtype=float).reshape(-1)
                accs = np.array(by_param[param][k]["accuracy"], dtype=float).reshape(-1)
                errs = np.array(by_param[param][k]["error"], dtype=float).reshape(-1)

                if len(spaces) > 0:
                    # calculate mean and std error of the mean
                    sqrt_space_n = np.sqrt(spaces.size)
                    sqrt_acc_n = np.sqrt(accs.size)
                    sqrt_err_n = np.sqrt(errs.size)
                    final_stats[k]["mean_space"].append(np.mean(spaces))
                    final_stats[k]["std_space"].append(np.std(spaces) / sqrt_space_n)
                    final_stats[k]["mean_acc"].append(np.mean(accs))
                    final_stats[k]["std_acc"].append(np.std(accs) / sqrt_acc_n)
                    final_stats[k]["mean_err"].append(np.mean(errs))
                    final_stats[k]["std_err"].append(np.std(errs) / sqrt_err_n)

        # Save Data
        raw_key = "raw_data_by_n_features" if mode == "bucket" else "raw_data_by_min_df"
        output_json = (
            "20newsgroups_bucket_size_vs_accuracy.json"
            if mode == "bucket"
            else "20newsgroups_size_vs_accuracy.json"
        )
        data_to_save = {"n_pairs": n_pairs, "cats_per_class": 1, raw_key: {}}
        for param, param_dict in by_param.items():
            data_to_save[raw_key][param] = {}
            for metric, sub_dict in param_dict.items():
                spaces = np.array(sub_dict["space"], dtype=float)
                accuracies = np.array(sub_dict["accuracy"], dtype=float)
                errors = np.array(sub_dict["error"], dtype=float)

                if mode == "bucket":
                    data_to_save[raw_key][param][metric] = {
                        "space": float(np.mean(spaces)),
                        "space_by_seed_pair": np.moveaxis(spaces, 0, 1).tolist(),
                        "accuracy_mean": float(np.mean(accuracies)),
                        "accuracy_sem": float(
                            np.std(accuracies.reshape(-1)) / np.sqrt(accuracies.size)
                        ),
                        "accuracy_scores_by_seed_pair": np.moveaxis(
                            accuracies, 0, 1
                        ).tolist(),
                        "error_mean": float(np.mean(errors)),
                        "error_sem": float(
                            np.std(errors.reshape(-1)) / np.sqrt(errors.size)
                        ),
                        "error_scores_by_seed_pair": np.moveaxis(errors, 0, 1).tolist(),
                    }
                else:
                    data_to_save[raw_key][param][metric] = {
                        "space": float(np.mean(spaces)),
                        "space_by_pair": spaces.tolist(),
                        "accuracy_mean": float(np.mean(accuracies)),
                        "accuracy_sem": float(
                            np.std(accuracies.reshape(-1)) / np.sqrt(accuracies.size)
                        ),
                        "accuracy_scores_by_pair": accuracies.tolist(),
                        "error_mean": float(np.mean(errors)),
                        "error_sem": float(
                            np.std(errors.reshape(-1)) / np.sqrt(errors.size)
                        ),
                        "error_scores_by_pair": errors.tolist(),
                    }
        if mode == "bucket":
            data_to_save["bucket_seeds"] = bucket_seeds
            data_to_save["bucket_n_features"] = bucket_n_features
            data_to_save["bucket_seed_sample_seed"] = (
                bucket_utils.DEFAULT_BUCKET_SEED_SAMPLE_SEED
            )
            data_to_save["bucket_key_note"] = (
                "raw_data_by_n_features keys are requested bucket dimensions; "
                "a pair with fewer original features uses its full matrix."
            )
        with open(output_json, "w") as f:
            json.dump(data_to_save, f, indent=2)
        print(f"Saved raw data to {output_json}")

    # Plot: Size vs Accuracy
    plt.figure(figsize=figsize)
    for k in keys:
        xm, xs, ym, ys = get_sorted_arrays(
            final_stats[k]["mean_acc"],
            final_stats[k]["std_acc"],
            final_stats[k]["mean_space"],
            final_stats[k]["std_space"],
        )
        plot_parametric_hybrid(
            xm,
            xs,
            ym,
            ys,
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
            0.82,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        plt.text(
            0.78,
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
            0.06,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
    else:
        plt.text(
            0.835,
            8e4,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.873,
            9e3,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
        )
        plt.text(
            0.94,
            7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    plt.yscale("log")
    plt.xlabel("Accuracy")
    if mode == "bucket":
        plt.xticks([0.65, 0.75, 0.85, 0.95], ["65%", "75%", "85%", "95%"])
        plt.xlim(0.62, 0.97)
    else:
        plt.xticks(
            [0.84, 0.86, 0.88, 0.90, 0.92, 0.94],
            ["84%", "86%", "88%", "90%", "92%", "94%"],
        )
    plt.tick_params(direction="in", which="both", top=False, right=True)
    plt.ylabel("Machine size")
    plt.ylim(1e1, 2e5)
    # plt.legend()
    plt.grid(True, which="major", ls="-", alpha=0.1)
    plt.title("Binary classification")
    plt.tight_layout()
    output_pdf = (
        "20newsgroups_bucket_size_vs_accuracy.pdf"
        if mode == "bucket"
        else "20newsgroups_size_vs_accuracy.pdf"
    )
    plt.savefig(output_pdf)
    print(f"Saved {output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="20newsgroups Machine Size vs Accuracy Analysis"
    )
    parser.add_argument(
        "--n_pairs",
        type=int,
        default=100,
        help="Number of random pairs to average (for new run)",
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

    if args.load is not None:
        with open(args.load, "r") as f:
            data = json.load(f)
        run_analysis(
            from_json_data=data, mode=args.mode, n_bucket_seeds=args.n_bucket_seeds
        )
    elif args.n_pairs is not None:
        run_analysis(
            n_pairs=args.n_pairs, mode=args.mode, n_bucket_seeds=args.n_bucket_seeds
        )
    else:
        print("Please specify --n_pairs <N> (to run) or --load <file.json> (to plot).")
