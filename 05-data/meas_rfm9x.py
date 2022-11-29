#! /usr/bin/env python3
# measurement of rfm9x chipset radio
# version 1.0 - 29/11/22

import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
from talkpp_py import pp_configs, command, write2pp

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
except RuntimeError as error:
     # thrown on version mismatch
    print('RFM9x Error: ', error)

# Apply new modem config settings to the radio to improve its effective range
rfm9x.signal_bandwidth = 62500
rfm9x.coding_rate = 4/5
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True
rfm9x.tx_power = 17

# get info from Pi Platter
arg = '-s'
MYDATE = command(arg)
arg = '-f'
MYDATE = command(arg)

# print in file
file = open('power_info.txt', 'w')
print("Date of the Day" % MYDATE)
file.close()

# get battery value before sending packet
bitname = B
BATT = write2pp(bitname)
file = open('power_info.txt', 'w')
print("Battery Value =" % BATT)
file.close()

ITR = 1
while BATT > 3.05:
    # send a packet
    rfm9x.send(bytes("Hello World!\r\n","utf-8"))
    BATT = write2pp(bitname)
    file = open('power_info.txt', 'w')
    print("Battery Value =" % BATT)
    itr = itr + 1
    file.close()
    # 1 measurement every 5 minutes
    time.sleep(300)

file = open('power_info.txt', 'w')
print("Number of Iteration = " % ITR)
file.close()