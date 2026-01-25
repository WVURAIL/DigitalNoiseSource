#ifndef TRANSMITTER_LFSR256_V10__H
#define TRANSMITTER_LFSR256_V10__H
#ifdef __cplusplus
extern "C" {
#endif
/***************************** Include Files *********************************/
#ifndef __linux__
#include "xil_types.h"
#include "xil_assert.h"
#include "xstatus.h"
#include "xil_io.h"
#else
#include <stdint.h>
#include <assert.h>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stddef.h>
#endif
#include "transmitter_lfsr256_v10_hw.h"
/**************************** Type Definitions ******************************/
#ifdef __linux__
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
#else
typedef struct {
    u16 DeviceId;
    u32 transmitter_lfsr256_v10_BaseAddress;
} transmitter_lfsr256_v10_Config;
#endif
/**
* The transmitter_lfsr256_v10 driver instance data. The user is required to
* allocate a variable of this type for every transmitter_lfsr256_v10 device in the system.
* A pointer to a variable of this type is then passed to the driver
* API functions.
*/
typedef struct {
    u32 transmitter_lfsr256_v10_BaseAddress;
    u32 IsReady;
} transmitter_lfsr256_v10;
/***************** Macros (Inline Functions) Definitions *********************/
#ifndef __linux__
#define transmitter_lfsr256_v10_WriteReg(BaseAddress, RegOffset, Data) \
    Xil_Out32((BaseAddress) + (RegOffset), (u32)(Data))
#define transmitter_lfsr256_v10_ReadReg(BaseAddress, RegOffset) \
    Xil_In32((BaseAddress) + (RegOffset))
#else
#define transmitter_lfsr256_v10_WriteReg(BaseAddress, RegOffset, Data) \
    *(volatile u32*)((BaseAddress) + (RegOffset)) = (u32)(Data)
#define transmitter_lfsr256_v10_ReadReg(BaseAddress, RegOffset) \
    *(volatile u32*)((BaseAddress) + (RegOffset))

#define Xil_AssertVoid(expr)    assert(expr)
#define Xil_AssertNonvoid(expr) assert(expr)

#define XST_SUCCESS             0
#define XST_DEVICE_NOT_FOUND    2
#define XST_OPEN_DEVICE_FAILED  3
#define XIL_COMPONENT_IS_READY  1
#endif
/************************** Function Prototypes *****************************/
#ifndef __linux__
int transmitter_lfsr256_v10_Initialize(transmitter_lfsr256_v10 *InstancePtr, u16 DeviceId);
transmitter_lfsr256_v10_Config* transmitter_lfsr256_v10_LookupConfig(u16 DeviceId);
int transmitter_lfsr256_v10_CfgInitialize(transmitter_lfsr256_v10 *InstancePtr, transmitter_lfsr256_v10_Config *ConfigPtr);
#else
int transmitter_lfsr256_v10_Initialize(transmitter_lfsr256_v10 *InstancePtr, const char* InstanceName);
int transmitter_lfsr256_v10_Release(transmitter_lfsr256_v10 *InstancePtr);
#endif
/**
* Write to enable_tx gateway of transmitter_lfsr256_v10. Assignments are LSB-justified.
*
* @param	InstancePtr is the enable_tx instance to operate on.
* @param	Data is value to be written to gateway enable_tx.
*
* @return	None.
*
* @note    .
*
*/
void transmitter_lfsr256_v10_enable_tx_write(transmitter_lfsr256_v10 *InstancePtr, u32 Data);
/**
* Read from enable_tx gateway of transmitter_lfsr256_v10. Assignments are LSB-justified.
*
* @param	InstancePtr is the enable_tx instance to operate on.
*
* @return	u32
*
* @note    .
*
*/
u32 transmitter_lfsr256_v10_enable_tx_read(transmitter_lfsr256_v10 *InstancePtr);
/**
* Write to enable_data gateway of transmitter_lfsr256_v10. Assignments are LSB-justified.
*
* @param	InstancePtr is the enable_data instance to operate on.
* @param	Data is value to be written to gateway enable_data.
*
* @return	None.
*
* @note    .
*
*/
void transmitter_lfsr256_v10_enable_data_write(transmitter_lfsr256_v10 *InstancePtr, u32 Data);
/**
* Read from enable_data gateway of transmitter_lfsr256_v10. Assignments are LSB-justified.
*
* @param	InstancePtr is the enable_data instance to operate on.
*
* @return	u32
*
* @note    .
*
*/
u32 transmitter_lfsr256_v10_enable_data_read(transmitter_lfsr256_v10 *InstancePtr);
#ifdef __cplusplus
}
#endif
#endif
