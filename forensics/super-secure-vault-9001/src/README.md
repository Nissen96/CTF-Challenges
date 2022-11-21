# Challenge Generation

Short guide for how to recreate the challenge:

A small web app has been created in `/vault`.
This contains:
  - `access.php`: login page for the vault, comparing the posted key to a hardcoded master key
  - `robots.txt`: disallows only the path to `access.php.backup`
  - `access.php.backup`: a backup for the access page, from which the intruder can read the PHP-code, including the master key. In practice just a symbolic link to `access.php`
  - `vault.php`: the vault itself with the CEO's secret data, including:
    * `skolefoto86.jpg`: school photo of the CEO from 1986
    * `navne.txt`: a list of names for the CEO's baby
    * `fortrolig.pdf`: a confidential PDF containing the flag
  - `lock.php`: logout page, clearing the session

The web-app can be started locally from the vault folder with `php -S localhost:80`.
Open Wireshark and start capturing traffic on the loopback interface.
Then pretend to be the intruder and poke around the application. The requests I did was:
 - GET /index.html - 404 error
 - GET /index.php - 404 error
 - GET /admin.php - 404 error
 - GET /vault.php - 302 Redirection to /access.php
 - GET /access.php - 200 (automatically redirects here if using browser)
 - POST /access.php with a few wrong keys. I just did a few random and a few SQLi attempts:
    * key=key
    * key=lukmigind
    * key=jegviliiiiind
    * key='
    * key=' OR '1'='1
    * key='loneskumerdum'
    * key='AAAARRRGH'
 - GET /.htaccess - 404 error (intruder trying other pages)
 - GET /robots.txt - 200 (contains "Disallow: /access.php.backup")
 - GET /access.php.backup - 200 (intruder can now read PHP source, including master key)
 - GET /access.php - 200
 - POST /access.php, key=Sup3r_51kk3r_nøgl3_du_4ldr1g_gæ7t3r...håb3r_j3G - 200 (and key is correct)
 - GET /vault.php - 200 (intruder sees CEO's secrets and documents and downloads the docs):
    * GET /skolefoto86.jpg - 200
    * GET /navne.txt - 200
    * GET /fortrolig.txt - 200
 - GET /lock.php - 200 (logs out and is redirected)
 - GET /access.php - 200

Then stop the capture and save it as `vault.pcapng`. I just ran it all on localhost, so both the client and server had the same IP.
I then as a small extra step ran the tool `tracewrangler` on the file to replace the IP addresses with two other ones, so it seemed just a bit realistic (still keeping port 80 for the server).

That's basically it - so just run the webserver, start capturing packets, poke around however you want, and stop+save the capture.
