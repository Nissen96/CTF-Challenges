from base64 import urlsafe_b64encode
from Crypto.Util.number import long_to_bytes
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import crud, schemas, security
from .config import settings
from .database import SessionLocal


api_router = APIRouter()


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@api_router.get("/keys", response_model=schemas.JWKSet)
def keys():
    """
    Return public keys as a list of JWKs
    """
    key = settings.PUBLIC_KEY
    return {
        "keys": [{
            "alg": "RS256",
            "kty": "RSA",
            "use": "sig",
            "n": urlsafe_b64encode(long_to_bytes(key.n)).decode(),
            "e": urlsafe_b64encode(long_to_bytes(key.e)).decode(),
            "kid": settings.KID,
        }]
    }


@api_router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user - username must be unique
    """
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    return crud.create_user(db, user)


@api_router.get("/users/me", response_model=schemas.User)
def get_current_user(current_user: schemas.User | None = Depends(security.get_current_user)):
    """
    Get info for currently logged in user
    """
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No currently logged in user")
    return current_user


@api_router.post("/entries", response_model=schemas.DiaryEntry)
def create_diary_entry(entry: schemas.DiaryEntryCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(security.get_current_user)):
    """
    Add a new entry to the diary
    """
    if current_user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Only authorized users can add new diary entries")
    
    if len(entry.title) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
    if len(entry.title) > 30:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be longer than 30 characters")
    if len(entry.content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty")
    if len(entry.content) > 500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be longer than 500 characters")

    return crud.create_entry(db, entry, current_user.id, current_user.username)


@api_router.get("/entries", response_model=list[schemas.DiaryEntry])
def list_diary_entries(db: Session = Depends(get_db), current_user: schemas.User | None = Depends(security.get_current_user)):
    """
    Return diary entries the user has access to (public + optionally own private entries if logged in)
    """
    if current_user is None:
        return crud.get_entries(db)
    return crud.get_entries(db, current_user.id)


@api_router.get("/entries/{entry_id}")
def get_diary_entry_content(entry_id: str, db: Session = Depends(get_db), current_user: schemas.User | None = Depends(security.get_current_user)):
    """
    Get the raw content of specific diary entry.
    Only allowed for public entries and user's own private entries
    """
    if current_user is None:
        diary_entry = crud.get_entry(db, entry_id)
    else:
        diary_entry = crud.get_entry(db, entry_id, current_user.id)
    
    if diary_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found"
        )
    
    return Response(content=diary_entry.content)


@api_router.post("/login", response_model=schemas.Token)
async def login(creds: schemas.Credentials, db: Session = Depends(get_db)):
    user = security.authenticate_user(db, creds.username, creds.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    jwt = security.create_jwt(user.id)
    return {"access_token": jwt, "token_type": "bearer"}
