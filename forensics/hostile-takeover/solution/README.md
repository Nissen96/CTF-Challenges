# Writeup

* Open the pcap file in Wireshark to inspect the traffic
* Notice the first HTTP GET request, which downloads a PS script from `/sc/xkbqt.ps1` - extract this
* The script is slightly obfuscated, but it simply disables AMSI (Microsoft's Antimalware Scan Interface), before downloading another PowerShell script from `/download/xkbqt.ps1`, which is executed
* Looking a the next few packets in Wireshark, we see exactly this happening and we extract this script as well
* This script base64 decodes and deflates another encoded script and executes it
* Simplest way to extract this script is to just run the code in PowerShell, but skip the first part (`iex`), which runs the script
* We now have the main script which is used by the botmaster to communicate with the machine securely
* This is quite obfuscated by splitting everything up and reordering plus removing indentation. Variables and function names have, however been kept the same
* This is not too bad to deobfuscate manually, but much easier with an automatic deobfuscator such as https://github.com/Malandrone/PowerDecode
* We see a `Create-AesManagedObject()` function for setting up an AES-CBC encryptor/decryptor, an `Encrypt()` and `Decrypt()` function, a `shell()` function which seems to run a command and return the output, and then the main code itself
* The code itself sets a `key = 'MgE6i1GDQjARYBKWwQtf5pK6pAnLIVx2VWvY+J9PqYg='` and sets the IP and port of the C2 server. It then sends a POST request to the server with the hostname of the computer.
* Now the client starts continuously asking the C2 for commands and when receiving one, it decrypts the contents, runs the command, encrypts the response and sends it back.
* The crypto is done with AES-CBC and uses the previously found key. We see in the `Decrypt()` function, that the first 16 bytes are used as the IV, and the message is then the rest
* When encrypting, a random IV is chosen and used to encrypt the response, and the IV is then prepended to this before sending.
* We now know how to decrypt the remaining contents of the requests in the pcap
* All encrypted messages can be extracted with the following `tshark` command:
```
$ tshark -r takeover.pcapng -Y "http.file_data && frame.number > 40" -T fields -e "http.file_data" | sed "s/result=//" > messages.txt
```
The messages can then be decoded and decrypted with e.g. Python:
```py
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
```
* With this, we get all the commands and responses. We see the hacker requests various system information, creates a new admin user on the computer, and finds some interesting files in the `Downloads` and `Documents` folder
* In `Documents`, the file is `internal.zip`, and the hacker "downloads" this as hex with
```
powershell (Format-Hex .\Documents\internal.zip | Select-Object -Expand Bytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''
```
* The response is thus the hex encoded zip file, which we can decode with e.g. Python or CyberChef and save as a file.
* Unzipping, we find a PNG logo, a sensitive meeting notes file, and the flag

## Flag

`DDC{l00k_4t_m3_1_4m_th3_c4p741n_n0w}`
