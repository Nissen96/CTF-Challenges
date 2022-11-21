# Writeup

Connecting to the server - the chamber of secrets - we are greeted by a basilisk, requiring a codeword to let you pass.
We can here choose to guess the codeword or to get a "ssssneak peek" on the codeword checking code:

```
Thissss issss how I check if you are worthy of accessssing my ssssecret chamber.
Good luck underssstanding it, it'sssss in parsssseltongue:

  7           0 RESUME                   0

  8           2 LOAD_FAST                0 (codeword)
              4 LOAD_METHOD              0 (startswith)
             26 LOAD_CONST               1 ('DDC{')
             28 PRECALL                  1
             32 CALL                     1
             42 POP_JUMP_FORWARD_IF_FALSE    21 (to 86)
             44 LOAD_FAST                0 (codeword)
             46 LOAD_METHOD              1 (endswith)
             68 LOAD_CONST               2 ('}')
             70 PRECALL                  1
             74 CALL                     1
             84 POP_JUMP_FORWARD_IF_TRUE     2 (to 90)
        >>   86 LOAD_ASSERTION_ERROR
             88 RAISE_VARARGS            1

  9     >>   90 LOAD_GLOBAL              5 (NULL + len)
            102 LOAD_FAST                0 (codeword)
            104 PRECALL                  1
            108 CALL                     1
            118 LOAD_CONST               3 (39)
            120 COMPARE_OP               2 (==)
            126 POP_JUMP_FORWARD_IF_TRUE     2 (to 132)
            128 LOAD_ASSERTION_ERROR
            130 RAISE_VARARGS            1

 10     >>  132 LOAD_FAST                0 (codeword)
            134 LOAD_CONST               4 (21)
            136 BINARY_SUBSCR
            146 LOAD_CONST               5 ('d')
            148 COMPARE_OP               2 (==)
            154 POP_JUMP_FORWARD_IF_TRUE     2 (to 160)
            156 LOAD_ASSERTION_ERROR
            158 RAISE_VARARGS            1

 11     >>  160 LOAD_FAST                0 (codeword)
            162 LOAD_CONST               6 (13)
            164 BINARY_SUBSCR
            174 LOAD_GLOBAL              7 (NULL + chr)
            186 LOAD_GLOBAL              9 (NULL + ord)
            198 LOAD_FAST                0 (codeword)
            200 LOAD_CONST               7 (0)
            202 BINARY_SUBSCR
            212 PRECALL                  1
            216 CALL                     1
            226 LOAD_GLOBAL              9 (NULL + ord)
            238 LOAD_FAST                0 (codeword)
            240 LOAD_CONST               8 (9)
            242 BINARY_SUBSCR
            252 PRECALL                  1
            256 CALL                     1
            266 BINARY_OP               12 (^)
            270 PRECALL                  1
            274 CALL                     1
            284 COMPARE_OP               2 (==)
            290 POP_JUMP_FORWARD_IF_TRUE     2 (to 296)
            292 LOAD_ASSERTION_ERROR
            294 RAISE_VARARGS            1

 12     >>  296 LOAD_FAST                0 (codeword)
            298 LOAD_METHOD              5 (index)
            320 LOAD_CONST               9 ('my')
            322 PRECALL                  1
            326 CALL                     1
            336 LOAD_CONST              10 (23)
            338 COMPARE_OP               2 (==)
            344 POP_JUMP_FORWARD_IF_TRUE     2 (to 350)
            346 LOAD_ASSERTION_ERROR
            348 RAISE_VARARGS            1

 13     >>  350 LOAD_FAST                0 (codeword)
            352 LOAD_CONST              11 (8)
            354 LOAD_CONST              12 (12)
            356 BUILD_SLICE              2
            358 BINARY_SUBSCR
            368 LOAD_GLOBAL             13 (NULL + b64decode)
            380 LOAD_CONST              13 ('aDR2Mw==')
            382 PRECALL                  1
            386 CALL                     1
            396 LOAD_METHOD              7 (decode)
            418 PRECALL                  0
            422 CALL                     0
            432 COMPARE_OP               2 (==)
            438 POP_JUMP_FORWARD_IF_TRUE     2 (to 444)
            440 LOAD_ASSERTION_ERROR
            442 RAISE_VARARGS            1

 14     >>  444 LOAD_FAST                0 (codeword)
            446 LOAD_CONST              14 (6)
            448 LOAD_CONST              15 (3)
            450 LOAD_CONST              16 (-1)
            452 BUILD_SLICE              3
            454 BINARY_SUBSCR
            464 LOAD_CONST              17 ('u0y')
            466 COMPARE_OP               2 (==)
            472 POP_JUMP_FORWARD_IF_TRUE     2 (to 478)
            474 LOAD_ASSERTION_ERROR
            476 RAISE_VARARGS            1

 15     >>  478 LOAD_FAST                0 (codeword)
            480 LOAD_CONST              18 (37)
            482 BINARY_SUBSCR
            492 LOAD_FAST                0 (codeword)
            494 LOAD_CONST              19 (26)
            496 BINARY_SUBSCR
            506 COMPARE_OP               2 (==)
            512 POP_JUMP_FORWARD_IF_TRUE     2 (to 518)
            514 LOAD_ASSERTION_ERROR
            516 RAISE_VARARGS            1

 16     >>  518 LOAD_FAST                0 (codeword)
            520 LOAD_CONST              20 (28)
            522 LOAD_CONST              18 (37)
            524 BUILD_SLICE              2
            526 BINARY_SUBSCR
            536 LOAD_CONST              21 ('sS5')
            538 LOAD_GLOBAL             17 (NULL + int)
            550 LOAD_FAST                0 (codeword)
            552 LOAD_CONST              22 (27)
            554 BINARY_SUBSCR
            564 PRECALL                  1
            568 CALL                     1
            578 BINARY_OP                5 (*)
            582 COMPARE_OP               2 (==)
            588 POP_JUMP_FORWARD_IF_TRUE     2 (to 594)
            590 LOAD_ASSERTION_ERROR
            592 RAISE_VARARGS            1

 17     >>  594 LOAD_GLOBAL              9 (NULL + ord)
            606 LOAD_FAST                0 (codeword)
            608 LOAD_CONST              19 (26)
            610 BINARY_SUBSCR
            620 PRECALL                  1
            624 CALL                     1
            634 LOAD_CONST              23 (115)
            636 COMPARE_OP               4 (>)
            642 POP_JUMP_FORWARD_IF_FALSE    25 (to 694)
            644 LOAD_GLOBAL              9 (NULL + ord)
            656 LOAD_FAST                0 (codeword)
            658 LOAD_CONST              19 (26)
            660 BINARY_SUBSCR
            670 PRECALL                  1
            674 CALL                     1
            684 LOAD_CONST              24 (117)
            686 COMPARE_OP               0 (<)
            692 POP_JUMP_FORWARD_IF_TRUE     2 (to 698)
        >>  694 LOAD_ASSERTION_ERROR
            696 RAISE_VARARGS            1

 18     >>  698 LOAD_GLOBAL             17 (NULL + int)
            710 LOAD_FAST                0 (codeword)
            712 LOAD_CONST              22 (27)
            714 BINARY_SUBSCR
            724 PRECALL                  1
            728 CALL                     1
            738 LOAD_CONST              10 (23)
            740 LOAD_GLOBAL             17 (NULL + int)
            752 LOAD_FAST                0 (codeword)
            754 LOAD_CONST              25 (16)
            756 BINARY_SUBSCR
            766 PRECALL                  1
            770 CALL                     1
            780 BINARY_OP                6 (%)
            784 COMPARE_OP               2 (==)
            790 POP_JUMP_FORWARD_IF_TRUE     2 (to 796)
            792 LOAD_ASSERTION_ERROR
            794 RAISE_VARARGS            1

 19     >>  796 LOAD_FAST                0 (codeword)
            798 LOAD_CONST              26 (14)
            800 LOAD_CONST               4 (21)
            802 BUILD_SLICE              2
            804 BINARY_SUBSCR
            814 LOAD_CONST              27 ('s')
            816 LOAD_METHOD              9 (join)
            838 LOAD_CONST              28 ('a5S3')
            840 PRECALL                  1
            844 CALL                     1
            854 COMPARE_OP               2 (==)
            860 POP_JUMP_FORWARD_IF_TRUE     2 (to 866)
            862 LOAD_ASSERTION_ERROR
            864 RAISE_VARARGS            1

 20     >>  866 LOAD_FAST                0 (codeword)
            868 LOAD_METHOD             10 (count)
            890 LOAD_CONST              29 ('_')
            892 PRECALL                  1
            896 CALL                     1
            906 LOAD_CONST              30 (4)
            908 COMPARE_OP               2 (==)
            914 POP_JUMP_FORWARD_IF_TRUE     2 (to 920)
            916 LOAD_ASSERTION_ERROR
            918 RAISE_VARARGS            1
        >>  920 LOAD_CONST               0 (None)
            922 RETURN_VALUE
```

