import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_DIR = Path("projects/md_analysis_pipeline")

RESULTS_DIR = PROJECT_DIR / "results"

data = pd.read_csv(
    RESULTS_DIR / "stability_analysis.csv"
)

stable = data[
    data["all_stable"] == True
]

if stable.empty:
    print("No stable region detected.")
    raise SystemExit

first_stable = stable["time_ns"].iloc[0]

fig, axes = plt.subplots(
    3,
    1,
    figsize=(10, 10),
    sharex=True
)

# RMSD
axes[0].plot(
    data["time_ns"],
    data["rmsd_A"],
    marker="o"
)

axes[0].axvline(
    first_stable,
    linestyle="--",
    label="Stable region"
)

axes[0].set_ylabel("RMSD (Å)")
axes[0].set_title("MD Multi-Parameter Stability")
axes[0].legend()
axes[0].grid(True)

# Radius of gyration
axes[1].plot(
    data["time_ns"],
    data["rg_A"],
    marker="o"
)

axes[1].axvline(
    first_stable,
    linestyle="--"
)

axes[1].set_ylabel("Rg (Å)")
axes[1].grid(True)

# Hydrogen bonds
axes[2].plot(
    data["time_ns"],
    data["hbonds"],
    marker="o"
)

axes[2].axvline(
    first_stable,
    linestyle="--"
)

axes[2].set_xlabel("Time (ns)")
axes[2].set_ylabel("H-bonds")
axes[2].grid(True)

plt.tight_layout()

output = RESULTS_DIR / "multi_parameter_stability.png"

plt.savefig(
    output,
    dpi=300
)

plt.close()

print("Plot saved to:")
print(output)