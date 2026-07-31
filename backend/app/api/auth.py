from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.db.session import get_db
from app.auth.google_oauth import oauth

from app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    authenticate_user,
    create_google_user,
    update_google_user,
)

from app.auth.jwt_handler import create_user_token

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)

from app.auth.oauth2 import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

from fastapi.security import OAuth2PasswordRequestForm

# Register

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    existing_username = get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    return create_user(db, user)


# Login


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login user and return JWT.
    """

    db_user = authenticate_user(
        db,
        user.email,
        user.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_user_token(db_user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/token", response_model=Token)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2 login for Swagger Authorize.
    Username field should contain the user's email.
    """
    db_user = authenticate_user(
        db,
        form_data.username,  # email goes here
        form_data.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_user_token(db_user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

# Current User

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently logged-in user.
    """
    return current_user


# Google Login

@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirect user to Google login page.
    """
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


# Google Callback

@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Google OAuth callback.
    """

    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    email = user_info["email"]

    db_user = get_user_by_email(db, email)

    if not db_user:
        db_user = create_google_user(
            db=db,
            email=email,
            username=user_info.get(
                "given_name",
                email.split("@")[0],
            ),
            google_id=user_info["sub"],
            profile_picture=user_info.get("picture"),
        )

    elif db_user.auth_provider == "local":
        db_user = update_google_user(
            db=db,
            user=db_user,
            google_id=user_info["sub"],
            profile_picture=user_info.get("picture"),
        )

    jwt_token = create_user_token(db_user)

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "profile_picture": db_user.profile_picture,
        },
    }