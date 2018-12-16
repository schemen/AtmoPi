#!/usr/bin/env python3
import logging
from time import sleep
from queue import Queue
import utils as utils
from utils import create_pointvalue
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError




class Exporter(object):

    def __init__(self, queue: Queue):

        # Load config right at the start
        config = utils.load_config()

        self.client = None

        self.influxdb_server = config["INFLUXDB_SERVER"]
        self.influxdb_port = config["INFLUXDB_PORT"]
        self.influxdb_user = config["INFLUXDB_USER"]
        self.influxdb_password = config["INFLUXDB_PASSWORD"]
        self.influxdb_database = config["INFLUXDB_DATABASE"]

        self.queue = queue

    def exporter(self):
        logging.info("Exporter started!")
        while True:
                if not self.queue.empty():
                    message = self.queue.get()
                    logging.debug("Exporter write message: %s", message)
                    try:
                        self.write(message)
                    except InfluxDBClientError as exception:
                        logging.warning("Error!  %s \n Putting Entry back into queue.", exception)
                        self.queue.put(message)
                    
                sleep(1)

    def launch_client(self):
        # Start Client
        self.client = InfluxDBClient(host=self.influxdb_server, port=self.influxdb_port, username=self.influxdb_user,
                                     password=self.influxdb_password, database=self.influxdb_database)

    def create_database(self):
        self.client.create_database(self.influxdb_database)

    def write(self, sensor_data):
        self.client.write_points([create_pointvalue(sensor_data)])

    def drop_database(self):
        self.client.drop_database(self.influxdb_database)
