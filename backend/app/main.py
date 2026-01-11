from fastapi import FastAPI

from app.routes import order_routes, product_routes

app = FastAPI(title="Golden API")

app.include_router(product_routes.router)
app.include_router(order_routes.router)


@app.get("/")
def health_check():
    return {"status": "ok", "app": "Golden Service"}
