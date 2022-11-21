#!/bin/bash
nasm -f bin -o getflag getflag.asm
python3 convert.py
chmod +x deadinside
rm getflag