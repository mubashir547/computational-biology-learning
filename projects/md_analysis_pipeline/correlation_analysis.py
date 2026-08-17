import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent

INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# INPUT FILES
# ==========================================

RMSD_FILE = INPUT_DIR / "rmsd.csv"
RG_FILE = INPUT_DIR / "rg.csv"
HBONDS_FILE = INPUT_DIR / "hbonds.csv"


# ==========================================
# OUTPUT FILES
# ==========================================

CORRELATION_FILE = (
    RESULTS_DIR / "correlation_matrix.csv"
)

REPORT_FILE = (
    RESULTS_DIR / "correlation_report.txt"
)

PLOT_FILE = (
    RESULTS_DIR / "correlation_heatmap.png"
)


# ==========================================
# LOAD DATA
# ==========================================

print("==========================================")
print("      MD CORRELATION ANALYSIS")
print("==========================================")

rmsd = pd.read_csv(RMSD_FILE)
rg = pd.read_csv(RG_FILE)
hbonds = pd.read_csv(HBONDS_FILE)


# ==========================================
# MERGE DATA BY TIME
# ==========================================

data = rmsd.merge(
    rg,
    on="time_ns",
    how="inner"
)

data = data.merge(
    hbonds,
    on="time_ns",
    how="inner"
)


# ==========================================
# SELECT PARAMETERS
# ==========================================

analysis_data = data[
    [
        "time_ns",
        "rmsd_A",
        "rg_A",
        "hbonds"
    ]
].copy()


print(
    f"\nFrames analyzed: {len(analysis_data)}"
)

print(
    f"Trajectory duration: "
    f"{analysis_data['time_ns'].max()} ns"
)


# ==========================================
# CALCULATE PEARSON CORRELATION
# ==========================================

correlation = analysis_data[
    [
        "rmsd_A",
        "rg_A",
        "hbonds"
    ]
].corr(
    method="pearson"
)


# ==========================================
# SAVE CORRELATION MATRIX
# ==========================================

correlation.to_csv(
    CORRELATION_FILE
)


# ==========================================
# PRINT RESULTS
# ==========================================

print("\n===== PEARSON CORRELATION MATRIX =====")

print(
    correlation.round(3)
)


# ==========================================
# CORRELATION INTERPRETATION
# ==========================================

def interpret_correlation(r):

    absolute_r = abs(r)

    if absolute_r >= 0.8:
        strength = "very strong"

    elif absolute_r >= 0.6:
        strength = "strong"

    elif absolute_r >= 0.4:
        strength = "moderate"

    elif absolute_r >= 0.2:
        strength = "weak"

    else:
        strength = "very weak"

    if r > 0:
        direction = "positive"

    elif r < 0:
        direction = "negative"

    else:
        direction = "no"

    return f"{strength} {direction} correlation"


# ==========================================
# CREATE REPORT
# ==========================================

with open(
    REPORT_FILE,
    "w"
) as report:

    report.write(
        "============================================================\n"
    )

    report.write(
        "        MD CORRELATION ANALYSIS REPORT\n"
    )

    report.write(
        "============================================================\n\n"
    )

    report.write(
        "DATASET\n"
    )

    report.write(
        "------------------------------------------------------------\n"
    )

    report.write(
        f"Frames analyzed: {len(analysis_data)}\n"
    )

    report.write(
        f"Trajectory duration: "
        f"{analysis_data['time_ns'].max()} ns\n\n"
    )

    report.write(
        "PEARSON CORRELATION MATRIX\n"
    )

    report.write(
        "------------------------------------------------------------\n"
    )

    report.write(
        correlation.round(3).to_string()
    )

    report.write("\n\n")

    pairs = [
        ("rmsd_A", "rg_A", "RMSD vs Radius of Gyration"),
        ("rmsd_A", "hbonds", "RMSD vs Hydrogen Bonds"),
        ("rg_A", "hbonds", "Radius of Gyration vs Hydrogen Bonds")
    ]

    report.write(
        "PAIRWISE INTERPRETATION\n"
    )

    report.write(
        "------------------------------------------------------------\n"
    )

    for parameter1, parameter2, label in pairs:

        r = correlation.loc[
            parameter1,
            parameter2
        ]

        interpretation = interpret_correlation(r)

        report.write(
            f"{label}\n"
        )

        report.write(
            f"Pearson r: {r:.3f}\n"
        )

        report.write(
            f"Interpretation: {interpretation}\n\n"
        )

    report.write(
        "SCIENTIFIC NOTE\n"
    )

    report.write(
        "------------------------------------------------------------\n"
    )

    report.write(
        "Correlation analysis describes linear association between "
        "MD observables. Correlation does not establish causation. "
        "The observed relationships should therefore be interpreted "
        "together with trajectory stability, structural analysis, "
        "hydrogen-bond analysis, RMSF, and other mechanistic evidence.\n"
    )


# ==========================================
# CREATE HEATMAP
# ==========================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    correlation,
    interpolation="nearest",
    aspect="auto"
)

plt.colorbar(
    label="Pearson correlation (r)"
)

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation.index)),
    correlation.index
)

# Add correlation values

for i in range(
    len(correlation.index)
):

    for j in range(
        len(correlation.columns)
    ):

        value = correlation.iloc[i, j]

        plt.text(
            j,
            i,
            f"{value:.2f}",
            ha="center",
            va="center"
        )


plt.title(
    "MD Parameter Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    PLOT_FILE,
    dpi=300
)

plt.close()


# ==========================================
# FINAL MESSAGE
# ==========================================

print("\n===== FILES GENERATED =====")

print(
    f"Correlation matrix:\n"
    f"{CORRELATION_FILE}"
)

print(
    f"\nCorrelation report:\n"
    f"{REPORT_FILE}"
)

print(
    f"\nHeatmap:\n"
    f"{PLOT_FILE}"
)

print("\n==========================================")
print("      CORRELATION ANALYSIS COMPLETE")
print("==========================================")