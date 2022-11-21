from pwn import xor

with open("getflag", "rb") as f, open("deadinside", "wb") as g:
    elf = f.read()
    encoded = xor(elf, bytes.fromhex("deadbeef"))
    g.write(encoded)
