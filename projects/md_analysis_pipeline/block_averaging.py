import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RMSD_FILE = INPUT_DIR / "rmsd.csv"
RG_FILE = INPUT_DIR / "rg.csv"
HBONDS_FILE = INPUT_DIR / "hbonds.csv"

OUTPUT_CSV = RESULTS_DIR / "block_statistics.csv"
OUTPUT_REPORT = RESULTS_DIR / "block_averaging_report.txt"
OUTPUT_PLOT = RESULTS_DIR / "block_averaging.png"


# ============================================================
# PARAMETERS
# ============================================================

PARAMETERS = {
    "rmsd_A": RMSD_FILE,
    "rg_A": RG_FILE,
    "hbonds": HBONDS_FILE,
}


# ============================================================
# LOAD DATA
# ============================================================

def load_parameter(parameter, filepath):

    if not filepath.exists():
        raise FileNotFoundError(
            f"Required input file not found: {filepath}"
        )

    data = pd.read_csv(filepath)

    if parameter not in data.columns:
        raise ValueError(
            f"Column '{parameter}' not found in {filepath}"
        )

    values = pd.to_numeric(
        data[parameter],
        errors="coerce"
    ).dropna()

    return values.to_numpy()


# ============================================================
# DETERMINE BLOCK SIZE
# ============================================================

def choose_block_size(n):

    """
    Choose a conservative block size.

    For very small datasets, use approximately 4 blocks.
    For larger datasets, increase the number of blocks while
    keeping enough observations per block.
    """

    if n < 8:
        return None

    if n < 20:
        return max(2, n // 4)

    if n < 40:
        return max(4, n // 5)

    if n < 100:
        return max(5, n // 8)

    return max(10, n // 10)


# ============================================================
# BLOCK STATISTICS
# ============================================================

def analyze_blocks(values):

    n = len(values)

    block_size = choose_block_size(n)

    if block_size is None:
        return None

    n_complete = (n // block_size) * block_size

    trimmed = values[:n_complete]

    blocks = trimmed.reshape(
        -1,
        block_size
    )

    block_means = blocks.mean(axis=1)

    n_blocks = len(block_means)

    overall_mean = values.mean()
    overall_sd = values.std(ddof=1)

    naive_sem = (
        overall_sd / np.sqrt(n)
    )

    block_sd = block_means.std(
        ddof=1
    )

    block_sem = (
        block_sd / np.sqrt(n_blocks)
    )

    return {
        "frames": n,
        "block_size": block_size,
        "blocks": n_blocks,
        "discarded_frames": n - n_complete,
        "mean": overall_mean,
        "sd": overall_sd,
        "naive_sem": naive_sem,
        "block_mean_sd": block_sd,
        "block_sem": block_sem,
        "block_means": block_means,
    }


# ============================================================
# ANALYZE ALL PARAMETERS
# ============================================================

results = []
plot_data = {}

print("=" * 60)
print("        BLOCK AVERAGING UNCERTAINTY ANALYSIS")
print("=" * 60)

for parameter, filepath in PARAMETERS.items():

    print(f"\nAnalyzing: {parameter}")

    values = load_parameter(
        parameter,
        filepath
    )

    analysis = analyze_blocks(values)

    if analysis is None:

        print(
            "WARNING: Not enough frames for "
            "reliable block analysis."
        )

        continue

    results.append({
        "parameter": parameter,
        "frames": analysis["frames"],
        "block_size": analysis["block_size"],
        "blocks": analysis["blocks"],
        "discarded_frames": analysis["discarded_frames"],
        "mean": analysis["mean"],
        "sd": analysis["sd"],
        "naive_sem": analysis["naive_sem"],
        "block_mean_sd": analysis["block_mean_sd"],
        "block_sem": analysis["block_sem"],
    })

    plot_data[parameter] = (
        analysis["block_means"]
    )

    print(
        f"Frames: {analysis['frames']}"
    )

    print(
        f"Block size: {analysis['block_size']}"
    )

    print(
        f"Blocks: {analysis['blocks']}"
    )

    print(
        f"Mean: {analysis['mean']:.4f}"
    )

    print(
        f"Naive SEM: {analysis['naive_sem']:.4f}"
    )

    print(
        f"Block SEM: {analysis['block_sem']:.4f}"
    )


# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# CREATE PLOT
# ============================================================

if plot_data:

    plt.figure(figsize=(9, 6))

    for parameter, block_means in plot_data.items():

        plt.plot(
            range(1, len(block_means) + 1),
            block_means,
            marker="o",
            label=parameter
        )

    plt.xlabel("Block number")
    plt.ylabel("Block mean")

    plt.title(
        "MD Block-Averaging Convergence"
    )

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_PLOT,
        dpi=300
    )

    plt.close()


# ============================================================
# GENERATE REPORT
# ============================================================

with open(
    OUTPUT_REPORT,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "=" * 60 + "\n"
    )

    report.write(
        "        BLOCK AVERAGING UNCERTAINTY ANALYSIS\n"
    )

    report.write(
        "=" * 60 + "\n\n"
    )

    report.write(
        "PURPOSE\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Block averaging was used to estimate uncertainty "
        "while accounting for temporal correlation between "
        "neighboring MD trajectory frames.\n\n"
    )

    report.write(
        "METHOD\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "The trajectory was divided into approximately equal "
        "blocks. Means were calculated for each block, and "
        "the variability among block means was used to estimate "
        "a block-based standard error. Incomplete trailing "
        "frames were excluded from block calculations.\n\n"
    )

    report.write(
        "RESULTS\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    for _, row in results_df.iterrows():

        report.write(
            f"\n{row['parameter']}\n"
        )

        report.write(
            f"Frames: {int(row['frames'])}\n"
        )

        report.write(
            f"Block size: {int(row['block_size'])}\n"
        )

        report.write(
            f"Number of blocks: {int(row['blocks'])}\n"
        )

        report.write(
            f"Discarded trailing frames: "
            f"{int(row['discarded_frames'])}\n"
        )

        report.write(
            f"Mean: {row['mean']:.4f}\n"
        )

        report.write(
            f"Standard deviation: {row['sd']:.4f}\n"
        )

        report.write(
            f"Naive SEM: {row['naive_sem']:.4f}\n"
        )

        report.write(
            f"Block mean SD: {row['block_mean_sd']:.4f}\n"
        )

        report.write(
            f"Block-based SEM: {row['block_sem']:.4f}\n"
        )

    report.write(
        "\n\nSCIENTIFIC INTERPRETATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Frame-level standard errors assume that observations "
        "are independent. MD trajectory frames are commonly "
        "temporally correlated, so this assumption can lead "
        "to overconfident uncertainty estimates. Block "
        "averaging provides a simple diagnostic approach for "
        "evaluating how uncertainty changes when correlated "
        "frames are grouped together.\n\n"
    )

    report.write(
        "LIMITATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "The present demonstration trajectory contains only "
        "a small number of frames. Consequently, the number "
        "of available blocks is limited and block-based "
        "uncertainty estimates may themselves be unstable. "
        "For production MD studies, substantially longer "
        "trajectories with appropriately sampled frames are "
        "recommended.\n"
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print(" BLOCK AVERAGING ANALYSIS COMPLETE")
print("=" * 60)

print(f"\nCSV: {OUTPUT_CSV}")
print(f"Report: {OUTPUT_REPORT}")
print(f"Plot: {OUTPUT_PLOT}")
