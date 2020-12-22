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


def get_DHT11():
    humidity11, temperature11 = Adafruit_DHT.read(DHT11Sensor, GPIO_DHT11_Pin)
    if humidity11 is not None and temperature11 is not None:
        print("DHT11 Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature11, humidity11))
        time.sleep(0.3)
        return humidity11, temperature11
    else:
        print("Sensor failure...")


# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT22Sensor = Adafruit_DHT.DHT22

# The pin which is connected with the sensor will be declared here
GPIO_DHT22_Pin = 22  # look at output of "python3 pinout" command


def get_DHT22():
    humidity22, temperature22 = Adafruit_DHT.read(DHT22Sensor, GPIO_DHT22_Pin)
    if humidity22 is not None and temperature is not None:
        print("DHT22 Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature22, humidity22))
        time.sleep(0.3)
        return humidity22, temperature22
    else:
        print("Sensor failure...")


def printlog(level, string):
    """Change this to reflect the way logging is done."""
    sys.stderr.write("%s: %s\n" % (level, string))


debug = 0       # debug level in sds011 class module
cycles = 5     # serial read timeout in seconds, dflt 2
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
    print("Waited %d secs Values measured in %s:    PM2.5  " %
          (timing, unit), values[1], ", PM10 ", values[0])
    # print("Values measured in pcs/0.01sqf: PM2.5 %d, PM10 %d" % (Mass2Con('pm25',values[1]), Mass2Con('pm10',values[0])))


# pollution_API_key = 'uickU1nHiAR1KFq8pYndm3SPLhNSZUAj'
pollution_API_key = 'aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0'

airly_api_url = 'https://airapi.airly.eu/v2/measurements/nearest?lat={}&lng={}&maxDistanceKM=50&apikey=' + pollution_API_key


# zwycięstwa 12 50.2948198207,18.6680904694
city_latitude = 50.2948198207
city_longitude = 18.6680904694


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
humidity11 = 0
temperature11 = 0
humidity22 = 0
temperature22 = 0
with open('measures_file.csv', mode='w') as measures_file:
    measures_writer = csv.writer(
        measures_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    measures_writer.writerow(['Time now', 'Time before measurement [s]', 'Time between measurements [s]', 'DTH11 temperature [°C] ', 'DTH11 humidity [%]', 'DTH22 temperature [°C] ', 'DTH22 humidity [%]',  'Station pm10 [µg/m^3]',
                              'Station pm2.5 [µg/m^3]', 'Public station temperature [°C]', 'Public station humidity [%]', 'Public station pm10 [µg/m^3]', 'Public station pm2.5 [µg/m^3]'])

    for x in range(measurements_rate):

        time_before_measurement = 2.5
        time_between_measurements = 10

        if x == 1:
            time_before_measurement = 5
        if x == 2:
            time_before_measurement = 7.5
        if x == 3:
            time_before_measurement = 10
        if x == 4:
            time_before_measurement = 2.5
            time_between_measurements = 1
        if x == 5:
            time_before_measurement = 1
            time_between_measurements = 1

        try:

            print("\n%d X switching between measuring and sleeping mode:" % cycles)
            print(
                "\tMeasurement state: Read the values, on no read, wait 2 seconds and try again")
            print(
                "\tOn read success, put the mode into sleeping mode for {} seconds, and loop again".format(time_before_measurement))
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

                        try:
                            r = requests.get(airly_api_url.format(
                                city_latitude, city_longitude)).json()
                            pub_temperature = r['current']['values'][5]['value']
                            pub_humidity = r['current']['values'][4]['value']
                            pub_pm2_5 = r['current']['values'][1]['value']
                            pub_pm10 = r['current']['values'][2]['value']
                            print("Public station values read: ",
                                  pub_temperature, pub_humidity, pub_pm2_5, pub_pm10)
                        except:
                            print("error accessing station data")
                            pub_temperature = 0
                            pub_humidity = 0
                            pub_pm2_5 = 0
                            pub_pm10 = 0

                        # get DHT11
                        try:
                            humidity11, temperature11 = get_DHT11()  # unpacking tuple

                        except:
                            print(
                                "An exception occurred with reading humidity and temperature with DHT11")
                            humidity11 = 0
                            temperature11 = 0
                        # get DHT22
                        try:
                            humidity22, temperature22 = get_DHT22()  # unpacking tuple
                        except:
                            print(
                                "An exception occurred with reading humidity and temperature with DHT22")
                            humidity22 = 0
                            temperature22 = 0

                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        measures_writer.writerow(
                            [dt_string, time_before_measurement, time_between_measurements, temperature11, humidity11, temperature22, humidity22, pm10, pm25, pub_temperature, pub_humidity, pub_pm10, pub_pm2_5, ])

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
