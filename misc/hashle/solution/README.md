# Writeup

Connecting to the server, we get access to a Wordle-inspired game called Hashle.

In this game, the server chooses a random password from `rockyou.txt` and we have 6 attempts to guess it.
The catch is, that we only get information on the similarity of the password hash and guess hash.
When sending a guess, it is MD5-hashed and the hash is compared to the hash of the correct password.
For each hash character position, we get feedback on whether that character is *not* in the hash, *is* in the hash but at an *incorrect* position, or *is* in the hash at that position.

If at some point, we can deduce the correct hash, we then need to find the corresponding password and send this to get the flag.

The idea is to compute the hash of all passwords in `rockyou.txt`, make random guesses, and exclude all password-hash pairs, that do not fit the feedback.

Specifically, we start by sending an initial guess, e.g. `abc` to the server.
We then hash every password in `rockyou.txt` but only store those that fit the feedback to avoid storing the very large list of all password-hash pairs.
Then continually send a random password from the list of remaining options, get feedback, reduce the hash list, and repeat.
Do this until only one password-hash pair remains - this must be the right password, and sending this, we get the flag.

See [solve.py](solve.py) for an implementation of this solution.

## Flag

`DDC{1_l1k3_y0ur_Funny_w0rd5_m4g1c_m4n}`
