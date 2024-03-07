# ECE 445 Notebook - Constantin Legras

## 15/2/2024 - 21/2/2024

* Setup STM32 project in VSCode, figured out C++ compiler setup issues
* Setup Python project for the CAN controller GUI, implemented CAN communication
* Wrote setup guide for the Power Controller GUI

## 22/2/2024 - 28/2/2024

* Updated some STM32 pins to add necessary ones, such as thermistors and JTAG

  <img src="./assets/image-20240229100536302.png" alt="image-20240229100536302" style="zoom:50%;" />

* Wrote first version of a driver class for the INA219 EMeter

* Wrote first version of a driver class for the MPQ4214 buck boost converter

* Started to lay out UI for output controls in controller GUI

  <img src="./assets/image-20240229100100083.png" alt="image-20240229100100083" style="zoom:67%;" />

  <img src="./assets/image-20240229100129152.png" alt="image-20240229100129152" style="zoom:67%;" />
  

## 29/2/2024 - 6/3/2024

* Added external interrupt pins to microcontroller setup
* Wrote outline for CAN interrupt handler and EXTI interrupt handler
* Reorganized some code
* Went through MPQ4214 datasheet to determine default values for registers
* Wrote code to set those default values
