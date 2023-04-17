def xor(s1, s2):
    return bytes([s1[i % len(s1)] ^ s2[i % len(s2)] for i in range(max(len(s1), len(s2)))])

# Can be changed
flag     = "DDC{53cur17y_pr0f3ss0r_h4ck3d}"
username = "J3n5_MyruP_3r_5up3r_s3j_l0lz!!"
secret = f"""
+=====================================================+
| Superhemmelig igangværende security research:       |
| https://vbn.aau.dk/ws/files/484572782/WACCO2022.pdf |
|                                                     |
| Dagens XKCD: https://xkcd.com/936/                  |
+=====================================================+
{flag}
""".strip().encode()

# Validation - don't change!
password = "$Correct-Horse-Battery-Staple$"
assert len(flag) == len(password), "flag must have same length as password"
assert len(username) == len(password), "username must have same length as password"

key = xor(username.encode(), password.encode())
secret = xor(secret, key)

code = f"""
def xor(s1, s2):
    return bytes([s1[i % len(s1)] ^ s2[i % len(s2)] for i in range(max(len(s1), len(s2)))])


# Ingen adgang for andre end mig!

username = input("Indtast brugernavn:\\n> ")
if username != "{username}":
    print(f"Hey, det er kun Jens, der har adgang her!")
    exit()


# Password check hvis nogen finder mit brugernavn
# Overholder naturligvis alle nyeste anbefalinger

password = input("\\nIndtast password:\\n> ")
if not all([
    len(password) == len(username),
    password.startswith("$Correct"),
    password[15] == "B",
    password[13] == password[5],
    password[11] == "r",
    password[9] == "H",
    password[12] == "s",
    password[10] == "o",
    "Battery" in password,
    password[8] == password[14] == password[22] == "-",
    password.endswith("Staple$")
]):
    print("Næh, forkert password, smut!")
    exit()


# Umuligt at nogen gætter mine credentials
# Nu kan jeg vist godt bare give adgang til mine filer

key = xor(username.encode(), password.encode())
print("\\nVELKOMMEN TILBAGE, JENS!")
print(xor({secret}, key).decode())
""".strip()

print(code)
