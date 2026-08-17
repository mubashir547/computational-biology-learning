import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==============================
# PROJECT PATHS
# ==============================

PROJECT_DIR = Path(__file__).resolve().parent

INPUT_DIR = PROJECT_DIR / "input"
RESULTS_DIR = PROJECT_DIR / "results"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INPUT_FILE = INPUT_DIR / "rmsd.csv"

# ==============================
# SETTINGS
# ==============================

WINDOW_SIZE = 5

STABILITY_THRESHOLD = 0.02


# ==============================
# LOAD DATA
# ==============================

data = pd.read_csv(
    INPUT_FILE
)

print(
    "===== MD EQUILIBRATION DETECTOR ====="
)

print(
    f"Frames: {len(data)}"
)

print(
    f"Trajectory length: "
    f"{data['time_ns'].max()} ns"
)


# ==============================
# ROLLING ANALYSIS
# ==============================

data["rolling_mean"] = (
    data["rmsd_A"]
    .rolling(WINDOW_SIZE)
    .mean()
)

data["rolling_std"] = (
    data["rmsd_A"]
    .rolling(WINDOW_SIZE)
    .std()
)


# ==============================
# STABLE WINDOWS
# ==============================

stable = data[
    data["rolling_std"]
    <= STABILITY_THRESHOLD
].dropna()


if stable.empty:

    print(
        "\nNo stable region detected."
    )

    raise SystemExit


first_stable_time = (
    stable["time_ns"].iloc[0]
)

stable_frames = len(stable)


# ==============================
# POST-EQUILIBRATION DATA
# ==============================

post_equilibration = data[
    data["time_ns"]
    >= first_stable_time
]

post_mean = (
    post_equilibration["rmsd_A"]
    .mean()
)

post_std = (
    post_equilibration["rmsd_A"]
    .std()
)


# ==============================
# PRINT RESULTS
# ==============================

print(
    "\n===== EQUILIBRATION ANALYSIS ====="
)

print(
    f"Rolling window: "
    f"{WINDOW_SIZE} frames"
)

print(
    f"Stability threshold: "
    f"{STABILITY_THRESHOLD} Å"
)

print(
    f"First stable region: "
    f"{first_stable_time} ns"
)

print(
    f"Stable windows: "
    f"{stable_frames}"
)

print(
    f"Post-equilibration RMSD mean: "
    f"{post_mean:.3f} Å"
)

print(
    f"Post-equilibration RMSD SD: "
    f"{post_std:.3f} Å"
)


# ==============================
# SAVE CSV
# ==============================

stable_file = (
    RESULTS_DIR
    / "equilibrium_analysis.csv"
)

stable.to_csv(
    stable_file,
    index=False
)


# ==============================
# CREATE PLOT
# ==============================

plot_file = (
    RESULTS_DIR
    / "rmsd_equilibrium.png"
)

plt.figure(
    figsize=(9, 5)
)

plt.plot(
    data["time_ns"],
    data["rmsd_A"],
    marker="o",
    label="RMSD"
)

plt.axvline(
    first_stable_time,
    linestyle="--",
    label="Stable region"
)

plt.xlabel(
    "Time (ns)"
)

plt.ylabel(
    "RMSD (Å)"
)

plt.title(
    "MD Equilibration Analysis"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    plot_file,
    dpi=300
)

plt.close()


# ==============================
# REPORT
# ==============================

report_file = (
    RESULTS_DIR
    / "equilibrium_report.txt"
)

with open(
    report_file,
    "w"
) as report:

    report.write(
        "===== MD EQUILIBRATION REPORT =====\n\n"
    )

    report.write(
        f"Trajectory length: "
        f"{data['time_ns'].max()} ns\n"
    )

    report.write(
        f"Total frames: "
        f"{len(data)}\n"
    )

    report.write(
        f"Rolling window: "
        f"{WINDOW_SIZE} frames\n"
    )

    report.write(
        f"Stability threshold: "
        f"{STABILITY_THRESHOLD} Å\n"
    )

    report.write(
        f"First stable region: "
        f"{first_stable_time} ns\n"
    )

    report.write(
        f"Stable windows: "
        f"{stable_frames}\n"
    )

    report.write(
        f"Post-equilibration RMSD mean: "
        f"{post_mean:.3f} Å\n"
    )

    report.write(
        f"Post-equilibration RMSD SD: "
        f"{post_std:.3f} Å\n"
    )


print(
    "\nFiles generated:"
)

print(
    stable_file
)

print(
    plot_file
)

print(
    report_file
)