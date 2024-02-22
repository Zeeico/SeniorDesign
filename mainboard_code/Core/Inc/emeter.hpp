#pragma once

#include "stm32f1xx_hal.h"

enum tEmeterAddrPins {
	GND,
	VS,
	SDA,
	SCL,
	NUM_ADDR_PINS,
};

enum tEmeterRegisters {
	Configuration,	// R/W
	ShuntVoltage,	// R
	BusVoltage,		// R
	Power,			// R
	Current,		// R
	Calibration,	// R/W
};

class tEmeter {
   public:
	tEmeter(I2C_HandleTypeDef* phi2c, tEmeterAddrPins pinA0, tEmeterAddrPins pinA1);

	void WriteConfig(emeterConfigReg* reg);

	void ReadBusVoltage(emeterBusVoltageReg* reg);

	void ReadPower(emeterPowerReg* reg);

	void ReadCurrent(emeterCurrentReg* reg);

	void WriteCalibration(emeterCalibrationReg* reg);

   private:
	I2C_HandleTypeDef* m_phi2c;

	uint8_t m_address;

	static constexpr uint8_t m_baseAddress = 0b1000000;
};

struct __attribute__((packed)) emeterConfigReg {
	uint16_t mode : 3;
	uint16_t sadc : 4;
	uint16_t badc : 4;
	uint16_t pg : 4;
	uint16_t unused : 1;
	uint16_t reset : 1;
};

struct __attribute__((packed)) emeterBusVoltageReg {
	uint16_t ovf : 1;
	uint16_t cnvr : 1;
	uint16_t unused : 1;
	uint16_t bd : 13;
};

struct __attribute__((packed)) emeterPowerReg {
	uint16_t pd;
};

struct __attribute__((packed)) emeterCurrentReg {
	uint16_t cd : 15;
	uint16_t csign : 1;
};

struct __attribute__((packed)) emeterCalibrationReg {
	uint16_t fs;
};
