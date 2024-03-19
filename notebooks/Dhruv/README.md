### 2/16/24 ###

Importing components into Altium to begin layout:
    - 5V 1A LDO BD50FC0FP-E2
    - 3.3V 1A LDO AZ1117CD-3.3TRG1
    - J1031C5VDC.15S - Relay
    - 3413.0328.22 - SMD input fuse, 10A

### 2/20/24 ###

Redoing heatsink requirements for the Powerstage board, based on a new chip selected. The aim is to ensure the steady-state temperature of the switches in the DC/DC stay below the 60C threshold, for easy compliance with the FSAE rules. The theory behind the calculation is that a temperature delta can only exist across a thermal resistance. This is analogous to voltage and electrical resistance. We know the ambient temperature, required heat rejection, and the maximum operating temperature of our hardware. Using this, we can calculate the maximum allowable thermal resistance between the electronics and the air, and pick a heatsink that fulfills this requirement.

This is a conservative way of doing this math, but it offers simplicity and robustness in a subsystem that does not require hyper-optimisation. Form factor is not a high level requirement of our project.

### 2/24/24 ###

Re-did RC filter and ADC op-amp math with Akash, with the aim of maximising voltage range and resolution.

### 3/2/24 ###

- Creating schematics for the MCU subsystem PCB. Using a high accuracy voltage supply for the VDDA pin on the STM with decoupling capacitors.
- Implemented imported 5V LDO with debug LEDs.
- Fixing capacitor library details in Altium.
- Implemented relay control and logic level shifter to command the enable pin for our DC/DC control chip.

### 3/10/24 ###

- Finishing up schematics for controller board. Making engineering decision about MCU debug connection protocol - SWD vs JTAG. Decided to implement both on the board: SWD is better understood, and we have experience with it. However, JTAG has additional debugging features that could be helpful to us during the testing phase. Since implementing one does not impact the other, and we are under no physical constraints, we chose to implement both. In the event that our JTAG implementation fails, we can rest assured that we will not have to go through the tedious process of a board revision and re-manufacturing.
- Constructing BOMs for the boards, and completing purchasing requests.

