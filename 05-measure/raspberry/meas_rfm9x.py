#! /usr/bin/env python3
# measurement of rfm9x chipset radio
# version 1.0 - 29/11/22
# version 1.1 - 16/12/22 (delete warning of talkpp -c B value in while loop)

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

# apply new modem config settings to the radio to improve its effective range
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
with open('batt.txt', 'a') as f:
    f.write(str(MYDATE))
    f.write('\n')

# get battery value before sending packet
arg = 'B'
BATT = float(command(arg))

# print in file
with open('batt.txt', 'a') as f:
    f.write(str(BATT))
    f.write('\n')

ITR = 1
LOW_BATT = 3

while BATT > LOW_BATT:
    # Transmit mode - Idle mode, Sleep mode, Listen mode
    rfm9x.send(bytes("Hello World!\r\n","utf-8"))
    #rfm9x.idle()
    #rfm9x.sleep()
    #rfm9x.listen()

    # get battery value before sending packet
    arg = 'B'
    BATT = command(arg)
    a_string = BATT
    for character in 'WARN: 0':
        a_string = a_string.replace(character, '')
    BATT = float(a_string)
    # print in file
    with open('batt.txt', 'a') as f:
        f.write(str(BATT))
        f.write('\n')
    ITR = ITR + 1
    # 1 measurement every xx secondes
    time.sleep(60)
    
with open('batt.txt', 'a') as f:
    f.write(str(ITR))
    f.write('\n')
