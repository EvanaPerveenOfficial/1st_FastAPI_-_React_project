from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.database import create_all_tables
from app.routers import products

from dotenv import load_dotenv
import os


load_dotenv()


app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
    # "https://my-react-app.com"
]

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize database
create_all_tables()


# Database connection parameters
db_params = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}





# Maximum retry count

max_retries = 3

def establish_database_connection(max_retries):
    for attempt in range(1, max_retries + 1):
        try:
            connect = psycopg2.connect(**db_params, cursor_factory=RealDictCursor)
            print('Connection successful!')
            return connect
        except Exception as error:
            print(f'Connection attempt {attempt} failed:', error)
            if attempt < max_retries:
                print('Retrying in 5 seconds...')
                time.sleep(5)
    raise RuntimeError('Unable to establish database connection after multiple attempts')


# database connection
db_connection = establish_database_connection(max_retries)


# Routers
app.include_router(products.router, prefix="/api")
