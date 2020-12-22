#import RPi.GPIO as GPIO
import Adafruit_DHT
import time

# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

# The pin which is connected with the sensor will be declared here
GPIO_Pin = 27  # look at output of "python3 pinout" command

while True:
    humidity, temperature = Adafruit_DHT.read(DHTSensor, GPIO_Pin)
    if humidity is not None and temperature is not None:
        print("Temperature={}C  Humidity={}%".format(temperature, humidity))
    else:
        print("Sensor failure...")
    time.sleep(3)
