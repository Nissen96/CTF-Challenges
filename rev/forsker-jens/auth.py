def xor(s1, s2):
    return bytes([s1[i % len(s1)] ^ s2[i % len(s2)] for i in range(max(len(s1), len(s2)))])


# Ingen adgang for andre end mig!

username = input("Indtast brugernavn:\n> ")
if username != "J3n5_MyruP_3r_5up3r_s3j_l0lz!!":
    print(f"Hey, det er kun Jens, der har adgang her!")
    exit()


# Password check hvis nogen finder mit brugernavn
# Overholder naturligvis alle nyeste anbefalinger

password = input("\nIndtast password:\n> ")
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
print("\nVELKOMMEN TILBAGE, JENS!")
print(xor(b'EM<z\x10\x15\';e%\r|<\x07%\n,z;\x07<wz1%l!+y8SM<z\x10\x15\';e%\r|<\x07%\n,z;\x07<wz13[`6\x17p\x1e\x15s/HEwc4qWah]yYv1\xc5\x9cs/)h}qos\'p\x1c\x19u>\rZ\x7fu=yB"i\x008\x171g&\x1a!6Mp89hb4vT_.1OF4g9m\x1e%j\x15oD>!oVd9h8 e)!v2VB.\x10lkYIj(\x02s/J|Q1;\x0cF!jg,8q<6d%NP!g\r\x08:&x8\x10a!\x1a8\x171g&\x1a!jg,8q<6d%NP!g\r\x08:&x8\x10a!F\x12K1\x03g]d$4,@\x1a_R~%\x06\x04u7^\x125) sS%/YwZ>~5\x0c.jg,8q<6d%NP!g\r\x08:&xd:j<\x07%\n,z;\x07<wz1%l!+y8SM<z\x10\x15\';e%\r|<\x07%\n,z;\x07<wz1%l!+y8SM<z\x10\x03\x10B\x1c[Kt2YmE p\x7feq8wj+"o&6Z\x06Db,\x1eLg', key).decode())
