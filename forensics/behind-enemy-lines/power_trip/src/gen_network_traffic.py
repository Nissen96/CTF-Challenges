import json
import http.client
import os
import pwn
import signal
import subprocess
import time
from email.message import EmailMessage
from tlslite import HTTPTLSConnection, HandshakeSettings, SMTP_TLS

pwn.context.log_level = "warn"

HTTP_PORT = 80
HTTPS_PORT = 443
SMTP_PORT = 25
IM_PORT = 1337

# Force TLS 1.2 with RSA key exchange to allow easy decryption in Wireshark
tls_settings = HandshakeSettings()
tls_settings.keyExchangeNames = ["rsa"]
tls_settings.maxVersion = (3, 3)


def start_servers():
    print("[*] Starting HTTP server...")
    http_server = subprocess.Popen(f"python -m http.server {HTTP_PORT}", cwd="static", shell=True, preexec_fn=os.setsid)
    print("[*] Starting HTTPS server...")
    https_server = subprocess.Popen(f"tls.py server -k key.pem -c cert.pem localhost:{HTTPS_PORT}", cwd="static", shell=True, preexec_fn=os.setsid)
    print("[*] Starting SMTP server...")
    smtp_server = subprocess.Popen(f"smtp4dev --hostname=localhost --smtpport={SMTP_PORT} --tlsmode=StartTls --tlscertificate=$(pwd)/cert.pem --tlscertificateprivatekey=$(pwd)/key.pkcs8", cwd="static", shell=True, preexec_fn=os.setsid)
    print("[*] Starting Instant Messaging server...")
    im_server = subprocess.Popen(f"python im_server.py {IM_PORT}", shell=True, preexec_fn=os.setsid)
    return http_server, https_server, smtp_server, im_server



class Client:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def https_get(self, url):
        https_conn = HTTPTLSConnection("localhost", HTTPS_PORT, settings=tls_settings)
        https_conn.request("GET", url)
        html = https_conn.getresponse().read()
        for img in html.split(b"<img src=\"")[1:]:
            self.https_get(img[:img.index(b"\"")].decode())
        return html
    
    def http_get(self, url):
        http_conn = http.client.HTTPConnection("localhost", HTTP_PORT)
        http_conn.request("GET", url)
        html = http_conn.getresponse().read()
        for img in html.split(b"<img src=\"")[1:]:
            self.http_get(img[:img.index(b"\"")].decode())
        return html
    
    def smtp_send(self, recipient, subject, body=None, body_file=None):
        msg = EmailMessage()
        
        if body_file is not None:
            with open(body_file) as f:
                msg.set_content(f.read())
        else:
            msg.set_content(body)

        msg["Subject"] = subject
        msg["From"] = f"{self.name} <{self.email}>"
        msg["To"] = f"{recipient.name} <{recipient.email}>"
        
        smtp_conn = SMTP_TLS("localhost", SMTP_PORT)
        smtp_conn.starttls(settings=tls_settings)
        smtp_conn.send_message(msg)
    
    def instant_messaging(self, messages):
        with open("chat.json", "w") as f:
            json.dump(messages, f)

        conn = pwn.remote("localhost", IM_PORT, fam="ipv4")
        conn.sendline(b"#START CHAT#")
        if not conn.recvline().strip() == b"#CHAT ACCEPTED#":
            print("Chat not accepted")
            return
        
        for from_client, msg in messages:
            if from_client:
                conn.sendline(b"#MSG# " + msg.encode())
            else:
                response = conn.recvline().strip()
                print(response.decode())
                if response == b"#END CHAT#":
                    conn.sendline(b"#CHAT ENDED#")
                    return

        conn.sendline(b"#END CHAT#")


def main():
    servers = start_servers()
    time.sleep(5)

    try:
        # Generate a few personas
        dimitri = Client("Dimitri", "redeagle@astzk.gov.hkn")
        sergiu = Client("Sergiu Volda", "sergiu@helpdesk.astzk.hkn")
        dari = Client("Dari Ludum", "dari@astzk.gov.hkn")
        corman = Client("Corman Drex", "c0rm4n@astzk.hkn")
        simon = Client("Simon Wens", "swens@astzk.hkn")
        mailing_list = Client("Military Operations", "mil-ops@astzk.gov.hkn")

        # Random traffic, HTTPS, SMTP mail, and some unencryped HTTP by Dimitri
        dari.https_get("index.html")
        time.sleep(2)
        dimitri.http_get("index.html")
        time.sleep(10)
        dari.https_get("images.html")
        time.sleep(3)
        sergiu.https_get("index.html")
        time.sleep(2)
        dimitri.http_get("wiki.html?q=what+does+tls+stand+for")
        time.sleep(12)
        sergiu.https_get("news.html")
        time.sleep(10)
        dimitri.http_get("wiki.html?q=how+to+enable+tls")
        time.sleep(20)
        sergiu.smtp_send(dari, "Password reset", body_file="static/new_password.eml")
        time.sleep(1)
        dimitri.http_get("wiki.html?q=how+does+security+even+work")
        time.sleep(4)
        corman.smtp_send(simon, "Weekend plans?", body_file="static/random.eml")
        time.sleep(7)
        dimitri.http_get("images.html")
        time.sleep(23)

        # Dimitri contacts Sergiu on a direct unencrypted channel to get help
        dimitri.instant_messaging([
            (True, "Sergiu, do you copy?"),
            (False, "General Red Eagle, this is an old and unencrypted channel, you are not supposed to use this, everything is encrypted now!"),
            (True, "I know that but I somehow disabled TLS support and now I cannot get my stupid computer to use it again - I don't have access to anything now!"),
            (True, "It is crucial I get my access back very soon, I have a very important email to send out."),
            (False, "Should be a simple fix, I'll walk you through it."),
            (True, "I have a certificate and private key on my desktop, should I send that?"),
            (False, "NO NO NO, I do NOT need that, PLEASE do NOT send that to ANYONE, and ESPECIALLY not an unencrypted channel!"),
            (False, "The RSA private key is used by the server to setup TLS sessions! Whoever has this can decrypt and see EVERYTHING"),
            (True, "Obviously yes, we have used the same key for all servers and services, so we can monitor everyone"),
            (False, "I'll come by your office and take a look before you accidentally leak the private key here..."),
            (True, "Alright, but come quick!")
        ])
        time.sleep(17)

        # He gets encryption up and running and all remaining traffic is encrypted
        dimitri.https_get("index.html")
        time.sleep(9)
        dimitri.https_get("news.html")
        time.sleep(60)
        dimitri.smtp_send(sergiu, "Thanks", body_file="static/thank_you.eml")
        time.sleep(43)
        dimitri.smtp_send(mailing_list, "Operation Takeover", body_file="static/attack.eml")


        
    except Exception as e:
        print(e)
    finally:
        print("[*] Closing servers...")
        time.sleep(5)
        for server in servers:
            os.killpg(os.getpgid(server.pid), signal.SIGTERM)


if __name__ == "__main__":
    main()