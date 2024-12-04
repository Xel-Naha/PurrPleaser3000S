
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


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
