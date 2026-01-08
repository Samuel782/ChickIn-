##
## Barcode Scanner HID Reader 
## 
## Reads input exclusively from a specific USB HID barcode scanner
## identified by Vendor ID and Product ID.
## The scanner emulates a keyboard, but input is intercepted at
## device level to avoid interference with the physical keyboard.
## NOTE: ONLY FOR WINDOWS DEVICES
##
## Autor: Samuel Luggeri
##
import hid
import time
import logging
from queue import Queue

## --------------------------
##      Configuration
## --------------------------
VENDOR_ID = 0x1234          # Replace with your scanner Vendor ID
PRODUCT_ID = 0x5678         # Replace with your scanner Product ID
READ_SIZE = 64              # HID packet size

## --------------------------
## HID KEY MAP (US layout)
## --------------------------
SHIFT_MASK = 0x02
ENTER_KEY = 40
  
HID_KEYMAP = {
    **{i + 4: chr(ord('a') + i) for i in range(26)},
    **{30 + i: str((i + 1) % 10) for i in range(10)},
    44: ' '
}

SHIFT_KEYMAP = {
    30: '!', 31: '@', 32: '#', 33: '$', 34: '%',
    35: '^', 36: '&', 37: '*', 38: '(', 39: ')'
}

def barcode_listener(on_barcode_callback):
    """
    Blocking HID listener.
    Calls on_barcode_callback(barcode) when ENTER is received.
    """

    barcode = ""

    while True:
        try:
            device = hid.device()
            device.open(VENDOR_ID, PRODUCT_ID)
            device.set_nonblocking(True)
            logging.info("Barcode scanner connected")

            while True:
                data = device.read(READ_SIZE)
                if not data:
                    time.sleep(0.01)
                    continue

                modifier, _, keycode = data[:3]

                if keycode == 0:
                    continue

                if keycode == ENTER_KEY:
                    if barcode:
                        on_barcode_callback(barcode)
                        barcode = ""
                    continue

                if modifier & SHIFT_MASK:
                    char = SHIFT_KEYMAP.get(keycode)
                else:
                    char = HID_KEYMAP.get(keycode)

                if char:
                    barcode += char

        except Exception as e:
            logging.error(f"Scanner disconnected: {e}")
            time.sleep(2)


def main():
    for d in hid.enumerate():
        print(d)

if __name__ == "__main__":
    main()