import random
import string

from sqlalchemy.orm import Session

from . import schemas, crud
from .database import Base, engine, SessionLocal


def gen_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(alphabet) for _ in range(length))


def populate_db(db: Session) -> None:
    # Admin user
    admin_password = gen_password(30)
    admin = crud.create_user(db, schemas.UserCreate(username="admin", password=admin_password))
    print(f"Admin password: {admin_password}")

    # Initial admin diary entries
    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="The Start of Something New",
        content="Dear Diary,\n\nI'm really excited to start documenting my life through you!\nI can finally share my daily experiences with all my friends while keeping my personal stories secret.\nYou will be my companion through it all ❤️\n\nXOXO",
        is_public=True
    ), author_id=admin.id, author_name=admin.username)
    
    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="Don't Tell Anyone!",
        content="Dear Diary,\n\nMy heart is pumping like crazy right now! 💓\nI just met this really cute guy online and we chatted all night! 💻\nWe just connected on such a deep level immediately and he was so sweet and insightful ❤️\nI don't even know his real name yet, but he's my\n🥩 MrBeef 🥩\n\nXOXO",
        is_public=False
    ), author_id=admin.id, author_name=admin.username)

    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="Trip to Hawaii",
        content="Dear Diary,\n\nI just came back from Hawaii and it was\nA-M-A-Z-I-N-G\nWe went to see Kīlauea, the most active volcano in the world 🌋 - super impressive!\nWe also snorkeled in beautiful choral reefs at Hanauma Bay 🐠 and chilled on the beach 🌊 every evening with drinks 🍹 around the fire 🔥.\nI already miss it so much, I'm definitely going back another time!\n\nXOXO",
        is_public=True
    ), author_id=admin.id, author_name=admin.username)

    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="🚩 FLAG 🚩",
        content="DDC{d34r_d14ry_t0d4y_I_sp00f3d_4_JWK_d0n7_t311_4ny0n3_X0X0}",
        is_public=False
    ), author_id=admin.id, author_name=admin.username)

    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="Sharing is Caring",
        content="Dear Diary,\n\nToday I'm opening you up to the world so everyone can share their thoughts or store their personal stories privately.\nI'm super excited to see what lovely stories everyone has to share ❤️\n\nXOXO",
        is_public=True
    ), author_id=admin.id, author_name=admin.username)

    # First other user and entry
    other_user = crud.create_user(db, schemas.UserCreate(username="th3_r34l_4dm1n_f0r_r34lz", password=gen_password(30)))

    crud.create_entry(db, schemas.DiaryEntryCreate(
        title="Lololol Your Diary Website Sucks 😝",
        content="Dear Diarrhea,\n\nCCD{th15_15_n0t_th3_fl4g_y0u_4r3_l00k1ng_f0r!}\n\nTeehee 💩",
        is_public=True
    ), author_id=other_user.id, author_name=other_user.username)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()

        # Only populate once
        if crud.get_user_by_username(db, "admin") is None:
            populate_db(db)
    finally:
        db.close()
