from pwn import *
from tqdm import tqdm
import hashlib


io = remote("0.0.0.0", 1337)


def make_guess(guess):
    print(f"Sending guess '{guess}'...\n")
    io.sendlineafter(b"6: ", guess.encode())
    guess_hash = io.recvline().strip().decode()
    feedback = io.recvline().strip().decode()
    print(f"Hash:     {guess_hash}")
    print(f"Feedback: {feedback}\n")
    return guess_hash, feedback


def update_hash_digit_options(guess_hash, feedback, hash_digit_options):
    for i, (c, fb) in enumerate(zip(guess_hash, feedback)):
        # Correct digit: set as only option
        if fb == "■":
            hash_digit_options[i] = {c}
        # Incorrect position: remove as option for this position
        elif fb == "◩":
            hash_digit_options[i] -= {c}
        # Incorrect digit: remove as option for this position
        elif fb == "□":
            hash_digit_options[i] -= {c}

            # If same digit appears partially correct elsewhere, we know nothing more
            for ci, f in zip(guess_hash, feedback):
                if ci == c and f == "◩":
                    break
            else:
                # Else, remove as option for all positions where it is not already known to be correct
                for j, (ci, f) in enumerate(zip(guess_hash, feedback)):
                    if ci == c and f == "■":
                        continue
                    hash_digit_options[j] -= {c}


def main():
    print("Reading rockyou.txt...\n")
    with open("/usr/share/wordlists/rockyou.txt", "rb") as f:
        passwords = f.read().split()

    # Keep a set per hash digit of options still left
    hash_digit_options = [set("0123456789abcdef") for _ in range(32)]

    # Make initial guess and store all password hashes that match
    # This is just to avoid storing them all in a list or file, as this would be very large
    guess_hash, feedback = make_guess("abc")
    update_hash_digit_options(guess_hash, feedback, hash_digit_options)

    print("Hashing all passwords and storing hashes that match first guess")
    hashes_left = {}
    for pwd in tqdm(passwords):
        hash = hashlib.md5(pwd).hexdigest()
        if all(digit in digit_options for digit, digit_options in zip(hash, hash_digit_options)):
            hashes_left[hash] = pwd

    for guess in "abcd":
        print(f"\nPossible hashes remaining: {len(hashes_left)}\n")
        guess_hash, feedback = make_guess(guess)
        update_hash_digit_options(guess_hash, feedback, hash_digit_options)
        print("Filtering out now impossible hashes...")
        hashes_left = {hash: hashes_left[hash] for hash in hashes_left if all(digit in digit_options for digit, digit_options in zip(hash, hash_digit_options))}

        if len(hashes_left) == 1:
            break

    if len(hashes_left) > 1:
        print("\nCouldn't find the correct hash in 6 guesses, try running again.")
        return

    correct_hash = list(hashes_left)[0]
    password = hashes_left[correct_hash]  # Also easily crackable if you didn't store passwords with their hashes

    print(f"\nLast hash remaining: {correct_hash}")
    print(f"Corresponding password: {password.decode()}\n")

    print(f"Sending password {password.decode()}...\n")
    io.sendlineafter(b"6: ", password)

    io.interactive()


if __name__ == "__main__":
    main()
