from fastapi import FastAPI
from app.api import assets

app = FastAPI(title="Asset Management")

app.include_router(assets.router)

@app.get("/")
def root():
    return {"status": "API is running"}
