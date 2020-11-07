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
import sys
import time
from sds011 import SDS011

# Create a new sensor instance

'''
On Win, the path is one of the com ports. On Linux / Raspberry Pi
it depends. May be one of "/dev/ttyUSB..." or "/dev/ttyAMA...".
On the Pi make sure the login getty() is not using the serial interface.
Have a look at Win or Linux documentation.
Look e.g. via lsusb command for Qin Hen Electronics USB id.
'''


def printlog(level, string):
    """Change this to reflect the way logging is done."""
    sys.stderr.write("%s: %s\n" % (level, string))


debug = 0       # debug level in sds011 class module
cycles = 1      # serial read timeout in seconds, dflt 2
timeout = 1     # timeout on serial line read
# print values in mass or pieces
unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean

com_port = '/dev/ttyUSB0'


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


# simple parsing the command arguments for setting options
# Create an instance of your sensor
# options defaults: logging None, debug level 0, serial line timeout 2
# option unit_of_measure (default False) values in pcs/0.01sqf or mass ug/m3
sensor = SDS011(com_port, timeout=timeout, unit_of_measure=unit_of_measure)
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

pm10 = 0
pm25 = 0

try:
    # Example of switching the WorkState
    print("\n%d X switching between measuring and sleeping mode:" % cycles)
    print("\tMeasurement state: Read the values, on no read, wait 2 seconds and try again")
    print("\tOn read success, put the mode into sleeping mode for 5 seconds, and loop again")
    for a in range(cycles):
        print("%d time: push it into wake state" % a)
        sensor.workstate = SDS011.WorkStates.Measuring
        # Just to demonstrate. Should be 60 seconds to get qualified values.
        # The sensor needs to warm up!
        time.sleep(10)
        last = time.time()
        while True:
            last1 = time.time()
            values = sensor.get_values()
            pm10, pm25 = values
            print('pm25 and pm10: ', pm25, pm10)

            if values is not None:
                printValues(time.time() - last, values, sensor.unit_of_measure)
                break
            print("Waited %d seconds, no values read, wait 2 seconds, and try to read again" % (
                time.time() - last1))
            time.sleep(2)

        print('Final values: ', pm10, pm25)

        print('\nSetting sensor to sleep mode cuz running fan annoys me')
        sensor.workstate = SDS011.WorkStates.Sleeping
        time.sleep(5)

    # # end of test
    # print("\nSensor reset to normal")
    # sensor.reset()
    # sensor = None
    print('Final values: ', pm10, pm25)

    # sensor.workstate = SDS011.WorkStates.Sleeping #sensor is already sleeping after last iteration

except KeyboardInterrupt:
    sensor.reset()
    sensor = None
    sys.exit("Sensor reset due to a KeyboardInterrupt")

print("Finished test")
