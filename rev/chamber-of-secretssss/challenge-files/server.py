from pwn import server
from chamber_of_secrets import FLAG, check_codeword
import dis


def get_codeword(conn):
    conn.send("""
                                    ██░░░░████░░░░░░██░░██
                                    ██▒▒  ▒▒████▒▒  ▒▒░░░░████
                                    ██░░░░░░░░░░░░░░░░░░░░░░░░░░██████
                                    ██░░░░██░░░░██░░░░░░██▒▒░░░░▒▒░░▒▒██
                                ████░░░░░░░░░░░░░░░░██░░░░████████░░▒▒██
                                ██░░██▒▒▒▒▒▒██████▒▒██░░░░████▓▓▓▓▓▓▓▓██░░██
                            ▓▓▒▒░░██  ▓▓▒▒██████░░██░░▒▒████▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                            ██▒▒░░████  ██▓▓██▒▒██  ██░░████▒▒██▓▓▓▓▓▓▓▓██░░██
                            ██░░██▓▓██  ██▓▓██▒▒██  ██░░██▒▒████▓▓▓▓▓▓▓▓▓▓██▒▒██
                        ██▒▒██▓▓▓▓██  ██▓▓██▒▒██  ██░░████▒▒██▓▓▓▓▓▓▓▓▓▓██░░██
                        ██░░██▓▓▓▓▓▓██  ████▒▒██  ████▒▒▒▒████▓▓▓▓▓▓▓▓▓▓██▒▒██
                        ██▒▒██▓▓▓▓▓▓████████▒▒▒▒██░░██████▒▒██▓▓▓▓▓▓▓▓▓▓██░░██
                        ██░░██▓▓▓▓▓▓▓▓██████▒▒▒▒██░░██▒▒██████▓▓▓▓▓▓▓▓▓▓██▒▒██
                        ██▒▒██▓▓▓▓▓▓▓▓▓▓████▒▒▒▒░░██████▒▒▒▒██▓▓▓▓▓▓▓▓▓▓▓▓██░░
                        ██░░██▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░░░██▒▒▒▒▒▒████▓▓▓▓▓▓▓▓▓▓▓▓▒▒██
                        ██▒▒██▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░████▒▒▒▒████▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░██
                        ████▒▒██▓▓▓▓▓▓▓▓▓▓▓▓██████████████▒▒██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒██
                        ████░░▒▒██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▒▒████▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
                        ██████░░▒▒██▓▓▓▓▓▓▓▓▓▓▓▓██████████▒▒██▓▓▓▓▓▓▓▓▓▓▓▓████
                        ████▒▒░░▒▒██▓▓██▓▓▓▓██▒▒▒▒▒▒▒▒▒▒████▓▓▓▓▓▓▓▓▓▓████
                        ████░░▒▒░░▒▒██████████████████████▓▓▓▓▓▓██▓▓████
                        ██████░░▒▒░░████████▒▒▒▒▒▒▒▒▒▒▒▒████████▒▒████
                            ██████░░▒▒░░██▒▒▒▒████████████████░░▒▒████
                            ██████░░██████▒▒▒▒▒▒▒▒▒▒██████░░▒▒████    ████
                            ██████████▒▒▒▒██████████████▒▒░░▒▒████    ██▒▒░░██
                        ████▒▒░░▒▒██████████▒▒▒▒▒▒████▒▒░░▒▒████  ████▒▒░░▒▒░░██
                    ██░░▒▒░░▒▒██▒▒▒▒▒▒▒▒██████████░░░░██████████░░▒▒░░▒▒░░▒▒██
                    ██░░▒▒░░▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒████░░▒▒████████▒▒░░▒▒░░▒▒░░▒▒░░██
                    ██▒▒░░▒▒████████████████▒▒██▒▒▒▒██████▒▒░░░░▒▒░░▒▒░░▒▒░░▒▒██
                    ████▒▒░░██▒▒▒▒▒▒▒▒▒▒▒▒██████░░▒▒████▒▒░░▒▒░░░░▒▒░░▒▒░░▒▒████
                    ██░░██▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒░░████▒▒░░▒▒░░▒▒░░░░▒▒░░▒▒██▒▒██
                    ████▒▒████████████████████░░▒▒██▒▒░░▒▒░░▒▒░░▒▒░░░░████▒▒░░██
                    ██▒▒██░░██▒▒▒▒▒▒▒▒▒▒████░░▒▒░░▒▒░░▒▒░░▒▒░░▒▒░░████░░████████
                    ████▒▒██████████████████▒▒░░▒▒░░▒▒░░▒▒░░▒▒░░▒▒░░████▒▒░░██
                    ████████▒▒▒▒▒▒▒▒██████░░▒▒░░▒▒░░▒▒░░▒▒░░██████▒▒░░████
                            ██████████████████░░██░░▒▒████████░░▒▒░░████
                            ██████████████▒▒██░░████░░▒▒░░▒▒██████
                                ██████████▒▒██░░████▒▒████████
                                    ████████████████████

        ▄████▄   ██░ ██  ▄▄▄       ███▄ ▄███▓ ▄▄▄▄   ▓█████  ██▀███      ▒█████    █████▒
        ▒██▀ ▀█  ▓██░ ██▒▒████▄    ▓██▒▀█▀ ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒   ▒██▒  ██▒▓██   ▒
        ▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄  ▓██    ▓██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒   ▒██░  ██▒▒████ ░
        ▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██ ▒██    ▒██ ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄     ▒██   ██░░▓█▒  ░
        ▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒▒██▒   ░██▒░▓█  ▀█▓░▒████▒░██▓ ▒██▒   ░ ████▓▒░░▒█░
        ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ░  ░░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░   ░ ▒░▒░▒░  ▒ ░
        ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░░  ░      ░▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░     ░ ▒ ▒░  ░
        ░         ░  ░░ ░  ░   ▒   ░      ░    ░    ░    ░     ░░   ░    ░ ░ ░ ▒   ░ ░
        ░ ░       ░  ░  ░      ░  ░       ░    ░         ░  ░   ░            ░ ░
        ░                                           ░
                    ██████ ▓█████  ▄████▄   ██▀███  ▓█████▄▄▄█████▓  ██████
                    ▒██    ▒ ▓█   ▀ ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀▓  ██▒ ▓▒▒██    ▒
                    ░ ▓██▄   ▒███   ▒▓█    ▄ ▓██ ░▄█ ▒▒███  ▒ ▓██░ ▒░░ ▓██▄
                    ▒   ██▒▒▓█  ▄ ▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄░ ▓██▓ ░   ▒   ██▒
                    ▒██████▒▒░▒████▒▒ ▓███▀ ░░██▓ ▒██▒░▒████▒ ▒██▒ ░ ▒██████▒▒
                    ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒ ░░   ▒ ▒▓▒ ▒ ░
                    ░ ░▒  ░ ░ ░ ░  ░  ░  ▒     ░▒ ░ ▒░ ░ ░  ░   ░    ░ ░▒  ░ ░
                    ░  ░  ░     ░   ░          ░░   ░    ░    ░      ░  ░  ░
                        ░     ░    ░                      ░              ░

                                    What would you like to do?
                                      1: Get a ssssneak peek
                                      2: Accessss my chamber
                                              > """.encode())

    choice = conn.recvline().strip()
    if choice not in b"12":
      conn.sendline(b"What'sssss going on? That'ssss not a valid option, sssssee ya")
      conn.close()
      return

    if choice == b"1":
      conn.sendline("""

Thissss issss how I check if you are worthy of accessssing my ssssecret chamber.
Good luck underssstanding it, it'sssss in parsssseltongue:
""".encode())
      conn.send(dis.Bytecode(check_codeword).dis().encode())
      conn.close()
      return

    conn.send("""
    What'sssss the sssecret codeword?    ____
________________________________________/ O  \___/
_/_\_/_\_/_\_/_\_/_\_/_\_/_\_/_\_/_\_/_______/   \  """.encode())
    codeword = conn.recvline().strip().decode()

    try:
        check_codeword(codeword)
        assert codeword == FLAG
        conn.sendline(f"""

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

                             {FLAG}
""".encode())
    except AssertionError:
        conn.send('''

                        Thisss codeword isss incorrect!

                                                 .o@*hu
                          ..      .........   .u*"    ^Rc
                        oP""*Lo*#"""""""""""7d" .d*N.   $
                       @  u@""           .u*" o*"   #L  ?b
                      @   "              " .d"  .d@@e$   ?b.
                     8                    @*@me@#         '"Nu
                    @                                        '#b
                  .P                                           $r
                .@"                                  $L        $
              .@"                                   8"R      dP
           .d#"                                  .dP d"   .d#
          xP              .e                 .ud#"  dE.o@"(
          $             s*"              .u@*""     '""\\dP"
          ?L  ..                    ..o@""        .$  uP
           #c:$"*u.             .u@*""$          uR .@"
            ?L$. '"""***Nc    x@""   @"         d" JP
             ^#$.        #L  .$     8"         d" d"
               '          "b.'$.   @"         $" 8"
                           '"*@$L $"         $  @
                           @L    $"         d" 8\\
                           $$u.u$"         dF dF
                           $ """   o      dP xR
                           $      dFNu...@"  $
                           "N..   ?B ^"""   :R
                             """"* RL       d>
                                    "$u.   .$
                                      ^"*bo@"

                Leave now or ssssuffer the consssequencesss!'''.encode())
    finally:
        conn.close()


if __name__ == "__main__":
    s = server(5555, callback=get_codeword)
    print("Waiting for connections...")
    while True:
        s.next_connection()
