#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/16/18

import os
import spi
import yaml
import logging
import logging.config
from RFIDer import RFIDer
from socket import gethostname
from osc_basics import osc_client

# specify the script's full path. this is needed when running script as a service on the Pi
basepath = '/home/pi/gitbucket/MFRC522-python'


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def _get_logfile_name(hostname):
    '''format log file as "hostname.log"'''
    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def get_hostname():
    '''get hostname to use for log filename'''
    return gethostname().split('.')[0]


def configure_logger(hostname):
    '''read log.yaml config file to configure logging'''

    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()


if __name__ == '__main__':
    host = '10.1.10.3'
    logger = configure_logger(get_hostname())
    client = osc_client.OSCClient(host=host)
    
    # defaults to one SPI device. RFID reader SDA <-> GPIO pin 24 on the Pi
    # there is another SPI device available on the Pi: SDA <-> GPIO pin 26
    # set num_devices=2 to use both. this is NOT thoroughly tested
    rfider = RFIDer(num_devices=1)

    try:
        reading = True
        logger.info('scanning for cards...')

        while reading:
            # we loop through the devs list even if there's only one item
            # to support multiple readers connected to one Pi via SPI
            for dev in rfider.devs:
                spi.openSPI(device=dev)
                uid = rfider.read()
                spi.closeSPI()

                if uid:
                    logger.info('sending uid {} to host {}'.format(uid, host))
                    client.send([uid])  # osc_client expects a list

    except KeyboardInterrupt:
        logger.info('...user exit received...')
        client.shutdown()
        reading = False
