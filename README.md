# Data and Supplementary Examples for IEEE 33-/123-Bus Case Studies

This repository contains the data, results, supplementary materials, and illustrative example scripts associated with the paper:

**Asynchronous Distributed Scheduling of Active Distribution Network and Thermostatically Controlled Loads With MPC-Based Aggregation**  
DOI: `10.1109/TPWRS.2026.3670270`

## Overview

This repository provides:

- data files used in the IEEE 33-/123-bus case studies;
- reported scheduling results;
- supplementary PDF documents for the case studies and RL training settings;
- standalone toy example scripts that illustrate statistically feasible uncertainty-set construction methods in a simplified 2D setting.

## Repository Structure

```text
.
├─ IEEE33-unbalanced-distribution-system/
├─ docs/
│  ├─ Appendix for Case Studies.pdf
│  ├─ Asynchronous_Distributed_Scheduling_of_Active_Distribution_Network_and_Thermostatically_Controlled_Loads_With_MPC-Based_Aggregation.pdf
│  └─ RL settings and training process for caseA2.pdf
├─ data/
│  └─ Test_System_data.xlsx
├─ results/
│  └─ Scheduling results of TCL aggregators in the IEEE-123 case.xlsx
├─ examples/
│  └─ uncertainty_set_toy/
│     ├─ uncertainty_set_sm.py
│     ├─ uncertainty_set_osa.py
│     ├─ uncertainty_set_ellip.py
│     ├─ uncertainty_set_reconstr.py
│     └─ hyperplane.py
├─ LICENSE
├─ CITATION.cff
├─ requirements.txt
└─ README.md
```

## Notes on the Supplementary Example Scripts

The scripts under `examples/uncertainty_set_toy/` are **independent illustrative examples** rather than the main IEEE 33-/123-bus simulation workflow. Their purpose is to demonstrate uncertainty-set construction and statistically feasible optimization ideas in a simplified two-dimensional setting.

These scripts are provided to improve transparency and reproducibility of the methodological ideas. They can be run independently and do not modify the main case-study data.

## Requirements

Recommended environment:

- Python 3.10+
- `numpy`
- `matplotlib`
- `cvxpy`
- `gurobipy` / GUROBI solver

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Supplementary Examples

From the repository root:

```bash
python examples/uncertainty_set_toy/uncertainty_set_sm.py
python examples/uncertainty_set_toy/uncertainty_set_ellip.py
python examples/uncertainty_set_toy/uncertainty_set_reconstr.py
python examples/uncertainty_set_toy/uncertainty_set_osa.py
```

## Citation

If this repository, the code, the data, or the supplementary materials are useful in your research, please cite the associated paper.

```bibtex
@article{adn_tcl_mpc_aggregation_2026,
  title   = {Asynchronous Distributed Scheduling of Active Distribution Network and Thermostatically Controlled Loads With MPC-Based Aggregation},
  journal = {IEEE Transactions on Power Systems},
  year    = {2026},
  doi     = {10.1109/TPWRS.2026.3670270}
}
```

You may also use GitHub's **Cite this repository** button after `CITATION.cff` is added.

## Copyright and License

Copyright (c) 2026.

This repository is released under the Apache License 2.0 unless otherwise stated.
See the `LICENSE` file for details.

## Contact

For questions regarding the code, data, or paper, please open an issue in this repository.
