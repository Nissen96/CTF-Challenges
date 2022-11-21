from pydantic import BaseModel


class DiaryEntryBase(BaseModel):
    title: str | None = None
    content: str | None = None
    is_public: bool


class DiaryEntryCreate(DiaryEntryBase):
    pass


class DiaryEntry(DiaryEntryBase):
    id: str
    author_id: str
    author_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    diary_entries: list[DiaryEntry] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Credentials(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class JWK(BaseModel):
    alg: str
    kty: str
    use: str
    n: str
    e: str
    kid: str


class JWKSet(BaseModel):
    keys: list[JWK]