This output is Python disassembly, which we can reverse to get to the original Python code. The code is a number of `assert` statements, checking various properties of the codeword (e.g. length, first letters are `DDC{` etc.}). Reversing each part, we get the Python code:

```py
assert codeword.startswith("DDC{") and codeword.endswith("}")
assert len(codeword) == 39
assert codeword[21] == "d"
assert codeword[13] == chr(ord(codeword[0]) ^ ord(codeword[9]))
assert codeword.index("my") == 23
assert codeword[8:12] == b64decode("aDR2Mw==").decode()
assert codeword[6:3:-1] == "u0y"
assert codeword[37] == codeword[26]
assert codeword[28:28 + 9] == "sS5" * int(codeword[27])
assert ord(codeword[26]) > 115 and ord(codeword[26]) < 117
assert int(codeword[27]) == 23 % int(codeword[16])
assert codeword[14:21] == "s".join("a5S3")
assert codeword.count("_") == 4
```

Based on these checks, we can reverse the codeword that matches all criteria. This will be the flag, which as a check can be submitted to the basilisk, which will confirm it is correct and let you in:

```
That'ssss correct! Welcome inssside my chamber!

                ██████████
              ██░░░░░░░░░░██
              ██░░░░░░░░░░░░██
            ██░░██░░░░░░██░░██
            ██░░██░░░░░░██░░▒▒██
            ██░░░░░░░░░░░░░░▒▒██
              ██▒▒▒▒▒▒▒▒▒▒▒▒██
                ██████████████
            ████░░░░██░░░░▒▒████
          ██░░░░░░██░░░░░░▒▒██▒▒██
        ██░░░░██▒▒▒▒▒▒▒▒▒▒██░░▒▒▒▒██
        ██▒▒░░░░██████████░░░░▒▒██▒▒██
        ██▒▒░░░░░░░░░░░░░░░░░░▒▒██▒▒██
          ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████▒▒██
            ██████████████████    ██
```

## Flag

`DDC{y0u_h4v3_pas5sSs3d_my_t3sS5sS5sS5t}`
