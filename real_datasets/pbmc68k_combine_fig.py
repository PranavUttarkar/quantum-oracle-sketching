import argparse
import json

import bucket_utils
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

num_markers = 40

colors = {
    "quantum": "#CD591A",
    "streaming": "#2657AF",
    "sparse": "#606060",
    "jl_streaming": "#2A8C55",
}
labels = {
    "streaming": "Classical streaming",
    "sparse": "Classical sparse / QRAM",
    "quantum": "Quantum oracle sketching",
    "jl_streaming": "Classical sparse JL",
}
markers = {"streaming": "P", "sparse": "X", "quantum": "D", "jl_streaming": "o"}
markersize = {"streaming": 50, "sparse": 50, "quantum": 30, "jl_streaming": 42}
linewidth_marker = {"streaming": 0, "sparse": 0, "quantum": 0, "jl_streaming": 0}


def streaming_label_for_mode(mode):
    if mode == "bucket":
        return "Classical feature hashing"
    if mode == "jl":
        return "Classical sparse JL"
    return labels["streaming"]


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
    accuracy_panel=True,
    mode="rare",
):
    if x_std is not None and np.any(x_std > 0):
        ax.fill_betweenx(
            y_mean,
            x_mean - x_std,
            x_mean + x_std,
            color=color,
            alpha=0.2,
            edgecolor="none",
        )

    ax.plot(x_mean, y_mean, linestyle="-", color=color, linewidth=1.5, alpha=0.9)

    if mode in ("bucket", "jl"):
        marker_indices = np.arange(len(x_mean))
    elif accuracy_panel:
        marker_indices = np.arange(len(x_mean))
    else:
        x_min, x_max = np.min(x_mean), np.max(x_mean)
        target_x = np.linspace(x_min, x_max, num=num_markers)
        marker_indices = []
        for tx in target_x:
            idx = (np.abs(x_mean - tx)).argmin()
            if idx not in marker_indices:
                marker_indices.append(idx)
        marker_indices += [-5, -10, -15, -20]

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


def mean_and_sem(values):
    vals = np.array(values, dtype=float).reshape(-1)
    return float(np.mean(vals)), float(np.std(vals) / np.sqrt(vals.size))


def compute_stats_from_json(data, metric_type, keys=None):
    if keys is None:
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
        raw_data = data["raw_data_by_min_samples"]
    min_samps = sorted([int(k) for k in raw_data.keys()])

    for ms in min_samps:
        for k in keys:
            entry = raw_data[str(ms)][k]

            if "space_by_seed_pair" in entry:
                space, space_sem = mean_and_sem(entry["space_by_seed_pair"])
            elif "space_by_seed" in entry:
                space, space_sem = mean_and_sem(entry["space_by_seed"])
            else:
                space = float(entry["space"])
                space_sem = 0.0
            final_stats[k]["mean_space"].append(space)
            final_stats[k]["std_space"].append(space_sem)

            if metric_type == "accuracy":
                if "accuracy_scores_by_seed_pair" in entry:
                    acc_mean, acc_sem = mean_and_sem(
                        entry["accuracy_scores_by_seed_pair"]
                    )
                elif "accuracy_scores_by_pair" in entry:
                    acc_mean, acc_sem = mean_and_sem(entry["accuracy_scores_by_pair"])
                else:
                    acc_mean = float(entry["accuracy_mean"])
                    acc_sem = float(entry["accuracy_sem"])
                final_stats[k]["mean_x"].append(acc_mean)
                final_stats[k]["std_x"].append(acc_sem)

            elif metric_type == "variance":
                if "variance_recovery_by_seed" in entry:
                    var_rec, var_sem = mean_and_sem(entry["variance_recovery_by_seed"])
                else:
                    var_rec = float(entry["variance_recovery"])
                    var_sem = float(entry.get("variance_recovery_sem", 0.0))
                final_stats[k]["mean_x"].append(var_rec)
                final_stats[k]["std_x"].append(var_sem)

    for k in keys:
        for field in final_stats[k]:
            final_stats[k][field] = np.array(final_stats[k][field])

    return final_stats


