from pwn import xor

with open("deadinside", "rb") as f, open("getflag", "wb") as g:
    data = f.read()
    decoded = xor(data, bytes.fromhex("deadbeef"))
    g.write(decoded)
