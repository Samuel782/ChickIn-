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

## --------------------------
##      Configuration
## --------------------------
VENDOR_ID = 0x1234          # Replace with your scanner Vendor ID
PRODUCT_ID = 0x5678         # Replace with your scanner Product ID

READ_SIZE = 64       # HID packet size



def barcodeReader():
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    device.set_nonblocking(True)
    barcode = ""

    while True:
        data = device.read(64)
        if data:
            for byte in data:
                if byte == 40:  # ENTER
                    return barcode
                elif byte != 0:
                    barcode += chr(byte)


def main():
    for d in hid.enumerate():
        print(d)

if __name__ == "__main__":
    main()