#include "emeter.hpp"

/********************/
/* Public functions */
/********************/

tEmeter::tEmeter(I2C_HandleTypeDef* phi2c, eEmeterAddrPins pinA0, eEmeterAddrPins pinA1) {
	m_phi2c = phi2c;

	m_deviceAddress = m_baseAddress + (pinA1 << 2) + pinA0;
	m_writingAddress = m_deviceAddress << 1;  // Shift by 1 since bit 0 is the R/W bit
}

void tEmeter::WriteConfig(emeterConfigReg* reg) {
	uint8_t regValue[2];
	RegToUint8t((uint16_t*)reg, regValue);

	HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eEmeterRegisters::Configuration, I2C_MEMADD_SIZE_8BIT, regValue, sizeof(regValue), HAL_MAX_DELAY);
}

void tEmeter::ReadBusVoltage(emeterBusVoltageReg* reg) {
	ReadRegister((uint16_t*)reg, eEmeterRegisters::BusVoltage);
}

void tEmeter::ReadPower(emeterPowerReg* reg) {
	ReadRegister((uint16_t*)reg, eEmeterRegisters::Power);
}

void tEmeter::ReadCurrent(emeterCurrentReg* reg) {
	ReadRegister((uint16_t*)reg, eEmeterRegisters::Current);
}

void tEmeter::WriteCalibration(emeterCalibrationReg* reg) {
	uint8_t regValue[2];
	RegToUint8t((uint16_t*)reg, regValue);

	HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eEmeterRegisters::Calibration, I2C_MEMADD_SIZE_8BIT, regValue, sizeof(regValue), HAL_MAX_DELAY);
}

/*********************/
/* Private functions */
/*********************/

void tEmeter::RegToUint8t(uint16_t* reg, uint8_t* value) {
	*value = (uint8_t)((*reg >> 8) & 0xFF);
	*(value + 1) = (uint8_t)(*reg & 0xFF);
}

void tEmeter::ReadRegister(uint16_t* pData, eEmeterRegisters pReg) {
	uint8_t rxBuf[2];
	HAL_I2C_Mem_Read(m_phi2c, m_writingAddress, pReg, I2C_MEMADD_SIZE_8BIT, rxBuf, sizeof(rxBuf), HAL_MAX_DELAY);

	*pData = ((rxBuf[0] << 8) | (rxBuf[1]));
}
