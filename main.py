#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/20/18

import spi
import log_util
from RFIDer import RFIDer
from osc_basics import osc_basics


if __name__ == '__main__':
    logger = log_util.configure_logger()
    client = osc_basics.OSCClient()

    # defaults to one SPI device: RFID reader SDA <-> GPIO pin 24 on the Pi
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
                    logger.info('sending uid {} to host {} on port {}'.format(uid, client.host, client.port))
                    client.send([uid])  # osc_client expects a list

    except KeyboardInterrupt:
        logger.info('...user exit received...')
        client.shutdown()
        reading = False
