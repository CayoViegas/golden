from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="Golden API")

@app.get("/")
def health_check():
    return {"status": "ok", "app": "Golden Service"}