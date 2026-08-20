from pathlib import Path
from datetime import datetime
import html
import re


PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
OUTPUT_FILE = RESULTS_DIR / "publication_report.html"


# ============================================================
# HELPERS
# ============================================================

def read_text(filename):
    path = RESULTS_DIR / filename

    if not path.exists():
        return f"{filename} not available."

    return path.read_text(
        encoding="utf-8",
        errors="replace"
    )
def escape(text):
    return html.escape(text)


def report_section(title, filename):
    content = read_text(filename)

    return f"""
    <section>
        <h2>{escape(title)}</h2>
        <pre>{escape(content)}</pre>
    </section>
    """


def figure(filename, caption):
    path = RESULTS_DIR / filename

    if not path.exists():
        return f"""
        <div class="figure-missing">
            Figure unavailable: {escape(filename)}
        </div>
        """

    return f"""
    <figure>
        <img src="{escape(filename)}" alt="{escape(caption)}">
        <figcaption>{escape(caption)}</figcaption>
    </figure>
    """


# ============================================================
# READ KEY REPORTS
# ============================================================

summary = read_text("summary.csv")
scientific = read_text("scientific_interpretation.txt")
reproducibility = read_text("reproducibility_report.txt")
stability = read_text("stability_report.txt")
final_report = read_text("final_md_report.txt")


# ============================================================
# HTML DOCUMENT
# ============================================================

generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


html_document = f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Automated MD Analysis Report</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.6;
    margin: 0;
    background: #f4f6f8;
    color: #222;
}}

.container {{
    max-width: 1200px;
    margin: auto;
    background: white;
    padding: 45px;
}}

header {{
    border-bottom: 3px solid #333;
    margin-bottom: 35px;
    padding-bottom: 20px;
}}

h1 {{
    font-size: 34px;
    margin-bottom: 5px;
}}

h2 {{
    margin-top: 45px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 8px;
}}

h3 {{
    margin-top: 30px;
}}

.subtitle {{
    color: #666;
    font-size: 16px;
}}

pre {{
    background: #f7f7f7;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 20px;
    overflow-x: auto;
    white-space: pre-wrap;
    font-family: Consolas, monospace;
    font-size: 13px;
}}

figure {{
    margin: 30px 0;
    text-align: center;
}}

figure img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
}}

figcaption {{
    margin-top: 8px;
    color: #666;
    font-size: 14px;
}}

.summary-box {{
    background: #f0f4f8;
    border-left: 5px solid #333;
    padding: 20px;
    margin: 25px 0;
}}

.warning {{
    background: #fff4e5;
    border-left: 5px solid #cc8800;
    padding: 20px;
    margin: 25px 0;
}}

.success {{
    background: #eef8ee;
    border-left: 5px solid #4a8;
    padding: 20px;
    margin: 25px 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

th {{
    background: #f0f0f0;
}}

footer {{
    margin-top: 60px;
    border-top: 1px solid #ccc;
    padding-top: 20px;
    color: #666;
    font-size: 13px;
}}

.figure-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 25px;
}}

.figure-grid figure {{
    margin: 0;
}}

</style>

</head>


<body>

<div class="container">

<header>

<h1>Automated Molecular Dynamics Analysis Report</h1>

<div class="subtitle">
Computational Biology Learning — MD Analysis Pipeline
</div>

<div class="subtitle">
Generated: {generated}
</div>

</header>


<!-- ====================================================== -->
<!-- EXECUTIVE SUMMARY -->
<!-- ====================================================== -->

<section>

<h2>1. Executive Summary</h2>

<div class="summary-box">

<p>
This report presents an automated analysis of molecular dynamics
trajectory observables using a reproducible computational workflow.
The pipeline evaluates trajectory quality, structural stability,
equilibration behavior, molecular compactness, hydrogen-bond
interactions, residue-level flexibility, statistical relationships,
temporal correlation, uncertainty, and reproducibility.
</p>

