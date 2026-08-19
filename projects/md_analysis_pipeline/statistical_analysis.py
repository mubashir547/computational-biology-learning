import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr, spearmanr, t

# ==========================================
# PROJECT DIRECTORIES
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"

SUMMARY_FILE = RESULTS_DIR / "summary.csv"

OUTPUT_CSV = RESULTS_DIR / "statistical_correlations.csv"
OUTPUT_REPORT = RESULTS_DIR / "statistical_correlation_report.txt"


# ==========================================
# LOAD DATA
# ==========================================

data_files = {
    "rmsd_A": RESULTS_DIR / "../input/rmsd.csv",
    "rg_A": RESULTS_DIR / "../input/rg.csv",
    "hbonds": RESULTS_DIR / "../input/hbonds.csv",
}

datasets = {}

for parameter, filepath in data_files.items():

    filepath = filepath.resolve()

    if not filepath.exists():
        raise FileNotFoundError(
            f"Required input file not found: {filepath}"
        )

    data = pd.read_csv(filepath)

    if parameter not in data.columns:
        raise ValueError(
            f"Column '{parameter}' not found in {filepath}"
        )

    datasets[parameter] = data[parameter].dropna()


# ==========================================
# BOOTSTRAP CONFIDENCE INTERVAL
# ==========================================

def bootstrap_correlation(
    x,
    y,
    method="pearson",
    iterations=5000,
    confidence=0.95,
    random_seed=42
):

    rng = np.random.default_rng(random_seed)

    x = np.asarray(x)
    y = np.asarray(y)

    n = len(x)

    observed_values = []

    for _ in range(iterations):

        indices = rng.integers(
            0,
            n,
            n
        )

        xb = x[indices]
        yb = y[indices]

        if method == "pearson":

            value = pearsonr(
                xb,
                yb
            ).statistic

        else:

            value = spearmanr(
                xb,
                yb
            ).statistic

        observed_values.append(value)

    alpha = 1 - confidence

    lower = np.percentile(
        observed_values,
        100 * alpha / 2
    )

    upper = np.percentile(
        observed_values,
        100 * (1 - alpha / 2)
    )

    return lower, upper


# ==========================================
# PAIRWISE ANALYSIS
# ==========================================

pairs = [
    ("rmsd_A", "rg_A"),
    ("rmsd_A", "hbonds"),
    ("rg_A", "hbonds"),
]

results = []


for parameter_x, parameter_y in pairs:

    x = datasets[parameter_x]
    y = datasets[parameter_y]

    n = min(
        len(x),
        len(y)
    )

    x = x.iloc[:n]
    y = y.iloc[:n]

    # --------------------------------------
    # Pearson
    # --------------------------------------

    pearson_result = pearsonr(
        x,
        y
    )

    pearson_r = pearson_result.statistic
    pearson_p = pearson_result.pvalue

    pearson_ci_low, pearson_ci_high = (
        bootstrap_correlation(
            x,
            y,
            method="pearson"
        )
    )

    # --------------------------------------
    # Spearman
    # --------------------------------------

    spearman_result = spearmanr(
        x,
        y
    )

    spearman_rho = spearman_result.statistic
    spearman_p = spearman_result.pvalue

    spearman_ci_low, spearman_ci_high = (
        bootstrap_correlation(
            x,
            y,
            method="spearman"
        )
    )

    results.append({

        "parameter_x": parameter_x,

        "parameter_y": parameter_y,

        "n": n,

        "pearson_r": pearson_r,

        "pearson_p": pearson_p,

        "pearson_ci_low": pearson_ci_low,

        "pearson_ci_high": pearson_ci_high,

        "spearman_rho": spearman_rho,

        "spearman_p": spearman_p,

        "spearman_ci_low": spearman_ci_low,

        "spearman_ci_high": spearman_ci_high
    })


# ==========================================
# SAVE CSV
# ==========================================

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ==========================================
# INTERPRETATION
# ==========================================

def interpret_strength(value):

    value = abs(value)

    if value >= 0.90:
        return "very strong"

    elif value >= 0.70:
        return "strong"

    elif value >= 0.50:
        return "moderate"

    elif value >= 0.30:
        return "weak"

    else:
        return "very weak"


# ==========================================
# REPORT
# ==========================================

report = []

report.append(
    "=" * 60
)

report.append(
    "        STATISTICAL MD CORRELATION ANALYSIS"
)

report.append(
    "=" * 60
)

report.append("")

report.append(
    "METHODS"
)

report.append(
    "-" * 60
)

report.append(
    "Pearson correlation was used to assess linear association."
)

report.append(
    "Spearman correlation was used to assess monotonic association."
)

report.append(
    "95% confidence intervals were estimated using bootstrap resampling."
)

report.append(
    "Bootstrap iterations: 5000"
)

report.append("")


report.append(
    "PAIRWISE RESULTS"
)

report.append(
    "-" * 60
)


for _, row in results_df.iterrows():

    x = row["parameter_x"]
    y = row["parameter_y"]

    report.append("")

    report.append(
        f"{x} vs {y}"
    )

    report.append(
        f"n: {int(row['n'])}"
    )

    report.append(
        f"Pearson r: {row['pearson_r']:.3f}"
    )

    report.append(
        f"Pearson p-value: {row['pearson_p']:.6g}"
    )

    report.append(
        f"Pearson 95% CI: "
        f"{row['pearson_ci_low']:.3f} to "
        f"{row['pearson_ci_high']:.3f}"
    )

    report.append(
        f"Pearson interpretation: "
        f"{interpret_strength(row['pearson_r'])} "
        f"{'positive' if row['pearson_r'] > 0 else 'negative'} "
        f"association"
    )

    report.append(
        f"Spearman rho: {row['spearman_rho']:.3f}"
    )

    report.append(
        f"Spearman p-value: {row['spearman_p']:.6g}"
    )

    report.append(
        f"Spearman 95% CI: "
        f"{row['spearman_ci_low']:.3f} to "
        f"{row['spearman_ci_high']:.3f}"
    )


report.append("")

report.append(
    "SCIENTIFIC NOTE"
)

report.append(
    "-" * 60
)

report.append(
    "Correlation quantifies statistical association and does not "
    "establish causation. MD trajectory observations are also "
    "temporally correlated, so effective sample size and "
    "independence should be considered when interpreting "
    "p-values and confidence intervals."
)

report.append("")

report.append(
    "OUTPUT"
)

report.append(
    f"Results CSV: {OUTPUT_CSV.name}"
)

report.append(
    f"Report: {OUTPUT_REPORT.name}"
)


with open(
    OUTPUT_REPORT,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(report)
    )


print(
    "=============================================="
)

print(
    " STATISTICAL CORRELATION ANALYSIS COMPLETE"
)

print(
    "=============================================="
)

print(
    f"CSV: {OUTPUT_CSV}"
)

print(
    f"Report: {OUTPUT_REPORT}"
)