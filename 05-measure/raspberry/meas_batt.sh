#! /usr/bin/bash
# first script test to measure battery discharge time
# version 1.0 - 16/12/22 (add command to disable unnecessary services)

echo beginning of script

# disable BLE
sudo rfkill block bluetooth

# disable LED
#echo 1 > /sys/class/leds/led0/brightness     # turn on
echo 0 > /sys/class/leds/led0/brightness     # turn off

# disable HDMI output
sudo /usr/bin/tvservice -o

#MYDATE=$(talkpp -t)
MYDATE=$(talkpp -s)
MYDATE=$(talkpp -f)
echo $MYDATE >> batt.txt

itr=1
BATT=$(talkpp -c B)

# value with talkpp: 3.06 ; value with scope: 3.76 (min value)
while [[ $BATT>3.05 ]];
do
	echo $itr
	BATT=$(talkpp -c B)
	echo $BATT >> batt.txt
	((itr++))
	# 1 measurement every 5 minutes 
	sleep 300
done

echo $itr >> batt.txt