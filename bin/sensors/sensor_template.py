#!/usr/bin/env python3
import random
import logging
from queue import Queue
from datetime import datetime
from time import sleep
import bin.config as Config

# Sensor Meta Data
config = Config.load_config()
set_interval = int(config["POLL_INTERVAL"])
min_interval = 10
sensor_name = "sensor-template"

def start(queue: Queue):

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
                    "value": data
                },
            }
            queue.put(sensor_data)
        else:
            logging.warn("%s delivered fautly data, dropping.", sensor_name)
        sleep(interval)

def query_sensor():
    return True

def verify_data(sensor_data):
    return True

def status():
    logging.debug("Polling %s...", sensor_name)

    if query_sensor():
        return True
    else:
        return False