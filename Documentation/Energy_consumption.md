# uBike module power consumption
## Power Supply
To provide electricity to every module, we are currently using a Huawei branded Modem power supply, which suplies 12 volts at 1.5 amperes (maximum 18 watt per hour)

The current must be divided in 2 ways, one will pass through a Step-Down module, to lower the voltage that will reach the module, the other shall get cut at the Relay module, which will only keep that current going when the main module send the signal to the relay module.
## ESP32 Energy consumption and power output
The ESP32 DevKit ofers up to 3.3 volts at 40 mAmps (20 recomended) per gpio Pin
## Energy consumption sheet
- Led (Single) = 47 mAmps at 3.3 volts (Without resistor) = 150 mOhms
- RGB Led (White) = 80 mApms divided in 3 pins at 3.3 volts
- RGB Led (White, 16 ohm Resistor added) = 30 mAmps divided in 3 pins at 3.3 volts
- Buzzer = 15 mApms at 3.3 volts = 50 mOhms
- RC522 = 6 mAmps at 3.3 volts (On standby)
- Relay = 1.5 mAmp at 3.3 volt (On standby)
## Single Module consumption
A single module in neutral state (Waiting for a keychain) needs at least 200 mAmps to work correctly.
## Solenoid device consumption
The device that is used to lock the bikes uses almost the whole capacity of the power supply, hence, the resistance of the solenoid is 8 ohms, because of that, the circuit board of the module must contain electrolytic Capacitors, to hold the power while the solenoid circuit is closed.
- The solenoid doesn't need to be powered for more than half a second, that time is just enough to unlock the bike.

## Conclusion
The power supply we are currently using is enough to power multiple modules at once, however we will focus in make a single one working from it.