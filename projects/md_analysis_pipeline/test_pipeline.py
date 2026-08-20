from pathlib import Path
import subprocess
import sys

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

EXPECTED_MODULES = [
    "md_pipeline.py",
    "scientific_interpretation.py",
    "correlation_analysis.py",
    "correlation_stable.py",
    "statistical_analysis.py",
    "effective_sample_size.py",
    "block_averaging.py",
    "block_convergence.py",
    "reproducibility_report.py",
    "publication_report.py",
]

EXPECTED_OUTPUTS = [
    "summary.csv",
    "report.txt",
    "rmsd_A.png",
    "rg_A.png",
    "rmsf_A.png",
    "hbonds.png",
    "equilibrium_analysis.csv",
    "equilibrium_report.txt",
    "stability_analysis.csv",
    "stable_region.csv",
    "stability_report.txt",
    "multi_parameter_stability.png",
    "scientific_interpretation.txt",
    "correlation_matrix.csv",
    "correlation_report.txt",
    "correlation_heatmap.png",
    "stable_correlation_matrix.csv",
    "stable_correlation_report.txt",
    "statistical_correlations.csv",
    "statistical_correlation_report.txt",
    "effective_sample_size.csv",
    "effective_sample_size_report.txt",
    "autocorrelation.png",
    "block_statistics.csv",
    "block_averaging_report.txt",
    "block_averaging.png",
    "block_convergence.csv",
    "block_convergence_report.txt",
    "block_convergence.png",
    "reproducibility_report.txt",
    "reproducibility_summary.csv",
    "analysis_manifest.txt",
    "publication_report.html",
]


def check(condition, message):
    if condition:
        print(f"[PASS] {message}")
        return True

    print(f"[FAIL] {message}")
    return False


def main():

    print("=" * 60)
    print("        MD ANALYSIS PIPELINE TEST SUITE")
    print("=" * 60)

    passed = 0
    failed = 0

    print("\nINPUT CHECKS")
    print("-" * 60)

    if check(INPUT_DIR.exists(), "Input directory exists"):
        passed += 1
    else:
        failed += 1

    csv_files = list(INPUT_DIR.glob("*.csv"))

    if check(
        len(csv_files) >= 4,
        f"Input CSV files detected ({len(csv_files)})"
    ):
        passed += 1
    else:
        failed += 1

    print("\nMODULE CHECKS")
    print("-" * 60)

    for module in EXPECTED_MODULES:
        path = PROJECT_DIR / module

        if check(path.exists(), f"{module} exists"):
            passed += 1
        else:
            failed += 1

    print("\nOUTPUT CHECKS")
    print("-" * 60)

    for output in EXPECTED_OUTPUTS:
        path = RESULTS_DIR / output

        if check(
            path.exists() and path.stat().st_size > 0,
            f"{output} generated"
        ):
            passed += 1
        else:
            failed += 1

    print("\nPIPELINE EXECUTION TEST")
    print("-" * 60)

    runner = PROJECT_DIR / "run_analysis.py"

    if not runner.exists():

        print("[FAIL] run_analysis.py not found")
        failed += 1

    else:

        result = subprocess.run(
            [
                sys.executable,
                str(runner),
                "--input",
                "input",
            ],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:

            print("[PASS] Complete pipeline execution")
            passed += 1

        else:

            print("[FAIL] Complete pipeline execution")
            print(result.stderr)
            failed += 1

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    print(f"\nTests passed: {passed}")
    print(f"Tests failed: {failed}")

    if failed == 0:
        print("\nSTATUS: ALL TESTS PASSED")
        print("\nMD analysis pipeline is functioning correctly.")
        return 0

    print("\nSTATUS: TESTS FAILED")
    print("\nReview the failed checks above.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
