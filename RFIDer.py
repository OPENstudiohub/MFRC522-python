#!/usr/bin/python3
# rfid reader utility class for L300 built on MFRC522-python:
# https://github.com/mxgxw/MFRC522-python
# 3/9/18
# updated 3/14/18

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from string import hexdigits


class RFIDer:

    def __init__(self):
        self.MIFAREReader = MFRC522.MFRC522()

    def _scan(self):
        '''scan for rfid cards and return True if one is found'''

        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        if status == self.MIFAREReader.MI_OK:
            print('card detected')
            return True

    def _hexify(self, uid):
        '''
        currently MFRC522 returns id as ints,
        but we want it represented as hexadecimal
        '''

        hexs = tuple([hex(u) for u in uid])
        return ' '.join(hexs)

    def _get_uid(self):
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

        if status == self.MIFAREReader.MI_OK:
            hexuid = self._hexify(uid[0:4])
            hexuid = ''.join(s.upper() if s in hexdigits else s for s in hexuid)
            print('card UID: {}'.format(hexuid))
            return hexuid

    def read(self):
        '''return the uid if we have one'''

        try:
            return self._get_uid() if self._scan() else None
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise
