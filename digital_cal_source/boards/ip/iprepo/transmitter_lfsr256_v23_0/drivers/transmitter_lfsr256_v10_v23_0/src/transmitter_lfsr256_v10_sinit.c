/**
* @file transmitter_lfsr256_v10_sinit.c
*
* The implementation of the transmitter_lfsr256_v10 driver's static initialzation
* functionality.
*
* @note
*
* None
*
*/
#ifndef __linux__
#include "xstatus.h"
#include "xparameters.h"
#include "transmitter_lfsr256_v10.h"
extern transmitter_lfsr256_v10_Config transmitter_lfsr256_v10_ConfigTable[];
/**
* Lookup the device configuration based on the unique device ID.  The table
* ConfigTable contains the configuration info for each device in the system.
*
* @param DeviceId is the device identifier to lookup.
*
* @return
*     - A pointer of data type transmitter_lfsr256_v10_Config which
*    points to the device configuration if DeviceID is found.
*    - NULL if DeviceID is not found.
*
* @note    None.
*
*/
transmitter_lfsr256_v10_Config *transmitter_lfsr256_v10_LookupConfig(u16 DeviceId) {
    transmitter_lfsr256_v10_Config *ConfigPtr = NULL;
    int Index;
    for (Index = 0; Index < XPAR_TRANSMITTER_LFSR256_V10_NUM_INSTANCES; Index++) {
        if (transmitter_lfsr256_v10_ConfigTable[Index].DeviceId == DeviceId) {
            ConfigPtr = &transmitter_lfsr256_v10_ConfigTable[Index];
            break;
        }
    }
    return ConfigPtr;
}
int transmitter_lfsr256_v10_Initialize(transmitter_lfsr256_v10 *InstancePtr, u16 DeviceId) {
    transmitter_lfsr256_v10_Config *ConfigPtr;
    Xil_AssertNonvoid(InstancePtr != NULL);
    ConfigPtr = transmitter_lfsr256_v10_LookupConfig(DeviceId);
    if (ConfigPtr == NULL) {
        InstancePtr->IsReady = 0;
        return (XST_DEVICE_NOT_FOUND);
    }
    return transmitter_lfsr256_v10_CfgInitialize(InstancePtr, ConfigPtr);
}
#endif
