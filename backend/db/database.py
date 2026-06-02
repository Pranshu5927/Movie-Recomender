import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

load_dotenv()

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=DATABASE_PASSWORD,
    host="127.0.0.1",
    port=5432,
    database="movie_recommender"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)