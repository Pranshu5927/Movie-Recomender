import sys
import os
import pandas as pd

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

engine = create_engine(DATABASE_URL)

force = "--force" in sys.argv

with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM movies")).scalar()

if count > 0 and not force:
    print(f"Movies table already has {count} rows. Pass --force to truncate and re-seed.")
    sys.exit(0)

if force:
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE movies RESTART IDENTITY CASCADE"))
        conn.commit()
    print("Truncated movies table.")

df = pd.read_csv("../data/ml-latest-small/movies.csv")
df = df.rename(columns={"movieId": "movie_id"})

df.to_sql("movies", engine, if_exists="append", index=False)

print(f"Movies seeded successfully! ({len(df)} rows)")
