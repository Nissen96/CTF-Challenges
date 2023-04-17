from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.parse import unquote

with open("messages.txt") as f:
    messages = f.read().strip().split("\n")

key = b64decode("MgE6i1GDQjARYBKWwQtf5pK6pAnLIVx2VWvY+J9PqYg=")

for msg in messages:
    try:
        decoded = b64decode(unquote(msg))
        iv = decoded[:16]
        aes = AES.new(key, AES.MODE_CBC, iv=iv)
        pt = unpad(aes.decrypt(decoded[16:]), 16).decode()
        print(pt)
    except:
        continue
