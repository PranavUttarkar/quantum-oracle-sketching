import argparse
import json

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

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
num_markers = 20

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
markersize = {"streaming": 50, "sparse": 50, "quantum": 30}
linewidth_marker = {"streaming": 0, "sparse": 0, "quantum": 0}


def plot_parametric_hybrid(
    ax,
    x_mean,
    x_std,
    y_mean,
    y_std,
    color,
    marker,
    label,
    linewidth,
    marker_size,
    mode="rare",
):
    ax.fill_betweenx(
        y_mean, x_mean - x_std, x_mean + x_std, color=color, alpha=0.2, edgecolor="none"
    )
    ax.plot(x_mean, y_mean, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    if mode == "bucket":
        marker_indices = list(range(len(x_mean)))
    else:
        x_min, x_max = np.min(x_mean), np.max(x_mean)
        target_x = np.linspace(x_min, x_max, num=num_markers)
        marker_indices = []
        for tx in target_x:
            idx = (np.abs(x_mean - tx)).argmin()
            if idx not in marker_indices:
                marker_indices.append(idx)
        marker_indices.append(-3)

    ax.scatter(
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
    data = sorted(zip(x_mean, x_std, y_mean, y_std), key=lambda x: x[2])
    return (
        np.array([d[0] for d in data]),
        np.array([d[1] for d in data]),
        np.array([d[2] for d in data]),
        np.array([d[3] for d in data]),
    )


def compute_stats_from_json(data, x_fields):
    keys = ["streaming", "sparse", "quantum"]
    final_stats = {
        k: {
            "mean_space": [],
            "std_space": [],
            "mean_x": [],
            "std_x": [],
        }
        for k in keys
    }

    if "raw_data_by_n_features" in data:
        raw_data = data["raw_data_by_n_features"]
    else:
        raw_data = data["raw_data_by_min_df"]
    by_param = {int(k): v for k, v in raw_data.items()}
    target_params = (
        sorted(by_param.keys()) if "raw_data_by_n_features" in data else min_dfs
    )

    for param in sorted(set(target_params)):
        if param not in by_param:
            continue
        for k in keys:
            entry = by_param[param][k]
            if "space_by_seed_pair" in entry:
                spaces = np.array(entry["space_by_seed_pair"], dtype=float).reshape(-1)
            elif "space_by_pair" in entry:
                spaces = np.array(entry["space_by_pair"], dtype=float).reshape(-1)
            elif "space_by_seed" in entry:
                spaces = np.array(entry["space_by_seed"], dtype=float).reshape(-1)
            else:
                spaces = np.array(entry["space"], dtype=float).reshape(-1)

            x_vals = None
            for field in x_fields:
                if field in entry:
                    x_vals = np.array(entry[field], dtype=float).reshape(-1)
                    break
            if x_vals is None:
                x_vals = np.zeros_like(spaces)

            if len(spaces) > 0:
                sqrt_space_n = np.sqrt(spaces.size)
                sqrt_x_n = np.sqrt(x_vals.size)
                final_stats[k]["mean_space"].append(np.mean(spaces))
                final_stats[k]["std_space"].append(np.std(spaces) / sqrt_space_n)
                final_stats[k]["mean_x"].append(np.mean(x_vals))
                final_stats[k]["std_x"].append(np.std(x_vals) / sqrt_x_n)

    return final_stats


def plot_accuracy_panel(ax, stats, mode="rare"):
    keys = ["streaming", "sparse", "quantum"]
    for k in keys:
        xm, xs, ym, ys = get_sorted_arrays(
            stats[k]["mean_x"],
            stats[k]["std_x"],
            stats[k]["mean_space"],
            stats[k]["std_space"],
        )
        plot_parametric_hybrid(
            ax,
            xm,
            xs,
            ym,
            ys,
            colors[k],
            markers[k],
            labels[k],
            linewidth_marker[k],
            markersize[k],
            mode=mode,
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]
    if mode == "bucket":
        ax.text(
            0.2,
            0.82,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        ax.text(
            0.78,
            0.58,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
        )
        ax.text(
            0.15,
            0.06,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
    else:
        ax.text(
            0.83,
            9e4,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        ax.text(
            0.934,
            9e3,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        ax.text(
            0.94,
            7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    ax.set_yscale("log")
    ax.set_ylim(1e1, 2e5)
    ax.set_xlabel("Accuracy")
    if mode == "bucket":
        ax.set_xticks([0.65, 0.75, 0.85, 0.95])
        ax.set_xticklabels(["65%", "75%", "85%", "95%"])
        ax.set_xlim(0.62, 0.97)
    else:
        ax.set_xticks([0.84, 0.86, 0.88, 0.90, 0.92, 0.94])
        ax.set_xticklabels(["84%", "86%", "88%", "90%", "92%", "94%"])
    ax.set_ylabel("Machine size")
    ax.tick_params(direction="in", which="both", top=False, right=True)
    ax.grid(True, which="major", ls="-", alpha=0.1)
    ax.set_title("Binary classification")


def plot_variance_panel(ax, stats, mode="rare"):
    keys = ["streaming", "sparse", "quantum"]
    for k in keys:
        xm, xs, ym, ys = get_sorted_arrays(
            stats[k]["mean_x"],
            stats[k]["std_x"],
            stats[k]["mean_space"],
            stats[k]["std_space"],
        )
        plot_parametric_hybrid(
            ax,
            xm,
            xs,
            ym,
            ys,
            colors[k],
            markers[k],
            labels[k],
            linewidth_marker[k],
            markersize[k],
            mode=mode,
        )

    halo = [pe.withStroke(linewidth=3, foreground="white")]
    if mode == "bucket":
        ax.text(
            0.2,
            0.85,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        ax.text(
            0.95,
            0.58,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
        )
        ax.text(
            0.15,
            0.06,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
    else:
        ax.text(
            0.535,
            9e4,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        ax.text(
            0.98,
            9e3,
            "Classical streaming",
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        ax.text(
            1,
            7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    ax.set_yscale("log")
    ax.set_ylim(1e1, 2e5)
    ax.set_xlabel("Relative explained variance")
    if mode == "bucket":
        ax.set_xticks([0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["25%", "50%", "75%", "100%"])
        ax.set_xlim(0.08, 1.03)
    else:
        ax.set_xticks([0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_xticklabels(["60%", "70%", "80%", "90%", "100%"])
        ax.set_xlim(0.52, 1.03)
    ax.tick_params(direction="in", which="both", top=False, right=True)
    ax.grid(True, which="major", ls="-", alpha=0.1)
    ax.set_title("Dimension reduction")


def main():
    parser = argparse.ArgumentParser(
        description="Combine 20newsgroups size-vs-accuracy and size-vs-variance plots."
    )
    parser.add_argument(
        "--accuracy-json",
        type=str,
        default=None,
        help="Path to accuracy JSON file.",
    )
    parser.add_argument(
        "--variance-json",
        type=str,
        default=None,
        help="Path to variance JSON file.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output figure path.",
    )
    parser.add_argument("--mode", choices=["rare", "bucket"], required=True)
    args = parser.parse_args()

    if args.mode == "bucket":
        if args.accuracy_json is None:
            args.accuracy_json = "20newsgroups_bucket_size_vs_accuracy.json"
        if args.variance_json is None:
            args.variance_json = "20newsgroups_bucket_size_vs_variance.json"
    else:
        if args.accuracy_json is None:
            args.accuracy_json = "20newsgroups_size_vs_accuracy.json"
        if args.variance_json is None:
            args.variance_json = "20newsgroups_size_vs_variance.json"

    with open(args.accuracy_json, "r") as f:
        accuracy_data = json.load(f)
    with open(args.variance_json, "r") as f:
        variance_data = json.load(f)

    for path, data in [
        (args.accuracy_json, accuracy_data),
        (args.variance_json, variance_data),
    ]:
        is_bucket = "raw_data_by_n_features" in data
        if is_bucket != (args.mode == "bucket"):
            raise ValueError(f"{path} does not match --mode {args.mode}")

    if args.out is None:
        args.out = (
            "20newsgroups_bucket_combine.pdf"
            if args.mode == "bucket"
            else "20newsgroups_combine.pdf"
        )

    accuracy_stats = compute_stats_from_json(
        accuracy_data,
        [
            "accuracy_scores_by_seed_pair",
            "accuracy_scores_by_pair",
            "accuracy",
        ],
    )
    variance_stats = compute_stats_from_json(
        variance_data,
        [
            "variance_recovery_by_seed_pair",
            "variance_recovery_by_pair",
            "variance_recovery",
            "variance",
        ],
    )

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(6, 3.5), sharey=True)
    plot_accuracy_panel(ax_left, accuracy_stats, mode=args.mode)
    plot_variance_panel(ax_right, variance_stats, mode=args.mode)

    ax_right.tick_params(axis="y", labelleft=False)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
