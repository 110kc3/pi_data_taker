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
                    time.sleep(5)

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

            message = {
                "current": {
                    "indexes": [
                        {
                            "value": 45.91,
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
