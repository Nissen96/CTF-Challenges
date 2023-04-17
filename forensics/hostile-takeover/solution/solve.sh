#!/bin/bash

# Extract encrypted commands and respones and decrypt with Python script
tshark -r takeover.pcapng -Y "http.file_data && frame.number > 40" -T fields -e "http.file_data" | sed "s/result=//" > messages.txt
python3 decrypt.py
