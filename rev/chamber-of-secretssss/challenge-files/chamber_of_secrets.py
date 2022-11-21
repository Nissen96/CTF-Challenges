import dis
from base64 import b64decode

FLAG = "DDC{y0u_h4v3_pas5sSs3d_my_t3sS5sS5sS5t}"


def check_codeword(codeword):
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


if __name__ == "__main__":
    check_codeword(FLAG)  # Sanity check
    dis.dis(check_codeword)
