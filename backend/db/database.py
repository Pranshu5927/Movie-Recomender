import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

load_dotenv()

# Production (Railway/Neon/Render) supplies a full DATABASE_URL.
# Development falls back to constructing it from individual env vars.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Some providers use "postgres://" — SQLAlchemy needs "postgresql://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=os.getenv("DATABASE_PASSWORD"),
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
