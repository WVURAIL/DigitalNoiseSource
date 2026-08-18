# Digital Noise Source (DNS) aka Precision Emitter for 21 cm Array Coherent Calibration (PEACC)

Firmware and analysis code for the PEACC digital noise source, developed for drone-based and chamber-based dish beam calibration measurements at WVU and YALE. 

This repository accompanies https://arxiv.org/abs/2604.09859. The `data_analysis_notebooks/` scripts reproduce the beam maps, beam amplitude recovery curves, and related figures in that paper. For firmware, board bring-up, and hardware programming instructions, **see the [README in `digital_cal_source/`](digital_cal_source/README.md)**.

## Repository structure 

- `digital_cal_source/` — PEACC firmware, board bring-up, and hardware documentation. 
  **See the [README in that directory](digital_cal_source/README.md) for firmware-specific 
  build, programming, and dependency instructions.**
- `data_analysis_notebooks/` — data handling and analysis scripts, described below.
- `Zynq_ultrascale+_rfsoc/boards/` — Previously developed firmware files for lower bandwidth noise 
- `Images/` — supporting figures/diagrams
 
## Data analysis notebooks

### Raw data handling & utilities
| File | Purpose |
|---|---|
| `rawice.py` | Handles raw Iceboard data. (P. Sanghavi) |
| `time_utils.py` | Time-fitting utility functions. (W. Tyndall) |
| `analyse_raw_adc-checkpoint.ipynb` | Analyses raw ADC data from the Iceboard. |
| `dns_vdif_data_kbb.ipynb` | Handles and analyses raw Iceboard data in VDIF format. |
| `check_adc_levels_Ian.ipynb` | Checks ADC levels of CRS data. (I. Hendrickson) |

### Correlator (CRS) data handling
| File | Purpose |
|---|---|
| `run_pocket_correlator_observe.py` | Runs the CRS correlator observation; modified from t0.technology's script. **External code — see licensing note below.** |
| `test_pocket_correlator_auto.ipynb` | Runs the CRS correlator (provided by t0.technology). **External code — see licensing note below.** |
| `corr_data_noise_source_kbb.ipynb` | Analyses iceboard correlator data for noise-source parameters. |
| `crs_corr_data_analysis.ipynb` | Analyses CRS correlator data for noise-source parameters. |
| `autos&crosses_overlay.ipynb` | Overlays auto- and cross-correlated Iceboard data. |

### Chamber-test analysis
| File | Purpose |
|---|---|
| `KBB_dns_corrdata_analysis_chamberdata_final.ipynb` | Analyses correlator data and plots beam maps, chamber tests. |
| `KBB_dns_beamamprecovery_implement_chamberdata_final.ipynb` | Plots beam amplitude recovery error and related parameters, chamber data. |

### Drone-test analysis
| File | Purpose |
|---|---|
| `Drone_Angle_Code.ipynb` | Synchronises drone and correlator data. |
| `drone_data_investigate.ipynb` | Investigates drone data for instrumental delays, phase, DC offsets. |
| `KBB_dns_corrdata_analysis_dronedata_final.ipynb` | Analyses correlator data and plots beam maps, drone tests. |
| `KBB_dns_beamamprecovery_implement_dronedata_final.ipynb` | Plots beam amplitude recovery error and related parameters, drone data. |

### Publication plots
| File | Purpose |
|---|---|
| `chamber+bench_publication_plots.ipynb` | Plotting utilities for bench/chamber-test publication figures. |
| `drone_publications_plots.ipynb` | Plotting utilities for drone-test publication figures. |

## External code / attribution

- `run_pocket_correlator_observe.py` and `test_pocket_correlator_auto.ipynb` originate 
  from t0.technology's CRS correlator examples, modified for this project. [should be excluded from the BDS-clause 3 license scope.]
- `check_adc_levels_Ian.ipynb` provided by Ian Hendrickson.
- `rawice.py` and `time_utils.py` written by P. Sanghavi and W. Tyndall respectively.

## Installation / dependencies

python: 3.9.10 | numpy: 1.22.4 | scipy: 1.13.1 | pandas: 2.1.1 | matplotlib: 3.5.1 | h5py: 3.8.0 | allantools: 2024.04 | scikit-rf: 1.1.0 | psutil: 5.9.6 | pytz: 2023.3.post1 | PyYAML: 6.0.1 | pygeodesy: 25.12.31

Some scripts depend on internal modules also in this repo (`rawice.py`, `time_utils.py`)  — no separate installation needed, just ensure they're on your `PYTHONPATH` or run notebooks from the repo root.

## Citation

If you use this code, please cite: [paper citation — placeholder until published]

## License

BSD-3-clause — see [LICENSE](LICENSE). 

Note: portions of the correlator scripts are third-party in origin — see "External code / attribution" above.




