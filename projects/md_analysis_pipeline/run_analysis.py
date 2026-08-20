import subprocess
import sys
from pathlib import Path
import argparse


PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"


MODULES = [
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

def run_module(module):

    script = PROJECT_DIR / module

    print("\n" + "=" * 60)
    print(f"RUNNING: {module}")
    print("=" * 60)

    if not script.exists():
        print(f"ERROR: {module} not found")
        return False

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_DIR
    )

    if result.returncode != 0:
        print(
            f"WARNING: {module} failed "
            f"with exit code {result.returncode}"
        )
        return False

    print(f"{module} completed successfully.")
    return True


def main():

    parser = argparse.ArgumentParser(
        description="Automated MD Analysis Pipeline"
    )

    parser.add_argument(
        "--input",
        default="input",
        help="Input directory containing MD CSV files"
    )

    args = parser.parse_args()

    input_dir = PROJECT_DIR / args.input

    print("\n" + "=" * 60)
    print("        AUTOMATED MD ANALYSIS PIPELINE")
    print("=" * 60)

    print(f"\nProject directory:")
    print(PROJECT_DIR)

    print(f"\nInput directory:")
    print(input_dir)

    print(f"\nResults directory:")
    print(RESULTS_DIR)

    if not input_dir.exists():
        print("\nERROR: Input directory does not exist.")
        sys.exit(1)

    csv_files = list(input_dir.glob("*.csv"))

    print(f"\nInput CSV files found: {len(csv_files)}")

    if not csv_files:
        print("ERROR: No CSV files found.")
        sys.exit(1)

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    successful = 0
    failed = 0

    for module in MODULES:

        if run_module(module):
            successful += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("        PIPELINE SUMMARY")
    print("=" * 60)

    print(f"\nModules successful: {successful}")
    print(f"Modules failed:     {failed}")

    print(f"\nResults available in:")
    print(RESULTS_DIR)

    if failed == 0:

        print("\nSTATUS: COMPLETE")
        print(
            "\nAll MD analysis modules completed successfully."
        )

    else:

        print("\nSTATUS: COMPLETED WITH WARNINGS")
        print(
            "\nSome modules failed. "
            "Review the messages above."
        )


if __name__ == "__main__":
    main()
