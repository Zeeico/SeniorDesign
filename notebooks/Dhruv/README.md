### 2/16/24 ###

Importing components into Altium to begin layout:
    - 5V 1A LDO BD50FC0FP-E2
    - 3.3V 1A LDO AZ1117CD-3.3TRG1
    - J1031C5VDC.15S - Relay
    - 3413.0328.22 - SMD input fuse, 10A

### 2/20/24 ###

Redoing heatsink requirements for the Powerstage board, based on a new chip selected. The aim is to ensure the steady-state temperature of the switches in the DC/DC stay below the 60C threshold, for easy compliance with the FSAE rules. The theory behind the calculation is that a temperature delta can only exist across a thermal resistance. This is analogous to voltage and electrical resistance. We know the ambient temperature, required heat rejection, and the maximum operating temperature of our hardware. Using this, we can calculate the maximum allowable thermal resistance between the electronics and the air, and pick a heatsink that fulfills this requirement.

This is a conservative way of doing this math, but it offers simplicity and robustness in a subsystem that does not require hyper-optimization. Form factor is not a high level requirement of our project.

### 2/24/24 ###

Redid RC filter and ADC op-amp math with Akash, with the aim of maximising voltage range and resolution.

