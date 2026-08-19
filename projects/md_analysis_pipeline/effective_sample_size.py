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

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# PARAMETERS
# ============================================================

PARAMETERS = [
    "rmsd_A",
    "rg_A",
    "hbonds"
]

MAX_LAG_FRACTION = 0.5


# ============================================================
# AUTOCORRELATION FUNCTION
# ============================================================

def autocorrelation(series, max_lag=None):

    values = np.asarray(series, dtype=float)

    values = values[
        np.isfinite(values)
    ]

    n = len(values)

    if n < 3:
        raise ValueError(
            "At least 3 observations are required."
        )

    values = values - np.mean(values)

    variance = np.var(
        values,
        ddof=0
    )

    if variance == 0:
        return np.ones(1)

    if max_lag is None:

        max_lag = max(
            1,
            int(n * MAX_LAG_FRACTION)
        )

    acf = []

    for lag in range(max_lag + 1):

        if lag == 0:

            acf.append(1.0)

            continue

        numerator = np.sum(
            values[:-lag] *
            values[lag:]
        )

        denominator = np.sum(
            values ** 2
        )

        acf.append(
            numerator / denominator
        )

    return np.array(acf)


# ============================================================
# INTEGRATED AUTOCORRELATION TIME
# ============================================================

def integrated_autocorrelation_time(acf):

    tau = 0.5

    for lag in range(1, len(acf)):

        rho = acf[lag]

        # Initial-positive-sequence criterion.
        # Stop once autocorrelation becomes zero/negative.
        if rho <= 0:

            break

        tau += rho

    return tau


# ============================================================
# EFFECTIVE SAMPLE SIZE
# ============================================================

def effective_sample_size(n, tau):

    if tau <= 0:

        return float(n)

    ess = n / (
        2.0 * tau
    )

    return min(
        float(n),
        max(1.0, ess)
    )


# ============================================================
# ANALYZE ONE PARAMETER
# ============================================================

def analyze_parameter(data, parameter):

    if parameter not in data.columns:

        return None

    values = data[parameter].dropna()

    n = len(values)

    if n < 3:

        return None

    acf = autocorrelation(
        values
    )

    tau = integrated_autocorrelation_time(
        acf
    )

    ess = effective_sample_size(
        n,
        tau
    )

    independence_fraction = ess / n

    return {
        "parameter": parameter,
        "frames": n,
        "integrated_autocorrelation_time": tau,
        "effective_sample_size": ess,
        "independence_fraction": independence_fraction,
        "autocorrelation_lag_1": (
            acf[1]
            if len(acf) > 1
            else np.nan
        ),
        "autocorrelation_lag_2": (
            acf[2]
            if len(acf) > 2
            else np.nan
        )
    }, acf


# ============================================================
# LOAD INPUT DATA
# ============================================================

print("=" * 60)
print("        EFFECTIVE SAMPLE SIZE ANALYSIS")
print("=" * 60)

input_files = {
    "rmsd_A": INPUT_DIR / "rmsd.csv",
    "rg_A": INPUT_DIR / "rg.csv",
    "hbonds": INPUT_DIR / "hbonds.csv"
}


data = {}

for parameter, filepath in input_files.items():

    if not filepath.exists():

        print(
            f"WARNING: {filepath} not found."
        )

        continue

    df = pd.read_csv(
        filepath
    )

    if parameter not in df.columns:

        print(
            f"WARNING: {parameter} not found "
            f"in {filepath.name}"
        )

        continue

    data[parameter] = df


# ============================================================
# ANALYSIS
# ============================================================

results = []

acf_results = {}

for parameter in PARAMETERS:

    if parameter not in data:

        continue

    print(
        f"\nAnalyzing: {parameter}"
    )

    result = analyze_parameter(
        data[parameter],
        parameter
    )

    if result is None:

        print(
            "Insufficient data."
        )

        continue

    statistics, acf = result

    results.append(
        statistics
    )

    acf_results[parameter] = acf

    print(
        f"Frames: {statistics['frames']}"
    )

    print(
        "Lag-1 autocorrelation: "
        f"{statistics['autocorrelation_lag_1']:.3f}"
    )

    print(
        "Integrated autocorrelation time: "
        f"{statistics['integrated_autocorrelation_time']:.3f}"
    )

    print(
        "Effective sample size: "
        f"{statistics['effective_sample_size']:.2f}"
    )

    print(
        "Independent-frame fraction: "
        f"{statistics['independence_fraction']:.3f}"
    )


