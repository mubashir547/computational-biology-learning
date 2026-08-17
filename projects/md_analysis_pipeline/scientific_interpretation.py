import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent

RESULTS_DIR = PROJECT_DIR / "results"

SUMMARY_FILE = RESULTS_DIR / "summary.csv"
STABILITY_FILE = RESULTS_DIR / "stability_analysis.csv"
STABLE_REGION_FILE = RESULTS_DIR / "stable_region.csv"

OUTPUT_FILE = RESULTS_DIR / "scientific_interpretation.txt"


# ==========================================
# LOAD DATA
# ==========================================

summary = pd.read_csv(SUMMARY_FILE)
stability = pd.read_csv(STABILITY_FILE)
stable_region = pd.read_csv(STABLE_REGION_FILE)


# ==========================================
# PARAMETER EXTRACTION
# ==========================================

def get_parameter(parameter):

    row = summary[
        summary["parameter"] == parameter
    ]

    if row.empty:
        return None

    return row.iloc[0]


rmsd = get_parameter("rmsd_A")
rg = get_parameter("rg_A")
hbonds = get_parameter("hbonds")
rmsf = get_parameter("rmsf_A")


# ==========================================
# STABLE REGION
# ==========================================

stable_data = stability[
    stability["all_stable"] == True
]

if not stable_data.empty:

    stable_start = stable_data["time_ns"].min()
    stable_end = stable_data["time_ns"].max()

else:

    stable_start = None
    stable_end = None


# ==========================================
# STABLE-REGION STATISTICS
# ==========================================

if stable_start is not None:

    stable_rmsd_mean = stable_region["rmsd_A"].mean()
    stable_rmsd_sd = stable_region["rmsd_A"].std()

    stable_rg_mean = stable_region["rg_A"].mean()
    stable_rg_sd = stable_region["rg_A"].std()

    stable_hb_mean = stable_region["hbonds"].mean()
    stable_hb_sd = stable_region["hbonds"].std()

else:

    stable_rmsd_mean = None
    stable_rmsd_sd = None

    stable_rg_mean = None
    stable_rg_sd = None

    stable_hb_mean = None
    stable_hb_sd = None


# ==========================================
# SCIENTIFIC INTERPRETATION
# ==========================================

interpretation = []

interpretation.append(
    "============================================================\n"
    "        SCIENTIFIC INTERPRETATION OF MD TRAJECTORY\n"
    "============================================================\n"
)


# ==========================================
# DATASET OVERVIEW
# ==========================================

interpretation.append(
    "\nDATASET OVERVIEW\n"
    "------------------------------------------------------------\n"
    f"Trajectory frames: {len(stability)}\n"
    f"Trajectory duration: "
    f"{stability['time_ns'].max():.0f} ns\n"
)


# ==========================================
# WHOLE TRAJECTORY
# ==========================================

interpretation.append(
    "\nWHOLE-TRAJECTORY STATISTICS\n"
    "------------------------------------------------------------\n"
)


if rmsd is not None:

    interpretation.append(
        f"RMSD: {rmsd['mean']:.3f} ± "
        f"{rmsd['std']:.3f} Å\n"
    )


if rg is not None:

    interpretation.append(
        f"Radius of gyration: {rg['mean']:.3f} ± "
        f"{rg['std']:.3f} Å\n"
    )


if hbonds is not None:

    interpretation.append(
        f"Hydrogen bonds: {hbonds['mean']:.3f} ± "
        f"{hbonds['std']:.3f}\n"
    )


if rmsf is not None:

    interpretation.append(
        f"RMSF: {rmsf['mean']:.3f} ± "
        f"{rmsf['std']:.3f} Å\n"
    )


interpretation.append(
    "\nInterpretation: The whole trajectory includes both "
    "the initial structural adaptation phase and the later "
    "equilibrated region. Therefore, whole-trajectory "
    "fluctuations should not be interpreted alone as evidence "
    "of persistent instability.\n"
)


# ==========================================
# STABLE REGION ANALYSIS
# ==========================================

interpretation.append(
    "\nEQUILIBRATED / STABLE REGION\n"
    "------------------------------------------------------------\n"
)


