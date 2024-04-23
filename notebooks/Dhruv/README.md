### 2/16/24 ###

Importing components into Altium to begin layout:
    - 5V 1A LDO BD50FC0FP-E2
    - 3.3V 1A LDO AZ1117CD-3.3TRG1
    - J1031C5VDC.15S - Relay
    - 3413.0328.22 - SMD input fuse, 10A

### 2/20/24 ###

Redoing heatsink requirements for the Powerstage board, based on a new chip selected. The aim is to ensure the steady-state temperature of the switches in the DC/DC stay below the 60C threshold, for easy compliance with the FSAE rules. The theory behind the calculation is that a temperature delta can only exist across a thermal resistance. This is analogous to voltage and electrical resistance. We know the ambient temperature, required heat rejection, and the maximum operating temperature of our hardware. Using this, we can calculate the maximum allowable thermal resistance between the electronics and the air, and pick a heatsink that fulfills this requirement.

This is a conservative way of doing this math, but it offers simplicity and robustness in a subsystem that does not require hyper-optimisation. Form factor is not a high level requirement of our project.

![image](https://github.com/Zeeico/SeniorDesign/assets/100447224/63d58334-a66e-4778-bbe9-2ba9d933ff57)

### 2/24/24 ###

Re-did RC filter and ADC op-amp math with Akash, with the aim of maximising voltage range and resolution.

### 3/2/24 ###

- Creating schematics for the MCU subsystem PCB. Using a high accuracy voltage supply for the VDDA pin on the STM with decoupling capacitors.
- Implemented imported 5V LDO with debug LEDs.
- Fixing capacitor library details in Altium.
- Implemented relay control and logic level shifter to command the enable pin for our DC/DC control chip.

### 3/10/24 ###

- Finishing up schematics for controller board. Making engineering decision about MCU debug connection protocol - SWD vs JTAG. Decided to implement both on the board: SWD is better understood, and we have experience with it. However, JTAG has additional debugging features that could be helpful to us during the testing phase. Since implementing one does not impact the other, and we are under no physical constraints, we chose to implement both. In the event that our JTAG implementation fails, we can rest assured that we will not have to go through the tedious process of a board revision and re-manufacturing.

![image](https://github.com/Zeeico/SeniorDesign/assets/100447224/55109738-c3fd-4175-9e05-70b942bd3fc4)

- Constructing BOMs for the boards, and completing purchasing requests.

### 3/21/24 ###

- TODO: Add pictures!

### 3/27/24 ###
- Added pictures.
- Completed individual progress report.
- Creating priority task list to ensure progress.

### 4/10/24 ###

- Creating a look up table to convert voltage readings across the thermistor on each powerstage board to a temperature value. Added as a CSV in the 'docs' folder.
- Calculations as below. Variable names follow convention from PCB schematics.
- Raw data for table taken from [datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/ntc/chip-ntc-thermistor/data_sheet/datasheet_ntcg103jx103dt1s.pdf)

![WhatsApp Image 2024-04-18 at 11 52 28 PM](https://github.com/Zeeico/SeniorDesign/assets/100447224/ba4bfcb6-f770-4736-bbfd-bf77b28d43d8)

According to our schematics, our NTC thermistor forms a voltage divider circuit across 5V with constant 10kOhm resistor (R15 in the 2nd image below).
![image](https://github.com/Zeeico/SeniorDesign/assets/100447224/29c8c47d-b51e-4983-be10-bb54628c0cd8)
![image](https://github.com/Zeeico/SeniorDesign/assets/100447224/7ef2947a-cfcb-4f58-8c88-94584f3a42e7)

After the Op-Amp filtering, the 5V value is scaled using another voltage divider to turn it into a 3V3 foltage that the STM can safely read. Applying this conversion as well, we can create a transfer function from resistance to voltage. Applying this function to the data from datasheet, we can create a lookup table for voltage to temperature conversion :).

### 4/15/24 ###

- Debugging PCBs. During testing, we managed to burn through a 3.3V LDO, consequently killing our microcontroller. We dicovered this was due to a short circuit between 3.3V, GND and 12V on the board itself.
- Our debugging steps included removing the damaged components and measuring resistance between the lines. The short was still present, so we continued removing components that spanned these nets till the short disappeared.
- After re-soldering the components and turning the board on without the microcontroller, we found the rails to be stable. Thus, we validated that out issue was most likely caused by poor soldering.

### 4/20/24 ###

- Created a python script to help create the LUT for reading thermistor values.
- Interpolated datasheet values to make the LUT easier to use.

### 4/22/24 ###

- Temperature testing with the DCDCs showed higher than expected temperatures.
- Given that our dissapation calculations erred on the conservative side, we can guess that we are simply running less efficiently than we theorised. This can be validated by reading the input power into the system, subtracting the power distributed by the LDOs, and comparing this to the output power.

![Temp_Sense](https://github.com/Zeeico/SeniorDesign/assets/100447224/7b18d2a6-9f53-4c4f-8ccf-bc8b32fdc96d)
