from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

private_key = RSA.import_key(open("exfiltration_key").read())
cipher_rsa = PKCS1_OAEP.new(private_key)

with open("passes_Jens.txt") as f:
    sk, n, t, ct = f.read().split()

enc_session_key = bytes.fromhex(sk)
nonce = bytes.fromhex(n)
tag = bytes.fromhex(t)
ciphertext = bytes.fromhex(ct)

session_key = cipher_rsa.decrypt(enc_session_key)
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)

print(data.decode())
