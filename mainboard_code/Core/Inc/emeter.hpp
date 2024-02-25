#pragma once

#include "emeterRegs.hpp"
#include "stm32f1xx_hal.h"

class tEmeter {
   public:
	tEmeter(I2C_HandleTypeDef* phi2c, eEmeterAddrPins pinA0, eEmeterAddrPins pinA1);

	void WriteConfig(emeterConfigReg* reg);
	void ReadBusVoltage(emeterBusVoltageReg* reg);
	void ReadPower(emeterPowerReg* reg);
	void ReadCurrent(emeterCurrentReg* reg);
	void WriteCalibration(emeterCalibrationReg* reg);

   private:
	void RegToUint8t(uint16_t* reg, uint8_t* value);
	void ReadRegister(uint16_t* pData, eEmeterRegisters pReg);

	I2C_HandleTypeDef* m_phi2c;

	uint8_t m_deviceAddress;
	uint8_t m_writingAddress;

	static constexpr uint8_t m_baseAddress = 0b1000000;
};
