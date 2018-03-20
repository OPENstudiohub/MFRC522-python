#!/usr/bin/python3
# utilities to configure logging
# 3/9/18
# updated 3/20/18

'''
logging configuration utilities for MFRC522
log filename is based on hostname of the Pi, e.g 'rfidberry01.log'
'''


import os
import yaml
import logging
import logging.config
from socket import gethostname


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def _get_logfile_name(basepath, hostname):
    '''format log file as "hostname.log"'''
    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def _get_basepath():
    '''
    this method of getting the script's basepath is needed when
    running the script as a systemd service on the Pi
    '''
    return os.path.dirname(os.path.realpath(__file__))


def _get_hostname():
    '''get hostname to use for log filename'''
    return gethostname().split('.')[0]


def configure_logger():
    '''read log.yaml config file to configure logging'''
    basepath = _get_basepath()
    hostname = _get_hostname()

    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(basepath, hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()
