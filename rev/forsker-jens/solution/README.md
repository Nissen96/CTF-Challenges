# Writeup

Inspecting the validation code, we have first a username validation. This simply just checks whether the username is `J3n5_MyruP_3r_5up3r_s3j_l0lz!!`.

Following this is a number of checks for the password:

```py
len(password) == len(username)
password.startswith("$Correct")
password[15] == "B"
password[13] == password[5]
password[11] == "r"
password[9] == "H"
password[12] == "s"
password[10] == "o"
"Battery" in password
password[8] == password[14] == password[22] == "-"
password.endswith("Staple$")
```

We see the password must have the same length as the username, and using each check, we can recover pieces of the password:

```
______________________________
$Correct______________________
$Correct_______B______________
$Correct_____e_B______________
$Correct___r_e_B______________
$Correct_H_r_e_B______________
$Correct_H_rse_B______________
$Correct_Horse_B______________
$Correct-Horse-B______-_______
$Correct-Horse-B______-Staple$
$Correct-Horse-Battery-Staple$
```

Logging in with these credentials, we get access to the secret security research:

```
VELKOMMEN TILBAGE, JENS!
+=====================================================+
| Superhemmelig igangværende security research:       |
| https://vbn.aau.dk/ws/files/484572782/WACCO2022.pdf |
|                                                     |
| Dagens XKCD: https://xkcd.com/936/                  |
+=====================================================+
DDC{53cur17y_pr0f3ss0r_h4ck3d}
```

## Flag

`DDC{53cur17y_pr0f3ss0r_h4ck3d}`
