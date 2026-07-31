from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hashing import hash_password


def get_user_by_email(db: Session, email: str):
    """
    Return a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Return a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user.
    """
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

from app.auth.hashing import verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        print("User not found")
        return None

    print("Email:", email)
    print("Entered Password:", password)
    print("Stored Hash:", user.password_hash)

    result = verify_password(password, user.password_hash)
    print("Password Match:", result)

    if not result:
        return None

    return user

def create_google_user(
    db: Session,
    email: str,
    username: str,
    google_id: str,
    profile_picture: str,
):
    """
    Create a new Google user.
    """
    
    db_user = User(
        username=username,
        email=email,
        password_hash="",          # No password for Google users
        auth_provider="google",
        google_id=google_id,
        profile_picture=profile_picture,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_google_user(
    db: Session,
    user: User,
    google_id: str,
    profile_picture: str,
):
    """
    Update an existing local user with Google details.
    """
    user.google_id = google_id
    user.profile_picture = profile_picture
    user.auth_provider = "google"

    db.commit()
    db.refresh(user)

    return user