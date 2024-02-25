#include "mymain.h"

#include "emeter.hpp"
#include "mymain_cpp.h"

int mymain() {
	//! Final setup not handled by cubemx generated code
	HAL_ADC_Start_DMA(&hadc1, reinterpret_cast<uint32_t *>(thermistorValues.data()), thermistorValues.size());

	tEmeter emeter0(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::GND);
	tEmeter emeter1(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::VS);

	tEmeter emeter2(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::GND);
	tEmeter emeter3(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::VS);

	emeterConfigReg emeterConfig;
	emeterConfig.reset = 0b0;	 // Don't reset
	emeterConfig.brng = 0b1;	 // Bus voltage range 32V
	emeterConfig.pg = 0b10;		 // PG gain of 1/4, range of ±160 mV
	emeterConfig.badc = 0b0011;	 // 12 bit ADC, 532 μs conversion time
	emeterConfig.mode = 0b111;	 // Shunt and Bus continuous mode

	emeter0.WriteConfig(&emeterConfig);
	emeter1.WriteConfig(&emeterConfig);
	emeter2.WriteConfig(&emeterConfig);
	emeter3.WriteConfig(&emeterConfig);

	while (1) {
	}
}

// CAN Rx interrupt handler
// Make sure there are no issues with this not being in main.c
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *p_hcan) {
	CAN_RxHeaderTypeDef rxHeader;
	uint8_t rxData[8];
	HAL_CAN_GetRxMessage(p_hcan, CAN_RX_FIFO0, &rxHeader, rxData);

	switch (rxHeader.StdId) {
		// Handle messages here
		default:
			break;
	}
}
