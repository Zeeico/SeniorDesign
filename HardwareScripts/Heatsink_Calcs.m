%2024 Senior Design Heatsink Calculations

% Establish constants 
Max_T=60; %Celsius -Maximum desired temperature of chip
Ambient_Temperature=30; %Celsius 
DCDC_Power=2/4; %W -Max heat power
hc=5.5; %W/(m^2*K) -natural air convection coefficient (Air, free) 
Junction_Case_R = 3.1; %C/W - from Infineon switch datasheet

%Given power, temp difference, we can calculate the
%theoretical max value of Max_Required_Thermal_Res that allows the resistor to stay below max
%temp.

%Formula: (T_resistor - T_air) / Precharge_Power = Thermal Resistance between chip and air

%Max thermal resistance of heatsink that prevents resistor from overheating
Max_Required_Thermal_Res = ((Max_T - Ambient_Temperature) / DCDC_Power)  %C/W


%Thermal resistance of no heatsink
No_Heatsink_R = 60      %C/W - from datasheet

%Calculate Maximum Temp with Chosen Heatsink
Chosen_Heatsink_R = 20 %C/W
syms T
Eqn1=(T-Ambient_Temperature)==DCDC_Power*(Chosen_Heatsink_R + Junction_Case_R);
DCDC_Temp=vpasolve(Eqn1, T)    %C