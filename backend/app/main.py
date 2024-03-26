from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.database import create_all_tables
from app.routers import products

from app.cors import cors_middleware

from dotenv import load_dotenv
import os


load_dotenv()


app = FastAPI()

# Adding CORS middleware
app.add_middleware(cors_middleware)


# Initialize database
create_all_tables()





# Routers
app.include_router(products.router, prefix="/api")
