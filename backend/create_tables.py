"""
Run this once against any fresh database (local or Neon) to create all tables.

Usage:
  python create_tables.py                          # uses DATABASE_URL or local fallback from .env
  DATABASE_URL=postgresql://... python create_tables.py   (Windows: set it in .env temporarily)
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=os.getenv("DATABASE_PASSWORD"),
        host="127.0.0.1",
        port=5432,
        database="movie_recommender"
    )
elif isinstance(DATABASE_URL, str) and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

TABLES = [
    # 1. users — no dependencies
    """
    CREATE TABLE IF NOT EXISTS users (
        id            SERIAL PRIMARY KEY,
        username      VARCHAR(255) NOT NULL,
        email         VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        created_at    TIMESTAMP DEFAULT NOW()
    )
    """,

    # 2. movies — no dependencies
    """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY,
        title    VARCHAR(500) NOT NULL,
        genres   VARCHAR(500)
    )
    """,

    # 3. ratings — depends on users + movies
    """
    CREATE TABLE IF NOT EXISTS ratings (
        id         SERIAL PRIMARY KEY,
        user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
        movie_id   INTEGER REFERENCES movies(movie_id) ON DELETE CASCADE,
        rating     FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """,

    # 4. watchlist — depends on users + movies
    """
    CREATE TABLE IF NOT EXISTS watchlist (
        id         SERIAL PRIMARY KEY,
        user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
        movie_id   INTEGER REFERENCES movies(movie_id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """,

    # 5. ml_ratings — MovieLens dataset, no FK constraints (user_ids are ML dataset users, not app users)
    """
    CREATE TABLE IF NOT EXISTS ml_ratings (
        user_id   INTEGER,
        movie_id  INTEGER,
        rating    FLOAT,
        timestamp BIGINT
    )
    """,

    # 6. tags — MovieLens dataset, no FK constraints
    """
    CREATE TABLE IF NOT EXISTS tags (
        user_id   INTEGER,
        movie_id  INTEGER,
        tag       TEXT,
        timestamp BIGINT
    )
    """,
]

with engine.connect() as conn:
    for ddl in TABLES:
        conn.execute(text(ddl))
    conn.commit()

print("All tables created successfully!")
print("Next steps:")
print("  python seed_movies.py")
print("  python seed_ratings.py")
print("  python seed_tags.py")
