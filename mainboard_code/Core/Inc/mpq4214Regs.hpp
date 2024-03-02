#pragma once

#include <stdint.h>

enum eMPQ4214AddrPins {
	VLvl1,
	VLvl2,
	VLvl3,
	VLvl4,
	NUM_MPQ4214_ADDR_PINS,
};

enum eMPQ4214Registers {
	REF_LSB,		  // R/W
	REF_MSB,		  // R/W
	Control1,		  // R/W
	Control2,		  // R/W
	ILIM,			  // R/W
	InterruptStatus,  // R/W
	InterruptMask,	  // R/W
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214VRefLsbReg {
	uint8_t VREF_L : 3;
	uint8_t unused : 5;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214VRefMsbReg {
	uint8_t VREF_H;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214Control1Reg {
	uint8_t ENPWR : 1;
	uint8_t GO_BIT : 1;
	uint8_t Reserved : 1;
	uint8_t PNG_Latch : 1;
	uint8_t Dither : 1;
	uint8_t DISCHG : 1;
	uint8_t SR : 2;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214Control2Reg {
	uint8_t OVP_MODE : 2;
	uint8_t OCP_MODE : 2;
	uint8_t BB_FSW : 1;
	uint8_t unused : 1;
	uint8_t FSW : 2;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214ILIMReg {
	uint8_t ILIM : 3;
	uint8_t unused : 5;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214InterruptStatus {
	uint8_t PNG : 1;
	uint8_t OCP : 1;
	uint8_t OVP : 1;
	uint8_t CC : 1;
	uint8_t OTP : 1;
	uint8_t unused : 3;
};

struct __attribute__((packed, aligned(sizeof(uint8_t)))) MPQ4214InterruptMask {
	uint8_t M_PNG : 1;
	uint8_t M_OCP : 1;
	uint8_t M_OVP : 1;
	uint8_t M_CC : 1;
	uint8_t M_OTP : 1;
	uint8_t unused : 3;
};
