#include "mymain.h"

#include "mymain.hpp"

namespace {
static constexpr uint32_t cVoltageSetId = 0x100;
static constexpr uint32_t cRelaySetId = 0x200;

static constexpr uint32_t cEmeterFeedbackId = 0x300;
static constexpr uint32_t cEmeterFeedbackPeriod = 50;  // ms

static constexpr int cInvalidVoltageCmd = 0xFFFF;
}  // namespace

uint32_t g_CanTxTick = 0;  // Decrements, send message when it is 0
uint32_t g_CanRxTick = 0;  // Increments, reset to 0 whenever a CAN message is received

tEmeter emeter0(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::GND, 0);
tEmeter emeter1(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::VS, 1);
tEmeter emeter2(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::GND, 2);
tEmeter emeter3(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::VS, 3);

tMPQ4214 bbController0(&hi2c1, eMPQ4214AddrPins::VLvl1);
tMPQ4214 bbController1(&hi2c1, eMPQ4214AddrPins::VLvl4);
tMPQ4214 bbController2(&hi2c2, eMPQ4214AddrPins::VLvl1);
tMPQ4214 bbController3(&hi2c2, eMPQ4214AddrPins::VLvl4);

CAN_TxHeaderTypeDef emeterCanHeader;
uint32_t CanTxMailbox;

void InitEmeter(tEmeter &emeter);
void InitBBController(tMPQ4214 &controller);
void SendEmeterStatus(tEmeter &emeter);

int akash_red_bull_counter = 0;

