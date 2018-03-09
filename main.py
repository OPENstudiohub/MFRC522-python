#!/usr/bin/python3
# send RFID id's over OSC
# 3/9/18
# updated 3/9/18

import RPi.GPIO as GPIO
import MFRC522


if __name__ == '__main__':
    MIFAREReader = MFRC522.MFRC522()
    reading = True

    try:
        while reading:
            # Scan for cards
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print("Card detected")

            # Get the UID of the card and convert uid to tuple for unpacking
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            uid = tuple(uid)

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print("Card read UID: {}, {}, {}, {}".format(*uid))

                # This is the default key for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print("Authentication error")
    except KeyboardInterrupt:
        print('...user exit received...')
        reading = False
        GPIO.cleanup()
