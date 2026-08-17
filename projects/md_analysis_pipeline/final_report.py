import pandas as pd
from pathlib import Path

PROJECT_DIR = Path("projects/md_analysis_pipeline")
RESULTS_DIR = PROJECT_DIR / "results"

summary_file = RESULTS_DIR / "summary.csv"
stability_file = RESULTS_DIR / "stability_analysis.csv"

summary = pd.read_csv(summary_file)
stability = pd.read_csv(stability_file)

stable = stability[
    stability["all_stable"] == True
]

report_file = RESULTS_DIR / "final_md_report.txt"

with open(report_file, "w") as f:

    f.write("=" * 60 + "\n")
    f.write("        AUTOMATED MD ANALYSIS REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write("PROJECT\n")
    f.write("-" * 60 + "\n")
    f.write("Automated Molecular Dynamics Analysis Pipeline\n\n")

    f.write("DATASET SUMMARY\n")
    f.write("-" * 60 + "\n")

    for _, row in summary.iterrows():

        parameter = row["parameter"]

        f.write(f"\n{parameter}\n")
        f.write(f"Frames: {int(row['frames'])}\n")
        f.write(f"Mean: {row['mean']:.3f}\n")
        f.write(f"Minimum: {row['minimum']:.3f}\n")
        f.write(f"Maximum: {row['maximum']:.3f}\n")
        f.write(f"Standard deviation: {row['std']:.3f}\n")

    f.write("\n\nSTABILITY ANALYSIS\n")
    f.write("-" * 60 + "\n")

    if stable.empty:

        f.write("No multi-parameter stable region detected.\n")

    else:

        first_stable = stable["time_ns"].iloc[0]
        last_stable = stable["time_ns"].iloc[-1]

        f.write(
            f"First stable region: {first_stable} ns\n"
        )

        f.write(
            f"Last stable frame: {last_stable} ns\n"
        )

        f.write(
            f"Stable frames: {len(stable)}\n"
        )

        f.write("\n")

        f.write("Stable-region statistics:\n")

        f.write(
            f"RMSD mean: "
            f"{stable['rmsd_A'].mean():.3f} Å\n"
        )

        f.write(
            f"RMSD SD: "
            f"{stable['rmsd_A'].std():.3f} Å\n"
        )

        f.write(
            f"Rg mean: "
            f"{stable['rg_A'].mean():.3f} Å\n"
        )

        f.write(
            f"Rg SD: "
            f"{stable['rg_A'].std():.3f} Å\n"
        )

        f.write(
            f"H-bonds mean: "
            f"{stable['hbonds'].mean():.1f}\n"
        )

        f.write(
            f"H-bonds SD: "
            f"{stable['hbonds'].std():.3f}\n"
        )

    f.write("\n\nFINAL FRAME\n")
    f.write("-" * 60 + "\n")

    final = stability.iloc[-1]

    f.write(
        f"Time: {final['time_ns']} ns\n"
    )

    f.write(
        f"RMSD: {final['rmsd_A']:.3f} Å\n"
    )

    f.write(
        f"Rg: {final['rg_A']:.3f} Å\n"
    )

    f.write(
        f"H-bonds: {final['hbonds']:.0f}\n"
    )

    f.write("\n\nCONCLUSION\n")
    f.write("-" * 60 + "\n")

    if not stable.empty:

        f.write(
            "The trajectory contains a region in which "
            "RMSD, radius of gyration, and hydrogen-bond "
            "fluctuations simultaneously satisfy the "
            "defined stability criteria.\n"
        )

    else:

        f.write(
            "No region satisfied all predefined "
            "multi-parameter stability criteria.\n"
        )

    f.write("\n")
    f.write("=" * 60 + "\n")

print("Final report generated:")
print(report_file)