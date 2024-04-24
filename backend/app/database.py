from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os



load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')




if 'DB_URL' in os.environ:
    URL_DATABASE = os.environ.get('DB_URL') 
else:
    URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DATABASE}'
    
Dummy_URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/dummy'



engine = create_engine(URL_DATABASE)
dummy_engine = create_engine(Dummy_URL_DATABASE)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Dummy_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dummy_engine)


Base = declarative_base()
Dummy_Base = declarative_base()

def create_all_tables():
    Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()