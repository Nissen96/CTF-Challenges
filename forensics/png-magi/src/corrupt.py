with open("magic-original.png", "rb") as f:
    img = f.read()

# Remove header
img = bytes.fromhex("00 00 00 00 00 00 00 00") + img[8:]

# Corrupt IHDR field
img = img.replace(b"IHDR", b"JHDR", 1)

# Corrup size
img = img.replace(b"\x02\xf3", b"\x01\x37", 1)

with open("magic.png", "wb") as f:
    f.write(img)
