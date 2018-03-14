#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/14/18

from RFIDer import RFIDer
from osc_basics import osc_client


if __name__ == '__main__':
    rfider = RFIDer()
    client = osc_client.OSCClient(host='10.1.10.53')
    reading = True

    try:
        print('scanning for cards...')

        while reading:
            uid = rfider.read()

            if uid:
                client.send([uid])  # osc_client is expecting a list

    except KeyboardInterrupt:
        print('\n...user exit received...')
        reading = False
        # GPIO.cleanup()
