#!/bin/bash

tshark -r intel.pcap -T fields -e usbhid.data > usbdata.txt
git clone https://github.com/Nissen96/USB-HID-decoders.git
echo ""
python3 USB-HID-decoders/keyboard_decode.py usbdata.txt
rm -rf USB-HID-decoders usbdata.txt