def plot_jl_streaming(ax, stats):
    xm, xs, ym, ys = get_sorted_arrays(
        stats["streaming"]["mean_x"],
        stats["streaming"]["std_x"],
        stats["streaming"]["mean_space"],
        stats["streaming"]["std_space"],
    )
    if xs is not None and np.any(xs > 0):
        ax.fill_betweenx(
            ym,
            xm - xs,
            xm + xs,
            color=colors["jl_streaming"],
            alpha=0.10,
            edgecolor="none",
            zorder=1,
        )
    ax.plot(
        xm,
        ym,
        linestyle=(0, (1, 1.15)),
        color=colors["jl_streaming"],
        linewidth=1.8,
        alpha=0.95,
        dash_capstyle="round",
        zorder=4,
    )
    marker_indices = np.arange(len(xm))
    ax.scatter(
        xm[marker_indices],
        ym[marker_indices],
        marker=markers["jl_streaming"],
        facecolors="none",
        edgecolors=colors["jl_streaming"],
        label=labels["jl_streaming"],
        alpha=0.98,
        s=markersize["jl_streaming"],
        linewidth=1.2,
        zorder=5,
    )


def plot_accuracy_panel(ax, stats, mode="rare", jl_stats=None):
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
            (streaming_label_for_mode(mode) if k == "streaming" else labels[k]),
            linewidth_marker[k],
            markersize[k],
            mode=mode,
        )
    if jl_stats is not None:
        plot_jl_streaming(ax, jl_stats)

    halo = [pe.withStroke(linewidth=3, foreground="white")]

    if mode in ("bucket", "jl"):
        ax.text(
            0.2,
            0.9,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        ax.text(
            0.9,
            0.62,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
        )
        ax.text(
            0.15,
            0.04,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        if jl_stats is not None:
            ax.text(
                0.7,
                0.45,
                "Classical sparse JL",
                color=colors["jl_streaming"],
                fontsize=10,
                path_effects=halo,
                transform=ax.transAxes,
                ha="right",
            )
    else:
        ax.text(
            0.81,
            2e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
        )
        ax.text(
            0.888,
            1.2e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        ax.text(
            0.90,
            1.7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    ax.set_yscale("log")
    ax.set_ylim(1e1, 1e7)
    ax.set_xlabel("Accuracy")

    if mode in ("bucket", "jl"):
        ax.set_xticks([0.80, 0.82, 0.84, 0.86, 0.88, 0.90])
        ax.set_xticklabels(["80%", "82%", "84%", "86%", "88%", "90%"])
        ax.set_xlim(0.795, 0.91)
    else:
        ax.set_xticks([0.80, 0.82, 0.84, 0.86, 0.88, 0.90])
        ax.set_xticklabels(["80%", "82%", "84%", "86%", "88%", "90%"])
        ax.set_xlim(0.795, 0.915)

    ax.set_ylabel("Machine size")
    ax.tick_params(direction="in", which="both", top=False, right=True)
    ax.grid(True, which="major", ls="-", alpha=0.1)
    ax.set_title("Binary classification")


def plot_variance_panel(ax, stats, mode="rare", jl_stats=None):
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
            (streaming_label_for_mode(mode) if k == "streaming" else labels[k]),
            linewidth_marker[k],
            markersize[k],
            mode=mode,
        )
    if jl_stats is not None:
        plot_jl_streaming(ax, jl_stats)

    halo = [pe.withStroke(linewidth=3, foreground="white")]

    if mode in ("bucket", "jl"):
        ax.text(
            0.2,
            0.9,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        ax.text(
            0.9,
            0.62,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
            ha="right",
        )
        ax.text(
            0.15,
            0.04,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            transform=ax.transAxes,
        )
        if jl_stats is not None:
            ax.text(
                0.9,
                0.45,
                "Classical sparse JL",
                color=colors["jl_streaming"],
                fontsize=10,
                path_effects=halo,
                transform=ax.transAxes,
                ha="right",
            )
    else:
        ax.text(
            1,
            1e6,
            "Classical sparse / QRAM",
            color=colors["sparse"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        ax.text(
            0.996,
            1.2e4,
            streaming_label_for_mode(mode),
            color=colors["streaming"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )
        ax.text(
            1,
            1.7e1,
            "Quantum oracle sketching",
            color=colors["quantum"],
            fontsize=10,
            path_effects=halo,
            ha="right",
        )

    ax.set_yscale("log")
    ax.set_ylim(1e1, 1e7)
    ax.set_xlabel("Relative explained variance")

    if mode in ("bucket", "jl"):
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
        ax.set_xlim(-0.1, 1.1)
    else:
        ax.set_xticks([0.92, 0.94, 0.96, 0.98, 1.0])
        ax.set_xticklabels(["92%", "94%", "96%", "98%", "100%"])
        ax.set_xlim(0.915, 1.005)

    ax.tick_params(direction="in", which="both", top=False, right=True)
    ax.grid(True, which="major", ls="-", alpha=0.1)
    ax.set_title("Dimension reduction")


def main():
    parser = argparse.ArgumentParser(
        description="Combine PBMC68k size-vs-accuracy and size-vs-variance plots."
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
        "--jl-accuracy-json",
        type=str,
        default=None,
        help="Path to JL accuracy JSON for bucket_jl mode.",
    )
    parser.add_argument(
        "--jl-variance-json",
        type=str,
        default=None,
        help="Path to JL variance JSON for bucket_jl mode.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output figure path.",
    )
    parser.add_argument(
        "--mode",
        choices=["rare", "bucket", "jl", "bucket_jl"],
        required=True,
    )
    args = parser.parse_args()

    if args.mode in ("bucket", "bucket_jl"):
        if args.accuracy_json is None:
            args.accuracy_json = "pbmc68k_bucket_size_vs_accuracy.json"
        if args.variance_json is None:
            args.variance_json = "pbmc68k_bucket_size_vs_variance.json"
        if args.mode == "bucket_jl":
            if args.jl_accuracy_json is None:
                args.jl_accuracy_json = "pbmc68k_jl_size_vs_accuracy.json"
            if args.jl_variance_json is None:
                args.jl_variance_json = "pbmc68k_jl_size_vs_variance.json"
    elif args.mode == "jl":
        if args.accuracy_json is None:
            args.accuracy_json = "pbmc68k_jl_size_vs_accuracy.json"
        if args.variance_json is None:
            args.variance_json = "pbmc68k_jl_size_vs_variance.json"
    else:
        if args.accuracy_json is None:
            args.accuracy_json = "pbmc68k_size_vs_accuracy.json"
        if args.variance_json is None:
            args.variance_json = "pbmc68k_size_vs_variance.json"

    with open(args.accuracy_json, "r") as f:
        accuracy_data = json.load(f)
    with open(args.variance_json, "r") as f:
        variance_data = json.load(f)
    if args.mode != "bucket_jl":
        bucket_utils.validate_truncation_data(
            accuracy_data, args.mode, args.accuracy_json
        )
        bucket_utils.validate_truncation_data(
            variance_data, args.mode, args.variance_json
        )
    jl_accuracy_data = None
    jl_variance_data = None
    if args.mode == "bucket_jl":
        with open(args.jl_accuracy_json, "r") as f:
            jl_accuracy_data = json.load(f)
        with open(args.jl_variance_json, "r") as f:
            jl_variance_data = json.load(f)

    for path, data in [
        (args.accuracy_json, accuracy_data),
        (args.variance_json, variance_data),
    ]:
        is_feature_mode = "raw_data_by_n_features" in data
        if is_feature_mode != (args.mode in ("bucket", "jl", "bucket_jl")):
            raise ValueError(f"{path} does not match --mode {args.mode}")
        if args.mode == "bucket_jl" and data.get("truncation_mode") not in (
            None,
            "bucket",
        ):
            raise ValueError(f"{path} is not bucket data")
    if args.mode == "bucket_jl":
        for path, data in [
            (args.jl_accuracy_json, jl_accuracy_data),
            (args.jl_variance_json, jl_variance_data),
        ]:
            if "raw_data_by_n_features" not in data:
                raise ValueError(f"{path} does not contain JL feature-sweep data")
            if data.get("truncation_mode") not in (None, "jl"):
                raise ValueError(f"{path} is not JL data")
            if data.get("jl_transform") != bucket_utils.SPARSE_JL_TRANSFORM:
                raise ValueError(
                    f"{path} was not generated with balanced signed sparse JL"
                )

    if args.out is None:
        if args.mode == "bucket":
            args.out = "pbmc68k_bucket_combine.pdf"
        elif args.mode == "bucket_jl":
            args.out = "pbmc68k_bucket_jl_combine.pdf"
        elif args.mode == "jl":
            args.out = "pbmc68k_jl_combine.pdf"
        else:
            args.out = "pbmc68k_combine.pdf"

    plot_mode = "bucket" if args.mode == "bucket_jl" else args.mode
    accuracy_stats = compute_stats_from_json(accuracy_data, "accuracy")
    variance_stats = compute_stats_from_json(variance_data, "variance")
    jl_accuracy_stats = None
    jl_variance_stats = None
    if args.mode == "bucket_jl":
        jl_accuracy_stats = compute_stats_from_json(
            jl_accuracy_data, "accuracy", keys=["streaming"]
        )
        jl_variance_stats = compute_stats_from_json(
            jl_variance_data, "variance", keys=["streaming"]
        )

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(6, 3.5), sharey=True)
    plot_accuracy_panel(
        ax_left, accuracy_stats, mode=plot_mode, jl_stats=jl_accuracy_stats
    )
    plot_variance_panel(
        ax_right, variance_stats, mode=plot_mode, jl_stats=jl_variance_stats
    )

    ax_right.tick_params(axis="y", labelleft=False)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
