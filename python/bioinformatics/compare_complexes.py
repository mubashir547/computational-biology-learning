import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(
    "python/bioinformatics/complex_comparison.csv"
)


print("===== COMPLEX COMPARISON =====")
print(data)


print("\n===== MEAN VALUES =====")

print("Mean RMSD:")
print(data[["system", "mean_rmsd_A"]])

print("\nMean Radius of Gyration:")
print(data[["system", "mean_rg_A"]])

print("\nMean Hydrogen Bonds:")
print(data[["system", "mean_hbonds"]])

print("\nMMPBSA Binding Energy:")
print(data[["system", "mmpbsa_kcal_mol"]])


best_binding = data.loc[
    data["mmpbsa_kcal_mol"].idxmin()
]

print("\n===== STRONGEST BINDING =====")
print("System:", best_binding["system"])
print("Binding Energy:",
      best_binding["mmpbsa_kcal_mol"],
      "kcal/mol")
plt.figure(figsize=(8, 5))

plt.bar(
    data["system"],
    data["mmpbsa_kcal_mol"]
)

plt.xlabel("System")
plt.ylabel("MMPBSA Binding Energy (kcal/mol)")
plt.title("Comparison of MMPBSA Binding Energies")

plt.axhline(0, linewidth=0.8)

plt.tight_layout()

plt.savefig(
    "mmpbsa_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nPlot saved to mmpbsa_comparison.png")
print("\n===== MULTI-METRIC ANALYSIS =====")

print("\nLowest RMSD:")
print(
    data.loc[data["mean_rmsd_A"].idxmin(), ["system", "mean_rmsd_A"]]
)

print("\nHighest H-bonds:")
print(
    data.loc[data["mean_hbonds"].idxmax(), ["system", "mean_hbonds"]]
)

print("\nLowest Radius of Gyration:")
print(
    data.loc[data["mean_rg_A"].idxmin(), ["system", "mean_rg_A"]]
)

print("\nMost Negative MMPBSA:")
print(
    data.loc[data["mmpbsa_kcal_mol"].idxmin(),
             ["system", "mmpbsa_kcal_mol"]]
)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# RMSD
axes[0, 0].bar(data["system"], data["mean_rmsd_A"])
axes[0, 0].set_title("Mean RMSD")
axes[0, 0].set_ylabel("RMSD (Å)")

# Radius of gyration
axes[0, 1].bar(data["system"], data["mean_rg_A"])
axes[0, 1].set_title("Mean Radius of Gyration")
axes[0, 1].set_ylabel("Rg (Å)")

# Hydrogen bonds
axes[1, 0].bar(data["system"], data["mean_hbonds"])
axes[1, 0].set_title("Mean Hydrogen Bonds")
axes[1, 0].set_ylabel("H-bonds")

# MMPBSA
axes[1, 1].bar(data["system"], data["mmpbsa_kcal_mol"])
axes[1, 1].set_title("MMPBSA Binding Energy")
axes[1, 1].set_ylabel("ΔGbind (kcal/mol)")

fig.suptitle("S1, S2 and S3 MD Comparison")

plt.tight_layout()

plt.savefig(
    "md_multimetric_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nMulti-metric plot saved to md_multimetric_comparison.png")

with open("md_comparison_report.txt", "w") as report:

    report.write("===== MD COMPLEX COMPARISON REPORT =====\n\n")

    report.write("Systems analyzed: S1, S2, S3\n\n")

    report.write("Mean RMSD:\n")
    for _, row in data.iterrows():
        report.write(
            f"{row['system']}: {row['mean_rmsd_A']:.2f} Å\n"
        )

    report.write("\nMean Radius of Gyration:\n")
    for _, row in data.iterrows():
        report.write(
            f"{row['system']}: {row['mean_rg_A']:.2f} Å\n"
        )

    report.write("\nMean Hydrogen Bonds:\n")
    for _, row in data.iterrows():
        report.write(
            f"{row['system']}: {row['mean_hbonds']:.0f}\n"
        )

    report.write("\nMMPBSA Binding Energy:\n")
    for _, row in data.iterrows():
        report.write(
            f"{row['system']}: "
            f"{row['mmpbsa_kcal_mol']:.2f} kcal/mol\n"
        )

    best = data.loc[data["mmpbsa_kcal_mol"].idxmin()]

    report.write("\nStrongest predicted binding:\n")
    report.write(
        f"{best['system']}: "
        f"{best['mmpbsa_kcal_mol']:.2f} kcal/mol\n"
    )

print("Report saved to md_comparison_report.txt")
