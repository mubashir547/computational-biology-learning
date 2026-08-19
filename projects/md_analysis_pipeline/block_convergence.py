import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# DIRECTORIES
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = RESULTS_DIR / "block_convergence.csv"
OUTPUT_REPORT = RESULTS_DIR / "block_convergence_report.txt"
OUTPUT_PLOT = RESULTS_DIR / "block_convergence.png"


PARAMETERS = {
    "rmsd_A": INPUT_DIR / "rmsd.csv",
    "rg_A": INPUT_DIR / "rg.csv",
    "hbonds": INPUT_DIR / "hbonds.csv",
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data(filepath, parameter):

    data = pd.read_csv(filepath)

    if parameter not in data.columns:
        raise ValueError(
            f"{parameter} not found in {filepath}"
        )

    return pd.to_numeric(
        data[parameter],
        errors="coerce"
    ).dropna().to_numpy()


# ============================================================
# BLOCK ANALYSIS
# ============================================================

def block_statistics(values, block_size):

    n = len(values)

    n_blocks = n // block_size

    if n_blocks < 2:
        return None

    usable = (
        n_blocks * block_size
    )

    trimmed = values[:usable]

    blocks = trimmed.reshape(
        n_blocks,
        block_size
    )

    block_means = blocks.mean(axis=1)

    block_mean_sd = block_means.std(
        ddof=1
    )

    block_sem = (
        block_mean_sd /
        np.sqrt(n_blocks)
    )

    return {
        "frames": n,
        "block_size": block_size,
        "blocks": n_blocks,
        "discarded_frames": n - usable,
        "block_mean_sd": block_mean_sd,
        "block_sem": block_sem,
    }


# ============================================================
# RUN ANALYSIS
# ============================================================

print("=" * 60)
print("        BLOCK-SIZE CONVERGENCE ANALYSIS")
print("=" * 60)

all_results = {}
plot_data = {}

for parameter, filepath in PARAMETERS.items():

    values = load_data(
        filepath,
        parameter
    )

    n = len(values)

    print(
        f"\nAnalyzing: {parameter}"
    )

    parameter_results = []

    # Test a range of block sizes.
    # Require at least 2 complete blocks.
    max_block_size = n // 2

    for block_size in range(
        2,
        max_block_size + 1
    ):

        result = block_statistics(
            values,
            block_size
        )

        if result is None:
            continue

        result["parameter"] = parameter

        parameter_results.append(
            result
        )

        print(
            f"Block size {block_size}: "
            f"{result['blocks']} blocks, "
            f"SEM = {result['block_sem']:.5f}"
        )

    all_results[parameter] = (
        parameter_results
    )

    plot_data[parameter] = (
        [r["block_size"] for r in parameter_results],
        [r["block_sem"] for r in parameter_results]
    )


# ============================================================
# SAVE CSV
# ============================================================

rows = []

for parameter, parameter_results in all_results.items():

    rows.extend(
        parameter_results
    )

results_df = pd.DataFrame(rows)

results_df = results_df[
    [
        "parameter",
        "frames",
        "block_size",
        "blocks",
        "discarded_frames",
        "block_mean_sd",
        "block_sem",
    ]
]

results_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9, 6))

for parameter, (
    block_sizes,
    sem_values
) in plot_data.items():

    plt.plot(
        block_sizes,
        sem_values,
        marker="o",
        label=parameter
    )

plt.xlabel(
    "Block size (frames)"
)

plt.ylabel(
    "Block-based SEM"
)

plt.title(
    "Block-Size Convergence of MD Uncertainty"
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
# REPORT
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
        "        BLOCK-SIZE CONVERGENCE ANALYSIS\n"
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
        "Block-size sensitivity was evaluated to determine "
        "how uncertainty estimates change as increasingly "
        "large groups of temporally correlated MD frames "
        "are averaged together.\n\n"
    )

    report.write(
        "METHOD\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Multiple block sizes were evaluated independently. "
        "For each block size, complete blocks were constructed, "
        "block means were calculated, and the standard error "
        "of the block means was estimated.\n\n"
    )

    report.write(
        "RESULTS\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    for parameter, parameter_results in all_results.items():

        report.write(
            f"\n{parameter}\n"
        )

        for result in parameter_results:

            report.write(
                f"Block size: "
                f"{result['block_size']} frames | "
                f"Blocks: "
                f"{result['blocks']} | "
                f"Discarded: "
                f"{result['discarded_frames']} | "
                f"Block SEM: "
                f"{result['block_sem']:.5f}\n"
            )

    report.write(
        "\n\nSCIENTIFIC INTERPRETATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Block-size convergence provides a diagnostic for "
        "whether uncertainty estimates become stable as "
        "temporally correlated observations are grouped. "
        "Strong variation across block sizes indicates that "
        "the available trajectory may be too short to obtain "
        "a robust uncertainty estimate.\n\n"
    )

    report.write(
        "LIMITATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Only 21 frames are currently available. Consequently, "
        "large block sizes produce very few independent blocks, "
        "and apparent convergence should not be interpreted "
        "as definitive evidence of statistical convergence. "
        "Longer trajectories with substantially more sampled "
        "frames are required for production-level uncertainty "
        "quantification.\n"
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print(" BLOCK-SIZE CONVERGENCE ANALYSIS COMPLETE")
print("=" * 60)

print(f"\nCSV: {OUTPUT_CSV}")
print(f"Report: {OUTPUT_REPORT}")
print(f"Plot: {OUTPUT_PLOT}")
