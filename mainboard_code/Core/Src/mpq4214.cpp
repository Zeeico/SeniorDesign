#include "mpq4214.hpp"

/********************/
/* Public functions */
/********************/

tMPQ4214::tMPQ4214(I2C_HandleTypeDef* phi2c, eMPQ4214AddrPins addrPin, uint8_t id) {
	m_phi2c = phi2c;
	m_ID = id;

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

void tMPQ4214::FindAddress(MPQ4214VRefLsbReg* lsbReg) {
	HAL_StatusTypeDef ret;
	int goodAddress = -1;
	for (uint8_t i = 0; i < 0x7F; i++) {
		if (i == 65)
			continue;
		ret = HAL_I2C_Mem_Write(m_phi2c, i << 1, eMPQ4214Registers::REF_LSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)lsbReg, sizeof(*lsbReg), 1000);
		if (ret == HAL_OK) {
			goodAddress = i << 1;
		}
	}
	if (goodAddress == -1) {
		m_Status = 2;
	} else {
		m_Status = 1;
	}
	m_Status = 0;
}

void tMPQ4214::SetVoltage(MPQ4214VRefLsbReg* lsbReg, MPQ4214VRefMsbReg* msbReg) {
	// FindAddress(lsbReg);
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::REF_LSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)lsbReg, sizeof(*lsbReg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}

	ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::REF_MSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)msbReg, sizeof(*msbReg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
	m_Status = 10;
}

void tMPQ4214::ReadVoltage(MPQ4214VRefLsbReg* lsbReg, MPQ4214VRefMsbReg* msbReg) {
	HAL_I2C_Mem_Read(m_phi2c, m_writingAddress, eMPQ4214Registers::REF_LSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)lsbReg, sizeof(*lsbReg), 1000);

	HAL_I2C_Mem_Read(m_phi2c, m_writingAddress, eMPQ4214Registers::REF_MSB, I2C_MEMADD_SIZE_8BIT, (uint8_t*)msbReg, sizeof(*msbReg), 1000);
}

void tMPQ4214::SetControl1(MPQ4214Control1Reg* reg) {
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::Control1, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
}

void tMPQ4214::SetControl2(MPQ4214Control2Reg* reg) {
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::Control2, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
}

void tMPQ4214::SetILIMReg(MPQ4214ILIMReg* reg) {
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::ILIM, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
}

void tMPQ4214::SetInterruptStatus(MPQ4214InterruptStatus* reg) {
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::InterruptStatus, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
}

void tMPQ4214::ReadInterruptStatus(MPQ4214InterruptStatus* reg) {
	HAL_I2C_Mem_Read(m_phi2c, m_writingAddress, eMPQ4214Registers::InterruptStatus, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
}

void tMPQ4214::SetInterruptMask(MPQ4214InterruptMask* reg) {
	HAL_StatusTypeDef ret = HAL_I2C_Mem_Write(m_phi2c, m_writingAddress, eMPQ4214Registers::InterruptMask, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg, sizeof(*reg), 1000);
	if (ret != HAL_OK) {
		m_Status++;
	}
}
