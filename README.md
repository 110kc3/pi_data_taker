
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [License](#license)

## General info
This repo is executive part of Weather station management system - API is from https://github.com/110kc3/python_weather_api
It requires connected Nova SDS011 and DHT22 (or DHT11) sensor to Raspberry Pi board.

## Technologies
Project is created with:
* Python version: 3
* pyserial library 
* Adafruit_DHT library 

## Setup
Application can be set up with the usage of requirements.sh script that installs required programs, libraries 
and sets up autostart of the program at start of the Raspberry Pi.

The listening port is set up on localhost:8082 but it can be changed in station_websocket.py file.

When successfully requested data from the websocket you will get 200 response status code
with "response": "successful",

The server responds to the following endpoints:
```
$ /data - JSON response with station data
$ /agent - user-agent data
```

All setup can be done with below command
```
$ sudo ./requirements.sh
```

requirements.sh script was created in order for the end user to have easier time installing measurement station
Script does bellow things in order: 
- updates your Raspberry Pi software
- installs required libriaries and programs
- sets up autostart of the measurement station server

## Components physical setup    
![image](https://user-images.githubusercontent.com/35073233/158072783-6c1a213a-f318-42a1-aea2-a9d1d541dced.png)

			
## License
SDS011 library by Frank Heuer https://gitlab.com/frankrich/sds011_particle_sensor

Copyright 2020, Kamil Choiński, Poland 

Pi data taker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
