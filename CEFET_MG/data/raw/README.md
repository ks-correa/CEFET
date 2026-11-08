# Dataset: D-Stabilization of a Coupled-Tank System Using Experimental Data

## Overview

This dataset contains experimental data collected from a coupled-tank system located at the Laboratory of Signals and Systems, CEFET-MG, Divinópolis, Brazil.

The data were used for the synthesis of state-feedback controllers with D-stability guarantees using a data-driven approach that accounts for measurement and process noise.

This dataset supports two scientific articles (see below) and is made publicly available for reproducibility and further research in data-driven control.

### Associated Articles:
1. "D-stabilização baseada em dados corrompidos por ruído via controladores do tipo PI" – Coelho, M. O. & Leite, V. J. S.
2. "D-estabilização por realimentação de estados via dados experimentais" – Silva, G. H. S., Coelho, M. O. & Leite, V. J. S.

Both articles present data-driven control methodologies validated on the same experimental setup described below.

## Experimental Setup
### Physical System
- Two coupled cylindrical tanks (T1 and T2), each with a capacity of 200 liters.
- Actuator: hydraulic pump with control signal ranging from 0% to 100% of its maximum capacity.
- Measured variables:
    - `h1`: water level in tank 1 (cm)
    - `h2`: water level in tank 2 (cm)
- The system is inherently nonlinear but was operated around a linearization operating point, where its behavior can be approximated by a linear model.
### Operating Point
- Constant input: 50% of pump capacity.
- Steady-state levels:
    - `h1* = 47.4 cm`
    - `h2* = 31.2 cm`
- State variables are defined as deviations from this operating point:
    - `x1 = h1(t) – h1*`
    - `x2 = h2(t) – h2*`

## Data Collection Protocol

**Sampling period:** `Ts = 4 seconds`

**Input signal:** Pseudo-random sequence with 10 levels between -50% and +50% (relative to operating point)

**Number of repeated experiments:** `N = 10`

The same input sequence was applied in all 10 experiments.

## Files

**h1.csv** (81×11)
- Water level (cm) in tank 1 (`h1`) for 10 experiments
- First column: `t_ref` (time in seconds)
- Columns 2–11: `Experiment1` to `Experiment10`

**h2.csv** (81×11)
- Water level (cm) in tank 2 (`h2`) for 10 experiments
- Same structure as `h1.csv`

**U.csv** (81×2)
- Control input applied to the pump
- Columns: `t_ref` (seconds) and `U` (% of pump capacity)

**complete_data.csv** 
- Data from the complete data collection experiment, including all 10 experiments.

## Acknowledgments

The authors thank the Federal Center for Technological Education of Minas Gerais (CEFET-MG) for the institutional support. This work was partially financed by CNPq (402393/2025-2, 408411/2023-6, 311891/2022-5) and FAPEMIG (APQ-05551-25).