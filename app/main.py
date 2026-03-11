from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import mimetypes
from app.api import assets
from app.api import auth as auth_api
from app.api import attachments
from app.api import changelog
from app.api import user_history
from app.core.database import Base, engine, SessionLocal
from app.models.auth import User
from app.models.attachment import Attachment
from app.models.changelog import ChangeLog
from app.models.user_history import UserHistory
from app.api.auth import get_current_user_optional, COOKIE_NAME, serializer, SESSION_MAX_AGE

# Fix Windows MIME type issue — ensures .css is served as text/css
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")

app = FastAPI(title="Asset Management")

# Create all tables (including new ones)
Base.metadata.create_all(bind=engine)

# Seed default admin user
db = SessionLocal()
try:
    auth_api.seed_default_user(db)
finally:
    db.close()

# Static files (CSS, JS)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# API routers
app.include_router(auth_api.router)
app.include_router(assets.router)
app.include_router(attachments.router)
app.include_router(changelog.router)
app.include_router(user_history.router)


def _is_logged_in(request: Request) -> bool:
    """Check if the user has a valid session cookie."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return False
    try:
        serializer.loads(token, max_age=SESSION_MAX_AGE)
        return True
    except Exception:
        return False


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Serve the login page. Redirect to / if already logged in."""
    if _is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)
    file_path = os.path.join(STATIC_DIR, "login.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    """Serve the main asset list page. Redirect to /login if not authenticated."""
    if not _is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    file_path = os.path.join(STATIC_DIR, "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/detail", response_class=HTMLResponse)
def detail_page(request: Request):
    """Serve the asset detail page. Redirect to /login if not authenticated."""
    if not _is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    file_path = os.path.join(STATIC_DIR, "detail.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/favicon.ico")
def favicon():
    """Return an inline SVG favicon."""
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="80" font-size="80">💻</text></svg>'
    return Response(content=svg, media_type="image/svg+xml")