<p>
The analysis is intended to provide a systematic computational
assessment of MD trajectory behavior rather than relying on a
single stability metric.
</p>

</div>

</section>


<!-- ====================================================== -->
<!-- DATASET -->
<!-- ====================================================== -->

<section>

<h2>2. Dataset Overview</h2>

<pre>{escape(summary)}</pre>

</section>


<!-- ====================================================== -->
<!-- QC -->
<!-- ====================================================== -->

<section>

<h2>3. Quality Control</h2>

<p>
The automated pipeline performs input validation before calculating
trajectory statistics and generating figures.
</p>

<pre>{escape(final_report)}</pre>

</section>


<!-- ====================================================== -->
<!-- RMSD -->
<!-- ====================================================== -->

<section>

<h2>4. RMSD Analysis</h2>

<p>
Root-mean-square deviation (RMSD) is used to assess structural
deviation of the simulated system relative to the reference
structure or starting conformation.
</p>

{figure("rmsd_A.png", "RMSD trajectory")}

{figure("rmsd_equilibrium.png",
        "RMSD trajectory with detected equilibrium region")}

</section>


<!-- ====================================================== -->
<!-- RMSF -->
<!-- ====================================================== -->

<section>

<h2>5. RMSF Analysis</h2>

<p>
Root-mean-square fluctuation (RMSF) describes residue-level
flexibility throughout the analyzed trajectory.
</p>

{figure("rmsf_A.png", "Residue-level RMSF profile")}

</section>


<!-- ====================================================== -->
<!-- RADIUS OF GYRATION -->
<!-- ====================================================== -->

<section>

<h2>6. Radius of Gyration</h2>

<p>
The radius of gyration provides an estimate of the overall
compactness of the simulated molecular system.
</p>

{figure("rg_A.png", "Radius of gyration trajectory")}

</section>


<!-- ====================================================== -->
<!-- HYDROGEN BONDS -->
<!-- ====================================================== -->

<section>

<h2>7. Hydrogen-Bond Analysis</h2>

<p>
Hydrogen-bond analysis provides information about the persistence
and variability of intermolecular or intramolecular hydrogen-bond
interactions during the trajectory.
</p>

{figure("hbonds.png", "Hydrogen-bond trajectory")}

</section>


<!-- ====================================================== -->
<!-- EQUILIBRATION -->
<!-- ====================================================== -->

<section>

<h2>8. Equilibration Analysis</h2>

<pre>{escape(read_text("equilibrium_report.txt"))}</pre>

</section>


<!-- ====================================================== -->
<!-- MULTI PARAMETER STABILITY -->
<!-- ====================================================== -->

<section>

<h2>9. Multi-Parameter Stability</h2>

<pre>{escape(stability)}</pre>

{figure(
    "multi_parameter_stability.png",
    "Multi-parameter stability analysis"
)}

</section>


<!-- ====================================================== -->
<!-- SCIENTIFIC INTERPRETATION -->
<!-- ====================================================== -->

<section>

<h2>10. Scientific Interpretation</h2>

<pre>{escape(scientific)}</pre>

</section>


<!-- ====================================================== -->
<!-- CORRELATION -->
<!-- ====================================================== -->

<section>

<h2>11. Correlation Analysis</h2>

<pre>{escape(read_text("correlation_report.txt"))}</pre>

{figure(
    "correlation_heatmap.png",
    "Pearson correlation heatmap"
)}

<h3>Equilibrated Region</h3>

<pre>{escape(
    read_text("stable_correlation_report.txt")
)}</pre>

</section>


<!-- ====================================================== -->
<!-- STATISTICAL VALIDATION -->
<!-- ====================================================== -->

<section>

<h2>12. Statistical Validation</h2>

<pre>{escape(
    read_text("statistical_correlation_report.txt")
)}</pre>

<div class="warning">

<strong>Statistical caution:</strong>