int mymain() {
	akash_red_bull_counter++;
	//! Final setup not handled by cubemx generated code
	HAL_ADC_Start_DMA(&hadc1, reinterpret_cast<uint32_t *>(thermistorValues.data()), thermistorValues.size());

	akash_red_bull_counter++;
	// InitEmeter(emeter0);
	// InitEmeter(emeter1);
	// InitEmeter(emeter2);
	// InitEmeter(emeter3);

	akash_red_bull_counter++;
	// InitBBController(bbController0);
	// InitBBController(bbController1);
	// InitBBController(bbController2);
	// InitBBController(bbController3);

	akash_red_bull_counter++;
	emeterCanHeader.StdId = cEmeterFeedbackId;
	emeterCanHeader.RTR = CAN_RTR_DATA;
	emeterCanHeader.IDE = CAN_ID_STD;
	emeterCanHeader.DLC = 8;
	emeterCanHeader.TransmitGlobalTime = DISABLE;

	while (1) {
		akash_red_bull_counter++;
		if (g_CanTxTick == 0) {
			// SendEmeterStatus(emeter0);
			// SendEmeterStatus(emeter1);
			// SendEmeterStatus(emeter2);
			// SendEmeterStatus(emeter3);

			static int val = 0;
			uint8_t tx_data[8];
			tx_data[0] = val++;
			HAL_CAN_AddTxMessage(&hcan, &emeterCanHeader, tx_data, &CanTxMailbox);

			g_CanTxTick = cEmeterFeedbackPeriod;
		}

		// CAN_RxHeaderTypeDef rxHeader;
		// uint8_t rxData[8];
		// if (HAL_CAN_GetRxMessage(&hcan, CAN_RX_FIFO0, &rxHeader, rxData) == HAL_OK) {
			// static int rx_counter = 0;
			// rx_counter++;
		// }
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

void SendEmeterStatus(tEmeter &emeter) {
	emeterBusVoltageReg voltage;
	emeterCurrentReg current;
	emeterPowerReg power;

	emeter.ReadBusVoltage(&voltage);
	emeter.ReadCurrent(&current);
	emeter.ReadPower(&power);

	uint8_t txData[8];
	txData[0] = emeter.GetID();

	txData[2] = voltage.bd & 0xFF;
	txData[3] = voltage.bd >> 8;

	int16_t signedCurrent = current.csign ? -current.cd : current.cd;  // Do the signed conversion manually
	txData[4] = signedCurrent & 0xFF;
	txData[5] = signedCurrent >> 8;

	txData[6] = power.pd & 0xFF;
	txData[7] = power.pd >> 8;

	HAL_CAN_AddTxMessage(&hcan, &emeterCanHeader, txData, &CanTxMailbox);
}

// CAN Rx interrupt handler
// Make sure there are no issues with this not being in main.c
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *p_hcan) {
	CAN_RxHeaderTypeDef rxHeader;
	uint8_t rxData[8];
	if (HAL_CAN_GetRxMessage(p_hcan, CAN_RX_FIFO0, &rxHeader, rxData) == HAL_OK)
		g_CanRxTick = 0;

	switch (rxHeader.StdId) {
		// Voltage set
		case cVoltageSetId: {
			std::array<uint16_t, 4> voltageSettings;

			int i = 0;
			for (uint16_t &vset : voltageSettings) {
				vset = rxData[i++];
				vset += (rxData[i++]) << 8;
			}

			MPQ4214VRefLsbReg VRefLsb;
			MPQ4214VRefMsbReg VRefMsb;

			if (voltageSettings[0] != cInvalidVoltageCmd) {
				VRefLsb.unused = 0b00000;
				VRefLsb.VREF_L = voltageSettings[0] & 0b111;
				VRefMsb.VREF_H = (voltageSettings[0] >> 3) & 0xFF;
				bbController0.SetVoltage(&VRefLsb, &VRefMsb);
			}

			if (voltageSettings[1] != cInvalidVoltageCmd) {
				VRefLsb.unused = 0b00000;
				VRefLsb.VREF_L = voltageSettings[1] & 0b111;
				VRefMsb.VREF_H = (voltageSettings[1] >> 3) & 0xFF;
				bbController1.SetVoltage(&VRefLsb, &VRefMsb);
			}

			if (voltageSettings[2] != cInvalidVoltageCmd) {
				VRefLsb.unused = 0b00000;
				VRefLsb.VREF_L = voltageSettings[2] & 0b111;
				VRefMsb.VREF_H = (voltageSettings[2] >> 3) & 0xFF;
				bbController2.SetVoltage(&VRefLsb, &VRefMsb);
			}

			if (voltageSettings[3] != cInvalidVoltageCmd) {
				VRefLsb.unused = 0b00000;
				VRefLsb.VREF_L = voltageSettings[3] & 0b111;
				VRefMsb.VREF_H = (voltageSettings[3] >> 3) & 0xFF;
				bbController3.SetVoltage(&VRefLsb, &VRefMsb);
			}
			break;
		}

		// Current set
		// Relay set
		case cRelaySetId:
			HAL_GPIO_WritePin(relay0cmd_GPIO_Port, relay0cmd_Pin, (GPIO_PinState)(rxData[0] & 0b0001));
			HAL_GPIO_WritePin(relay1cmd_GPIO_Port, relay1cmd_Pin, (GPIO_PinState)(rxData[0] & 0b0010));
			HAL_GPIO_WritePin(relay2cmd_GPIO_Port, relay2cmd_Pin, (GPIO_PinState)(rxData[0] & 0b0100));
			HAL_GPIO_WritePin(relay3cmd_GPIO_Port, relay3cmd_Pin, (GPIO_PinState)(rxData[0] & 0b1000));

			break;

		// Handle messages here
		default:
			break;
	}
}

// Power Controller external interrupt handler
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
	return;
	tMPQ4214 *p_controller;
	switch (GPIO_Pin) {
		case controller0exti_Pin:
			// Controller 0 interrupt triggered
			p_controller = &bbController0;
			break;

		case controller1exti_Pin:
			// Controller 1 interrupt triggered
			p_controller = &bbController1;
			break;

		case controller2exti_Pin:
			// Controller 2 interrupt triggered
			p_controller = &bbController2;
			break;

		case controller3exti_Pin:
			// Controller 3 interrupt triggered
			p_controller = &bbController3;
			break;

		default:
			return;
	}

	MPQ4214InterruptStatus reg;
	p_controller->ReadInterruptStatus(&reg);

	if (reg.OTP) {
	}
	if (reg.CC) {
	}
	if (reg.OVP) {
	}
	if (reg.OCP) {
	}
	if (reg.PNG) {
	}

	// Clear the interrupts
	uint8_t statusReset = 0xFF;
	p_controller->SetInterruptStatus((MPQ4214InterruptStatus *)(&statusReset));
}
