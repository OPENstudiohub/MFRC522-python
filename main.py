#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/9/18

import MFRC522
import RPi.GPIO as GPIO
from osc_basics import osc_client


def hexify(uid):
    hexs = tuple([hex(u) for u in uid])

    return '{} {} {} {}'.format(*hexs)


if __name__ == '__main__':
    MIFAREReader = MFRC522.MFRC522()
    client = osc_client.OSCClient(host='rfidberry.local')
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
            hexuid = hexify(uid)
            print('card UID: {}'.format(hexuid))

            # make sure no errors popped up in the above exchange
            if status == MIFAREReader.MI_OK:
                # send UID over OSC
                client.send(hexuid)

    except KeyboardInterrupt:
        print('\n...user exit received...')
        reading = False
        GPIO.cleanup()
