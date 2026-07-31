from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from app.core.config import settings

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt

from app.schemas.user import TokenData


def create_user_token(user):
    """
    Create JWT token for a user.
    """
    return create_access_token(
        {
            "sub": user.email,
            "user_id": user.id,
        }
    )


def get_token_data(token: str):
    """
    Decode JWT token.
    """
    payload = verify_access_token(token)

    if payload is None:
        return None

    return TokenData(email=payload.get("sub"))

def verify_access_token(token: str):
    """
    Verify a JWT token and return its payload.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        return None