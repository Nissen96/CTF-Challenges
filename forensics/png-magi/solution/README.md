# Writeup

The png file is corrupted in three places that need to be fixed, using a hex editor or a language like Python.

- Magic bytes are all set to `00`. Change these to `89 50 4e 47 0d 0a 1a 0a`
- `IHDR` tag has been replaced with `JHDR` and needs to be changed back
- The height is set to be too small, meaning the user can now open the image but only see part of it (not the flag).
   - Can be changed to something larger randomly and hope to recover
   - Or, can be recovered using the image size, width, and the IHDR CRC, to find the correct height
 - Open the image to see the flag.

A solve script is in [fix.py](fix.py).

## Flag

`DDC{PNG_f1l3_m4g1c14n}`
