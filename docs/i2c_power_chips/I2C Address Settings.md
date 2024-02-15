## I^2^C Address Settings

| MODE Pin | I^2^C Target Address |
| -------- | -------------------- |
| Low      | 0x75 = 117           |
| High     | 0x74 = 116           |

**I^2^C address settings for TPS55289 HV converter**



| ADD Pin | ADD1 | ADD0 | I^2^C Target Address   |
| ------- | ---- | ---- | ---------------------- |
| VAUX    | 0    | 0    | 0b000'1000 = 0x08 = 8  |
| GND     | 0    | 1    | 0b000'1010 = 0x0A = 10 |

**I^2^C address settings for STPD01 LV converter**



| A1 Pin | A0 Pin | I^2^C Target Address   |
| ------ | ------ | ---------------------- |
| GND    | GND    | 0b100'0000 = 0x40 = 64 |
| GND    | V~S+~  | 0b100'0001 = 0x41 = 65 |
| V~S+~  | GND    | 0b100'0100 = 0x44 = 68 |
| V~S+~  | V~S+~  | 0b100'0101 = 0x45 = 69 |

**I2C address setting for INA219 E-Meter** 