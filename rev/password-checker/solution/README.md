# Writeup

This reverse engineering challenge is a simple password checker binary, compiled with no optimizations and with debugging symbols, meaning we have access to all function and variable names. The password is the flag, which we can derive using a few different solution paths:

**Static Analysis:**

Open the binary in any disassembler/decompiler and decompile the `main` function:

```c
int main(int argc, const char **argv, const char **envp) {
  char pwd[256];

  printf("Password: ");
  if ( fgets(pwd, 256, _bss_start) ) {
    puts("Validating...");
    sleep(1u);
    if ( check_password(pwd) )
      puts("Permission granted!");
    else
      puts("Invalid password!");
    return 0;
  } else {
    puts("Error reading from stdin!");
    return -1;
  }
}
```

This just asks for a password and runs `check_password` on the input:

```c
bool check_password(char *pwd) {
  int i;
  bool correct;

  correct = 1;
  for ( i = 0; i < 53; ++i ) {
    if ( pwd[i] != masked[i] - 66 )
      correct = 0;
  }
  return correct;
}
```

`check_password` runs a loop that compares the password input to a hardcoded character array called `masked`, subtracting 66 (0x42) from each masked character before comparing.
That means, we can find the password by extracting the `masked` array and subtract 0x42 from each byte. This is simple with e.g. Python:

```py
masked = bytes.fromhex("""
86 86 85 bd af 76 b5 ad 73 b0 a9 a1 af bb a1 b2
76 b5 b5 b9 72 b4 a 72 b7 ae a6 a1 a4
75 a1 a9 72 72 a6 a1 75 b0 72 b7 a9 aa a1 b4 73
a9 aa b6 81 bf
""")
password = bytes([c - 0x42 for c in masked]).decode()
```

**Dynamic Analysis:**

Debug the program with `gdb`, inspect the functions names, and break on `check_password`.
Give the program a random long password for testing, e.g. just 50 `A`s.
Now step through the password checking loop until getting to the comparison between the first input character and first actual password character (at `<check_password+60>  cmp  dl, al`).
Notice the input character is stored in RDX and actual password character in RAX. Note down the value of RAX - this is the first character of the actual password.
Create a breakpoint at this comparison with `break *(check_password+60)`, and then continually run through the loop with `continue`, noting down each expected password char.
At the end, you have all the expected password chars - without needing to know exactly how each was derived.

## Flag

`DDC{m4sk1ng_my_p4ssw0rd_5h0uld_b3_g00d_3n0ugh_r1ght?}`
