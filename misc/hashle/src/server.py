from pwn import server
import hashlib
import random


FLAG = "DDC{1_l1k3_y0ur_Funny_w0rd5_m4g1c_m4n}"
GUESSES = 6


# Using a filtered and slightly reduced version of rockyou.txt (<100 MB)
with open("rockyou-reduced.txt", "rb") as f:
    print("Reading rockyou.txt...")
    passwords = f.read().split()


def cmp_hashes(pw_hash, guess_hash):
    # If g is in `word` n times, only mark partially correct up until the n'th occurrence in guess, excluding fully correct
    partial_counts = {
        c: pw_hash.count(c) - sum(c == w == g for w, g in zip(pw_hash, guess_hash)) for c in set(guess_hash)
    }
    result = ""
    for g, w in zip(guess_hash, pw_hash):
        if g == w:
            result += "■"
        elif g in pw_hash and partial_counts[g] > 0:
            result += "◩"
            partial_counts[g] -= 1
        else:
            result += "□"
    return result


def play(conn):
    conn.sendline(f"""
    '##::::'##::::'###:::::'######::'##::::'##:'##:::::::'########:
     ##:::: ##:::'## ##:::'##... ##: ##:::: ##: ##::::::: ##.....::
     ##:::: ##::'##:. ##:: ##:::..:: ##:::: ##: ##::::::: ##:::::::
     #########:'##:::. ##:. ######:: #########: ##::::::: ######:::
     ##.... ##: #########::..... ##: ##.... ##: ##::::::: ##...::::
     ##:::: ##: ##.... ##:'##::: ##: ##:::: ##: ##::::::: ##:::::::
     ##:::: ##: ##:::: ##:. ######:: ##:::: ##: ########: ########:
    ..:::::..::..:::::..:::......:::..:::::..::........::........::

Welcome to Hashle, the password guessing game!

The rules are simple:
I choose a random password from rockyou.txt and you have {GUESSES} tries to guess it.

When you make a guess, I will compute its MD5 hash and compare it to my password's hash.

For each hex digit in your hash, I will provide the following feedback:
    □: Not in my hash
    ◩: In my hash but incorrect position
    ■: In my hash and correct position

If you guess my password, I will give you a reward!

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Note: A hex digit can occur multiple times in a hash.
If so, you get feedback per occurrence you guess.
Examples with digit '2' on multiple positions in password hash:
    a232f       a232f       a232f       a232f
    82f1b       a425c       d27d2       e2820
    □■◩□□       ■□◩□□       □■□□◩       □■□■□

If a digit occurs N times but your hash contains it at >N positions,
only the best N positions will be marked:
    a232f       a232f
    f456f       0aa89
    □□□□■       □◩□□□

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

""".encode())
    password = random.choice(passwords)
    pw_hash = hashlib.md5(password).hexdigest()
    print(f"Randomly chosen password: {password.decode()} with MD5 hash {pw_hash}")

    for i in range(GUESSES):
        try:
            conn.send(f"Guess {i + 1} / {GUESSES}: ".encode())
            guess = conn.recvline().strip()
            guess_hash = hashlib.md5(guess).hexdigest()
            print(f"Guess: {guess.decode()} with MD5 hash {guess_hash}")
        except (OSError, EOFError):
            conn.close()
            return

        cmp = cmp_hashes(pw_hash, guess_hash)
        conn.sendline(f"         {guess_hash}".encode())
        conn.sendline(f"         {cmp}".encode())
        if guess == password:
            conn.sendline(f"\nCorrect! {FLAG}\n".encode())
            break
    else:
        conn.sendline(b"\nOut of guesses! No flag for you :P")

    conn.close()



if __name__ == "__main__":
    s = server(1337, callback=play)
    print("Waiting for connections...")
    while True:
        s.next_connection()
