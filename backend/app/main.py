from fastapi import FastAPI
from app.core.config import settings
from app.routes import product_routes

app = FastAPI(title="Golden API")

app.include_router(product_routes.router)

@app.get("/")
def health_check():
    return {"status": "ok", "app": "Golden Service"}