# ============================================================
# SAVE CSV
# ============================================================

results_df = pd.DataFrame(
    results
)

csv_file = (
    RESULTS_DIR /
    "effective_sample_size.csv"
)

results_df.to_csv(
    csv_file,
    index=False
)


# ============================================================
# AUTOCORRELATION PLOT
# ============================================================

if acf_results:

    plt.figure(
        figsize=(9, 6)
    )

    for parameter, acf in acf_results.items():

        lags = np.arange(
            len(acf)
        )

        plt.plot(
            lags,
            acf,
            marker="o",
            label=parameter
        )

    plt.axhline(
        0,
        linestyle="--",
        linewidth=1
    )

    plt.xlabel(
        "Lag (frames)"
    )

    plt.ylabel(
        "Autocorrelation"
    )

    plt.title(
        "MD Trajectory Autocorrelation"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plot_file = (
        RESULTS_DIR /
        "autocorrelation.png"
    )

    plt.savefig(
        plot_file,
        dpi=300
    )

    plt.close()

else:

    plot_file = None


# ============================================================
# SCIENTIFIC REPORT
# ============================================================

report_file = (
    RESULTS_DIR /
    "effective_sample_size_report.txt"
)


with open(
    report_file,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "=" * 60 + "\n"
    )

    report.write(
        "        EFFECTIVE SAMPLE SIZE ANALYSIS\n"
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
        "Effective sample size (ESS) estimates the number of "
        "approximately independent observations represented by "
        "a temporally correlated MD trajectory.\n\n"
    )

    report.write(
        "METHOD\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "Autocorrelation was calculated across trajectory frames. "
        "The integrated autocorrelation time was estimated using "
        "an initial-positive-sequence approach, and ESS was "
        "estimated as N/(2*tau).\n\n"
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
            "Lag-1 autocorrelation: "
            f"{row['autocorrelation_lag_1']:.4f}\n"
        )

        report.write(
            "Lag-2 autocorrelation: "
            f"{row['autocorrelation_lag_2']:.4f}\n"
        )

        report.write(
            "Integrated autocorrelation time: "
            f"{row['integrated_autocorrelation_time']:.4f}\n"
        )

        report.write(
            "Effective sample size: "
            f"{row['effective_sample_size']:.2f}\n"
        )

        report.write(
            "Independent-frame fraction: "
            f"{row['independence_fraction']:.4f}\n"
        )

    report.write(
        "\n\nSCIENTIFIC INTERPRETATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "MD trajectory frames are generally temporally correlated "
        "and therefore should not automatically be treated as "
        "independent statistical observations. ESS provides a "
        "more conservative estimate of the information content "
        "of the trajectory than the raw frame count.\n\n"
    )

    report.write(
        "A substantially smaller ESS than the raw number of frames "
        "indicates strong temporal correlation. Statistical tests "
        "and confidence intervals based on the raw frame count "
        "should therefore be interpreted cautiously.\n\n"
    )

    report.write(
        "IMPORTANT LIMITATION\n"
    )

    report.write(
        "-" * 60 + "\n"
    )

    report.write(
        "The present dataset contains only a limited number of "
        "trajectory frames. ESS estimates can therefore be "
        "unstable and should be interpreted as diagnostic rather "
        "than definitive. For production MD analysis, a much "
        "larger number of appropriately sampled frames is "
        "recommended.\n"
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print(
    "\n=============================================="
)

print(
    " EFFECTIVE SAMPLE SIZE ANALYSIS COMPLETE"
)

print(
    "=============================================="
)

print(
    f"\nCSV: {csv_file}"
)

print(
    f"Report: {report_file}"
)

if plot_file:

    print(
        f"Plot: {plot_file}"
    )
