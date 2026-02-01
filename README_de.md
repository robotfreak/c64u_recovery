# Wiederbelebung eines Ultimate Elite II / Commodore C64 Ultimate Boards

Die folgende Anleitung zeigt die notwendigen Schritte um ein gebricktes Ultimate Elite II oder ein Commodore C64 Ultimate (C64U) Board wieder zu beleben. Andere Boards werden mit dieser Methode derzeit nicht unterstützt, bzw. brauchen andere Firmware.

Ein gebricktes Board heisst in diesem Zusammenhang, auf das Board wurde eine falsche oder fehlerhafte Firmware geflashed. Das Board ist entweder halb gebricked (FPGA startet, aber die Soft Core RISC CPU crashed, z.B. bleibt der Bildschirm schwarz) oder vollständig gebricked (keinerlei Lebenszeichen nach dem Einschalten).

## Vorbereitung
Folgende Hard bzw. Software wird benötigt

### Hardware

* PC / Laptop 
* FT232H basierter USB JTAG Programmer, z.B. Adafruit FT232H Board
* 5 Jumper Kabel weiblich/weiblich
* Philips PH2 Schraubendreher
* Lötkolben zum Anlöten der JTAG Steckverbinder

![JTAG USB Programmer](./images/usb-jtag.JPG)


### Software Installation

### Linux
1. Terminal öffnen.
2. `./install.sh` ausführen.
3. Gerät neu einstecken.

### Windows
1. `install.bat` ausführen.
2. 
3. [Zadig](https://zadig.akeo.ie/) herunterladen und den Treiber für den FT232H auf `libusb-win32` oder `WinUSB` ändern.

### macOS
1. Homebrew installieren und: `brew install libusb`
2. `./install.sh` ausführen.


### Hardware Installation

Die Hardware bedarf einiger Vorbereitung und sorgfältige Verdrahtung. Fehler können das Board beschädigen. 

#### JTAG USB

Der USB JTAG Adapter kommt mit Stiftleisten, die erst noch mit einem Lötkolben angelötet werden müsssen.

Die Anbindung zwischen USB JTAG Adapter und dem 64U board erfolgt über den JTAG Port P5 mit 5 Jumperkabel. Die 3V3 werden nur verbunden, falls der Programmer über eine Target Spannungs Detektierung verfügt. Der Adafruit FT232H JTAG Adapter hat das nicht.

![JTAG Pinout](./images/jtag-pinout.png)


| USB JTAG | Bezeichnung | 64U P5 Pin  |
|----------|-------------|-------------|
| AD0      | TCK         | 1           |              
| AD1      | TDI         | 9           |              
| AD2      | TDO         | 3           |              
| AD3      | TMS         | 5           |              
| GND      | GND         | 2/10        |   

![JTAG USB Connection](./images/c64u-jtag-connection.png)


## U64 Board anschliessen

Vor dem Anschliessen der Jumperkabel an das U64 Board:

* Board stromlos machen. C64U Stromversorgungsstecker ziehen! Achtung bei eingestecktem Stromversorgungsstecker sind schon einige Komponenten des Boards aktiv, wie z.B. der ESP32 Wifi Chip.
* Jumperkabel für JTAG und Console stecken und Verkabelung überprüfen
* JTAG USB Programmer und USB Serial Board an freien USB Ports am PC anstecken.
* C64U Stromversorgungsstecker anstecken
* C64U Board anschalten. Rocker Switch kurz nach oben

## C64U Recovery Skript

Verwende einfach den mitgelieferten Starter für deine Plattform:
- **Linux/macOS:** `./run.sh`
- **Windows:** `run.bat`
-    
Das Skript recovery.py dient zum Laden des FPGA Bitcode und Ultimate Applikation in den DRAM. Der Flash wird dabei nicht geändert. Nach einem Power Cycle würde das das Board einfach wieder das Programm aus dem Flash ausführen. 

## Letzte Schritte

Das C64U Board sollte mit dem Commodore Basic starten. 
* Öffnen sie das Ultimate Menü  
* Starten sie den Disk File Browser
* Selektieren sie das korrekte update.ue2 File
* starten sie das System Update durch Auswahl von 'Run Update'
