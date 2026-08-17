import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


project_dir = Path(
    "python/bioinformatics/complex_comparison"
)

input_file = project_dir / "complexes.csv"

data = pd.read_csv(input_file)
# ==============================
# MULTI-METRIC RANKING
# ==============================

data["RMSD_rank"] = data["mean_rmsd_A"].rank(
    ascending=True,
    method="min"
)

data["Rg_rank"] = data["mean_rg_A"].rank(
    ascending=True,
    method="min"
)

data["HBond_rank"] = data["mean_hbonds"].rank(
    ascending=False,
    method="min"
)

data["MMPBSA_rank"] = data["mmpbsa_kcal_mol"].rank(
    ascending=True,
    method="min"
)

data["overall_score"] = (
    data["RMSD_rank"]
    + data["Rg_rank"]
    + data["HBond_rank"]
    + data["MMPBSA_rank"]
)
# ==============================
# WEIGHTED RANKING
# ==============================

data["weighted_score"] = (
    data["RMSD_rank"] * 0.25
    + data["Rg_rank"] * 0.10
    + data["HBond_rank"] * 0.25
    + data["MMPBSA_rank"] * 0.40
)

weighted_ranking = data.sort_values(
    "weighted_score",
    ascending=True
)

print("\n===== WEIGHTED MULTI-METRIC RANKING =====")

print(
    weighted_ranking[
        [
            "system",
            "RMSD_rank",
            "Rg_rank",
            "HBond_rank",
            "MMPBSA_rank",
            "overall_score",
            "weighted_score"
        ]
    ].to_string(index=False)
)

best_weighted = weighted_ranking.iloc[0]

print("\n===== WEIGHTED WINNER =====")

print(
    f"Best weighted system: "
    f"{best_weighted['system']}"
)

print(
    f"Weighted score: "
    f"{best_weighted['weighted_score']:.2f}"
)

ranking = data.sort_values(
    "overall_score",
    ascending=True
)

print("===== COMPLEX COMPARISON =====")
print(data)
print("\n===== MULTI-METRIC RANKING =====")

print(
    ranking[
        [
            "system",
            "RMSD_rank",
            "Rg_rank",
            "HBond_rank",
            "MMPBSA_rank",
            "overall_score"
        ]
    ].to_string(index=False)
)


best_system = ranking.iloc[0]


print("\n===== OVERALL RANKING =====")

print(
    f"Best overall system: "
    f"{best_system['system']}"
)

print(
    f"Overall score: "
    f"{best_system['overall_score']:.0f}"
)

print("\n===== BASIC STATISTICS =====")

numeric_columns = [
    "mean_rmsd_A",
    "mean_rg_A",
    "mean_hbonds",
    "mmpbsa_kcal_mol"
]

print(data[numeric_columns].describe())


# Identify best systems

lowest_rmsd = data.loc[
    data["mean_rmsd_A"].idxmin()
]

lowest_rg = data.loc[
    data["mean_rg_A"].idxmin()
]

highest_hbonds = data.loc[
    data["mean_hbonds"].idxmax()
]

strongest_binding = data.loc[
    data["mmpbsa_kcal_mol"].idxmin()
]


print("\n===== MULTI-METRIC RESULTS =====")

print(
    f"Lowest RMSD: "
    f"{lowest_rmsd['system']} "
    f"({lowest_rmsd['mean_rmsd_A']:.2f} Å)"
)

print(
    f"Lowest Rg: "
    f"{lowest_rg['system']} "
    f"({lowest_rg['mean_rg_A']:.2f} Å)"
)

print(
    f"Highest H-bonds: "
    f"{highest_hbonds['system']} "
    f"({highest_hbonds['mean_hbonds']:.0f})"
)

print(
    f"Most negative MMPBSA: "
    f"{strongest_binding['system']} "
    f"({strongest_binding['mmpbsa_kcal_mol']:.2f} kcal/mol)"
)


# Save summary

summary_file = (
    project_dir / "complex_comparison.csv"
)

data.to_csv(
    summary_file,
    index=False
)


# Create MMPBSA plot

plt.figure(figsize=(8, 5))

plt.bar(
    data["system"],
    data["mmpbsa_kcal_mol"]
)

plt.xlabel("System")
plt.ylabel("MMPBSA Binding Energy (kcal/mol)")
plt.title("MMPBSA Binding Energy Comparison")

plt.axhline(
    0,
    linewidth=0.8
)

plt.tight_layout()

plot_file = (
    project_dir / "complex_comparison.png"
)

plt.savefig(
    plot_file,
    dpi=300
)

plt.close()


# Create text report

report_file = (
    project_dir / "complex_comparison_report.txt"
)

with open(report_file, "w") as report:

    report.write(
        "===== COMPLEX COMPARISON REPORT =====\n\n"
    )

    report.write(
        "Systems analyzed: "
        f"{len(data)}\n\n"
    )

    report.write(
        "Lowest RMSD:\n"
        f"{lowest_rmsd['system']} "
        f"({lowest_rmsd['mean_rmsd_A']:.2f} Å)\n\n"
    )

    report.write(
        "Lowest Radius of Gyration:\n"
        f"{lowest_rg['system']} "
        f"({lowest_rg['mean_rg_A']:.2f} Å)\n\n"
    )

    report.write(
        "Highest Hydrogen Bonds:\n"
        f"{highest_hbonds['system']} "
        f"({highest_hbonds['mean_hbonds']:.0f})\n\n"
    )

    report.write(
        "Most Negative MMPBSA:\n"
        f"{strongest_binding['system']} "
        f"({strongest_binding['mmpbsa_kcal_mol']:.2f} "
        "kcal/mol)\n"
    )


print("\nFiles generated:")

print(summary_file)
print(plot_file)
print(report_file)