import dis


# Provided - not part of bytecode
secret = b"sSSss"


def reveal():
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


if __name__ == "__main__":
    dis.dis(reveal)
