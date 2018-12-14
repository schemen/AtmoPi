#!/usr/bin/env python3
import logging
from queue import Queue
from time import sleep
from threading import Thread
import bin.config as Config
from bin.sensors import mock,mock_temp,grove_temp_hum_pro

class Collector(object):

    SENSORS = {
        "mock": mock,
        "mock_temp": mock_temp,
        "grove_temp_hum_pro": grove_temp_hum_pro,
    }

    def __init__(self, queue: Queue):

        # Load config right at the start
        self.config = Config.load_config()

        self.sensor_list = self.config["SENSOR_LIST"].split(",")
        self.sensor_list = [sensor.strip() for sensor in self.sensor_list]
        self.queue = queue


    def launch_sensors(self):
        logging.info("Collector Started!")
        logging.info("Activated sensors: %s", self.config["SENSOR_LIST"].split(","))
        for sensor in self.sensor_list:
            if sensor in self.SENSORS:
                logging.info("Starting sensor: %s", sensor)
                Thread(target=self.SENSORS[sensor].start, args=(self.queue,)).start()

    def sensor_health(self):
        logging.info("Checking sensor health...")
        logging.info("Activated sensors: %s", self.config["SENSOR_LIST"].split(","))
        for sensor in self.sensor_list:
            if sensor in self.SENSORS:
                logging.info("Checking sensor %s...", sensor)
                if self.SENSORS[sensor].status():
                    logging.info("%s healthy!", sensor)
                else:
                    logging.info("Something is wrong with %s!", sensor)
