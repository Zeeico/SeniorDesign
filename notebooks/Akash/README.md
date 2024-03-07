### 2/12/2024

We decided to mount the board at a right angle instead of laying them down flat to make the boards fit the 100 x 100 mm requirement. We also found this 4 switch DC/DC controller from TI. 

### 2/17/2024

We found this DC/DC controller from MPS. The MPQ4214GU which is a external 4 switch controller that is actually in stock. 

### 2/27/2024

Based on the sample application on the MPQ4214 datasheet, I am now calculating operating parameters. 

### 2/29/2024

![image-20240302155538364](./assets/image-20240302155538364.png)

This is the schematic for the DCDC controller IC based off of the given reference design. I still need to make sure that the operating parameters still fall within our  operating parameters.

### 3/5/2024

We didn't pass the PCBWay audit since the testpoints were broken. I fixed them after the deadline (sad). 
![image-20240307104137664](./assets/image-20240307104137664.png)

![image-20240307104401135](./assets/image-20240307104401135.png)

Finished PCB. 

There are testpoints on almost all important nets, except the temp sense. The BOM didn't export correctly due to mismatched resistors and caps. They will need to be remade.   