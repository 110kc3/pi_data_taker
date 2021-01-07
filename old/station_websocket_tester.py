#!/bin/env python
'''
SDS011 library Copyright 2016, Frank Heuer, Germany
Server code by Kamil Choiński, Copyright 2020

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''
import sys
import signal
import http.server
import socketserver
import json


import time


pm10 = 0
pm25 = 0
port = 8000


class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # message in json to send when gotten GET request
        message = {
            "response": "successful",
        }
        self.send_response(200)

        # for later - answers with localhost:port/agent
        if self.path == '/agent':
            message = self.headers['user-agent']

        if self.path == '/data':

            humidity = 15
            temperature = 15
            pm10 = 15
            pm25 = 15

            color = "#00E400"
            description = "Test data"

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
                color = "#990000"
                description = "Hazardous air"

            message = {
                "current": {
                    "indexes": [
                        {
                            "stationcity": "Gliwice",
                            "color": color,
                            "advice": "Take a breath!",
                            "name": "AIRLY_CAQI",
                            "description": description,
                            "level": "LOW"
                        }
                    ],
                    "values": [
                        {
                            "name": "PM1",
                            "value": 0
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
                            "value": 0,
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
