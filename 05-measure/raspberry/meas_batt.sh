#! /usr/bin/bash
# first script test to measure battery discharge time
# version 1.0 - 16/12/22 (add command to disable unnecessary services)

echo beginning of script

# enable/disable BLE
sudo rfkill block bluetooth
#sudo rfkill unblock bluetooth

# set the Pi Zero ACT LED trigger to 'none'.
echo none | sudo tee /sys/class/leds/led0/trigger

# Turn off the Pi Zero ACT LED.
echo 1 | sudo tee /sys/class/leds/led0/brightness # turn off
#echo 0 > /sys/class/leds/led0/brightness          # turn on

# disable HDMI output
sudo /usr/bin/tvservice -o
#sudo /usr/bin/tvservice -p

#MYDATE=$(talkpp -t)
MYDATE=$(talkpp -s)
MYDATE=$(talkpp -f)
echo $MYDATE >> batt.txt

itr=1
BATT=$(talkpp -c B)

# value with talkpp: 3.06 ; value with scope: 3.76 (min value)
while [ $BATT>3.05 ];
do
	echo $itr
	BATT=$(talkpp -c B)
	echo $BATT >> batt.txt
	itr=$(($itr + 1))
	# 1 measurement every 5 minutes 
	sleep 300
done

echo $itr >> batt.txt