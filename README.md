# Pi data taker
This repo is executive part of Weather station management system - API is from https://github.com/110kc3/python_weather_api
It requires connected Nova SDS011 and DHT22 (or DHT11) sensor to Raspberry Pi board.

## Instaling
Application can be set up with the usage of requirements.sh script that installs required programs, libraries 
and sets up autostart of the program at start of the Raspberry Pi.

The listening port is set up on localhost:8082 but it can be changed in station_websocket.py file.

When successfully requested data from the websocket you will get 200 response status code
with "response": "successful",

Server respons to following endpoints:
/agent
message = self.headers['user-agent']

/data
#JSON response with station data
            
			
			
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
