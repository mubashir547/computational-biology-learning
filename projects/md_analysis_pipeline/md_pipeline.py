import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==============================
# PROJECT DIRECTORIES
# ==============================

PROJECT_DIR = Path(
    "projects/md_analysis_pipeline"
)

INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==============================
# ANALYZE ONE FILE
# ==============================

def analyze_file(filepath):

    data = pd.read_csv(filepath)

    numeric_columns = [
        column
        for column in data.select_dtypes(
            include="number"
        ).columns
        if column != "time_ns"
    ]

    results = []

    for column in numeric_columns:

        results.append({
            "parameter": column,
            "frames": len(data),
            "mean": data[column].mean(),
            "minimum": data[column].min(),
            "maximum": data[column].max(),
            "std": data[column].std()
        })

    return data, results

def quality_control(data, filename):

    print("\n===== QUALITY CONTROL =====")
    print(f"File: {filename}")

    # Check required time column
    if "time_ns" not in data.columns:
        print("ERROR: time_ns column missing")
        return False

    # Check empty dataset
    if data.empty:
        print("ERROR: Dataset is empty")
        return False

    # Check missing values
    missing = data.isnull().sum()

    if missing.sum() > 0:
        print("WARNING: Missing values detected")
        print(missing)
    else:
        print("Missing values: PASS")

    # Check duplicate rows
    duplicates = data.duplicated().sum()

    if duplicates > 0:
        print(
            f"WARNING: {duplicates} duplicate rows"
        )
    else:
        print("Duplicate rows: PASS")

    # Check numeric time
    if not pd.api.types.is_numeric_dtype(
        data["time_ns"]
    ):
        print("ERROR: time_ns is not numeric")
        return False

    # Check time progression
    if not data["time_ns"].is_monotonic_increasing:
        print(
            "WARNING: Time is not monotonically increasing"
        )
    else:
        print("Time progression: PASS")

    print("QC completed.")

    return True
# ==============================
# CREATE PLOT
# ==============================

def create_plot(data, parameter, output_file):

    plt.figure(figsize=(8, 5))

    plt.plot(
        data["time_ns"],
        data[parameter],
        marker="o"
    )

    plt.xlabel("Time (ns)")
    plt.ylabel(parameter)

    plt.title(
        f"{parameter} vs Time"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.close()


# ==============================
# MAIN PIPELINE
# ==============================

# ==============================
# MAIN PIPELINE
# ==============================

print("================================")
print(" AUTOMATED MD ANALYSIS PIPELINE")
print("================================")

csv_files = sorted(
    filepath
    for filepath in INPUT_DIR.glob("*.csv")
)

print(
    f"\nInput files found: {len(csv_files)}"
)

all_results = []

for filepath in csv_files:

    print(
        f"\nAnalyzing: {filepath.name}"
    )

    data, results = analyze_file(
        filepath
    )

    qc_passed = quality_control(
        data,
        filepath.name
    )

    if not qc_passed:
        print(
            f"Skipping {filepath.name}"
        )
        continue

    all_results.extend(results)

    for result in results:

        parameter = result["parameter"]

        plot_file = (
            RESULTS_DIR
            / f"{parameter}.png"
        )

        create_plot(
            data,
            parameter,
            plot_file
        )

        print(
            f"Plot created: {plot_file}"
        )


# ==============================
# SUMMARY
# ==============================

summary = pd.DataFrame(
    all_results
)

summary_file = (
    RESULTS_DIR / "summary.csv"
)

summary.to_csv(
    summary_file,
    index=False
)


# ==============================
# REPORT
# ==============================

report_file = (
    RESULTS_DIR / "report.txt"
)

with open(
    report_file,
    "w"
) as report:

    report.write(
        "===== AUTOMATED MD ANALYSIS REPORT =====\n\n"
    )

    report.write(
        f"Input files analyzed: {len(csv_files)}\n\n"
    )

    for _, row in summary.iterrows():

        report.write(
            f"{row['parameter']}\n"
        )

        report.write(
            f"Frames: {int(row['frames'])}\n"
        )

        report.write(
            f"Mean: {row['mean']:.3f}\n"
        )

        report.write(
            f"Minimum: {row['minimum']:.3f}\n"
        )

        report.write(
            f"Maximum: {row['maximum']:.3f}\n"
        )

        report.write(
            f"Standard deviation: {row['std']:.3f}\n\n"
        )


# ==============================
# FINAL OUTPUT
# ==============================

print("\n================================")
print(" PIPELINE COMPLETE")
print("================================")

print(
    f"\nSummary: {summary_file}"
)

print(
    f"Report: {report_file}"
)

print(
    f"Results directory: {RESULTS_DIR}"
)

# ==============================
# ADVANCED MD ANALYSIS
# ==============================

import subprocess
import sys


def run_module(script_name):
    """Run an additional analysis module."""

    script_path = PROJECT_DIR / script_name

    if not script_path.exists():
        print(
            f"\nWARNING: {script_name} not found."
        )
        return False

    print("\n================================")
    print(f" RUNNING: {script_name}")
    print("================================")

    result = subprocess.run(
        [
            sys.executable,
            str(script_path)
        ],
        check=False
    )

    if result.returncode != 0:
        print(
            f"WARNING: {script_name} "
            f"returned exit code "
            f"{result.returncode}"
        )
        return False

    print(
        f"{script_name} completed successfully."
    )

    return True


# ==============================
# EQUILIBRATION ANALYSIS
# ==============================

run_module(
    "equilibrium_detector.py"
)


# ==============================
# MULTI-PARAMETER STABILITY
# ==============================

run_module(
    "multi_parameter_stability.py"
)


# ==============================
# STABILITY VISUALIZATION
# ==============================

run_module(
    "stability_plot.py"
)


# ==============================
# FINAL REPORT
# ==============================

run_module(
    "final_report.py"
)


# ==============================
# FINAL PIPELINE MESSAGE
# ==============================

print("\n================================")
print(" COMPLETE MD ANALYSIS FINISHED")
print("================================")

print(
    f"\nAll results are available in:"
)

print(RESULTS_DIR)