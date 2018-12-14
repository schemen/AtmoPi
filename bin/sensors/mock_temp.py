#!/usr/bin/env python3
import random
import logging
from queue import Queue
from datetime import datetime
from time import sleep
import bin.config as Config

# Load config right at the start
config = Config.load_config()

set_interval = int(config["POLL_INTERVAL"])
min_interval = 30
sensor_name = "mock-temp"
interval = None

def start(queue: Queue):

    if set_interval > min_interval:
        interval = set_interval
    else:
        logging.warn("The set interval is lower that %s can handle! Setting Polling to %s seconds.", sensor_name, str(min_interval))
        interval = min_interval

    while True:
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        sensor_data = {
            "name": sensor_name,
            "time": current_time,
            "fields": {
                "value": query_sensor()
            },
        }
        queue.put(sensor_data)
        sleep(interval)

def query_sensor():
    return random.randint(-10, 38)

def verify_data(sensor_data):
    pass

def status():
    logging.debug("Polling %s...", sensor_name)
    try:
        data = query_sensor()
    except Exception as fuck:
        pass
        
    if data:
        return True
    else:
        return False