import sys
import platform
import subprocess
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

OUTPUT_REPORT = RESULTS_DIR / "reproducibility_report.txt"
OUTPUT_SUMMARY = RESULTS_DIR / "reproducibility_summary.csv"
OUTPUT_MANIFEST = RESULTS_DIR / "analysis_manifest.txt"


def get_git_info():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_DIR,
            text=True
        ).strip()

        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=PROJECT_DIR,
            text=True
        ).strip()

        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_DIR,
            text=True
        ).strip()

        clean = "CLEAN" if not status else "MODIFIED"

        return commit, branch, clean

    except Exception:
        return "UNKNOWN", "UNKNOWN", "UNKNOWN"


def detect_modules():

    modules = [
        "md_pipeline.py",
        "equilibrium_detector.py",
        "multi_parameter_stability.py",
        "stability_plot.py",
        "final_report.py",
        "scientific_interpretation.py",
        "correlation_analysis.py",
        "correlation_stable.py",
        "statistical_analysis.py",
        "effective_sample_size.py",
        "block_averaging.py",
        "block_convergence.py",
        "reproducibility_report.py",
    ]

    results = []

    for module in modules:
        path = PROJECT_DIR / module

        results.append({
            "module": module,
            "status": "PASS" if path.exists() else "MISSING"
        })

    return results


def inspect_input_files():

    files = sorted(INPUT_DIR.glob("*.csv"))

    records = []

    total_frames = None
    duration = None

    for file in files:

        try:
            data = pd.read_csv(file)

            records.append({
                "file": file.name,
                "rows": len(data),
                "columns": ", ".join(data.columns)
            })

            if total_frames is None and "time_ns" in data.columns:
                total_frames = len(data)

                if len(data) > 0:
                    duration = float(data["time_ns"].max())

        except Exception:

            records.append({
                "file": file.name,
                "rows": "ERROR",
                "columns": "ERROR"
            })

    return files, records, total_frames, duration


def main():

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    commit, branch, git_status = get_git_info()

    files, file_records, frames, duration = inspect_input_files()

    modules = detect_modules()

    now = datetime.now().astimezone()

    report = []

    report.append(
        "============================================================"
    )
    report.append(
        "        MD ANALYSIS REPRODUCIBILITY REPORT"
    )
    report.append(
        "============================================================\n"
    )

    report.append("PROJECT")
    report.append("-" * 60)
    report.append("Project: Automated MD Analysis Pipeline")
    report.append(f"Analysis date: {now.isoformat()}\n")

    report.append("TRAJECTORY")
    report.append("-" * 60)
    report.append(
        f"Frames: {frames if frames is not None else 'UNKNOWN'}"
    )
    report.append(
        f"Duration: {duration if duration is not None else 'UNKNOWN'} ns\n"
    )

    report.append("SOFTWARE ENVIRONMENT")
    report.append("-" * 60)
    report.append(f"Python: {sys.version.split()[0]}")
    report.append(f"Pandas: {pd.__version__}")
    report.append(f"NumPy: {np.__version__}")
    report.append(f"Matplotlib: {matplotlib.__version__}")
    report.append(f"Platform: {platform.platform()}\n")

    report.append("VERSION CONTROL")
    report.append("-" * 60)
    report.append(f"Branch: {branch}")
    report.append(f"Commit: {commit}")
    report.append(f"Working tree: {git_status}\n")

    report.append("INPUT FILES")
    report.append("-" * 60)

    for record in file_records:
        report.append(
            f"{record['file']} | "
            f"Rows: {record['rows']} | "
            f"Columns: {record['columns']}"
        )

    report.append("")

    report.append("ANALYSIS MODULES")
    report.append("-" * 60)

    for module in modules:
        report.append(
            f"[{module['status']}] {module['module']}"
        )

    report.append("")

    report.append("OUTPUT FILES")
    report.append("-" * 60)

    output_files = sorted(
        RESULTS_DIR.iterdir()
    )

    for file in output_files:

        if file.name not in {
            OUTPUT_REPORT.name,
            OUTPUT_SUMMARY.name,
            OUTPUT_MANIFEST.name
        }:

            report.append(
                f"[PASS] {file.name}"
            )

    report.append("")

    missing_modules = [
        x["module"]
        for x in modules
        if x["status"] == "MISSING"
    ]

    report.append("REPRODUCIBILITY STATUS")
    report.append("-" * 60)

    if git_status == "CLEAN" and not missing_modules:
        report.append("PASS")
        report.append(
            "The analysis environment and tracked modules "
            "are documented and reproducible."
        )
    else:
        report.append("REVIEW REQUIRED")

        if missing_modules:
            report.append(
                "Missing modules: "
                + ", ".join(missing_modules)
            )

        if git_status != "CLEAN":
            report.append(
                "The Git working tree contains uncommitted changes."
            )

    report_text = "\n".join(report)

    OUTPUT_REPORT.write_text(
        report_text,
        encoding="utf-8"
    )

    summary = pd.DataFrame([
        {
            "analysis_date": now.isoformat(),
            "frames": frames,
            "duration_ns": duration,
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "git_branch": branch,
            "git_commit": commit,
            "git_status": git_status,
            "input_files": len(files),
            "analysis_modules": len(modules),
            "missing_modules": len(missing_modules)
        }
    ])

    summary.to_csv(
        OUTPUT_SUMMARY,
        index=False
    )

    manifest = []

    manifest.append(
        "===== MD ANALYSIS MANIFEST =====\n"
    )

    manifest.append(
        f"Generated: {now.isoformat()}"
    )

    manifest.append(
        f"Git commit: {commit}"
    )

    manifest.append(
        f"Git branch: {branch}"
    )

    manifest.append(
        f"Git status: {git_status}\n"
    )

    manifest.append(
        "INPUT FILES"
    )

    for file in files:
        manifest.append(
            str(file.relative_to(PROJECT_DIR))
        )

    manifest.append("\nANALYSIS MODULES")

    for module in modules:
        manifest.append(
            f"{module['status']}: {module['module']}"
        )

    OUTPUT_MANIFEST.write_text(
        "\n".join(manifest),
        encoding="utf-8"
    )

    print("==============================================")
    print(" MD REPRODUCIBILITY ANALYSIS")
    print("==============================================")
    print(f"Report: {OUTPUT_REPORT}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print(f"Manifest: {OUTPUT_MANIFEST}")
    print("==============================================")


if __name__ == "__main__":
    main()
