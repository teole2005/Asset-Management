from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from app.api import assets

app = FastAPI(title="Asset Management")

app.include_router(assets.router)

@app.get("/page", response_class=HTMLResponse)
def get_page():
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/action")
def perform_action():
    return {"message": "Action completed! Message sent from backend."}

@app.get("/")
def root():
    return {"status": "API is running"}
