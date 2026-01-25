#include "transmitter_lfsr256_v10.h"
#ifndef __linux__
int transmitter_lfsr256_v10_CfgInitialize(transmitter_lfsr256_v10 *InstancePtr, transmitter_lfsr256_v10_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->transmitter_lfsr256_v10_BaseAddress = ConfigPtr->transmitter_lfsr256_v10_BaseAddress;

    InstancePtr->IsReady = 1;
    return XST_SUCCESS;
}
#endif
void transmitter_lfsr256_v10_enable_tx_write(transmitter_lfsr256_v10 *InstancePtr, u32 Data) {

    Xil_AssertVoid(InstancePtr != NULL);

    transmitter_lfsr256_v10_WriteReg(InstancePtr->transmitter_lfsr256_v10_BaseAddress, 4, Data);
}
u32 transmitter_lfsr256_v10_enable_tx_read(transmitter_lfsr256_v10 *InstancePtr) {

    u32 Data;
    Xil_AssertVoid(InstancePtr != NULL);

    Data = transmitter_lfsr256_v10_ReadReg(InstancePtr->transmitter_lfsr256_v10_BaseAddress, 4);
    return Data;
}
void transmitter_lfsr256_v10_enable_data_write(transmitter_lfsr256_v10 *InstancePtr, u32 Data) {

    Xil_AssertVoid(InstancePtr != NULL);

    transmitter_lfsr256_v10_WriteReg(InstancePtr->transmitter_lfsr256_v10_BaseAddress, 0, Data);
}
u32 transmitter_lfsr256_v10_enable_data_read(transmitter_lfsr256_v10 *InstancePtr) {

    u32 Data;
    Xil_AssertVoid(InstancePtr != NULL);

    Data = transmitter_lfsr256_v10_ReadReg(InstancePtr->transmitter_lfsr256_v10_BaseAddress, 0);
    return Data;
}
