import time
from datetime import datetime
from SDS011_library import *
import aqi

sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)


def get_data(n=3):
    sensor.sleep(sleep=False)
    pmt_2_5 = 0
    pmt_10 = 0
    time.sleep(10)
    for i in range(n):
        x = sensor.query()
        pmt_2_5 = pmt_2_5 + x[0]
        pmt_10 = pmt_10 + x[1]
        time.sleep(2)
    pmt_2_5 = round(pmt_2_5/n, 1)
    pmt_10 = round(pmt_10/n, 1)
    sensor.sleep(sleep=True)
    time.sleep(2)
    return pmt_2_5, pmt_10


def conv_aqi(pmt_2_5, pmt_10):
    aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
    aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
    return aqi_2_5, aqi_10


def save_log():
    with open("/home/pi/air_quality.csv", "a") as log:
        date_time_now = datetime.now()
        log.write("{},{},{},{},{}\n".format(date_time_now,
                                            pmt_2_5, aqi_2_5,       pmt_10, aqi_10))
        log.close()


def save_log_txt():
    with open("/home/pi/air_quality.log", "a") as log:
        date_time_now = datetime.now()
        log.write("{},{},{},{},{}\n".format(date_time_now,
                                            pmt_2_5, aqi_2_5,       pmt_10, aqi_10))
        log.close()


while(True):
    pmt_2_5, pmt_10 = get_data()
    aqi_2_5, aqi_10 = conv_aqi(pmt_2_5, pmt_10)
    print(pmt_2_5, type(pmt_2_5))
    print(aqi_2_5, type(aqi_2_5))
    try:
        print('saving log...')
        save_log_txt()
    except:
        print("[INFO] Failure in logging data")
    time.sleep(60)
