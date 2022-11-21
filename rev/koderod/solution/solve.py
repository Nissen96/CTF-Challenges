#!/usr/bin/python

import subprocess

# Get a list of all CALLER:CALLED pairs
cmd = """objdump -d koderod | grep '<' | sed -e 's/^[^<]*//' | sed 's/<\([^+]*\)[^>]*>/\\1/' | awk 'BEGIN { FS = ":" } \\
        NF>1 { w=$1; } \\
        NF==1 && w != $1 { print  w ":" $0 }' | sort -u | grep -v ':start' | grep -v getrandom | grep -v __stack_chk"""

output, _ = subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

# Create a dictionary of CALLED=CALLER pairs
sym = {}
for s in output.decode().split("\n"):
  s = s.split(':')
  if len(s) == 2:
    sym[s[1]] = s[0]

# Start from CALLED = "end" and lookup its CALLER - continue this chain until reaching the beginning
# Prepend the function name to the result at each step
cur = 'end'
flag = ""
while cur in sym.keys():
  cur = sym[cur]
  flag = cur + flag

print(flag)
