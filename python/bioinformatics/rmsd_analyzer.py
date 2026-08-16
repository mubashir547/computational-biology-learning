import sys
import numpy as np
import matplotlib.pyplot as plt


if len(sys.argv) != 2:
    print("Usage: py rmsd_analyzer.py <rmsd.csv>")
    sys.exit()


filename = sys.argv[1]

data = np.loadtxt(
    filename,
    delimiter=",",
    skiprows=1
)

time = data[:, 0]
rmsd = data[:, 1]


print("===== RMSD ANALYSIS =====")

print("Number of frames:", len(rmsd))
print("Mean RMSD:", round(np.mean(rmsd), 3), "Å")
print("Minimum RMSD:", round(np.min(rmsd), 3), "Å")
print("Maximum RMSD:", round(np.max(rmsd), 3), "Å")
print("Standard deviation:", round(np.std(rmsd), 3), "Å")
with open("rmsd_results.txt", "w") as file:
    file.write("===== RMSD ANALYSIS =====\n")
    file.write(f"Number of frames: {len(rmsd)}\n")
    file.write(f"Mean RMSD: {np.mean(rmsd):.3f} Å\n")
    file.write(f"Minimum RMSD: {np.min(rmsd):.3f} Å\n")
    file.write(f"Maximum RMSD: {np.max(rmsd):.3f} Å\n")
    file.write(f"Standard deviation: {np.std(rmsd):.3f} Å\n")

print("\nResults saved to rmsd_results.txt")

plt.plot(time, rmsd)

plt.xlabel("Time (ns)")
plt.ylabel("RMSD (Å)")
plt.title("Molecular Dynamics RMSD Analysis")

plt.tight_layout()

plt.savefig("rmsd_plot.png", dpi=300, bbox_inches="tight")

print("Plot saved to rmsd_plot.png")