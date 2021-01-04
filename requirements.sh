#!/bin/sh
#######################################
# This script was created in order for the end user to have easier time installing measurement station
# Script does bellow things in order: 
# updates your Raspberry Pi software
# installs required libriaries and programs
# sets up autostart of the measurement station server
#
#
#
# be aware that in order for it to work it has to be run with root privileges - with "sudo ./requirements.sh"


#The -y tells apt-get not to prompt you and just get on with installing


#######################################

## Update packages and Upgrade system
echo '###Updating the system..'
sudo apt-get update -y

# Git #
echo '###Installing Git..'
sudo apt-get install git -y

# Python #
echo '###Installing Python3 pip..'
sudo apt-get install python3-pip -y


pip3 --version


# python modules
echo '###Installing Python3 modules pyserial and Adafruit_DHT..'
pip3 install pyserial Adafruit_DHT

# copying server file and library to /opt directory

echo '###Removing old server files ..'
sudo rm -rf /opt/pi_data_taker

echo '###Creating new server files ..'
sudo mkdir /opt/pi_data_taker
sudo mkdir /opt/pi_data_taker/logs
sudo cp -i $HOME/pi_data_taker/station_websocket.py /opt/pi_data_taker
sudo cp -i $HOME/pi_data_taker/sds011.py /opt/pi_data_taker
# changing permissions
echo '###Changing server files permissions ..'
sudo chmod 777 /opt/pi_data_taker /opt/pi_data_taker/station_websocket.py /opt/pi_data_taker/sds011.py

# adding to autostart - with solution not to allow entries to be added twice
echo '###Adding to autostart ..'
(crontab -l ; echo "@reboot nohup python3 /opt/pi_data_taker/station_websocket.py > /opt/pi_data_taker/logs/station_log.log &") | sort - | uniq - | crontab -


# restarting station
echo '###Restarting station .. server should be available at '
ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'
echo 'with port :8082'
sudo reboot