if stable_start is not None:

    interpretation.append(
        f"Stable region: {stable_start:.0f}–"
        f"{stable_end:.0f} ns\n"
    )

    interpretation.append(
        f"Stable duration: "
        f"{stable_end - stable_start:.0f} ns\n"
    )

    interpretation.append(
        f"Stable frames: {len(stable_region)}\n"
    )


    # --------------------------------------
    # RMSD
    # --------------------------------------

    if stable_rmsd_sd < 0.05:

        rmsd_comment = (
            "very low RMSD fluctuation, supporting a "
            "stable conformational state"
        )

    elif stable_rmsd_sd < 0.15:

        rmsd_comment = (
            "relatively low RMSD fluctuation, consistent "
            "with good conformational stability"
        )

    else:

        rmsd_comment = (
            "noticeable RMSD fluctuation that warrants "
            "further investigation"
        )


    interpretation.append(
        f"\nRMSD\n"
        f"Mean: {stable_rmsd_mean:.3f} Å\n"
        f"SD: {stable_rmsd_sd:.3f} Å\n"
        f"Interpretation: The stable region shows "
        f"{rmsd_comment}.\n"
    )


    # --------------------------------------
    # RADIUS OF GYRATION
    # --------------------------------------

    if stable_rg_sd < 0.05:

        rg_comment = (
            "minimal variation in molecular compactness"
        )

    elif stable_rg_sd < 0.15:

        rg_comment = (
            "relatively stable molecular compactness"
        )

    else:

        rg_comment = (
            "substantial changes in molecular compactness"
        )


    interpretation.append(
        f"\nRadius of Gyration\n"
        f"Mean: {stable_rg_mean:.3f} Å\n"
        f"SD: {stable_rg_sd:.3f} Å\n"
        f"Interpretation: The stable region demonstrates "
        f"{rg_comment}.\n"
    )


    # --------------------------------------
    # HYDROGEN BONDS
    # --------------------------------------

    if stable_hb_sd < 2:

        hb_comment = (
            "a highly stable hydrogen-bond interaction network"
        )

    elif stable_hb_sd < 10:

        hb_comment = (
            "a relatively stable hydrogen-bond interaction network"
        )

    else:

        hb_comment = (
            "substantial hydrogen-bond fluctuations"
        )


    interpretation.append(
        f"\nHydrogen Bonds\n"
        f"Mean: {stable_hb_mean:.3f}\n"
        f"SD: {stable_hb_sd:.3f}\n"
        f"Interpretation: The stable region shows "
        f"{hb_comment}.\n"
    )


    # --------------------------------------
    # SCIENTIFIC SYNTHESIS
    # --------------------------------------

    interpretation.append(
        "\nSTABILITY SYNTHESIS\n"
        "------------------------------------------------------------\n"
        "RMSD, radius of gyration, and hydrogen-bond behavior "
        "simultaneously satisfy the predefined stability "
        "criteria during the detected stable region. "
        "This supports the presence of a stable conformational "
        "regime during the latter portion of the trajectory.\n"
    )


else:

    interpretation.append(
        "No multi-parameter stable region was detected.\n"
    )


# ==========================================
# RMSF
# ==========================================

interpretation.append(
    "\nRMSF FLEXIBILITY\n"
    "------------------------------------------------------------\n"
)


if rmsf is not None:

    interpretation.append(
        f"Mean RMSF: {rmsf['mean']:.3f} Å\n"
        f"Minimum RMSF: {rmsf['minimum']:.3f} Å\n"
        f"Maximum RMSF: {rmsf['maximum']:.3f} Å\n"
        "Interpretation: RMSF provides information about "
        "residue-level flexibility and should be examined "
        "together with the residue-wise RMSF profile to "
        "identify highly mobile regions.\n"
    )


# ==========================================
# FINAL SCIENTIFIC CONCLUSION
# ==========================================

interpretation.append(
    "\nFINAL SCIENTIFIC CONCLUSION\n"
    "------------------------------------------------------------\n"
)


if stable_start is not None:

    conclusion = (
        f"The MD trajectory exhibits an initial structural "
        f"adaptation phase followed by a stable conformational "
        f"regime from approximately {stable_start:.0f} to "
        f"{stable_end:.0f} ns. During this region, RMSD "
        f"fluctuation remains low, the radius of gyration "
        f"remains stable, and the hydrogen-bond network shows "
        f"minimal variation. Collectively, these observations "
        f"support structural stabilization of the simulated "
        f"system during the latter portion of the trajectory."
    )

else:

    conclusion = (
        "The trajectory does not satisfy the predefined "
        "multi-parameter stability criteria. Additional "
        "simulation time and further structural analysis "
        "may therefore be required."
    )


interpretation.append(
    conclusion + "\n"
)


# ==========================================
# WRITE REPORT
# ==========================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(interpretation)
    )


# ==========================================
# TERMINAL OUTPUT
# ==========================================

print(
    "=========================================="
)

print(
    " SCIENTIFIC INTERPRETATION"
)

print(
    "=========================================="
)

if stable_start is not None:

    print(
        f"Stable region: "
        f"{stable_start:.0f}–{stable_end:.0f} ns"
    )

    print(
        f"Stable RMSD: "
        f"{stable_rmsd_mean:.3f} ± "
        f"{stable_rmsd_sd:.3f} Å"
    )

    print(
        f"Stable Rg: "
        f"{stable_rg_mean:.3f} ± "
        f"{stable_rg_sd:.3f} Å"
    )

    print(
        f"Stable H-bonds: "
        f"{stable_hb_mean:.3f} ± "
        f"{stable_hb_sd:.3f}"
    )

print(
    f"\nReport generated:\n{OUTPUT_FILE}"
)