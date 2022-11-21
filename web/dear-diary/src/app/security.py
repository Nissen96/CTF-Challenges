from base64 import urlsafe_b64decode
from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA
from fastapi import HTTPException, status, Depends
from fastapi.security.http import HTTPBearer, HTTPBasicCredentials
from httpx import AsyncClient
from jose import jwt
from passlib.context import CryptContext
from simplejson.errors import JSONDecodeError
from sqlalchemy.orm import Session
from urllib.parse import urlparse

from . import crud, schemas
from .config import settings
from .database import SessionLocal


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth = HTTPBearer(auto_error=False)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    """
    Checks user credentials and returns matching user from DB
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_jwt(user_id: int):
    """
    Creates and signs a JSON Web Token for the given user
    """
    return jwt.encode(
        { "user_id": user_id },
        settings.PRIVATE_KEY,
        algorithm="RS256", 
        headers={
            "jku": f"http://{settings.AUTH_NETLOC}/api/keys",
            "kid": settings.KID
        }
    )


async def fetch_jku(url: str) -> schemas.JWKSet:
    """
    Returns a list of keys from a given JWK Set URL (JKU)
    """
    # Ensure URL from JWT matches configured auth URL
    parsed_url = urlparse(url)
    if parsed_url.netloc != settings.AUTH_NETLOC:
        raise credentials_exception
    
    from . import main
    async with AsyncClient(app=main.app) as ac:
        jwks = await ac.get(url)

    try:
        return schemas.JWKSet(**jwks.json())
    except JSONDecodeError:
        raise credentials_exception


async def get_jwk(url: str, kid: str):
    """
    Returns a JSON Web Key from a JKU based on the provided Key ID
    """
    jwks = await fetch_jku(url)

    jwk = next(filter(lambda j: j.kid == kid, jwks.keys), None)
    if jwk is None:
        raise credentials_exception

    return jwk


async def decode_jwt(token: str):
    """
    Verifies and decodes the provided JWT using the corresponding JWK
    """
    try:
        headers = jwt.get_unverified_header(token)
    except (jwt.JWTError):
        raise credentials_exception

    if not (jku := headers.get("jku")):
        raise credentials_exception

    if not (kid := headers.get("kid")):
        raise credentials_exception

    # Get JSON Web Key from the specified JKU matching the specified KID
    jwk = await get_jwk(jku, kid)

    # Get RSA public key from JWK
    n = bytes_to_long(urlsafe_b64decode(jwk.n))
    e = bytes_to_long(urlsafe_b64decode(jwk.e))
    rsa_key = RSA.construct((n, e))

    # Verify token with RSA public key retrieved from JKU
    try:
        claim = jwt.decode(
            token,
            rsa_key.export_key(),
            algorithms=["RS256"]
        )
    except (jwt.JWTError, jwt.JWTClaimsError):
        raise credentials_exception

    return claim


async def get_current_user(db: Session = Depends(get_db), creds: HTTPBasicCredentials = Depends(auth)) -> schemas.User | None:
    """
    Get user matching the id in the provided JWT if valid
    """
    if creds is None:
        return None
    
    token = creds.credentials

    claim = await decode_jwt(token)

    user_id = claim.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = crud.get_user(db, user_id)
    if user is None:
        raise credentials_exception

    return user
