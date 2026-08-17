import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
INPUT_DIR = PROJECT_DIR / "input"

OUTPUT_MATRIX = RESULTS_DIR / "stable_correlation_matrix.csv"
OUTPUT_REPORT = RESULTS_DIR / "stable_correlation_report.txt"


# ==========================================
# LOAD DATA
# ==========================================

rmsd = pd.read_csv(INPUT_DIR / "rmsd.csv")
rg = pd.read_csv(INPUT_DIR / "rg.csv")
hbonds = pd.read_csv(INPUT_DIR / "hbonds.csv")


# ==========================================
# MERGE DATA
# ==========================================

data = rmsd.merge(
    rg,
    on="time_ns"
).merge(
    hbonds,
    on="time_ns"
)


# ==========================================
# SELECT EQUILIBRATED REGION
# ==========================================

stable = data[
    data["time_ns"] >= 150
].copy()


if stable.empty:
    raise ValueError(
        "No data found in the 150–200 ns stable region."
    )


# ==========================================
# CORRELATION MATRIX
# ==========================================

parameters = [
    "rmsd_A",
    "rg_A",
    "hbonds"
]

correlation = stable[parameters].corr(
    method="pearson"
)


# ==========================================
# SAVE CORRELATION MATRIX
# ==========================================

correlation.to_csv(
    OUTPUT_MATRIX
)


# ==========================================
# INTERPRETATION FUNCTION
# ==========================================

def interpret_correlation(r):

    absolute_r = abs(r)

    if absolute_r >= 0.90:
        strength = "very strong"

    elif absolute_r >= 0.70:
        strength = "strong"

    elif absolute_r >= 0.50:
        strength = "moderate"

    elif absolute_r >= 0.30:
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
# GENERATE REPORT
# ==========================================

report = []

report.append("=" * 60)
report.append("        EQUILIBRATED MD CORRELATION ANALYSIS")
report.append("=" * 60)
report.append("")

report.append("STABLE REGION")
report.append("-" * 60)

report.append(
    f"Frames analyzed: {len(stable)}"
)

report.append(
    f"Time range: {stable['time_ns'].min()}–"
    f"{stable['time_ns'].max()} ns"
)

report.append("")

report.append("PEARSON CORRELATION MATRIX")
report.append("-" * 60)

report.append(
    correlation.to_string(
        float_format=lambda x: f"{x:.3f}"
    )
)

report.append("")

report.append("PAIRWISE INTERPRETATION")
report.append("-" * 60)


# ==========================================
# PAIRWISE ANALYSIS
# ==========================================

pairs = [
    (
        "RMSD",
        "rmsd_A",
        "Radius of Gyration",
        "rg_A"
    ),
    (
        "RMSD",
        "rmsd_A",
        "Hydrogen Bonds",
        "hbonds"
    ),
    (
        "Radius of Gyration",
        "rg_A",
        "Hydrogen Bonds",
        "hbonds"
    )
]


for name1, col1, name2, col2 in pairs:

    r = correlation.loc[col1, col2]

    report.append(
        f"{name1} vs {name2}"
    )

    report.append(
        f"Pearson r: {r:.3f}"
    )

    report.append(
        f"Interpretation: "
        f"{interpret_correlation(r)}"
    )

    report.append("")


# ==========================================
# SCIENTIFIC NOTE
# ==========================================

report.append("SCIENTIFIC NOTE")
report.append("-" * 60)

report.append(
    "Correlation describes linear association between "
    "MD observables and does not establish causation. "
    "Because the analysis is restricted to the equilibrated "
    "region, these relationships are less likely to reflect "
    "the initial structural adaptation phase. Nevertheless, "
    "correlation should be interpreted together with RMSD, "
    "Rg, hydrogen-bond, RMSF, and structural analyses."
)


# ==========================================
# WRITE REPORT
# ==========================================

with open(
    OUTPUT_REPORT,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(report)
    )


# ==========================================
# TERMINAL OUTPUT
# ==========================================

print("================================")
print(" STABLE REGION CORRELATION")
print("================================")

print(
    f"Frames analyzed: {len(stable)}"
)

print(
    f"Time range: {stable['time_ns'].min()}–"
    f"{stable['time_ns'].max()} ns"
)

print("\nCorrelation matrix:")

print(
    correlation.round(3)
)

print("\nFiles generated:")

print(
    OUTPUT_MATRIX
)

print(
    OUTPUT_REPORT
)
