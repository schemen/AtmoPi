#!/usr/bin/env python3
import os
import logging
import configparser
import sys


def create_pointvalue(sensor_data):
    config = load_config()
    point_value = {
        "measurement": sensor_data["name"],
        "tags": {
            "ap_location": config["AP_LOCATION"],
            "ap_name": config["AP_NAME"]
        },
        "time": sensor_data["time"],
        "fields": sensor_data["fields"]

    }
    logging.debug("Point Value: \n %s", point_value)
    return point_value


def initialize_logger(output_dir):
    config = load_config()
    level = logging.DEBUG if config["DEBUG"] == "True" else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=level)


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
