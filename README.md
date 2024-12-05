<p align="center">
<img src="Logo/Logo_PurrPleaserS.png" width=50% height=50%>
</p>

# PurrPleaser3000 Single

This is the PurrPleaser 3000S, an automatic cat feeder for a single cat. With this cat feeder you’ve got a complete project to build your own feeder which automatically dispenses food for your cat over weeks. Further it is fully configurable via Home Assistant, to for example change feeding times, feeding amounts, give treats etc. Further, this project contains everything you needs, if you have basic electronics + Arduino knowledge and a 3D-printer at hand. This is actually the fifths iteration of my cat feeder build, but the first one I publish – so it has been tested and improved over the years. 
Further details and guidance can be found at: climbing-engineer


## Multiple Cats

This project has originally started as a dual feeder for two cat; unfortunately one of my cats has passed – so it is a single feeder now. Nevertheless, the code is flexible and actually still optimized for multiple cats and can be adapted accordingly. Also the repo with an example for two cats still exist, although it is not updated anymore: https://github.com/Poing3000/PurrPleaser3000

## Usage

  1. Build your cat feeder. You can use the 3D Files here (also on: LINK) and the schematics to build your driver board our use the provided design to let it manufacture. Further info at: climbing-engineer
  2. Download all external dependencies via the Arduino library manager.
  3. Download this repository  / folder FP3000_PicoW (LINK!).
  4. Open FP3000_PicoW.ino  in the FP3000_PicoW folder.
  5. Change the settings in Credentials.h and PP3000S_Config.h according to your needs.
  6. IMPORTANT,  allow Flash to be used for LittleFS (Go to Tools -> Flash Size -> FS: 64kb)!
  7. Flash your Raspberry Pico W.
  8. Run it / let it be detected buy your home assistant (will be integrated automatically).
  9. Configure your home assistant, e.g. build a Dashboard like this: LINK!
  10. Configure your Feeder via Home Assistant (Calibrate the scale, set your schedule..).
  11. Enjoy – See Home Assistant / Interface below.

## Software

> [!NOTE]
> This code (C++) is written to run on a Raspberry Pico W.

> [!NOTE]
> At the moment the feeder uses Home Assistant as an interface. It is easily possible to extent the code to implement a website or so; however, I don’t need it at the moment – feel free to implement changes that suit your needs.

### External Dependencies (Libraries)
You will need to download and install the following external Arduino libraries:

| Name | Link | Version Tested |
| --- | --- | --- |
| TimeZone.h 	  | https://github.com/JChristensen/Timezone  | 1.2.4 |
| ArduinoHA.h  | https://github.com/dawidchyrzynski/arduino-home-assistant  | 2.1.0 |
| Arduino_DebugUtils.h | https://github.com/arduino-libraries/Arduino_DebugUtils | 1.4.0 |
| MCP23017.h | https://github.com/wollewald/MCP23017_WE/tree/master | 1.6.8 |
| TMCStepper.h | https://github.com/teemuatlut/TMCStepper | 0.7.3 |
| HX711.h | https://github.com/RobTillaart/HX711 | 0.5.2 |

### How this code works

First of all, I am not a professional, nor am I really good at coding; however, it works and I tried my best in my free time. In case you’ve got improvements / suggestions, please feel free to implement them.

> [!NOTE]
> At first you should note that this code has been specifically written for the Raspberry Pico W. It further uses both cores of the RP2040, whereat at communication, WiFi, scheduling etc. runs on Core 0 and all hardware (sensors, drivers, motors) linked functionalities run on Core 1.

The main parts you should be interested in when reading this are:

+ **PP3000S_PicoW.ino** 
    
    This is the main Arduino sketch, which should give you an idea how the feeder basically works and what dependencies it uses. However, in case you don’t want to change any functionality this should stay as it is.


+ **PP3000S_Config.h**

    This is the configuration file, which allows to change fundamental settings to your needs. Some things are that you certainly want to change, e.g. your cat name. But there are also further settings mostly tailored to the given design, so if you don’t want to change it, most settings can be left as is (e.g. connections to the pico board pins, motor driver settings etc.).

