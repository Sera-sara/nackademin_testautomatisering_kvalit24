from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.backend.database import Base, engine
from application.backend.routes import auth, users, products
from application.backend.init_db import init_db

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
init_db()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)


# Healthcheck
@app.get("/health")
def healthcheck():
    return "alive"
