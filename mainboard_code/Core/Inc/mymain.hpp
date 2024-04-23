#pragma once

#include <array>

#include "emeter.hpp"
#include "mpq4214.hpp"
#include "mymain.h"

/***********************/
/* Class instantations */
/***********************/
tEmeter emeter0(&hi2c2, eEmeterAddrPins::VS, eEmeterAddrPins::GND, 0);
tEmeter emeter1(&hi2c2, eEmeterAddrPins::GND, eEmeterAddrPins::GND, 1);
tEmeter emeter2(&hi2c1, eEmeterAddrPins::GND, eEmeterAddrPins::GND, 2);
tEmeter emeter3(&hi2c1, eEmeterAddrPins::VS, eEmeterAddrPins::GND, 3);

tMPQ4214 bbController0(&hi2c2, eMPQ4214AddrPins::VLvl4, 0);
tMPQ4214 bbController1(&hi2c2, eMPQ4214AddrPins::VLvl1, 1);
tMPQ4214 bbController2(&hi2c1, eMPQ4214AddrPins::VLvl1, 2);
tMPQ4214 bbController3(&hi2c1, eMPQ4214AddrPins::VLvl4, 3);

/*************************/
/* Variable declarations */
/*************************/
std::array<uint32_t, 4> thermistorValues;
CAN_TxHeaderTypeDef emeterCanHeader;
CAN_TxHeaderTypeDef thermistorCanHeader;
CAN_TxHeaderTypeDef relayCanHeader;
uint32_t CanTxMailbox;

/*************************/
/* Function declarations */
/*************************/
//! \brief Called periodically to check if new boards are connected
void CheckBoardConnections();

//! \brief Initialise a CAN Tx Header
//! \param header The \p CAN_TxHeaderTypeDef to be initialised
//! \param id The CAN id for the header
void InitCANTxHeader(CAN_TxHeaderTypeDef *header, uint32_t id);

//! \brief Initialise the emeter chip on newly connected board
//! \param emeter Reference to the \p tEmeter class to be initialised
void InitEmeter(tEmeter &emeter);

//! \brief Initialise a new buck boost controller
//! \param controller Reference to the \p tMPQ4214 class to be initialised
void InitBBController(tMPQ4214 &controller);

//! \brief Called periodically to send read emeter data and send it over CAN
//! \param emeter Reference to the \p tEmeter class to get the data from
void SendEmeterStatus(tEmeter &emeter);

//! \brief Called periodically to send temperature information over CAN
void SendThermistorData();

//! \brief Send relay command status information over CAN
void SendRelayCmdStatus();

//! \brief Enable the output on a buck boost controller
//! \param controller Reference to the \p tMPQ4214 class to have its output enabled
void EnableOutput(tMPQ4214 &controller);

//! \brief Set a voltage output
//! \param controller Reference to the \p tMPQ4214 class to set the voltage on
//! \param millivolts The desired output voltage, in millivolts (mV)
void SetVoltage(tMPQ4214 &controller, uint16_t millivolts);

//! \brief Turn off all the relays, used when the alarm pin is triggered
void TurnOffAllRelays();
