from dotenv import load_dotenv
from fastapi import FastAPI

from app.cors import cors_middleware
from app.database import create_all_tables
from app.routers import auth_user, products

load_dotenv()

app = FastAPI()

app.add_middleware(cors_middleware)

create_all_tables()

app.include_router(products.router, prefix="/api")
app.include_router(auth_user.router, prefix="/auth")
