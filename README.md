# pi_data_taker
This repo is executive part of Weather station management system - API is from https://github.com/110kc3/python_weather_api




When successfully requested data from the websocket you will get 200 response status code
        message = {
            "response": "successful",
        }
        self.send_response(200)

        #answers with localhost:port/agent
        if self.path == '/agent':
            message = self.headers['user-agent']

        if self.path == '/data':
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