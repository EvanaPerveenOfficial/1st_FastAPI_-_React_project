from fastapi import FastAPI

from app.database import create_all_tables
from app.routers import products, auth_user

from app.cors import cors_middleware

from dotenv import load_dotenv


load_dotenv()


app = FastAPI()

# Adding CORS middleware
app.add_middleware(cors_middleware)


# Initialize database
create_all_tables()





# Routers
app.include_router(products.router, prefix="/api")
app.include_router(auth_user.router, prefix="/auth")
