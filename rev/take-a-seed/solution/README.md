# Writeup

We are given a stripped binary and the output of an encryption of the flag. Some reversing is required first:

* Open the binary in a decompiler such as Ghidra or IDA and decompile
* With IDA, you will see a main function like below:

```c
stream = fopen("flag.txt", "r");
fgets(s, 1008, stream);
v10 = strlen(s);
v9 = 16 - v10 % 16;
for ( i = 0; i < v9; ++i )
  s[v10 + i] = v9;
v8 = v10 + v9;
*(_QWORD *)seed = time(0LL);
srand(seed[0]);
for ( j = 0; j <= 15; ++j )
  v5[j] = rand();
sub_15FB(v4, off_5050, v5);
sub_24D7(v4, s, (int)v8);
sub_11A9(s, v8);
return 0LL;
```

The first part quite clearly reads the flag into `s` and the length is found. Then a small piece of code that experienced rev players should be familiar with: adding padding to make the input 16-byte aligned, hinting at a block cipher. After this, a seed is set based on the time, and 16 random bytes inserted in `v5`.

Then three unknown functions are called. Opening the last of these, we see it simply prints a byte array as hex. In the first of the function calls, we have a global variable, `off_5050`, and inspecting its contents, we see it is a 16-byte string, `"bprsuyndnuecrkne"`. So the first function takes this hardcoded string, the random 16-byte array, and a final variable `v4`, which is also used in the second function call. This call also contains the plaintext `s` and its length in `v8`.

More experienced reverse engineers should again spot the block encryption here fairly quickly. It is very usual in encryptions, hashing, etc. to have a first function call setting up the encryption context which takes the key and IV, and then the actual encryption afterwards. This fits what we have seen well, and so `"bprsuyndnuecrkne"` is most likely the key (since this is hardcoded) and the random string the IV (since this should not be reused).

The type of encryption can be found to be AES in multiple ways, either by looking at the function calls or finding the (well known) S-box in the `.rodata` section almost immediately after where the key was found. Alternatively, this is so well known ChatGPT will also likely identify it :) Renaming based on this info yields a quite readable piece of code:

```c
// Read flag
stream = fopen("flag.txt", "r");
fgets(flag, 1008, stream);
len = strlen(flag);

// Pad flag
padding = 16 - len % 16;
for ( i = 0; i < padding; ++i )
  flag[len + i] = padding;
total_len = len + padding;

// Generate random IV based on padding
*seed = time(0);
srand(seed);
for ( i = 0; i <= 15; i++ )
  iv[i] = rand();

// Encrypt flag and output result as hex
AES_setup(ctx, key, iv);
AES_encrypt(ctx, flag, total_len);
print_hex(flag, total_len);

return 0;
```

To decrypt this, the same key and IV must be used, but the IV is not immediately known. For those unaware, in CBC mode, the IV is only needed to decrypt the first block, all remaining blocks only depend on previous ciphertext blocks. This means that most of the flag is possible to decrypt by using the found key and any random IV, resulting in 16 bytes of garbage followed by `f0r_AES-d1d_y0u_5ne4k_p34k_w17h_4_r4nd0m_1V?}` as a small easter egg.

The IV is, however, needed to decrypt the first block. The description hints quite a lot that the encryption was done during DDC regionals 2023, and so the seed and thus IV can be bruteforced.

A [solve script](solve.c) has been provided, which does exactly this: iterates from the start time to the end time of the competition, generates the IV for this, and tries to decrypt the ciphertext, checking whether the result matches the flag format. This should be doable with any AES library like the most used one from here: https://github.com/kokke/tiny-AES-c/.

People less comfortable with C can avoid having to integrate with an AES library by just generating all the possible IVs, saving them to a file, and do the bruteforcing decryption in e.g. Python.

## Flag

`DDC{1V_533d_r3v_f0r_AES-d1d_y0u_5ne4k_p34k_w17h_4_r4nd0m_1V?}`
