#!/usr/bin/env python3
import os
import logging
import bin.config as Config

# Load config right at the start
config = None
if not config:
    config = Config.load_config()

def create_pointvalue(sensor_data):
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


def createFolder(folder):
    '''
    Function to create folders
    '''
    if not os.path.exists(folder):
        os.makedirs(folder)
        logging.debug("Folder %s Created!" % folder)
    else:
        logging.debug("Folder %s Exists!" % folder)
