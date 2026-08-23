# Reproducibility notes

This repository contains the firmware and analysis code used for the PEACC paper. The analysis notebooks are research records, not a self-contained data release: raw measurements and several intermediate products are not stored in this repository.

## Software snapshot

The manuscript release is `peacc_v1.0.0`, published on 2026-08-20. Clone the repository with its pinned upstream RFSoC dependency:

```sh
git clone --recurse-submodules https://github.com/WVURAIL/DigitalNoiseSource.git
cd DigitalNoiseSource
```

The recorded analysis runtime was Python 3.9.10. Create an isolated environment and install the recorded packages plus the explicitly unversioned imports:

```sh
python3.9 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-analysis.txt
```

The requirements file distinguishes exact versions recorded by the project from imports whose versions were not recorded. The `pocket_correlator`/`pychfpga` dependency used by the correlator examples has neither a recorded distribution source nor a recorded version and must be supplied separately by an operator of that hardware.

## Data and paths

The data underlying the paper are openly available in the [PEACC Zenodo dataset](https://doi.org/10.5281/zenodo.21997893) under CC BY 4.0, as recorded in the paper's v2 data-availability statement. The dataset is not bundled in this repository.

Before running a notebook, obtain the relevant raw and intermediate data and replace its machine-specific paths (for example, `/Users/...`, `/Volumes/...`, and `/home/...`) with paths on your system. Run Jupyter from `data_analysis_notebooks/` so the local `rawice.py` and `time_utils.py` modules are importable:

```sh
cd data_analysis_notebooks
jupyter lab
```

The top-level [README](README.md) maps each notebook to its role. Reproduction also requires knowing which input files and notebook cells produced each figure; that mapping was not recorded comprehensively. Treat saved notebook output as a record of the authors' run, not as proof of a clean rerun on another machine.

## Hardware workflow

The analysis environment above is separate from RFSoC board operation. The supported board workflow targets PYNQ 2.7 and Vivado 2020.2 and requires the hardware-specific files and instructions under [`digital_cal_source/`](digital_cal_source/README.md). Board notebooks contain deployment-specific paths that must be updated on the target system.

## Vendored source

`data_analysis_notebooks/rawice.py` is pinned to an exact upstream revision. Its source, byte-level comparison, and reviewed update policy are documented in [RAWICE_PROVENANCE.md](RAWICE_PROVENANCE.md).
