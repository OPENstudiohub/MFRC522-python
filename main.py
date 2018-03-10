#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/9/18

import MFRC522
import RPi.GPIO as GPIO
from string import hexdigits
from osc_basics import osc_client


def hexify(uid):
    hexs = tuple([hex(u) for u in uid])

    return ' '.join(hexs)


if __name__ == '__main__':
    MIFAREReader = MFRC522.MFRC522()
    client = osc_client.OSCClient(host='10.1.10.53')
    reading = True

    try:
        print('scanning for cards...')

        while reading:
            # scan for cards
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # if a card is found
            if status == MIFAREReader.MI_OK:
                print('card detected')

            # get the UID of the card and convert it to hex
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            # if we have the UID, hexify it and send it over OSC
            if status == MIFAREReader.MI_OK:
                hexuid = hexify(uid[0:4])
                hexuid = ''.join(s.upper() if s in hexdigits else s for s in hexuid)
                print('card UID: {}'.format(hexuid))
                client.send([hexuid])  # osc_client is expecting a list

    except KeyboardInterrupt:
        print('\n...user exit received...')
        reading = False
        GPIO.cleanup()
