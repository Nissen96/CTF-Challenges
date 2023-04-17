# Writeup

**INTENDED:**

* Register a new account at `/register` and login at `/login` to get a token. This must be supplied in an `x-auth-token` header for any authenticated requests going forward
* Update the user at `/update`, supplying a JSON object containing a prototype pollution to set a custom secret: `{ "__proto__": { "secret": SECRET } }`
* This pollutes the prototype of `Object`, meaning you get `SECRET` as the value when accessing the field `.secret` on any object that doesn't have this set already.
* Since the admin user has no secret field set, this chosen secret will now be used when verifying an admin JWT.
* This means we can forge a new JWT with username set to `admin` and sign it with our custom secret
* Supplying this in `x-auth-token`, we can use the API as admin. Specifically, we can run code at `/run` with no protection
* To get full shell, setup a local netcat listener and pass in a standard revshell to the `/run` using `require("child_process").exec(<revshell>)`.
* Flag is in a randomly named folder in the root directory on the server, so `/<random-uuid>/flag.txt`
* It is therefore also enough to just `cat` the flag using wildcards, i.e. `cat /*/flag.txt` - but full shell is obviously cooler.

See solution script [rce.py](rce.py).

**UNINTENDED:**

The code uses the `vm2` sandbox for non-admin users to safely evaluate JS code.
This was meant to be safe, and not the inteded path, but a critical vulnerability was found in the library shortly before the challenge release which was not discovered. This made the challenge easier than intended but was still a cool vulnerability - that's fair game.

See PoC here: https://gist.github.com/seongil-wi/2a44e082001b959bfe304b62121fb76d

## Flag

`DDC{m0r3_l1k3_3xpl01t4t10n_4s_4_53rv1c3}`
