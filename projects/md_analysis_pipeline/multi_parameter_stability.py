import pandas as pd
from pathlib import Path


# ==============================
# PROJECT PATHS
# ==============================

PROJECT_DIR = Path(
    "projects/md_analysis_pipeline"
)

INPUT_DIR = (
    PROJECT_DIR / "input"
)

RESULTS_DIR = (
    PROJECT_DIR / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==============================
# SETTINGS
# ==============================

WINDOW_SIZE = 5

RMSD_SD_THRESHOLD = 0.02
RG_SD_THRESHOLD = 0.05
HBOND_SD_THRESHOLD = 10.0


# ==============================
# LOAD DATA
# ==============================

rmsd = pd.read_csv(
    INPUT_DIR / "rmsd.csv"
)

rg = pd.read_csv(
    INPUT_DIR / "rg.csv"
)

hbonds = pd.read_csv(
    INPUT_DIR / "hbonds.csv"
)

rmsf = pd.read_csv(
    INPUT_DIR / "rmsf.csv"
)


# ==============================
# COMBINE DATASETS
# ==============================

data = rmsd.merge(
    rg,
    on="time_ns"
)

data = data.merge(
    hbonds,
    on="time_ns"
)

data = data.merge(
    rmsf,
    on="time_ns"
)


print(
    "===== MULTI-PARAMETER STABILITY ANALYSIS ====="
)

print(
    f"Frames analyzed: {len(data)}"
)

print(
    f"Trajectory length: "
    f"{data['time_ns'].max()} ns"
)


# ==============================
# ROLLING STATISTICS
# ==============================

data["rmsd_rolling_std"] = (
    data["rmsd_A"]
    .rolling(WINDOW_SIZE)
    .std()
)

data["rg_rolling_std"] = (
    data["rg_A"]
    .rolling(WINDOW_SIZE)
    .std()
)

data["hbonds_rolling_std"] = (
    data["hbonds"]
    .rolling(WINDOW_SIZE)
    .std()
)

data["rmsf_rolling_std"] = (
    data["rmsf_A"]
    .rolling(WINDOW_SIZE)
    .std()
)


# ==============================
# STABILITY CONDITIONS
# ==============================

data["rmsd_stable"] = (
    data["rmsd_rolling_std"]
    <= RMSD_SD_THRESHOLD
)

data["rg_stable"] = (
    data["rg_rolling_std"]
    <= RG_SD_THRESHOLD
)

data["hbonds_stable"] = (
    data["hbonds_rolling_std"]
    <= HBOND_SD_THRESHOLD
)


# ==============================
# MULTI-PARAMETER STABILITY
# ==============================

data["all_stable"] = (
    data["rmsd_stable"]
    &
    data["rg_stable"]
    &
    data["hbonds_stable"]
)


stable = data[
    data["all_stable"]
].dropna()


# ==============================
# RESULTS
# ==============================

if stable.empty:

    print(
        "\nNo multi-parameter stable "
        "region detected."
    )

else:

    first_stable_time = (
        stable["time_ns"].iloc[0]
    )

    stable_frames = len(stable)

    post_equilibration = data[
        data["time_ns"]
        >= first_stable_time
    ]

    print(
        "\n===== STABILITY RESULTS ====="
    )

    print(
        f"First stable region: "
        f"{first_stable_time} ns"
    )

    print(
        f"Stable frames: "
        f"{stable_frames}"
    )

    print(
        "\nPost-equilibration statistics:"
    )

    print(
        f"RMSD mean: "
        f"{post_equilibration['rmsd_A'].mean():.3f} Å"
    )

    print(
        f"RMSD SD: "
        f"{post_equilibration['rmsd_A'].std():.3f} Å"
    )

    print(
        f"Rg mean: "
        f"{post_equilibration['rg_A'].mean():.3f} Å"
    )

    print(
        f"Rg SD: "
        f"{post_equilibration['rg_A'].std():.3f} Å"
    )

    print(
        f"H-bonds mean: "
        f"{post_equilibration['hbonds'].mean():.1f}"
    )

    print(
        f"H-bonds SD: "
        f"{post_equilibration['hbonds'].std():.3f}"
    )


# ==============================
# SAVE RESULTS
# ==============================

output_file = (
    RESULTS_DIR
    / "stability_analysis.csv"
)

data.to_csv(
    output_file,
    index=False
)


# ==============================
# SAVE STABLE REGION
# ==============================

stable_file = (
    RESULTS_DIR
    / "stable_region.csv"
)

stable.to_csv(
    stable_file,
    index=False
)


# ==============================
# REPORT
# ==============================

report_file = (
    RESULTS_DIR
    / "stability_report.txt"
)

with open(
    report_file,
    "w"
) as report:

    report.write(
        "===== MULTI-PARAMETER "
        "STABILITY REPORT =====\n\n"
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
        f"{WINDOW_SIZE} frames\n\n"
    )

    report.write(
        "Stability thresholds:\n"
    )

    report.write(
        f"RMSD SD: "
        f"{RMSD_SD_THRESHOLD} Å\n"
    )

    report.write(
        f"Rg SD: "
        f"{RG_SD_THRESHOLD} Å\n"
    )

    report.write(
        f"H-bond SD: "
        f"{HBOND_SD_THRESHOLD}\n\n"
    )

    if stable.empty:

        report.write(
            "No stable region detected.\n"
        )

    else:

        report.write(
            f"First stable region: "
            f"{first_stable_time} ns\n"
        )

        report.write(
            f"Stable frames: "
            f"{stable_frames}\n"
        )


print(
    "\n===== FILES GENERATED ====="
)

print(output_file)
print(stable_file)
print(report_file)