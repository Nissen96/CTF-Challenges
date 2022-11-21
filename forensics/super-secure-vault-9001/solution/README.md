# Writeup

Opening the packet capture in Wireshark, we notice the traffic is just simple HTTP requests.
We can get a quick overview of all the web traffic by applying `http` as a filter.
Going more into detail, we right-click the first and choose "Follow -> TCP Stream" and scroll through the request/response pairs.

The intruder first tries to access a few pages without luck, but then `/vault.php`, redirecting them to `/access.php` to login.
Here, they try entering a few master keys before giving up and looking elsewhere.

They try first `/.htaccess` with no luck, but then `/robots.txt` where they find `"Disallow: /access.php.backup"`.
This clearly seems very interesting, and `/access.php.backup` is also the next page they access.
Here, they find a backup of the PHP-code for the access page, including the hardcoded master key, `Sup3r_51kk3r_nøgl3_du_4ldr1g_gæ7t3r...håb3r_j3G`.

Knowing the master key, they re-visit `/access.php` where they enter it, granting them access to the vault.
In here, they find and download a school photo, a list of baby names, and most importantly a confidential PDF.

We can export this PDF in Wireshark with `File -> Export Objects -> HTTP`, choosing `fortrolig.pdf` (and possibly the others if you are interested).

Opening the PDF, we get the flag.


## Flag

`DDC{1ng3n_får_adg4n6_t1l_m1n_sup3r_s3cur3_v4ul7_9001!}`
