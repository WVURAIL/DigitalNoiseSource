Regenerating Vivado project from .tcl file 


1. Browse to https://github.com/WVURAIL/Digital_Noise_Source (github repo for the project) 

2. Clone the repository on your local machine. 

3. Open Vivado 2020.2 (run as administrator -> good practice); in tcl console change the directory to the one where your .tcl file is saved (file name: make_block_design.tcl) 

cd file_path/file_name 

4. Now source the .tcl file: 

source make_block_design.tcl 

This should regenerate the whole project! 

5. Error might pop up about path saved for constraints.xdc file which is saved in the same directory as .tcl -> change the path for constraints.xdc by editing .tcl file in Vivado and again follow the same procedure as above; this time you should succeed!  

6. Once the project and block design gets generated, created HDL wrapper by right-clicking rfsoc_radio.bd in Design Sources in Sources window. This makes newly created rfsoc_radio_wrapper your top module.   

 
