#pragma once

#include "emeterRegs.hpp"
#include "stm32f1xx_hal.h"

class tEmeter {
   public:
	tEmeter(I2C_HandleTypeDef* phi2c, eEmeterAddrPins pinA0, eEmeterAddrPins pinA1, uint8_t id);

	void WriteConfig(emeterConfigReg* reg);
	void ReadBusVoltage(emeterBusVoltageReg* reg);
	void ReadPower(emeterPowerReg* reg);
	void ReadCurrent(emeterCurrentReg* reg);
	void WriteCalibration(emeterCalibrationReg* reg);

	uint8_t GetID() { return m_ID; }

	void SetInitialised(bool val) { m_Initialised = val; }
	bool GetInitialised() { return m_Initialised; }

	void CheckStatus();

   private:
	void RegToUint8t(uint16_t* reg, uint8_t* value);
	void ReadRegister(uint16_t* pData, eEmeterRegisters pReg);

	I2C_HandleTypeDef* m_phi2c;

	uint8_t m_deviceAddress;
	uint8_t m_writingAddress;
	uint8_t m_ID;

	bool m_Initialised{false};
	int m_Status = 0;

	static constexpr uint8_t m_baseAddress = 0b1000000;
};
