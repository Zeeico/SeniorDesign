#ifndef MYMAIN_H
#define MYMAIN_H

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"

//! Private defines

//! Function prototypes
int mymain();

//! Extern variables
extern uint32_t g_CanTxTick;
extern uint32_t g_CanRxTick;
extern uint32_t g_BoardDetectTick;

extern CAN_HandleTypeDef hcan;

#ifdef __cplusplus
}
#endif

#endif	// MYMAIN_H