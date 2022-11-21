from pydantic import BaseModel, BaseSettings
from Crypto.PublicKey import RSA


# Custom RsaKey model to play nicely with pydantic
class RsaKey(BaseModel):
    n: int
    e: int


KEY = RSA.generate(2048)

class Settings(BaseSettings):
    KID: str = "dear-diary-key"
    PUBLIC_KEY: RsaKey = RsaKey(n=KEY.public_key().n, e=KEY.public_key().e)
    PRIVATE_KEY: str = KEY.export_key()
    AUTH_NETLOC: str = "dear-diary.hkn"

settings = Settings()
