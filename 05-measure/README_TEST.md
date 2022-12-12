# Description of Solar Pi Platter Test Files
In this folder, we will find different codes in order to test battery/solar panel performance in different operating modes. In fact, we will improve a strategy of battery optimization in order to have a full autonomous node.

## talkpp_py.py
This pyhton code is a communication driver between Pi Platter board and RPi zero.

## meas_batt.sh
This shell script allows you to sent command to Pi Platter board in order to know battery level and write results in a text file (batt.txt). 

## meas_rfm9x.py
This python code allows you to test the different operating mode of the RFM95 chipset and the different configuration of Lora protcol like, spreading factor, power transmit, data rate...
