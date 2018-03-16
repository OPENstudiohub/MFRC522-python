wrapper around [MFRC522-python](https://github.com/mxgxw/MFRC522-python).
currently reads RFID tags and returns their hexadecimal representation.
to use 2 SPI readers on one Pi, instantiate RFIDer(num_devices=2).
currently defaults to num_devices=1.

main.py sends the UID of the scanned RFID tag in an OSC message. it uses osc_client from
the [osc_basics repo](https://github.com/OPENstudiohub/osc_basics), which should be nested inside this repo

original MFRC522 readme follows:

#MFRC522-python
==============

A small class to interface with the NFC reader Module MFRC522 on the Raspberry Pi.

This is a Python port of the example code for the NFC module MF522-AN.

##Requirements
This code requires you to have SPI-Py installed from the following repository:
https://github.com/lthiery/SPI-Py

##Examples
This repository includes a couple of examples showing how to read, write, and dump data from a chip. They are thoroughly commented, and should be easy to understand.

## Pins
You can use [this](http://i.imgur.com/y7Fnvhq.png) image for reference.

| Name | Pin # | Pin name   |
|------|-------|------------|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | Any   | Any Ground |
| RST  | 22    | GPIO25     |
| 3.3V | 1     | 3V3        |

##Usage
Import the class by importing MFRC522 in the top of your script. For more info see the examples.
