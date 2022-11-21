# Writeup

Navigating to the URL, we see a pretty diary website, where users can post their diary entries publically or, if logged in, privately.
All users can see all public entries, but only authenticated users can see their own private entires.

**Authentication Description**

User authentication is handled with RSA-signed JWTs. The server generates an RSA key pair and uses the private key for signing the JWT upon login. The public key is stored as a JSON Web Key (JWK) in a JSON Web Key Set (JWKS) that is hosted at `/api/keys`. The JWK has a Key Identifier (KID) used to identify this specific key among other potential JWKs in the set.

The generated JWT stores this URL in its JKU field (JWK Set URL) and stores the KID so the server knows where to lookup the JWKS and can identify the correct JWK with the KID.

Upon any requests requiring authorization, the client must send its JWT in the Authorization header. The server then decodes the JWT, fetches the JWKS from the specified JKU, and finds the correct JWK using the specified KID. This JWK contains the public RSA key used to verify the token signature.

**Vulnerability**

An attack on this would be to generate your own RSA key pair, host the public key at your own website, and set the JKU in the JWT to point to this. Then you could just sign this JWT with your own private key, and make the server use your own public key to sign it.

But! The server checks that the netloc of the JKU is `dear-diary.hkn`, so the public key must be hosted somewhere on the site.
The server is still, however, vulnerable to JWKS spoofing - by uploading the JWK as a new diary entry.
The endpoint `http://dear-diary.hkn/api/entries/<id>` gets the contents of a diary entry as plaintext and can be set as the JKU in the token.
This has the correct netloc and will cheat the server to use this public key for validation.
This means we can create our own RSA key pair, submit the public key as a diary entry, generate a JWT that has this entry URl as its JKU, and sign the JWT with our private key.

**Step-by-step solution**

1. Get the admin id (stored with each diary entry when fetched)
2. Register an account and login
3. Generate an RSA key pair
4. Fetch a JWK from `/api/keys` to see how it is formatted
5. Create an identical JWK but with the `n`-value from your RSA key
6. Create a new public diary entry with any title and post your forged JWK as the content
7. Get the `id` of this entry when created
8. Get your current token from your cookies and decode it
9. Change the `user_id` to the admin id found previously
10. Change the `jku` to `http://dear-diary.hkn/api/entries/<id>` where `<id>` is the id of the entry with your own JWK
11. Sign this new token with your own private key
12. Update your token cookie with this new token and refresh
13. You are now logged in as admin - read the private entries to find the flag

See [solve.py](solve.py) for an automated implementation of this exploit.

## Flag

`DDC{d34r_d14ry_t0d4y_I_sp00f3d_4_JWK_d0n7_t311_4ny0n3_X0X0}`
