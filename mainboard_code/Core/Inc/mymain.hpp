#pragma once

#include <array>

#include "emeter.hpp"
#include "mpq4214.hpp"
#include "mymain.h"

std::array<uint32_t, 4> thermistorValues;

extern tEmeter emeter0;
extern tEmeter emeter1;
extern tEmeter emeter2;
extern tEmeter emeter3;

extern tMPQ4214 bbController0;
extern tMPQ4214 bbController1;
extern tMPQ4214 bbController2;
extern tMPQ4214 bbController3;
