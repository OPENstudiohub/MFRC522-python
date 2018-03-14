#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/14/18

import os
import yaml
import logging
import logging.config
from RFIDer import RFIDer
from socket import gethostname
from osc_basics import osc_client

basepath = '/home/pi/gitbucket/MFRC522-python'


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def get_hostname():
    return gethostname().split('.')[0]


def _get_logfile_name(hostname):
    '''format log file as "hostname.log"'''

    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def configure_logger(hostname):
    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()


if __name__ == '__main__':
    logger = configure_logger(get_hostname())
    host = '10.1.10.53'
    client = osc_client.OSCClient(host=host)
    rfider = RFIDer()

    try:
        reading = True
        logger.info('scanning for cards...')

        while reading:
            uid = rfider.read()

            if uid:
                logger.info('sending uid {} to host {}'.format(uid, host))
                client.send([uid])  # osc_client is expecting a list

    except KeyboardInterrupt:
        logger.info('...user exit received...')
        reading = False
