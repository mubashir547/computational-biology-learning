\# Automated Molecular Dynamics Analysis Pipeline



\## Overview



A Python-based automated pipeline for analyzing molecular dynamics

simulation data.



The pipeline processes MD-derived CSV files and automatically performs:



\- Quality control

\- RMSD analysis

\- Radius of gyration analysis

\- RMSF analysis

\- Hydrogen-bond analysis

\- Equilibration detection

\- Multi-parameter stability analysis

\- Visualization

\- Automated report generation



\## Input



The pipeline accepts CSV files containing:



\- time\_ns

\- rmsd\_A

\- rg\_A

\- rmsf\_A

\- hbonds



\## Analysis Workflow



CSV Input

&#x20;  ↓

Quality Control

&#x20;  ↓

Statistical Analysis

&#x20;  ↓

MD Parameter Visualization

&#x20;  ↓

Equilibration Detection

&#x20;  ↓

Multi-Parameter Stability Analysis

&#x20;  ↓

Stable Region Identification

&#x20;  ↓

Automated Final Report



\## Current Test Dataset



Trajectory length:



200 ns



Parameters:



\- RMSD

\- Radius of gyration

\- RMSF

\- Hydrogen bonds



\## Results



The current test trajectory produced:



\- First stable region: 150 ns

\- Stable frames: 6

\- Post-equilibration RMSD: 2.710 ± 0.014 Å

\- Post-equilibration Rg: 32.695 ± 0.010 Å

\- Post-equilibration H-bonds: 496.0 ± 0.894



\## Output



The pipeline automatically generates:



\- PNG plots

\- CSV analysis files

\- Stability analysis

\- Equilibration analysis

\- Automated text reports



\## Run



From the repository root:



```bash

py projects/md\_analysis\_pipeline/md\_pipeline.py

