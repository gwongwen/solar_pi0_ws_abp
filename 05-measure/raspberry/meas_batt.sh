#! /usr/bin/bash
# first script test to measure battery discharge time
# version 1.0 - 16/12/22 (add command to disable unnecessary services)

echo beginning of script

# enable/disable BLE
sudo rfkill block bluetooth
echo bluetooth disable
#sudo rfkill unblock bluetooth

# disable HDMI output
sudo /usr/bin/tvservice -o
#sudo /usr/bin/tvservice -p

# set the Pi Zero ACT LED trigger to 'none'.
echo none | sudo tee /sys/class/leds/led0/trigger
echo Pi Zero ACT LED trigger OFF

# Turn off the Pi Zero ACT LED.
echo 1 | sudo tee /sys/class/leds/led0/brightness # turn off
echo Pi Zero ACT LED OFF
#echo 0 > /sys/class/leds/led0/brightness          # turn on

# enable/disable BLE
sudo rfkill block wifi
echo wifi disable
#sudo rfkill unblock wifi

#MYDATE=$(talkpp -t)
MYDATE=$(talkpp -s)
MYDATE=$(talkpp -f)
echo $MYDATE >> batt.txt

itr=1
while [ itr -le 200]:
do
	BATT=$(talkpp -c B)
	echo $BATT >> batt.txt
	((itr=itr+1))
	# 1 measurement every 5 minutes 
	sleep 300
done