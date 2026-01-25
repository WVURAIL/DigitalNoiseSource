proc generate {drv_handle} {
    xdefine_include_file $drv_handle "xparameters.h" "transmitter_lfsr256_v10" "NUM_INSTANCES" "DEVICE_ID" "C_TRANSMITTER_LFSR256_V10_S_AXI_BASEADDR" "C_TRANSMITTER_LFSR256_V10_S_AXI_HIGHADDR" 
    xdefine_config_file $drv_handle "transmitter_lfsr256_v10_g.c" "transmitter_lfsr256_v10" "DEVICE_ID" "C_TRANSMITTER_LFSR256_V10_S_AXI_BASEADDR" 
    xdefine_canonical_xpars $drv_handle "xparameters.h" "transmitter_lfsr256_v10" "DEVICE_ID" "C_TRANSMITTER_LFSR256_V10_S_AXI_BASEADDR" "C_TRANSMITTER_LFSR256_V10_S_AXI_HIGHADDR" 

}