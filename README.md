# Reviving a Ultimate Elite II / Commodore C64 Ultimate board

The following instructions show the necessary steps to revive a bricked Ultimate Elite II (U64ii) or a Commodore C64 Ultimate (C64U). Other boards are not supported by this method or may require different firmware.

In this context, a bricked board means that incorrect or faulty firmware has been flashed onto the board. The board is either partially bricked (the FPGA starts, but the soft core RISC CPU crashes, e.g., the screen remains black) or completely bricked (no signs of life after powering on).

## Preparation
The following hardware and software are required:

### Hardware

* PC / Laptop
* FT232H-based USB JTAG programmer, e.g., Adafruit FT232H board
* 8 female-to-female jumper wires
* Philips PH2 screwdriver
* Soldering iron for the JTAG pin headers

![JTAG USB Programmer](./images/usb-jtag.JPG)

### Software Installation

#### Linux
1. open terminal.
2. run `./install.sh`
3. attach USB JTAG device

#### Windows
1. run `install.bat` 
2. Download [Zadig](https://zadig.akeo.ie/) and change driver for FT232H to `libusb-win32` oder `WinUSB` 

#### macOS
1. Install libusb with Homebrew: `brew install libusb`
2. execute `./install.sh`


### Hardware Installation

The hardware requires some preparation and careful wiring. Errors can damage the board.

#### JTAG USB

The USB JTAG adapter comes with pin headers that must be soldered on.

The connection between the USB JTAG adapter and the 64U board is made via the JTAG port P5 using 5 jumper wires. The 3.3V pins should only be connected, when you programmer has an target voltage detection input. The Adafruit FT232 programmer does not have this input.

![JTAG Pinout](./images/jtag-pinout.png)


| USB JTAG | Label | 64U P5 Pin |
|----------|-------------|-------------|
| AD0 | TCK | 1 |
| AD1 | TDI | 9 |
| AD2 | TDO | 3 |
| AD3 | TMS | 5 |
| GND | GND | 2/10 |

![JTAG USB Connection](./images/c64u-jtag-connection.png)

## Connecting the U64 Board

Before connecting the jumper cables to the U64 board:

* Disconnect the board from power. Unplug the U64 power supply connector!. Keep in mind: Parts of the board will always under power, when the power supply connector is inserted (for example the ESP32 Wifi chip).
* Connect the jumper cables for JTAG and Serial Console and doublecheck the wiring.
* Connect the JTAG USB Programmer and USB Serial Board to free USB ports on the PC.
* Connect the U64 power supply connector.
* Turn on the U64 board. Briefly move the rocker switch upwards. It should power up the C64U and the JTAG board 

## Start Recovery Script

Use the starter script for your platform:
- **Linux/macOS:** `./run.sh`
- **Windows:** `run.bat`

The recovery.py script is used to load the FPGA bitcode and the Ultimate Application into DRAM.  The flash memory is not modified. After a power cycle, the board woud just restart with the program from the FLASH memory. 

## Final steps

The 64U board should start and display the BASIC prompt on the screen. Switch to the menu and do a system update by flashing the 'update.ue2' package