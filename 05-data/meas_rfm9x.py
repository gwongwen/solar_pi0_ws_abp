#! /usr/bin/env python3
# measurement of rfm9x chipset radio
# version 1.0 - 29/11/22

import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

# import the RFM9x radio module.
import adafruit_rfm9x

# create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# attempt to set up the RFM9x Module
try: 
    # initialize RFM radio
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.1)
    display.text('RFM9x: Detected', 0, 0, 1)
except RuntimeError as error:
     # thrown on version mismatch
    print('RFM9x Error: ', error)

# Apply new modem config settings to the radio to improve its effective range
rfm9x.signal_bandwidth = 62500
rfm9x.coding_rate = 4/5
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True
rfm9x.tx_power = 17

while True:
    # send a packet
    rfm9x.send(bytes("Hello World!\r\n","utf-8"))
    time.sleep(0.1)