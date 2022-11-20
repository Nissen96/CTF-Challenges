def encrypt(message, key):
    if type(message) != str:
        raise ValueError("Message must be a string.")

    if type(key) != list or len(key) != 128 or not all(v == 0 or v == 1 for v in key):
        raise ValueError("Key must be a list of length 128 of 0s and 1s.")

    pad = 8 - (len(message) % 8)
    message = list(message) + [str(pad)] * pad

    for i in range(0, len(message), 8):
        for j in range(len(key)):
            if key[j]:
                message[i + (j % 8)], message[i + ((j + 1) % 8)] = message[i + ((j + 1) % 8)], message[i + (j % 8)]

    return "".join(message)
