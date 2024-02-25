#include "mpq4214.hpp"

/********************/
/* Public functions */
/********************/

tMPQ4214::tMPQ4214(I2C_HandleTypeDef* phi2c, eMPQ4214AddrPins addrPin) {
	m_phi2c = phi2c;

	switch (addrPin) {
		case eMPQ4214AddrPins::VLvl1:
			m_deviceAddress = 0x60;
			break;

		case eMPQ4214AddrPins::VLvl2:
			m_deviceAddress = 0x62;
			break;

		case eMPQ4214AddrPins::VLvl3:
			m_deviceAddress = 0x63;
			break;

		case eMPQ4214AddrPins::VLvl4:
			m_deviceAddress = 0x66;
			break;

		default:
			break;
	}

	m_writingAddress = m_deviceAddress << 1;
}

void tMPQ4214::SetVoltage(MPQ4214RefLsbReg* lsbReg, MPQ4214RefMsbReg* msbReg) {
	HAL_I2C_Mem_Write(m_phi2c, m_deviceAddress, eMPQ4214Registers::REF_LSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)lsbReg, sizeof(lsbReg), HAL_MAX_DELAY);

	HAL_I2C_Mem_Write(m_phi2c, m_deviceAddress, eMPQ4214Registers::REF_MSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)msbReg, sizeof(msbReg), HAL_MAX_DELAY);
}

void tMPQ4214::ReadVoltage(MPQ4214RefLsbReg* lsbReg, MPQ4214RefMsbReg* msbReg) {
	HAL_I2C_Mem_Read(m_phi2c, m_deviceAddress, eMPQ4214Registers::REF_LSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)lsbReg, sizeof(lsbReg), HAL_MAX_DELAY);

	HAL_I2C_Mem_Read(m_phi2c, m_deviceAddress, eMPQ4214Registers::REF_MSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)msbReg, sizeof(msbReg), HAL_MAX_DELAY);
}
