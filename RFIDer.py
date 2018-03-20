#!/usr/bin/python3
# rfid reader utility class for L300 built on MFRC522-python:
# https://github.com/mxgxw/MFRC522-python
# 3/9/18
# updated 3/20/18

import logging
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from string import hexdigits


class RFIDer:
    '''
    class that wraps around the MFRC522-python library for reading RFID tags.
    logging is configured in main.py and log.yaml

    we set the # of readers connected to SPI on the Pi via num_devices in __init__(),
    then instantiate MFRC522 RFID reader instance. when RFIDer.read() is called,
    we scan for cards, and if we find one we try to get the UID. if we get an id,
    we convert it from int representation to hexadecimal and capitalize
    all hex letters in the id, then return it
    '''

    def __init__(self, num_devices=1):
        self.num_devices = num_devices
        self.devs = self._set_devs()
        self.logger = self._initialize_logger()
        self.MIFAREReader = MFRC522.MFRC522()

    def _initialize_logger(self):
        logger = logging.getLogger('rfider')
        logger.info('rfider logger instantiated')

        return logger

    def _set_devs(self):
        '''
        returns a list of SPI devices to loop through when scanning for RFID cards.

        returns the default /dev/spidev0.0 unless num_devices=2, in which case it returns
        both SPI devices on the Pi. returns a list either way to support easy looping
        '''

        return ['/dev/spidev0.0', '/dev/spidev0.1'] if self.num_devices == 2 else ['/dev/spidev0.0']

    def _scan(self):
        '''scan for rfid cards and return True if one is found'''

        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        if status == self.MIFAREReader.MI_OK:
            self.logger.info('card detected')
            return True

    def _hexify(self, uid):
        '''
        currently MFRC522 returns id as ints, but we want it represented as hexadecimal
        we also capitalize all letters but 'x' in the id
        '''

        hexs = tuple([hex(u) for u in uid])
        return ' '.join(hexs)

    def _get_uid(self):
        '''
        get the UID from RFID tag, convert to hex, and capitalize all letters except 'x'
        '''

        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

        if status == self.MIFAREReader.MI_OK:
            hexuid = self._hexify(uid[0:4])
            hexuid = ''.join(s.upper() if s in hexdigits else s for s in hexuid)
            self.logger.info('card UID: {}'.format(hexuid))
            return hexuid

    def read(self):
        '''
        return the uid if we have one. on user exit, clean up GPIO and reraise the exception
        '''

        try:
            return self._get_uid() if self._scan() else None
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise
