#include "emeter.hpp"

tEmeter::tEmeter(I2C_HandleTypeDef* phi2c, tEmeterAddrPins pinA0, tEmeterAddrPins pinA1) {
	m_phi2c = phi2c;

	m_address = m_baseAddress + (pinA1 << 2) + pinA0;
}

void tEmeter::WriteConfig(emeterConfigReg* reg) {
	// Should be all that's needed I think
	HAL_I2C_Master_Transmit(m_phi2c, m_address, (uint8_t*)reg, sizeof(reg), HAL_MAX_DELAY);
}

void tEmeter::ReadBusVoltage(emeterBusVoltageReg* reg) {
	// Do some magic here to set the register to read
	HAL_I2C_Master_Receive(m_phi2c, m_address, (uint8_t*)reg, sizeof(reg), HAL_MAX_DELAY);
}

void tEmeter::ReadPower(emeterPowerReg* reg) {
	// Do some magic here to set the register to read
	HAL_I2C_Master_Receive(m_phi2c, m_address, (uint8_t*)reg, sizeof(reg), HAL_MAX_DELAY);
}

void tEmeter::ReadCurrent(emeterCurrentReg* reg) {
	// Do some magic here to set the register to read
	HAL_I2C_Master_Receive(m_phi2c, m_address, (uint8_t*)reg, sizeof(reg), HAL_MAX_DELAY);
}

void tEmeter::WriteCalibration(emeterCalibrationReg* reg) {
	// Should be all that's needed I think
	HAL_I2C_Master_Transmit(m_phi2c, m_address, (uint8_t*)reg, sizeof(reg), HAL_MAX_DELAY);
}
