## RFSoC Digital Calibration Source 
This repository is compatible with following versions of pynq images, design softwares and boards: 

PYNQ image v2.7 (https://www.pynq.io/boards.html)

Vivado 2020.2 

MATLAB R2020a 

RFSoC4x2 (https://www.rfsoc-pynq.io)

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

SD card image for this board --> <Copy the image from card, upload it repo and redirect from here>


## Regenerating Vivado project from .tcl file 

1. Browse to https://github.com/WVURAIL/Digital_Noise_Source/digital_cal_source 

2. Clone the repository on your local machine. 

3. Open Vivado 2020.2 (run as administrator -> good practice); open make_block_design.tcl file to make changes for path of constraints.xdc file --
Make following changes to the line --
add_files -fileset constrs_1 -norecurse constraints.xdc 

4. In tcl console change the directory to the one where your .tcl file is saved (file name: make_block_design.tcl); make sure make_block_design.tcl and rfsoc_radio.tcl are saved in same directory as first uses the other to recreate the whole project. 
$cd file_path/file_name 

5. Now source the .tcl file: 
$source make_block_design.tcl 

This should regenerate the whole project! 

6. Once the project and block design gets generated, create HDL wrapper by right-clicking rfsoc_radio.bd in Design Sources in Sources window. This makes newly created rfsoc_radio_wrapper your top module for further synthesis, implementation and creating bitstream files.
 
