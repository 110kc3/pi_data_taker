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

sudo apt-get install python3-pip -y


pip3 --version


# python modules

pip3 install pyserial Adafruit_DHT