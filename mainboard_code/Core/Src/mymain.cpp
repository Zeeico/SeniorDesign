#include "mymain.h"

#include "mymain_cpp.h"

int mymain() {
	//! Final setup not handled by cubemx generated code
	HAL_ADC_Start_DMA(&hadc1, reinterpret_cast<uint32_t*>(thermistorValues.data()), thermistorValues.size());

	for (uint32_t& val : thermistorValues) {
		val++;
	}

	int k = 0;
	for (int i = 0; i < 4; i++) {
		k += *(thermistorValues.data() + i);
	}

	if (k == 0) {
		k = -1;
	} else {
		k = 2;
	}

	while (1) {
	}
}