MD trajectory frames are temporally correlated.
Therefore, conventional statistical tests based on the raw
number of frames may overestimate the amount of independent
information available in the trajectory.

</div>

</section>


<!-- ====================================================== -->
<!-- ESS -->
<!-- ====================================================== -->

<section>

<h2>13. Effective Sample Size</h2>

<pre>{escape(
    read_text("effective_sample_size_report.txt")
)}</pre>

{figure(
    "autocorrelation.png",
    "Trajectory autocorrelation analysis"
)}

</section>


<!-- ====================================================== -->
<!-- BLOCK AVERAGING -->
<!-- ====================================================== -->

<section>

<h2>14. Block Averaging</h2>

<pre>{escape(
    read_text("block_averaging_report.txt")
)}</pre>

{figure(
    "block_averaging.png",
    "Block averaging uncertainty analysis"
)}

</section>


<!-- ====================================================== -->
<!-- BLOCK CONVERGENCE -->
<!-- ====================================================== -->

<section>

<h2>15. Block-Size Convergence</h2>

<pre>{escape(
    read_text("block_convergence_report.txt")
)}</pre>

{figure(
    "block_convergence.png",
    "Block-size convergence analysis"
)}

</section>


<!-- ====================================================== -->
<!-- REPRODUCIBILITY -->
<!-- ====================================================== -->

<section>

<h2>16. Reproducibility</h2>

<pre>{escape(reproducibility)}</pre>

</section>


<!-- ====================================================== -->
<!-- LIMITATIONS -->
<!-- ====================================================== -->

<section>

<h2>17. Limitations</h2>

<div class="warning">

<ul>

<li>
The demonstration dataset contains a limited number of trajectory
frames.
</li>

<li>
Effective sample size estimates are therefore limited by the
available trajectory length.
</li>

<li>
Correlation does not establish causal relationships between
molecular observables.
</li>

<li>
Stability detection is dependent on the thresholds and windows
defined by the analysis workflow.
</li>

<li>
Statistical uncertainty estimates should be reassessed using
longer production trajectories with appropriate frame sampling.
</li>

<li>
Computational stability alone does not establish biological
efficacy or experimental validity.
</li>

</ul>

</div>

</section>


<!-- ====================================================== -->
<!-- GENERATED FILES -->
<!-- ====================================================== -->

<section>

<h2>18. Generated Analysis Files</h2>

<table>

<tr>
<th>Category</th>
<th>Files</th>
</tr>

<tr>
<td>Trajectory plots</td>
<td>
RMSD, RMSF, radius of gyration, hydrogen bonds
</td>
</tr>

<tr>
<td>Stability</td>
<td>
Equilibration and multi-parameter stability analyses
</td>
</tr>

<tr>
<td>Correlation</td>
<td>
Pearson correlation matrix and heatmap
</td>
</tr>

<tr>
<td>Statistics</td>
<td>
Pearson/Spearman correlations and confidence intervals
</td>
</tr>

<tr>
<td>Temporal correlation</td>
<td>
Autocorrelation and effective sample size
</td>
</tr>

<tr>
<td>Uncertainty</td>
<td>
Block averaging and block-size convergence
</td>
</tr>

<tr>
<td>Reproducibility</td>
<td>
Environment, manifest and version-control information
</td>
</tr>

</table>

</section>


<footer>

<p>
Generated automatically by the Automated MD Analysis Pipeline.
</p>

<p>
This report is intended for computational research and
methodological assessment. Numerical results should be interpreted
in the context of trajectory length, sampling frequency,
force-field selection, simulation protocol, and experimental
evidence.
</p>

</footer>

</div>

</body>

</html>
"""


# ============================================================
# WRITE REPORT
# ============================================================

OUTPUT_FILE.write_text(
    html_document,
    encoding="utf-8"
)

print("=" * 60)
print("       PUBLICATION REPORT GENERATED")
print("=" * 60)
print()
print(f"Report: {OUTPUT_FILE}")
print()
print("Open publication_report.html in a web browser.")
