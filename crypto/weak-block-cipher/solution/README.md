# Writeup

This crypto challenge is meant to showcase how easily some weak block cipher can be broken, in this case in ECB mode through a single known block of a (plaintext, ciphertext)-pair.
An encrypted flag is provided together with the encryption function it was encrypted with.

The encryption function splits the message into 8-character blocks. The key is used to generate a permutation, which is used on each block to shuffle them.
Guessing the plaintext starts with `'The flag'`, the permutation can be easily found by mapping the known chars to their position in the ciphertext.
The message is decrypted by using the leaked permutation on each block to recover the corresponding plaintext block.

See `solve.py` for a solution script.

## Flag

`DDC{Sw1pp1ty_sw4pp1ty_y0ur_pl41nt3xt_1s_n0w_my_pr0p3rty}`