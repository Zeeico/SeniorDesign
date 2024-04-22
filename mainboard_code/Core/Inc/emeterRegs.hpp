#pragma once
#include <stdint.h>

enum eEmeterAddrPins {
	GND,
	VS,
	SDA,
	SCL,
	NUM_EMETER_ADDR_PINS,
};

enum eEmeterRegisters {
	Configuration,	// R/W
	ShuntVoltage,	// R, probably not using it
	BusVoltage,		// R
	Power,			// R
	Current,		// R
	Calibration,	// R/W
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterConfigReg {
	uint16_t mode : 3;
	uint16_t sadc : 4;
	uint16_t badc : 4;
	uint16_t pg : 2;
	uint16_t brng : 1;
	uint16_t unused : 1;
	uint16_t reset : 1;
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterBusVoltageReg {
	uint16_t ovf : 1;
	uint16_t cnvr : 1;
	uint16_t unused : 1;
	uint16_t bd : 13;
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterPowerReg {
	uint16_t pd;
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterCurrentReg {
	uint16_t cd : 15;
	uint16_t csign : 1;
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterCalibrationReg {
	uint16_t fs;
};

struct __attribute__((packed, aligned(sizeof(uint16_t)))) emeterShuntVoltageReg {
	uint16_t sd : 14;
	uint16_t sign : 2;
};
