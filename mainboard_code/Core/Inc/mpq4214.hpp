#pragma once

#include "mpq4214Regs.hpp"
#include "stm32f1xx_hal.h"

class tMPQ4214 {
   public:
	tMPQ4214(I2C_HandleTypeDef* phi2c, eMPQ4214AddrPins addrPin);

	void SetVoltage(MPQ4214VRefLsbReg* lsbReg, MPQ4214VRefMsbReg* msbReg);
	void ReadVoltage(MPQ4214VRefLsbReg* lsbReg, MPQ4214VRefMsbReg* msbReg);

	void SetControl1(MPQ4214Control1Reg* reg);
	void SetControl2(MPQ4214Control2Reg* reg);

	void SetILIMReg(MPQ4214ILIMReg* reg);

	void SetInterruptStatus(MPQ4214InterruptStatus* reg);
	void ReadInterruptStatus(MPQ4214InterruptStatus* reg);

	void SetInterruptMask(MPQ4214InterruptMask* reg);

   private:
	I2C_HandleTypeDef* m_phi2c;

	uint8_t m_deviceAddress;
	uint8_t m_writingAddress;
};
