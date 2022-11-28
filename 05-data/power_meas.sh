#! /usr/bin/bash
# first script test to measure baterry discharge time

echo beginning of script

#MYDATE=$(talkpp -t)
MYDATE=$(talkpp -s)
MYDATE=$(talkpp -f)
echo $MYDATE >> /home/rrousseau/solar_pi0_ws_abp/05-data/power_info.txt

itr=1
BATT=$(talkpp -c B)
cd /home/rrousseau/solar_pi0_ws_abp/01-hardware/tests
python3 test_rfm9x.py

# value with talkpp: 3.06 ; value with scope: 3.76 (min value)
while [[ $BATT>3.05 ]];
do
	echo $itr
	BATT=$(talkpp -c B)
	echo $BATT >> /home/rrousseau/solar_pi0_ws_abp/05-data/power_info.txt
	((itr++))
	# 1 measurement every 5 minutes 
	sleep 300
done
echo $itr >> /home/rrousseau/solar_pi0_ws_abp/05-data/power_info.txt