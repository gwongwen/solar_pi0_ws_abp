#! /usr/bin/bash
# first script test to measure baterry discharge time

echo beginning of script

#MYDATE=$(talkpp -t)
MYDATE=$(talkpp -s)
MYDATE=$(talkpp -f)
echo $MYDATE >> power_info.txt

itr=1
BATT=$(talkpp -c B)

# value with talkpp: 3.06 ; value with scope: 3.76 (min value)
while [[ $BATT>3.05 ]];
do
	echo $itr
	BATT=$(talkpp -c B)
	echo $BATT >> power_info.txt
	((itr++))
	# 1 measurement every 5 minutes 
	sleep 300
done
echo $itr >> power_info.txt