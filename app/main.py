from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, products, cart, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShopHub API",
    description="E-commerce API with JWT authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Welcome to ShopHub API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}