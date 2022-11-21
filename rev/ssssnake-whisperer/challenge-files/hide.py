flag = b"ictf{do_y0u_sSSssp34k_p4rssSSs3lT0ngu3?}"

flag = flag[::-1]

hidden = str(int.from_bytes(flag[28:35], 'big')).encode()

for c in flag[15:23]:
    hidden += bytes([(c - 1337) % 256])

hidden += flag[:10]

for c in flag[-5:]:
    hidden += bytes([c ^ 100])

with open("hidden.bin", "wb") as f:
    f.write(hidden)
