import asyncio
from fastapi import FastAPI
from app.database import create_all_tables
from app.routers import products, auth_user
from app.cors import cors_middleware
from dotenv import load_dotenv


load_dotenv()


app = FastAPI()


app.add_middleware(cors_middleware)


@app.on_event("startup")
async def startup_event():
   await create_all_tables()


app.include_router(products.router, prefix="/api")
app.include_router(auth_user.router, prefix="/auth")