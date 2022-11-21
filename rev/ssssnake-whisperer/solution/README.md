# Writeup

This challenge is an exercise in reversing Python bytecode disassembly, which is easiest done line by line, following the [documentation](https://docs.python.org/3/library/dis.html#python-bytecode-instructions). This challenge only uses simple constructs, but otherwise it is recommended to write some Python examples and disassemble yourself to test whether your hypotheses hold.

Doing so for this challenge reveals the following Python script:

```py
with open("hidden.bin", "rb") as f:
    hidden = f.read()

flag = hidden[-15:-5]
flag += secret
for c in hidden[17:-15]:
    flag += bytes([(c + 1337) % 256])

flag += secret[::-1]
flag += int(hidden[:17]).to_bytes(7, "big")

for n in hidden[-5:]:
    flag += bytes([n ^ 100])

flag = flag[::-1]
```

This opens the hidden file and builds the flag from it through a number of different transformations. It refers to `secret`, which we get from the challenge description:

```py
secret = b"sSSss"
```

The entire solve script can be found in [reveal.py](reveal.py), and running this reveals the flag.

## Flag

`ictf{do_y0u_sSSssp34k_p4rssSSs3lT0ngu3?}`
