from fastapi import APIRouter, Depends, HTTPException, Request, Response, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.auth import User
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

router = APIRouter(prefix="/api/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for signing session cookies
SECRET_KEY = "asset-mgmt-secret-key-change-in-production"
SESSION_MAX_AGE = 86400  # 24 hours
serializer = URLSafeTimedSerializer(SECRET_KEY)

COOKIE_NAME = "session_token"


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency: extract user from session cookie. Returns User or raises 401."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        data = serializer.loads(token, max_age=SESSION_MAX_AGE)
        user_id = data.get("user_id")
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    """Returns User or None (no exception)."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        data = serializer.loads(token, max_age=SESSION_MAX_AGE)
        user_id = data.get("user_id")
        return db.query(User).filter(User.id == user_id).first()
    except (BadSignature, SignatureExpired):
        return None


@router.post("/login")
async def login_handler(
    response: Response,
    db: Session = Depends(get_db),
    username: str = Body(...),
    password: str = Body(...),
):
    """Login with username and password. Sets a signed session cookie."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create signed token
    token = serializer.dumps({"user_id": user.id, "username": user.username})

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=SESSION_MAX_AGE,
        path="/",
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "display_name": user.display_name,
        },
    }


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    """Return current logged-in user info."""
    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name,
    }


@router.post("/logout")
def logout(response: Response):
    """Clear the session cookie."""
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return {"message": "Logged out"}


def seed_default_user(db: Session):
    """Create the default admin user if it doesn't exist."""
    existing = db.query(User).filter(User.username == "admin").first()
    if not existing:
        user = User(
            username="admin",
            password_hash=pwd_context.hash("admin123"),
            display_name="Administrator",
        )
        db.add(user)
        db.commit()
