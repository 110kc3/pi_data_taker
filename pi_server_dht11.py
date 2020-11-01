#!/bin/env python
import sys
import signal
import http.server
import socketserver
import json

# import RPi.GPIO as GPIO
import Adafruit_DHT
import time

# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

# The pin which is connected with the sensor will be declared here
GPIO_Pin = 27  # look at output of "python3 pinout" command


def get_DHT11(self):
    humidity, temperature = Adafruit_DHT.read(DHTSensor, GPIO_Pin)
    if humidity is not None and temperature is not None:
        print("Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(
            temperature, humidity))
        return humidity, temperature
    else:
        print("Sensor failure...")


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

            humidity, temperature = get_DHT11()  # unpacking tuple
            print(humidity, temperature)

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
                            "value": 17.45
                        },
                        {
                            "value": 27.55,
                            "name": "PM25"
                        },
                        {
                            "value": 42.95,
                            "name": "PM10"
                        },
                        {
                            "value": 1016.45,
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

# Now loop forever
try:
    while True:
        sys.stdout.flush()
        server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
