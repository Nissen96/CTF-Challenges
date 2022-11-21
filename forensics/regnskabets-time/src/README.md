# Challenge Generation

The script `gen_challenge.py` can be used to automatically generate the challenge *if* you are running Windows.
This uses the Python module `pywin32`, which can be installed on Windows with `pip install pywin3`.
The script automatically generates the entire Excel file with the macros included - you can then manually insert the instructional image in the spreadsheet.
Note, this image is in Danish - should probably be translated for general use.

The challenge is basically just a classic Excel macro which runs a PowerShell command that downloads a malicious script from an attacker's website and runs it.
The flag is contained in the PowerShell script, which is base64 encoded, so it can be run with `powershell -e B64-SCRIPT-HERE`.

The Python script takes the powershell command string, encrypts it with `KEY`, and inserts it in the VBA macro code.
The VBA macro itself then contains a decryption function to decrypt the command string before running it.
The key for this is set in a small different macro script called `SecretGen`.

Additional obfuscation has been added by:

  * Inserting random unused variables
  * Inserting a few useless loops
  * Renaming all variables to a random text string
  * Removing all indentation and extra newlines

Step 3 and 4 are performed by the `obfuscate` function.

The script can also be run with `python3 gen_challenge.py DEBUG`, which will skip obfuscation step 3 and 4 to make the resulting code more readable.
This will also add a debug print statement to the code to print the decrypted powershell script, ensuring it looks correct.
