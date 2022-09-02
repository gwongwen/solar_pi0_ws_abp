#!/bin/bash
#
# solar_pi0_ws install requirements
# 
# 19-10-2020 v1.0
# 26-10-2021 v1.1
# 18-11-2021 v1.2
# 21-07-2022 v1.3 

if [ "$EUID" -ne 0 ]
  then echo "Please this script needs for root authorisations, execute it as root."
  exit
  
fi

wget --spider --quiet http://google.com
if [ "$?" != 0 ]
  then echo "Not internet connection detected, may connect to internet to run this script"
  exit
fi

# raspbian repository update
sudo apt-get update

# talkpp and ppd firmwares install
sudo apt-get install libudev-dev
cd ../solar_pi0_ws_abp/02-configuration/talkpp
gcc -o talkpp talkpp.c -ludev
sudo mv talkpp /usr/local/bin
gcc -o ppd ppd.c -ludev
sudo mv ppd /usr/local/bin
cd ../..

# python install and dependencies
sudo apt-get install -y python3-pip python3-dev i2c-tools python3-smbus python3-spidev python3-setuptools
sudo pip3 install python-dotenv

# LoRa Bonnet dependencies 
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-tinylora

# BMP388 sensor dependencies
sudo pip3 install adafruit-circuitpython-bmp3xx

# activate I2C ports
echo "i2c-dev" >> /etc/modules
echo "i2c-bcm2835" >> /etc/modules
echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "dtparam=i2c1=on" >> /boot/config.txt
echo "dtparam=i2s=on" >> /boot/config.txt

# activate SPI interface
echo "dtparam=spi=on" >> /boot/config.txt

# disable BLE
echo "dtoverlay=disable-bt" >> /boot/config.txt

# disable LED
echo "dtparam=act_led_trigger=none" >> /boot/config.txt
echo "dtparam=act_led_activelow=off" >> /boot/config.txt

# disable HDMI output
echo "/usr/bin/tvservice -o" >> /etc/rc.local

sudo reboot