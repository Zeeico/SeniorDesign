#include "mymain.h"

#include "emeter.hpp"
#include "mpq4214.hpp"
#include "mymain_cpp.h"

void InitEmeter(tEmeter &emeter);
void InitBBController(tMPQ4214 &controller);

int mymain() {
	//! Final setup not handled by cubemx generated code
	HAL_ADC_Start_DMA(&hadc1, reinterpret_cast<uint32_t *>(thermistorValues.data()), thermistorValues.size());

	tEmeter emeter0(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::GND);
	tEmeter emeter1(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::VS);
	tEmeter emeter2(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::GND);
	tEmeter emeter3(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::VS);

	InitEmeter(emeter0);
	InitEmeter(emeter1);
	InitEmeter(emeter2);
	InitEmeter(emeter3);

	tMPQ4214 bbController0(&hi2c1, eMPQ4214AddrPins::VLvl1);
	tMPQ4214 bbController1(&hi2c1, eMPQ4214AddrPins::VLvl4);
	tMPQ4214 bbController2(&hi2c2, eMPQ4214AddrPins::VLvl1);
	tMPQ4214 bbController3(&hi2c2, eMPQ4214AddrPins::VLvl4);

	InitBBController(bbController0);
	InitBBController(bbController1);
	InitBBController(bbController2);
	InitBBController(bbController3);

	while (1) {
	}
}

void InitEmeter(tEmeter &emeter) {
	emeterConfigReg emeterConfig;
	emeterConfig.reset = 0b0;	 // Don't reset
	emeterConfig.brng = 0b1;	 // Bus voltage range 32V
	emeterConfig.pg = 0b10;		 // PG gain of 1/4, range of ±160 mV
	emeterConfig.badc = 0b0011;	 // 12 bit ADC, 532 μs conversion time
	emeterConfig.mode = 0b111;	 // Shunt and Bus continuous mode

	emeter.WriteConfig(&emeterConfig);
}

void InitBBController(tMPQ4214 &controller) {
	MPQ4214VRefLsbReg controllerVRefLsb;
	MPQ4214VRefMsbReg controllerVRefMsb;
	controllerVRefLsb.unused = 0b00000;
	controllerVRefLsb.VREF_L = 0b000;		 // Initialise VREF to 0
	controllerVRefMsb.VREF_H = 0b0000'0000;	 // Initialise VREF to 0
	controller.SetVoltage(&controllerVRefLsb, &controllerVRefMsb);

	MPQ4214Control1Reg controllerControl1;
	controllerControl1.SR = 0b00;		 // VRef slew rate = 38 mV/ms
	controllerControl1.DISCHG = 0b0;	 // Disable output discharge resistor
	controllerControl1.Dither = 0b0;	 // Disable dither
	controllerControl1.PNG_Latch = 0b1;	 // Activate Power Not Good latch
	controllerControl1.Reserved = 0b1;	 // Has to be set to 1
	controllerControl1.GO_BIT = 0b0;	 // Disable changing VOut
	controllerControl1.ENPWR = 0b0;		 // Disable power switching
	controller.SetControl1(&controllerControl1);

	MPQ4214Control2Reg controllerControl2;
	controllerControl2.FSW = 0b00;		 // 200 kHz switching frequency
	controllerControl2.BB_FSW = 0b0;	 // Higher switching frequency in buck-boost region
	controllerControl2.OCP_MODE = 0b01;	 // Hiccup protection, no latching
	controllerControl2.OVP_MODE = 0b10;	 // Latch off protection, no discharge after OVP
	controller.SetControl2(&controllerControl2);

	MPQ4214ILIMReg controllerCurrentLim;
	controllerCurrentLim.ILIM = 0b111;	// Highest current limit, actual limiting done in emeter
	controllerCurrentLim.unused = 0b00000;
	controller.SetILIMReg(&controllerCurrentLim);

	MPQ4214InterruptMask controllerInterruptMask;
	controllerInterruptMask.M_OTP = 0b0;  // Don't mask interrupt
	controllerInterruptMask.M_CC = 0b0;	  // Don't mask interrupt
	controllerInterruptMask.M_OVP = 0b0;  // Don't mask interrupt
	controllerInterruptMask.M_OCP = 0b0;  // Don't mask interrupt
	controllerInterruptMask.M_PNG = 0b0;  // Don't mask interrupt
	controller.SetInterruptMask(&controllerInterruptMask);
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
