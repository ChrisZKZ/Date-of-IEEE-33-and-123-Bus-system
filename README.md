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

## Notes on the Supplementary Example Scripts

The scripts under `examples/uncertainty_set_toy/` are **independent illustrative examples** rather than the main IEEE 33-/123-bus simulation workflow. Their purpose is to demonstrate uncertainty-set construction and statistically feasible optimization ideas in a simplified two-dimensional setting.

These scripts are provided to improve transparency and reproducibility of the methodological ideas. They can be run independently and do not modify the main case-study data.

## Running the Supplementary Examples

From the repository root:

```bash
python examples/uncertainty_set_toy/uncertainty_set_ellip.py
python examples/uncertainty_set_toy/uncertainty_set_reconstr.py
python examples/uncertainty_set_toy/uncertainty_set_sm.py
python examples/uncertainty_set_toy/uncertainty_set_osa.py
```

## Citation

If this repository, the code, the data, or the supplementary materials are useful in your research, please cite the associated paper.

```bibtex
@article{zhang2026asynchronous,
  title={Asynchronous Distributed Scheduling of Active Distribution Network and Thermostatically Controlled Loads With MPC-Based Aggregation},
  author={Zhang, Kaizhe and Zhu, Jie and Xu, Yinliang and Tai, Nengling and Xie, Yurong and Wen, Qiangyu and Sun, Hongbin},
  journal={IEEE Transactions on Power Systems},
  year={2026},
  publisher={IEEE}
}
```

## Copyright and License

Copyright (c) 2026 Kaizhe Zhang

This repository is released under the Apache License 2.0 unless otherwise stated.
See the `LICENSE` file for details.

