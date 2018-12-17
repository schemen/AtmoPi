#!/usr/bin/env python3
import random
import logging
from queue import Queue
from datetime import datetime
from time import sleep
import sensors.config as Config

# Sensor Meta Data
config = Config.load_config()
set_interval = int(config["POLL_INTERVAL"])
min_interval = 10
sensor_name = "sensor-template"

def start(queue: Queue):
    """Start the sensor!"""

    # Make sure we don't go under the minimal interval of the sensor
    if set_interval > min_interval:
        interval = set_interval
    else:
        logging.warn("The Set interval is lower that %s can handle! Setting Polling to %s seconds.", sensor_name, str(min_interval))
        interval = min_interval

    # Launching the sensor loop
    while True:
        # Get the datetime of that data set
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        # Get all the data!
        data = query_sensor()

        # Verify and deliver data
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
        
        # Wait for next run!
        sleep(interval)

def query_sensor():
    """This sensor returns N"""
    return True

def verify_data(sensor_data):
    """Verify the sensor data, return False if corrupt"""
    return True

def status():
    """Pull the sensor to check if it's healthy"""
    logging.debug("Polling %s...", sensor_name)
    if query_sensor():
        return True
    else:
        return False