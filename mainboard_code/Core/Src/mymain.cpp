#include "mymain.h"

#include "emeter.hpp"
#include "mymain_cpp.h"

int mymain() {
	//! Final setup not handled by cubemx generated code
	HAL_ADC_Start_DMA(&hadc1, reinterpret_cast<uint32_t*>(thermistorValues.data()), thermistorValues.size());

	tEmeter emeter0(&hi2c1, tEmeterAddrPins::GND, tEmeterAddrPins::GND);
	tEmeter emeter1(&hi2c1, tEmeterAddrPins::GND, tEmeterAddrPins::VS);

	tEmeter emeter2(&hi2c2, tEmeterAddrPins::GND, tEmeterAddrPins::GND);
	tEmeter emeter3(&hi2c2, tEmeterAddrPins::GND, tEmeterAddrPins::VS);

	while (1) {
	}
}