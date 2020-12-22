#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Copyright 2016, Frank Heuer, Germany
test.py is demonstrating some capabilities of the SDS011 module.
If you run this using your Nova Fitness Sensor SDS011 and
do not get any error (one warning will be ok) all is fine.

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''
import Adafruit_DHT
import sys
import time
from sds011 import SDS011
import csv
import requests

from datetime import datetime
import json


'''
On Win, the path is one of the com ports. On Linux / Raspberry Pi
it depends. May be one of "/dev/ttyUSB..." or "/dev/ttyAMA...".
On the Pi make sure the login getty() is not using the serial interface.
Have a look at Win or Linux documentation.
Look e.g. via lsusb command for Qin Hen Electronics USB id.
'''

# import RPi.GPIO as GPIO


# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT11Sensor = Adafruit_DHT.DHT11

# The pin which is connected with the sensor will be declared here
GPIO_DHT11_Pin = 27  # look at output of "python3 pinout" command


# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT22Sensor = Adafruit_DHT.DHT22

# The pin which is connected with the sensor will be declared here
GPIO_DHT22_Pin = 22  # look at output of "python3 pinout" command


def get_DHT11():
    humidity11, temperature11 = Adafruit_DHT.read(DHT11Sensor, GPIO_DHT11_Pin)
    if humidity11 is not None and temperature11 is not None:
        print("DHT11 Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature11, humidity11))
        time.sleep(0.3)
        return humidity11, temperature11
    else:
        print("Sensor failure...")


def get_DHT22():
    humidity22, temperature22 = Adafruit_DHT.read(DHT22Sensor, GPIO_DHT22_Pin)
    if humidity22 is not None and temperature is not None:
        print("DHT22 Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature22, humidity22))
        time.sleep(0.3)
        return humidity22, temperature22
    else:
        print("Sensor failure...")


pm10 = 0
pm25 = 0
time_before_measurement = 0
time_between_measurements = 0


measurements_rate = 6


pub_temperature = 0
pub_humidity = 0
pub_pm2_5 = 0
pub_pm10 = 0
humidity11 = 0
temperature11 = 0
humidity22 = 0
temperature22 = 0
with open('temperature_measures_file.csv', mode='w') as measures_file:
    measures_writer = csv.writer(
        measures_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    measures_writer.writerow(['Time now', 'Time between measurements [s]', 'DTH11 temperature [°C] ',
                              'DTH11 humidity [%]', 'DTH22 temperature [°C] ', 'DTH22 humidity [%]'])

    for x in range(measurements_rate):

        time_before_measurement = 0.5
        time_between_measurements = 1

        if x == 1:
            time_before_measurement = 5

        if x == 4:
            time_before_measurement = 2.5
            time_between_measurements = 10
        if x == 5:
            time_before_measurement = 1
            time_between_measurements = 1

        try:

            for a in range(cycles):

                while True:

                    # get DHT22
                    try:
                        humidity22, temperature22 = get_DHT22()  # unpacking tuple
                    except:
                        print(
                            "An exception occurred with reading humidity and temperature with DHT22")
                        humidity22 = 0
                        temperature22 = 0
                    # get DHT11
                    try:
                        humidity11, temperature11 = get_DHT11()  # unpacking tuple

                    except:
                        print(
                            "An exception occurred with reading humidity and temperature with DHT11")
                        humidity11 = 0
                        temperature11 = 0

                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                    measures_writer.writerow(
                        [dt_string, time_before_measurement, temperature11, humidity11, temperature22, humidity22])

                    break

                print("Read was succesfull. Going to sleep for {} seconds".format(
                    time_between_measurements))

                time.sleep(time_between_measurements)

        # sensor.workstate = SDS011.WorkStates.Sleeping

        except KeyboardInterrupt:

            sys.exit("Sensor reset due to a KeyboardInterrupt")

print("Finished test")
