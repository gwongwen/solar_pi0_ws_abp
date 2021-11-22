#! /usr/bin/env python3
# test: send physical data from sensor to LoRaWAN TTN by ABP identification
# version 1.0 - 19/11/21

import sys,adafruit_ssd1306,adafruit_bmp3xx,board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
sys.path.insert(0, '/home/pi/solar_pi0_ws_otaa/01-hardware/SX127x')
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
sys.path.insert(0, '/home/pi/solar_pi0_ws_otaa/04-lorawan')
from LoRaWAN.MHDR import MHDR
from random import randrange

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANsend(LoRa):
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose = False):
        super(LoRaWANsend, self).__init__(verbose)
        self.devaddr = devaddr
        self.nwkey = nwkey
        self.appkey = appkey

    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")
        sys.exit(0)

    def start(self):
        lorawan = LoRaWAN.new(nwskey, appskey)
        lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': 1, 'data': list(map(ord, 'Python rules!')) })

        self.write_payload(lorawan.to_raw())
        self.set_mode(MODE.TX)
        while True:
            sleep(1)

def getPayloadMockBMP388():
    press_val = bmp.pressure
    temp_val = bmp.temperature + temperature_offset
    alt_val = bmp.altitude
    return encodePayload(press_val,temp_val,alt_val)

def encodePayload(pressure,temperature,altitude):
    # encode float as int
    press_val = int(pressure * 100) 
    temp_val = int(temperature * 100)
    alt_val = int(altitude * 100)
    abs_temp_val = abs(temp_val)

    # encode payload as bytes
    # pressure (needs 3 bytes)
    data[0] = (press_val >> 16) & 0xff
    data[1] = (press_val >> 8) & 0xff
    data[2] = press_val & 0xff

    # temperature (needs 3 bytes 327.67 max value) (signed int)
    if(temp_val < 0):
        data[3] = 1 & 0xff
    else:
        data[3] = 0 & 0xff
    data[4] = (abs_temp_val >> 8) & 0xff
    data[5] = abs_temp_val & 0xff

    # altitude (needs 3 bytes)
    data[6] = (alt_val >> 16) & 0xff
    data[7] = (alt_val >> 8) & 0xff
    data[8] = alt_val & 0xff

    return data

def sendDataTTN(data):
    lora.send_data(data, len(data), lora.frame_counter)
    lora.frame_counter += 1
    display.fill(0)
    display.text('Packet sent', 10, 0, 1)
    display.show()

# init
devaddr = [0x26, 0x01, 0x3D, 0x54]
nwskey = [0x0F, 0xFE, 0xDF, 0x1D, 0x36, 0x6D, 0x51, 0x89, 0x76, 0xD7, 0x76, 0xBB, 0x92, 0xA5, 0x9A, 0xE9]
appskey = [ 0x4A, 0xD7, 0xB6, 0x3F, 0x86, 0xAB, 0xC7, 0x54, 0xCF, 0x26, 0x8E, 0xE5, 0x60, 0xDE, 0x1C, 0x99]
lora = LoRaWANsend(False)

# setup
lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([1,0,0,0,0,0])
lora.set_freq(868.1)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(7)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

# create the i2c interface
i2c = board.I2C()   # uses board.SCL and board.SDA
 
# 128x32 OLED display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25
bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1
temperature_offset = -5

# link buttons
btnA = DigitalInOut(board.D5) # button A
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
btnB = DigitalInOut(board.D6) # button B
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
btnC = DigitalInOut(board.D12) # button C
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    print("Sending LoRaWAN message\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

# 2b array to store sensor data
data = bytearray(9)

for meas in range (0, 15, 1):
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('Retrieving data', 10, 0, 1)
    display.show()

    time.sleep(1)
    
    sendDataTTN(getPayloadMockBMP388())
    print("packet sent!")

    time.sleep(2)