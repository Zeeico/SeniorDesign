## I^2^C Address Settings

| Lower Limit (V) | Upper Limit (V) | I^2^C Target Address       | ENPWR Default Value |
| --------------- | --------------- | -------------------------- | ------------------- |
| **0.00**        | **0.23**        | **0b110'0000 = 0x60 = 96** | 1                   |
| **0.27**        | **0.47**        | **0b110'0010 = 0x62 = 98** | 1                   |
| 0.51            | 0.68            | 0b110'0011 = 0x63 = 99     | 0                   |
| 0.74            | 6.50            | 0b110'0110 = 0x66 = 102    | 0                   |

![image-20240227221034291](C:\Users\temp\AppData\Roaming\Typora\typora-user-images\image-20240227221034291.png)

**I2C address setting for MPQ4214 DC/DC** 

| A1 Pin  | A0 Pin    | I^2^C Target Address       |
| ------- | --------- | -------------------------- |
| **GND** | **GND**   | **0b100'0000 = 0x40 = 64** |
| **GND** | **V~S+~** | **0b100'0001 = 0x41 = 65** |
| V~S+~   | GND       | 0b100'0100 = 0x44 = 68     |
| V~S+~   | V~S+~     | 0b100'0101 = 0x45 = 69     |

**I2C address setting for INA219 E-Meter** 