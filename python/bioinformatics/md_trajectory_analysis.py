import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv(
    "python/bioinformatics/md_trajectory.csv"
)


print("===== MD TRAJECTORY ANALYSIS =====")

print("\nFirst 5 frames:")
print(data.head())

print("\nLast 5 frames:")
print(data.tail())

print("\nNumber of frames:", len(data))

print("\nColumns:")
print(list(data.columns))

print("\n===== TRAJECTORY STATISTICS =====")

print("\nRMSD:")
print("Mean:", round(data["rmsd_A"].mean(), 3))
print("Minimum:", data["rmsd_A"].min())
print("Maximum:", data["rmsd_A"].max())
print("Standard deviation:",
      round(data["rmsd_A"].std(), 3))


print("\nRadius of Gyration:")
print("Mean:", round(data["rg_A"].mean(), 3))
print("Minimum:", data["rg_A"].min())
print("Maximum:", data["rg_A"].max())


print("\nHydrogen Bonds:")
print("Mean:", round(data["hbonds"].mean(), 2))
print("Minimum:", data["hbonds"].min())
print("Maximum:", data["hbonds"].max())

print("\n===== EQUILIBRATION ANALYSIS =====")

equilibrated = data[data["time_ns"] >= 60]

print("Equilibration threshold: 60 ns")
print("Frames after equilibration:", len(equilibrated))

print("\nPost-equilibration RMSD:")
print("Mean:",
      round(equilibrated["rmsd_A"].mean(), 3))
print("Standard deviation:",
      round(equilibrated["rmsd_A"].std(), 3))

plt.figure(figsize=(9, 5))

plt.plot(
    data["time_ns"],
    data["rmsd_A"],
    marker="o",
    linewidth=1.5
)

plt.axvline(
    60,
    linestyle="--",
    linewidth=1.5,
    label="Equilibration threshold (60 ns)"
)

plt.xlabel("Time (ns)")
plt.ylabel("RMSD (Å)")
plt.title("RMSD Trajectory Analysis")

plt.legend()

plt.tight_layout()

plt.savefig(
    "rmsd_equilibration.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nRMSD plot saved to rmsd_equilibration.png")

print("\n===== ROLLING RMSD ANALYSIS =====")

window = 5

data["rmsd_rolling_mean"] = (
    data["rmsd_A"]
    .rolling(window=window)
    .mean()
)

data["rmsd_rolling_std"] = (
    data["rmsd_A"]
    .rolling(window=window)
    .std()
)

print(
    data[
        [
            "time_ns",
            "rmsd_A",
            "rmsd_rolling_mean",
            "rmsd_rolling_std"
        ]
    ].tail(10)
)
plt.figure(figsize=(9, 5))

plt.plot(
    data["time_ns"],
    data["rmsd_A"],
    marker="o",
    label="RMSD"
)

plt.plot(
    data["time_ns"],
    data["rmsd_rolling_mean"],
    linewidth=2,
    label="5-point rolling mean"
)

plt.axvline(
    60,
    linestyle="--",
    linewidth=1.5,
    label="60 ns threshold"
)

plt.xlabel("Time (ns)")
plt.ylabel("RMSD (Å)")
plt.title("RMSD and Rolling Mean")

plt.legend()

plt.tight_layout()

plt.savefig(
    "rmsd_rolling_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nRolling RMSD plot saved to rmsd_rolling_analysis.png")

print("\n===== STABILITY SCREENING =====")

stability_threshold = 0.02

stable_windows = data[
    data["rmsd_rolling_std"] <= stability_threshold
].copy()

print(
    "Rolling RMSD SD threshold:",
    stability_threshold,
    "Å"
)

print(
    "Number of stable windows:",
    len(stable_windows)
)

if len(stable_windows) > 0:

    first_stable_time = stable_windows["time_ns"].iloc[0]

    print(
        "First stable window begins at:",
        first_stable_time,
        "ns"
    )

    print("\nStable region:")
    print(
        stable_windows[
            [
                "time_ns",
                "rmsd_A",
                "rmsd_rolling_mean",
                "rmsd_rolling_std"
            ]
        ].tail(10)
    )

print("\n===== MULTI-PARAMETER STABILITY =====")

window = 5

data["rg_rolling_mean"] = (
    data["rg_A"]
    .rolling(window=window)
    .mean()
)

data["rg_rolling_std"] = (
    data["rg_A"]
    .rolling(window=window)
    .std()
)

