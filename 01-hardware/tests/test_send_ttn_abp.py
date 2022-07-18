#! /usr/bin/env python3
# test: send random data  to LoRaWAN TTN by ABP identification
# version 1.0 - 23/11/21
# version 1.1 - 14/12/21 (simplified coded in order to sent only bytes to TTN application)
# version 1.2 - 18/07/22 (add RfM93  modem comfig for meausremennts)

import board, busio, time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# init TTN application and device
devaddr = [0x26, 0x01, 0x3D, 0x54]
nwkey = [0x0F, 0xFE, 0xDF, 0x1D, 0x36, 0x6D, 0x51, 0x89, 0x76, 0xD7, 0x76, 0xBB, 0x92, 0xA5, 0x9A, 0xE9]
app = [ 0x4A, 0xD7, 0xB6, 0x3F, 0x86, 0xAB, 0xC7, 0x54, 0xCF, 0x26, 0x8E, 0xE5, 0x60, 0xDE, 0x1C, 0x99]

# TinyLoRa configuration (RFM9x)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D22)
rst = DigitalInOut(board.D25)

# initialize ThingsNetwork configuration
ttn_config = TTN(devaddr, nwkey, app, country="EU")

# initialize lora object
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# initialize RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, rst, 868.0)

# Apply new modem config settings to the radio to improve its effective range
#rfm9x.signal_bandwidth = 62500
rfm9x.coding_rate = 6
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True

for meas in range (0, 5, 1):
    data = bytearray(b"\x43\x57\x54\x46")
    print("Sending packet...")
    lora.send_data(data, len(data), lora.frame_counter)
    lora.frame_counter +=1
    print("Packet sent!")

    time.sleep(5)