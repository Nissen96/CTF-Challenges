# Writeup

The WAV-file contains a PNG image, hidden with least significant bit steganography, using the most popular audio steganography tool: [WavSteg](https://github.com/ragibson/Steganography#WavSteg). This can be installed with

```bash
pip install stego-lsb
```

and the least significant bit can be extracted from each byte with

```bash
stegolsb wavsteg -r -i message.wav -o hidden.png -n 1 -b 200000
```

`-n 1` is set to just extract one bit per byte and `-b 200000` specifies the number of bytes to extract bits from. Setting it this high will extract the entire image. Before knowing it is an image, this can be set lower, and the PNG header will be clear from the result.

## Flag

`DDC{UFO_guy_i5_r1ght_w3_4r3_0ut_h3r3_m4n}`
