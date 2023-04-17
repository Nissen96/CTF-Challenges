#!/bin/bash
gcc encrypt.c aes.c aes.h -o prog && strip prog
