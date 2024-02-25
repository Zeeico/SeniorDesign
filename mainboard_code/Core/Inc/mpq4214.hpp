#pragma once

#include "mpq4214Regs.hpp"
#include "stm32f1xx_hal.h"

class tMPQ4214 {
   public:
	tMPQ4214(I2C_HandleTypeDef* phi2c, eMPQ4214AddrPins addrPin);

	void SetVoltage(MPQ4214RefLsbReg* lsbReg, MPQ4214RefMsbReg* msbReg);
	void ReadVoltage(MPQ4214RefLsbReg* lsbReg, MPQ4214RefMsbReg* msbReg);

   private:
	I2C_HandleTypeDef* m_phi2c;

	uint8_t m_deviceAddress;
	uint8_t m_writingAddress;
};
