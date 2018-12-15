#!/usr/bin/env python3
import os
import logging
import configparser
import sys


def create_pointvalue(sensor_data):
    config = load_config()
    pointValue = {
        "measurement": sensor_data["name"],
        "tags": {
            "ap_location": config["AP_LOCATION"],
            "ap_name": config["AP_NAME"]
        },
        "time": sensor_data["time"],
        "fields": sensor_data["fields"]

    }
    logging.debug("Point Value: \n %s", pointValue)
    return pointValue


def initialize_logger(output_dir):
    config = load_config()
    logger = logging.getLogger()
    if config["DEBUG"]:
        outputlevel = "debug"
        logger.setLevel(logging.DEBUG)
    else:
        outputlevel = "info"
        logger.setLevel(logging.INFO)

    logger.propagate = False

    # create console handler and set level to info
    handler = logging.StreamHandler()
    if outputlevel == "debug":
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
    elif outputlevel == "info":
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def create_folder(folder):
    """
    Function to create folders
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        logging.debug("Folder %s Created!" % folder)
    else:
        logging.debug("Folder %s Exists!" % folder)


def validate_config(location):
    """
    Checks if a valid config.ini exists.
    Exits the program if no valid config is found.
    """
    if not os.path.exists(location):
        full_path = os.path.abspath(location)
        logging.fatal('Config not found - expected a configfile at: [{loc}] - exiting.'.format(loc=full_path))
        sys.exit(1)


def load_config(location='config.ini'):
    """Function that returns a configuration as dict"""
    validate_config(location)
    config = {}
    config_reader = configparser.ConfigParser()
    config_reader.optionxform = str
    config_reader.read(location)

    for key, value in config_reader.items("CONFIG"):
        if key in os.environ:
            config[key] = os.environ[key]
        else:
            config[key] = value

    return config
