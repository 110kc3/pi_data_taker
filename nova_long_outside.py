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
DHTSensor = Adafruit_DHT.DHT11

# The pin which is connected with the sensor will be declared here
GPIO_DHT_Pin = 27  # look at output of "python3 pinout" command


def get_DHT11():
    humidity, temperature = Adafruit_DHT.read(DHTSensor, GPIO_DHT_Pin)
    if humidity is not None and temperature is not None:
        print("Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature, humidity))
        time.sleep(0.3)
        return humidity, temperature
    else:
        print("Sensor failure...")


def printlog(level, string):
    """Change this to reflect the way logging is done."""
    sys.stderr.write("%s: %s\n" % (level, string))


debug = 0       # debug level in sds011 class module
cycles = 3      # serial read timeout in seconds, dflt 2
timeout = 2     # timeout on serial line read
# print values in mass or pieces
unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
for arg in range(len(sys.argv) - 1, 0, -1):
    if sys.argv[arg][0:2] == '-d':
        debug += 1
        debug = int(sys.argv[arg + 1])
        del sys.argv[arg + 1]
        del sys.argv[arg]
    elif sys.argv[arg][0:2] == '-c':
        cycles = int(sys.argv[arg + 1])
        del sys.argv[arg + 1]
        del sys.argv[arg]
    elif sys.argv[arg][0:2] == '-t':
        timeout = int(sys.argv[arg + 1])
        del sys.argv[arg + 1]
        del sys.argv[arg]
    elif sys.argv[arg][0:2] == '-u':
        if sys.argv[arg + 1] == '0':
            unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
        elif sys.argv[arg + 1] == '1':
            unit_of_measure = SDS011.UnitsOfMeasure.ParticelConcentrationImperial
        else:
            raise RuntimeError("%s is not a valid unit of measure")
        del sys.argv[arg + 1]
        del sys.argv[arg]
print('Argument List:', str(sys.argv))
if len(sys.argv) < 2:
    sys.exit("Usage: python test.py [-d {1..5}] [-c cnt] [-t secs] [-u 0|1] com_port [duty_cycle 0..30]\n"
             "com port e.g. /dev/ttyUSB0\n"
             "-d(ebug) debug level (dflt 0). Use 10, 14, 16, 18, 20, 30, 40, 50. Low value means verbose, 0 means off\n"
             "-c(nt) cnt defines the amount of test cycles (dflt 4).\n"
             "-t(imeout) secs defines the timeout of serial line readings (dflt 2).\n"
             "-u(nit_of_measure):\n\
             \t0: output in µg/m3 (default);\n\
             \t1: output in pcs/0.01qf (pieces per cubic feet)\n"
             "\t\tduty cycle defines sensor measurement time in minutes (dflt 2).")
if debug > 0:
    # Activate simple logging
    import logging
    import logging.handlers
    logger = logging.getLogger()
    # Available levels are the well known
    # logging.INFO, logging.WARNING and so forth.
    # Between INFO (=20)and DEBUG (=10) are fine grained
    # messages with levels 14,16 and 18. You might want
    # to use these values. Here is an Example with 16
    # logger.setLevel(16)
    # Activate simple logging
    logger.setLevel(debug)


def printValues(timing, values, unit_of_measure):
    if unit_of_measure == SDS011.UnitsOfMeasure.MassConcentrationEuropean:
        unit = 'µg/m³'
    else:
        unit = 'pcs/0.01cft'
    print("Waited %d secs\nValues measured in %s:    PM2.5  " %
          (timing, unit), values[1], ", PM10 ", values[0])
    # print("Values measured in pcs/0.01sqf: PM2.5 %d, PM10 %d" % (Mass2Con('pm25',values[1]), Mass2Con('pm10',values[0])))


# pollution_API_key = 'uickU1nHiAR1KFq8pYndm3SPLhNSZUAj'
pollution_API_key = 'aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0'

airly_api_url = 'https://airapi.airly.eu/v2/measurements/nearest?lat={}&lng={}&maxDistanceKM=50&apikey=' + pollution_API_key

city_latitude = 50.289934
city_longitude = 18.659788


# simple parsing the command arguments for setting options
# Create an instance of your sensor
# options defaults: logging None, debug level 0, serial line timeout 2
# option unit_of_measure (default False) values in pcs/0.01sqf or mass ug/m3
sensor = SDS011(sys.argv[1], timeout=timeout, unit_of_measure=unit_of_measure)
# raise KeyboardInterrupt
# Now we have some details about it
print("SDS011 sensor info:")
print("Device ID: ", sensor.device_id)
print("Device firmware: ", sensor.firmware)
print("Current device cycle (0 is permanent on): ", sensor.dutycycle)
print(sensor.workstate)
print(sensor.reportmode)

# print("\n%d measurements in permanent measuring mode" % (cycles * 2))
# print("This will make the sensor getting old. The TTL is just 8000 hours!")
# print("Do you really need to use the permanent measurering mode?")
# print("In sleep mode the fan will be turned off.")
# # Set dutycyle to nocycle (permanent)
# sensor.reset()
# for a in range(2 * cycles):
#     while True:
#         values = sensor.get_values()
#         if values is not None:
#             printValues(0, values, sensor.unit_of_measure)
#             break

sensor.reset()
pm10 = 0
pm25 = 0
time_before_measurement = 0
time_between_measurements = 0


measurements_rate = 6


pub_temperature = 0
pub_humidity = 0
pub_pm2_5 = 0
pub_pm10 = 0
humidity = 0
temperature = 0

with open('measures_file.csv', mode='w') as measures_file:
    measures_writer = csv.writer(
        measures_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    measures_writer.writerow(['Time now', 'Time before measurement [s]', 'Time between measurements [s]', 'Station temperature [°C] ', 'Station humidity [%]', 'Station pm10 [µg/m^3]',
                              'Station pm2.5 [µg/m^3]', 'Public station temperature [°C]', 'Public station humidity [%]', 'Public station pm10 [µg/m^3]', 'Public station pm2.5 [µg/m^3]'])

    for x in range(measurements_rate):

        time_before_measurement = (x+1)*2.5
        if x == 4:
            time_before_measurement = (x+1)*5
        if x == 5:
            time_before_measurement = (x+1)*10
        if x == 6:
            time_before_measurement = (x+1)*20
        time_between_measurements = 120
        try:

            print("\n%d X switching between measuring and sleeping mode:" % cycles)
            print(
                "\tMeasurement state: Read the values, on no read, wait 2 seconds and try again")
            print(
                "\tOn read success, put the mode into sleeping mode for 5 seconds, and loop again")
            for a in range(cycles):
                print("%d time: push it into wake state" % a)
                sensor.workstate = SDS011.WorkStates.Measuring
                # Just to demonstrate. Should be 60 seconds to get qualified values.
                # The sensor needs to warm up!
                time.sleep(time_before_measurement)
                last = time.time()
                while True:
                    last1 = time.time()
                    values = sensor.get_values()
                    if values is not None:
                        printValues(time.time() - last, values,
                                    sensor.unit_of_measure)
                        pm10, pm25 = values

                        r = requests.get(airly_api_url.format(
                            city_latitude, city_longitude)).json()

                        try:
                            humidity, temperature = get_DHT11()  # unpacking tuple
                            print('Humidity and temp:', humidity, temperature)
                        except:
                            print(
                                "An exception occurred with reading humidity and temperature with DHT11")
                            humidity = 55
                            temperature = 25

                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        pub_temperature = r['current']['values'][5]['value']
                        pub_humidity = r['current']['values'][4]['value']
                        pub_pm2_5 = r['current']['values'][1]['value']
                        pub_pm10 = r['current']['values'][2]['value']
                        print("Public station values read: ",
                              pub_temperature, pub_humidity, pub_pm2_5, pub_pm10)

                        measures_writer.writerow(
                            [dt_string, time_before_measurement, time_between_measurements, temperature, humidity, pm10, pm25, pub_temperature, pub_humidity, pub_pm10, pub_pm2_5, ])

                        break
                    print("Waited %d seconds, no values read, wait 0.5 seconds, and try to read again" % (
                        time.time() - last1))
                    time.sleep(0.5)
                print("Read was succesfull. Going to sleep for {} seconds".format(
                    time_between_measurements))
                sensor.workstate = SDS011.WorkStates.Sleeping
                time.sleep(time_between_measurements)

        # sensor.workstate = SDS011.WorkStates.Sleeping

        except KeyboardInterrupt:
            sensor.reset()
            sensor = None
            sys.exit("Sensor reset due to a KeyboardInterrupt")

print("Finished test")