data["hbonds_rolling_mean"] = (
    data["hbonds"]
    .rolling(window=window)
    .mean()
)

multi_stable = data[
    (data["rmsd_rolling_std"] <= 0.02) &
    (data["rg_rolling_std"] <= 0.05)
].copy()

print(
    "RMSD SD threshold: 0.02 Å"
)

print(
    "Rg SD threshold: 0.05 Å"
)

print(
    "Number of multi-parameter stable windows:",
    len(multi_stable)
)

if len(multi_stable) > 0:

    print(
        "First multi-parameter stable window:",
        multi_stable["time_ns"].iloc[0],
        "ns"
    )

    print("\nLatest stable windows:")

    print(
        multi_stable[
            [
                "time_ns",
                "rmsd_rolling_std",
                "rg_rolling_std",
                "hbonds_rolling_mean"
            ]
        ].tail(10)
    )

print("\n===== FINAL MD ANALYSIS REPORT =====")

final_time = data["time_ns"].max()

post_equil = data[
    data["time_ns"] >= 60
]

final_report = {
    "trajectory_length_ns": final_time,
    "total_frames": len(data),

    "equilibration_cutoff_ns": 60,

    "post_equilibration_frames": len(post_equil),

    "post_equilibration_rmsd_mean_A":
        post_equil["rmsd_A"].mean(),

    "post_equilibration_rmsd_sd_A":
        post_equil["rmsd_A"].std(),

    "first_stable_window_ns":
        multi_stable["time_ns"].iloc[0]
        if len(multi_stable) > 0
        else None,

    "stable_windows":
        len(multi_stable),

    "final_rmsd_A":
        data["rmsd_A"].iloc[-1],

    "final_rg_A":
        data["rg_A"].iloc[-1],

    "final_hbonds":
        data["hbonds"].iloc[-1]
}


with open(
    "md_trajectory_report.txt",
    "w"
) as report:

    report.write(
        "===== MD TRAJECTORY ANALYSIS REPORT =====\n\n"
    )

    report.write(
        f"Trajectory length: "
        f"{final_report['trajectory_length_ns']} ns\n"
    )

    report.write(
        f"Total frames: "
        f"{final_report['total_frames']}\n"
    )

    report.write(
        f"Equilibration cutoff: "
        f"{final_report['equilibration_cutoff_ns']} ns\n"
    )

    report.write(
        f"Post-equilibration frames: "
        f"{final_report['post_equilibration_frames']}\n"
    )

    report.write(
        f"Post-equilibration RMSD mean: "
        f"{final_report['post_equilibration_rmsd_mean_A']:.3f} Å\n"
    )

    report.write(
        f"Post-equilibration RMSD SD: "
        f"{final_report['post_equilibration_rmsd_sd_A']:.3f} Å\n"
    )

    report.write(
        f"First multi-parameter stable window: "
        f"{final_report['first_stable_window_ns']} ns\n"
    )

    report.write(
        f"Stable windows: "
        f"{final_report['stable_windows']}\n"
    )

    report.write("\nFinal frame:\n")

    report.write(
        f"RMSD: "
        f"{final_report['final_rmsd_A']:.2f} Å\n"
    )

    report.write(
        f"Radius of gyration: "
        f"{final_report['final_rg_A']:.2f} Å\n"
    )

    report.write(
        f"Hydrogen bonds: "
        f"{final_report['final_hbonds']}\n"
    )

print(
    "\nReport saved to md_trajectory_report.txt"
)

fig, axes = plt.subplots(
    3, 1,
    figsize=(9, 10),
    sharex=True
)

axes[0].plot(
    data["time_ns"],
    data["rmsd_A"],
    marker="o"
)
axes[0].set_ylabel("RMSD (Å)")
axes[0].set_title("MD Trajectory Analysis")

axes[1].plot(
    data["time_ns"],
    data["rg_A"],
    marker="o"
)
axes[1].set_ylabel("Rg (Å)")

axes[2].plot(
    data["time_ns"],
    data["hbonds"],
    marker="o"
)
axes[2].set_ylabel("H-bonds")
axes[2].set_xlabel("Time (ns)")

for ax in axes:
    ax.axvline(
        60,
        linestyle="--",
        linewidth=1.2
    )

plt.tight_layout()

plt.savefig(
    "md_combined_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nCombined MD figure saved to md_combined_analysis.png")