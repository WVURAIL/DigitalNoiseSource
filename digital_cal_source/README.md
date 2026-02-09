## RFSoC Digital Calibration Source 
This repository is compatible with following versions of pynq images, design softwares and boards: 

[PYNQ image v2.7](https://www.pynq.io/boards.html)

[Vivado 2020.2](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive.html)

[MATLAB R2020a](https://www.mathworks.com/downloads)

System Generator for DSP ([MATLAB R2020a](https://www.mathworks.com/downloads) with [Vivado Design Suite 2020.2](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive.html))

[RFSoC4x2](https://www.rfsoc-pynq.io)

NOTE:: 
You should make sure you are using the supported version of Vivado for the respective PYNQ release which can be found below. 

System Generator is tightly version‑locked to specific MATLAB and Vivado releases; if you move to a newer MATLAB, you usually also need the matching System Generator release and a supported Vivado version; mixing arbitrary newer versions can lead to “version not supported” errors. 

Downgrading versions is not supported, only older --> newer is expected to work. 

The main risk is IP cores --> IP may get upgraded, change behavior, or be deprecated, so you must re-validate synthesis/implementation after migration. 

Here’s a table of the recommended Vivado versions for common PYNQ releases (for building overlays/bitstreams that match each SD image):
| PYNQ release | Recommended Vivado version |
|--------------|---------------------------|
| v2.3         | Vivado 2018.2             |
| v2.4         | Vivado 2018.2             |
| v2.5 / 2.5.1 | Vivado 2018.3             |
| v2.6         | Vivado 2020.1             |
| v2.7         | Vivado 2020.2             |
| v3.0 / 3.0.1 | Vivado 2022.1–2022.2      |
| v3.1         | Vivado 2022.1+ (3.x)      |

For this project, we target **PYNQ v2.7**, so all hardware should be built with **Vivado 2020.2**; avoid significantly newer versions unless you are willing to set **ignore_version=True** in overlay.py and debug potential IP mismatches.

SD card image for this board/project --> <Copy the image from card, upload it repo and redirect from here>

## About this project 
This repository contains design for Gaussian Noise Transmitter which transmits 1228.8MHz wide Gaussian noise that is sampled at 3.6864GHz, defining nyquist boundary at 1.8432GHz and Carrier frequency (Fc) = 900MHz targeting observing band ~300-1500MHz. DAC tile 229 (port DAC A) is in use for broadcasting the signal from the board. The firmware is designed to use external 10MHz timing reference. 

Rest of the firmware specific details are given in the python notebook written to program the board: [dns_notebook](https://github.com/WVURAIL/Digital_Noise_Source/blob/main/digital_cal_source/notebooks/dns_notebook.ipynb)

The run-time parameter reconfiguration is possible for the following parameters through same notebook code:

1. Carrier Frequency (Default=900MHz)

2. Read/write DAC power output (allowed range: 2.4-40.5mA) (Default=20mA)

3. DAC tile startup/shutdown

4. Reading on-chip temperatures and voltages

5. Set LMK04828 and LMX2594 clock synthesizers frequency output (Make sure respective clock config file (.text) exists in "xrfclk" directory on-board; otherwise it would break the board and need to reboot it again to load default clock config files)
(Default=LMK=245.76MHz, LMX=409.6MHz)

Addition to make: "Add snippet of DNS notebook" 

## Regenerating Vivado project from .tcl file 

1. Browse to https://github.com/WVURAIL/Digital_Noise_Source/digital_cal_source 

2. Clone the repository on your local machine. 

3. Open Vivado 2020.2 (run as administrator -> good practice); open make_block_design.tcl file to make changes for path of constraints.
xdc file --

Make following changes to the line --

add_files -fileset constrs_1 -norecurse constraints.xdc 

4. In tcl console change the directory to the one where your .tcl file is saved (file name: make_block_design.tcl); make sure make_block_design.tcl and rfsoc_radio.tcl are saved in same directory as first uses the other to recreate the whole project. 

'$cd file_path/file_name'

5. Now source the .tcl file: 

'$source make_block_design.tcl'

**This should regenerate the whole project!**

6. Once the project and block design gets generated, create HDL wrapper by right-clicking rfsoc_radio.bd in Design Sources in Sources window. This makes newly created rfsoc_radio_wrapper your top module for further synthesis, implementation and creating bitstream (.bit) and hardware definition (.hwh) files.
 

 ## Programming the board
Follow the instructions to upload corresponding project files to SD card:

-- Make sure SD card flashed with PYNQ image v2.7 is inserted in the card slot and boot switch toggled to "SD" mode which makes sure board will be booted using SD card and not JTAG. 

-- Power on your RFSoC board. 

-- Navigate to Jupyter Labs by opening a browser (preferably Chrome) and connecting to 
'''bash
http://<board_ip_address>:9090/lab

-- Make new directory and upload following files to it: 
1. .bit file 
2. .hwh file 
3. dns_notebook (you can also write your own)
bitstream and hardware definition files for this project are also available [here](https://github.com/WVURAIL/Digital_Noise_Source/tree/main/digital_cal_source/bitstream_files)

-- Make subdirectory for overlay files: and add all the files from [here](https://github.com/WVURAIL/Digital_Noise_Source/tree/main/digital_cal_source/rfsoc_radio)

-- Once done and all files are on-board, run code cell in [dns_notebook](https://github.com/WVURAIL/Digital_Noise_Source/blob/main/digital_cal_source/notebooks/dns_notebook.ipynb) -->
<Provide snippet of the code>



