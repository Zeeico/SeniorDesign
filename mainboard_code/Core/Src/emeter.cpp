#include "emeter.hpp"

tEmeter::tEmeter(I2C_HandleTypeDef* phi2c, tEmeterAddrPins pinA0, tEmeterAddrPins pinA1) {
	m_phi2c = phi2c;

	m_address = m_baseAddress + (pinA1 << 2) + pinA0;
}