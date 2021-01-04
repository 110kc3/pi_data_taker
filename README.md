# pi_data_taker



When succesfully requested data from the websocket you will get 200 response status code
        message = {
            "response": "successul",
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