import numpy as np
import matplotlib.pyplot as plt


time = np.array([
    0, 10, 20, 30, 40,
    50, 60, 70, 80, 90
])

rmsd = np.array([
    1.82, 2.15, 2.31, 2.45, 2.38,
    2.51, 2.42, 2.36, 2.48, 2.55
])


print("MD Simulation Data")
print("==================")

print("\nRMSD Statistics:")
print("Mean:", round(np.mean(rmsd), 3))
print("Minimum:", round(np.min(rmsd), 3))
print("Maximum:", round(np.max(rmsd), 3))
print("Standard deviation:", round(np.std(rmsd), 3))


plt.plot(time, rmsd)

plt.xlabel("Time (ns)")
plt.ylabel("RMSD (Å)")
plt.title("MD Simulation RMSD")

plt.tight_layout()
plt.show()