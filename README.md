# Reviving a Ultimate Elite II / Commodore C64 Ultimate board

The following instructions show the necessary steps to revive a bricked Ultimate Elite II (U64ii) or a Commodore C64 Ultimate (C64U). Other boards are not supported by this method or may require different firmware.

In this context, a bricked board means that incorrect or faulty firmware has been flashed onto the board. The board is either partially bricked (the FPGA starts, but the soft core RISC CPU crashes, e.g., the screen remains black) or completely bricked (no signs of life after powering on).

## Preparation
The following hardware and software are required:

### Hardware

* PC / Laptop
* FT232H-based USB JTAG programmer, e.g., Adafruit FT232H board
* FTDI USB to serial converter, e.g., FT232RL USB to TTL Serial
* 8 female-to-female jumper wires
* Philips PH2 screwdriver
* Soldering iron for the JTAG pin headers

![JTAG USB Programmer](./images/usb-jtag.JPG)

![Serial USB Board](./images/usb-serial.JPG)


### Software

* Tested only with Linux OS, e.g., Ubuntu 24.04LTS. Not tested with Windows or Mac OS.
* Development tools: git, python3, pip3.

## Installation

First, install the necessary tools.

### Software Installation

Git, Python3, and Pip3 are usually pre-installed. You can test the installation in the terminal by running:

```
python3 --version
pip3 --version
git --version
```

If anything is missing, you can install it afterward by running:

```
sudo apt install -y python3 pip3 git
```

Some Python packages are still required. However, in current Ubuntu versions, Python packages should no longer be installed globally. Instead, a virtual Python environment is set up.

To do this, we create a subfolder 'c64' and install the virtual environment within it:

```
mkdir c64 && cd c64
python3 -m venv ./myenv
```

Next, we start the virtual environment and install the necessary packages.

For the command-line version, one package is sufficient:

```
. myenv/bin/activate
pip3 install pyftdi
```

''' The final step involves detecting the FTDI adapters and accessing them as a user:

```
sudo cp ./60-openocd.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -a -G plugdev $USER
```

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

#### Serial USB

Optionally you can watch the debug output of the serial console. The USB serial adapter is fully assembled and connects to the console port on the 64U board using two jumper wires. The 3.3V pins are not connected. The 5V/3.3V jumper must be set to 3.3V.

| USB Serial | Label | 64U Console |
|------------|--------------|-------------|
| 1 | GND | GND |
| 2 | CTS# | -- |
| 3 | VCC | -- |
| 4 | TX out | -- |
| 5 | RX in | TxD |
| 6 | RTS# | |

![Serial USB Connection](./images/c64u-serial-connection.png)

## Connecting the U64 Board

Before connecting the jumper cables to the U64 board:

* Disconnect the board from power. Unplug the U64 power supply connector!. Keep in mind: Parts of the board will always under power, when the power supply connector is inserted (for example the ESP32 Wifi chip).
* Connect the jumper cables for JTAG and Serial Console and doublecheck the wiring.
* Connect the JTAG USB Programmer and USB Serial Board to free USB ports on the PC.
* Connect the U64 power supply connector.
* Turn on the U64 board. Briefly move the rocker switch upwards. It should power up the C64U and the JTAG board 

## C64U Recovery Script

The Python Virtual Environment must be enabled for these to work.

The scripts are executed from the 'c64u_recovery' folder.

```
cd c64
python3 -m venv ./myenv
cd c64u_recovery
```
The recovery.py script is used to load the FPGA bitcode and the Ultimate Application into DRAM.  The flash memory is not modified. After a power cycle, the board woud just restart with the program from the FLASH memory. The USB Serial board can be used to show Debug Output messages. To use it:

* open a second terminal
* run a serial program like minicom with 'minicom -D /dev/ttyUSB0 -b 115200' 

The recovery script is started with:

```
python3 ./recovery.py
```

## Final steps

The 64U board should start and display the BASIC prompt on the screen. Switch to the menu and do a system update by flashing the 'update.ue2' package