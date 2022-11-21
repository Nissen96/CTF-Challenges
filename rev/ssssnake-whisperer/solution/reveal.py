# Provided - not part of bytecode
secret = b"sSSss"

# Reversed bytecode
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

# Print the result
print(flag.decode())
