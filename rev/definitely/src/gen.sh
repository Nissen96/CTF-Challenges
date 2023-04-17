#!/bin/bash
echo "Generating psyduck program..."
python convert.py > definitely.c

echo "Compile with"
echo "\$ gcc -o definitely -gdwarf-4 -no-pie -O0 definitely.c"
echo "and decompile for easiest solve"
