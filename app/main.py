from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
import os
import mimetypes
from app.api import assets

# Fix Windows MIME type issue — ensures .css is served as text/css
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")

app = FastAPI(title="Asset Management")

# Static files (CSS, JS)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# API router
app.include_router(assets.router)


@app.get("/", response_class=HTMLResponse)
def index_page():
    """Serve the main asset list page."""
    file_path = os.path.join(STATIC_DIR, "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/detail", response_class=HTMLResponse)
def detail_page():
    """Serve the asset detail page."""
    file_path = os.path.join(STATIC_DIR, "detail.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/favicon.ico")
def favicon():
    """Return an inline SVG favicon."""
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="80" font-size="80">💻</text></svg>'
    return Response(content=svg, media_type="image/svg+xml")
