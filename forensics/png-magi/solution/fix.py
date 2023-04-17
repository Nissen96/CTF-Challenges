with open("magic.png", "rb") as f:
    img = f.read()

# Fix magic bytes
img = bytes.fromhex("89 50 4e 47 0d 0a 1a 0a") + img[8:]

# Fix IHDR
img = img.replace(b"JHDR", b"IHDR", 1)

# Fix size
img = img.replace(b"\x01\x37", b"\x02\xf3", 1)

with open("fixed.png", "wb") as f:
    f.write(img)
