#!/usr/bin/env python3
import logging
import sys
import math

try:
    import grovepi
except ModuleNotFoundError:
    sys.stdout.write("Groves Sensor won't work as grovepi module is missing!\n")
except RuntimeError:
    print('Can\'t import grovepi - not running on raspberry pi?')
    # TODO disable module if we can't import this

from queue import Queue
from datetime import datetime
from time import sleep
import utils

# TODO move this into a function - we shouldn't run code on import
# Sensor Meta Data

config = utils.load_config()
set_interval = int(config["POLL_INTERVAL"])
min_interval = 10
sensor_name = "grove_temp_hum_pro"

# The Sensor goes on digital port 4.
sensor = 4
# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.


def start(queue: Queue):
    logging.info("%s started.", sensor_name)
    if set_interval > min_interval:
        interval = set_interval
    else:
        logging.warn("The Set interval is lower that %s can handle! Setting Polling to %s seconds.", sensor_name, str(min_interval))
        interval = min_interval

    while True:
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = query_sensor()
        if verify_data(data):
            sensor_data = {
                "name": sensor_name,
                "time": current_time,
                "fields": {
                    "temperature": data[0],
                    "humidity": data[1]
                },
            }
            queue.put(sensor_data)
        else:
            logging.warn("Dropping unhealthy data")
        
        sleep(interval)


def query_sensor():
    [temp,humidity] = grovepi.dht(sensor,white)
    return temp, humidity


def verify_data(sensor_data):
    if not math.isnan(sensor_data[0]) and not math.isnan(sensor_data[1]):
        logging.debug("%s data healthy: %s", sensor_name, str(sensor_data))
        return True
    else:
        logging.warn("%s data unhealthy! Values: %s", sensor_name, str(sensor_data))
        return False


def status():
    logging.debug("Polling %s...", sensor_name)

    if query_sensor():
        logging.info("Polling Result: %s", str(query_sensor()))
        return True
    else:
        return False