+ **Credentials.h**

    This is your secrets file, it lets you change your wifi settings etc. and helps you keep them secret for example in case you are uploading your code on your on github etc. (https://arduino.stackexchange.com/questions/40411/hiding-wlan-password-when-pushing-to-github).

In case you need more details or want to change things, you should have a look a the external libraries (see above) and the libraries I have created (see below).

### Internal Dependencies
The code has some generic (working with more than one cat) helper functionalities in FoodSchedule.h/.cpp and SupprtFunctions.h. These mostly extent the main .ino file and help to de-clutter the code. Then there are FP3000.h/.cpp and SpeedyStepper4Purr.h/.cpp, both belong to the heart piece of the cat feeder, the [FoodPump3000](https://github.com/Poing3000/FoodPump3000).  The food pump considers the actual working hardware of the cat feeder and can also be used on it’s own / implemented in another project. All necessary info can be found at the FoodPump3000 repository and at climbing-engineer.

## Home Assistant / Interface
Currently the feeder is designed to be used along with Home Assistant ([ArduinoHA](https://github.com/dawidchyrzynski/arduino-home-assistant)). Though, if you need another interface it should be easy to extent the code, e.g. to use an external display or to provide a webserver.

When your MQTT settings are correct in Credentials.h, the cat feeder should automatically appear in your device list without any notification (Settings > Devices & Services > MQTT > Devices > "Your Feeder Name"). This provides you the basic controls over the feeder:

1. Set individual feeding amounts (max. 4x feedings /day).
2. Autotune – This autotunes the stall detection with the TMC2209 driver for error detection (I found it not to be too important, though I've spend a lot of time on it). If you've got food in the feeder, prepare to collect a lot of dispensed food!

> [!Important]
> In any case, do autotuning once – it helps with error detection and handling!

4. Calibrate – This calibrates the scale and needs to be done the first time the scale is beeing used.
> [!Tip]
> When you press "Calibrate", you'll receive messeages, telling you what you need to do: "You've got **20 seconds to empty the scale bucket** > then the scale tares > then you've go **20 seconds to put 20g into the bucket** > the scale is calibrated.

6. Set a daily feeding amount. This overrides / sets the individual amounts and spreads the daily amount over four feedings.
7. Feeding Times (Hour + Minute). This allows to set the (max.) four feedings times at which the set amount of food will be dispensed.
8. Reset. Restarts the feeder (calibrations are saved permenently).
9. Save Schedule. Feeding amounts and time are only permenently saved if you press this button.
10. Stall Warnings – I don't really use it. It gives you a warning whenever a stall has been detected from the stepper drivers (may be sensitive).
11. Treat. Treat your cat!
12. Amount to be dispensed for a treat. Could also be used for extra manual feeding (e.g. by a Home Assistant routine).

Further, there are a few sensors that provide you dome informatiob over the feeder.
1. Days until empty. This is a rough estimate of how many days of food are left in the feeder.
> [!Tip]
> Days until empty only works if you've got the top and bottom fill sensor installed. Further you need to set the capacity yourself in PP3000S_CONFIG.h. Measure the amount: 1. when the bottom sensor is just covered (LOW_CAP) and from there 2. when the top sensor is just covered (LOW_CAP).

3. Debug tells you if there is something wrong (sensor failure, scale failure etc.).
4. Last amount that has been fed.
5. Status tells you what the feeder is currently doing (Standby, Feeding..).

> [!Note]
> In case something goes wrong the feeder will give everything to feed your cat. In case an error has been detected – e.g. scale not working -  the feeder will go into an emergency mode (no scale, increased current...) and will try to roughly dispense food at feeding times. Depending on the error type, the feeder may also be able to solve the issue on its own (freeing a stuck slider etc.).

I've created myself a dashboard that uses [Mushroom cards](https://github.com/piitaya/lovelace-mushroom). You find an example in the [Home Assistant folder](HomeAssistant).

## Hardware
### 3D Print
You will need a case, the food pump, a food silo and a scale. If you want to use my design feel free to 3D print it. If you want, you can change my design – all SolidWorks files are located in the Hardware/CAD (LINK) folder.

In case you use my design, it should be straight forward. In regard to printing, I did not use any significant settings. Most parts do not need much infill, rather do an extra loop on the walls. Tolerances may depend on your printer – tough I designed the gears to be hard to attach to the motors (once they are on, I can’t get them of without breaking. For the bigger (case) parts, I’ve used a 0.6 nozzle, though this was only to speed things up. Further I had issues with warping for the big parts (even with PLA), but it still fits / looks alright.

Materials I’ve used:
Case:	PLA
Silo:	PLA
Rest:	PETG / ABS
Optional
Seals:	TPU

### Parts to buy
**Case:**
- Filament
- Threaded inserts (I’ve used a standard set from Ruthex (M2-M5) – the short version is fine, though most holes are designed for the longer/standard ones; the outer case is better of with the short ones (M4)).
- Screws (just get yourself a set of M-Screw on Amazon etc. – they are cheap.)

**Electronics:**
*Outside*
1x 12V Power Supply (in case you want it fail safe you could e.g. use an Eaton 3S Mini UPS)

*In case*
- 2x TCRT 5000 optical sensor (silo fill sensors)
- 2x TCST2202 optical sensor (end-stop sensors)
- 2x NEMA-17 Stepper Motors (e.g.17HS08-1004S)
- 1x HX711 weighing wensor module
- 1x 500g Mini Load Cell (e.g. 500g TAL221 / SEN-14728)

*On PCB*
- 1x Raspberry Pico W
- 2x TMC2209 Stepper Driver (e.g. S2209 V4.0 form Fysetc)
-  Resistors:
 2x 10 kΩ
 1x 1 kΩ
 2x 100 Ω
- 2x 100 uF Capacitor
- 6x 4-Pin JST / XH Connectors (male + female)
- Standard Pin Headers (for raspberry, connections… get a few, they are always good to have)
- 1x Screw Terminal (e.g. DORABO DB128V-5.0-2P-OG-S)
*Optional:*
- 5x 4-Pin JST / XH Connectors (male + female) – extra GPIO (e.g. for a display)
- 9x 100 nF Capacitor  - no really needed but could be beneficial
- 6x Standard Jumpers - to easily apply board settings
- 1x Screw Terminal (e.g. DB128V-5.0-2P-GY-S) – in case you want to provide external 3.3V or source it from the board.
- 1x 3.3V Power Supply (from 12V input) – I use a separate 3.3V power supply from the one that it is on the pico, just to be on the safe side (pico: 300mA max) and to be able to add further things like a display etc. You can use e.g. a LMxx / TSR 1-2433 / D36V28F3 on board or supply the board from an external 3.3V supply. >> Don’t forget to short JEN1 if you don’t use the internal 3.3V Pico power supply. <<

Generally all CAD files and schematics should be self explaining (further info on climbing-engineer). You do not need to use my PCB design / buy a PCB, but I suggest to orientate on my schematics. Further my schematics already include some future improvements possibilities (access to GPIOs) and provide some flexibility in regard to the power supply. 
	
