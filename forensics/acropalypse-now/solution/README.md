# Writeup

* Use the existing script from https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02
* Find info on PNG specification here: http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html#C.IHDR
* PNG images has a color type set in IHDR - the script sets this to 2 for standard RGB
* The color type for RGBA is 6, so this should be updated in the script
* Finally, where the top is filled with magenta, the color bytes should include an alpha value (can be anything), i.e. changed from
```py
reconstructed_idat = bytearray((b"\x00" + b"\xff\x00\xff" * orig_width) * orig_height)
```
to e.g.
```py
reconstructed_idat = bytearray((b"\x00" + b"\xff\x00\xff\xff" * orig_width) * orig_height)
```
where alpha value has been set to `0xff` for fully opaque.
* Running this with the same width as the original image and a big enough height (like 400+) makes the flag (and this solution) visisble (so meta O.o)

See extracted image data in [leak.png](leak.png).

## Flag

`DDC{7h3_aCr0p4lyps3_1s_n34r}`
