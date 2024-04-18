#include "emeter.hpp"

/********************/
/* Public functions */
/********************/

static int lastBadStatus = 0;

void tEmeter::CheckStatus() {
	if (m_Status != 0) {
		lastBadStatus = m_Status;
	}
	m_Status = 0;
}

tEmeter::tEmeter(I2C_HandleTypeDef* phi2c, eEmeterAddrPins pinA0, eEmeterAddrPins pinA1, uint8_t id) {
	m_phi2c = phi2c;
	m_ID = id;

	m_deviceAddress = m_baseAddress + (pinA1 << 2) + pinA0;
	m_writingAddress = m_deviceAddress << 1;  // Shift by 1 since bit 0 is the R/W bit
}

void tEmeter::WriteConfig(emeterConfigReg* reg) {
	uint8_t regValue[2];
	RegToUint8t((uint16_t*)reg, regValue);

	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eEmeterRegisters::Configuration, I2C_MEMADD_SIZE_8BIT, regValue, sizeof(regValue), 1000);
	if (ret != HAL_OK) {
		m_Status |= 1 << 1;
	} else {
		m_Status &= ~(1 << 1);
	}
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

	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eEmeterRegisters::Calibration, I2C_MEMADD_SIZE_8BIT, regValue, sizeof(regValue), 1000);
	if (ret != HAL_OK) {
		m_Status |= 1 << 2;
	} else {
		m_Status &= ~(1 << 2);
	}
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
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Read(m_phi2c, m_writingAddress, pReg, I2C_MEMADD_SIZE_8BIT, rxBuf, sizeof(rxBuf), 1000);
	if (ret != HAL_OK) {
		m_Status |= 1 << 0;
	} else {
		m_Status &= ~(1 << 0);
	}

	*pData = ((rxBuf[0] << 8) | (rxBuf[1]));
}
