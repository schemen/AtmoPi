#!/usr/bin/env python3
import os
import sys
import click
import logging
from queue import Queue
from threading import Thread
import bin.config as Config
from bin.exporters import Exporter
from bin.collector import Collector
from bin.utils import initialize_logger


# Python 3 is required!
if sys.version_info[0] < 3:
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)


# Load config right at the start
config = Config.load_config()

# Logging
initialize_logger("log/")


# Create the core CLI launcher
@click.group()
def cli():
    """Welcome to AtmoPi, your very own DIY Weather station"""
    pass

#######################################
### Verify command                  ###
#######################################
@cli.command('start')
def start():
    """Start AtmoPi"""
    logging.info("Starting the AtmoPi Agent...")
    # Initiate QUEUE FOR ALL THE PY
    logging.info("Launching the Queue...")
    q = Queue()

    logging.info("Initiating the Workers...")
    collect = Collector(q)
    export = Exporter(q)
    export.launch_client()
    export.create_database()

    # start the shit
    logging.info("Starting the Workers...")
    Thread(target=export.exporter).start()
    Thread(target=collect.launch_sensors).run()
    



#######################################
### Sensor commands                ###
#######################################
@cli.group()
def sensor():
    """Commands regarding the sensors"""
    pass

@sensor.command()
def status():
    logging.info("Status of the Sensors")
    sensors = Collector(None)
    sensors.sensor_health()

#######################################
### Sensor commands                ###
#######################################
@cli.group()
def db():
    """Commands regarding the sensors"""
    pass

@db.command('status')
def db_status():
    logging.info("Status of the DB Connection")

@db.command('reset')
def db_reset():
    logging.info("Resetting DB...")
    export = Exporter(None)
    export.launch_client()
    export.drop_database()
    logging.info("Done.")

# Start the run
if __name__ == '__main__':
    cli()
