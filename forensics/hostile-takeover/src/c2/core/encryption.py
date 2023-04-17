import base64
import os

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generateKey():
    return base64.b64encode(os.urandom(32)).decode()


def ENCRYPT(pt, key):
    key = base64.b64decode(key)
    padded = pad(pt.encode(), AES.block_size)
    iv = Random.new().read(AES.block_size)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + aes.encrypt(padded)).decode()


def DECRYPT(ct, key):
    key = base64.b64decode(key)
    ct = base64.b64decode(ct)
    iv = ct[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    pt = aes.decrypt(ct[16:])
    return unpad(pt, AES.block_size).decode()
