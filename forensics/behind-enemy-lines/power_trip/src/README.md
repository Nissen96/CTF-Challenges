# Challenge Generation

For this challenge, users get access to a packet capture with both unencrypted and encrypted traffic.
The encrypted traffic uses TLS and with RSA - `TLS_RSA_WITH_AES_256_GCM_SHA384` - using a specific RSA key we generate.
The idea is, that users get access to a power trace from a decryption using the private key and from this, they need to generate a certificate to decrypt the traffic.

The file [gen_power_trace.py](gen_power_trace.py) hardcodes the private key value `d` and simulates a trace based on its bits.
This depends on the parameters set in the top, which can be tweaked to get a slightly different trace for the same bits. Some random noise is added in the end to make it realistic.

This key must be converted to PEM- and PKCS8-format, which is used to create the encrypted traffic.
All traffic is simulated with [gen_network_traffic.py](gen_network_traffic.py), which runs both a HTTP, TLS, SMTP, and Instant Messaging (custom) server.
It has been set up so new clients can easily be created and send various message types between each other, e.g.:

```py
dimitri = Client("Dimitri", "redeagle@astzk.gov.hkn")
sergiu = Client("Sergiu Volda", "sergiu@helpdesk.astzk.hkn")
dari = Client("Dari Ludum", "dari@astzk.gov.hkn")

dimitri.http_get("index.html")
dari.https_get("images.html")
sergiu.smtp_send(dari, "Password reset", body_file="static/new_password.eml")
```

The custom Instant Messaging protocol is unencrypted and used as an old and deprecated protocol, that the soldiers no longer should use, but that one accidentally does anyway.
The small server for this is implemented in [im_server.py](im_server.py).

This makes it simple to run many different simulations - with sleeps in between for realism.

The folder `/static` contains lots of static files that can be requested, e.g. web pages, images, emails, and also the certificates needed to setup the servers.
The email `attack.eml` is the only one strictly necessary, since it contains the flag.

Optionally at the end, `tracewrangler` can be used to replace localhost addresses with various fake IP addresses for realism.
