# Writeup

Opening the PCAP we see lots of USB-frames. The first few sets up the USB devices and we see a USB keyboard on interface 1, a USB mouse on interface 2, and an unknown device on interface 3. Following this is the actual data transmitted and we notice all of this is between the host and the device with address "1.2.1" - the keyboard.

Packets from the keyboard to the host has a HID Data field containing the actual data sent, corresponding to the keypresses done on the keyboard.
These can be extracted with `tshark` by extracting the field `usbhid.data`:

```bash
tshark -r intel.pcap -T fields -e usbhid.data > usbdata.txt
```

The keyboard data needs to be decoded and it is simple to find good scripts for this online, or to write your own based on the specification.
It is necessary to find one that handles SHIFT, CAPS LOCK, and BACKSPACE to decode correctly.

I have created my own script for this here: https://github.com/Nissen96/USB-HID-decoders. This can be run on the file with

```bash
python3 USB-HID-decoders/keyboard_decode.py usbdata.txt
```

This decodes the keystrokes and displays the following email to recipient `redeagle@astzk.gov.hkn` with subject `Mission Successful!`:

```
General Red Eagle!
We have successfully deployed NotYepta and taken down major parts of Kolechia's infrastructure.
They will be an easy target now and we are almost ready for the physical attack.
In case the worm spreads to our internal networks through any communications channel from Kolechia, our data can be recovered with the decryption key DDC{f1l3_3ncryp710n_b3_G0NE}

We are ready to attack on your command!

GLORY TO ARSTOTZKA!
```

The solve script [solve.sh](solve.sh) extracts the keycodes, downloads the decoder and runs it, and removes all artefacts.


## Flag

`DDC{f1l3_3ncryp710n_b3_G0NE}`
