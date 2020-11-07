#!/bin/env python
import sys
import signal
import http.server
import socketserver
import json

# NOVA sensor
from sds011 import SDS011


# import RPi.GPIO as GPIO - DHT11
import Adafruit_DHT
import time


# DTH11 SENSOR
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

# The pin which is connected with the dht11 sensor will be declared here
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

#############################################


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


pm10 = 0
pm25 = 0


class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # message in json to send when gotten GET request
        message = {
            "name": "John",
            "age": 30,
            "married": True,
            "divorced": False,
            "children": ("Ann", "Billy"),
            "pets": None,
            "cars": [
                {"model": "BMW 230", "mpg": 27.5},
                {"model": "Ford Edge", "mpg": 24.1}
            ]
        }
        self.send_response(200)

        # for later - answers with localhost:port/agent
        if self.path == '/agent':
            message = self.headers['user-agent']

        if self.path == '/data':
            # simple parsing the command arguments for setting options
            # Create an instance of your sensor
            # options defaults: logging None, debug level 0, serial line timeout 2
            # option unit_of_measure (default False) values in pcs/0.01sqf or mass ug/m3
            sensor = SDS011(com_port, timeout=timeout,
                            unit_of_measure=unit_of_measure)
            # raise KeyboardInterrupt
            # Now we have some details about it
            print("SDS011 sensor info:")
            print("Device ID: ", sensor.device_id)
            print("Device firmware: ", sensor.firmware)
            print("Current device cycle (0 is permanent on): ", sensor.dutycycle)
            print(sensor.workstate)
            print(sensor.reportmode)

            try:
                # Example of switching the WorkState
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
                    time.sleep(10)
                    last = time.time()
                    while True:
                        last1 = time.time()
                        values = sensor.get_values()
                        pm10, pm25 = values
                        print('pm25 and pm10: ', pm25, pm10)

                        if values is not None:
                            printValues(time.time() - last, values,
                                        sensor.unit_of_measure)
                            break
                        print("Waited %d seconds, no values read, wait 2 seconds, and try to read again" % (
                            time.time() - last1))
                        time.sleep(2)

                    print('pm25 and pm10: ', pm25, pm10)

                    print('\nSetting sensor to sleep mode cuz running fan annoys me')
                    sensor.workstate = SDS011.WorkStates.Sleeping
                    time.sleep(0.5)

                # # end of test
                # print("\nSensor reset to normal")
                # sensor.reset()
                # sensor = None
                print('pm25 and pm10: ', pm25, pm10)

                # sensor.workstate = SDS011.WorkStates.Sleeping #sensor is already sleeping after last iteration
            except KeyboardInterrupt:
                sensor.reset()
                sensor = None
                sys.exit("Nova Sensor reset due to a KeyboardInterrupt")

            humidity, temperature = get_DHT11()  # unpacking tuple
            print('Humidity and temp:', humidity, temperature)

            color = "#00E400"
            description = "Good"

            if pm25 >= 0 and pm25 <= 37:
                color = "#00E400"
                description = "Good air"

            if pm25 > 37 and pm25 <= 61:
                color = "#FFFF00"
                description = "Moderate air"

            if pm25 > 61 and pm25 <= 85:
                color = "#FF7E00"
                description = "Unhealthy air for Sensitive Groups"

            if pm25 > 85 and pm25 <= 121:
                color = "#ff3300"
                description = "Unhealthy air"

            if pm25 > 121 and pm25 <= 200:
                color = "#ff0000"
                description = "Very Unhealthy air"

            if pm25 > 200:
                color = "#00E400"
                description = "Hazardous air"

            # good = pm10 in range(0, 50)
            # if good is true:
            #     color = "#00E400"
            #     description = "Good"

            message = {
                "current": {
                    "indexes": [
                        {
                            "stationcity": "Gliwice",
                            "color": "#D1CF1E",
                            "advice": "Take a breath!",
                            "name": "AIRLY_CAQI",
                            "description": "Air is quite good.",
                            "level": "LOW"
                        }
                    ],
                    "values": [
                        {
                            "name": "PM1",
                            "value": 10
                        },
                        {
                            "value": pm25,
                            "name": "PM25"
                        },
                        {
                            "value": pm10,
                            "name": "PM10"
                        },
                        {
                            "value": 1000,
                            "name": "PRESSURE"
                        },
                        {
                            "value": humidity,
                            "name": "HUMIDITY"
                        },
                        {
                            "value": temperature,
                            "name": "TEMPERATURE"
                        }
                    ]
                }
            }

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # self.wfile.write(bytes(message, "utf8"))

        json_string = bytes(json.dumps(message), 'utf-8')

        self.wfile.write(json_string)

        return


# Reading portnumber from command line
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8082

# Note ForkingTCPServer does not work on Windows as the os.fork()
# function is not available on that OS. Instead we must use the
# subprocess server to handle multiple requests
server = socketserver.ThreadingTCPServer(
    ('', port), MyHandler)

# http.server.SimpleHTTPRequestHandler gives access to files on the server (in the folder)

# Ensures that Ctrl-C cleanly kills all spawned threads
server.daemon_threads = True
# Quicker rebinding
server.allow_reuse_address = True

# A custom signal handle to allow us to Ctrl-C out of the process


def signal_handler(signal, frame):
    print('Exiting http server (Ctrl+C pressed)')
    try:
        if(server):
            server.server_close()
    finally:
        sys.exit(0)


# Install the keyboard interrupt handler
signal.signal(signal.SIGINT, signal_handler)

print('Server started at:', server, port)

# Now loop forever
try:
    while True:
        sys.stdout.flush()
        server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
