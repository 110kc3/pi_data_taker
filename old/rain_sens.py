# raindrop sensor DO connected to GPIO27
# HIGH = no rain, LOW = rain detected

from time import sleep
from gpiozero import InputDevice
 

rain = InputDevice(22)
 

 
while True:
    if not rain.is_active:
        print("It's raining - get the washing in!")
    else:
	    print("Not raining")
    sleep(1)