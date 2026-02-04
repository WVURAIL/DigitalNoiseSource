Regenerating Vivado project from .tcl file 

1. Browse to https://github.com/WVURAIL/Digital_Noise_Source/digital_cal_source (github repo for the project) 

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

 
