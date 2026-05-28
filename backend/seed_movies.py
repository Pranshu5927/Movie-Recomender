import pandas as pd
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
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

df = pd.read_csv("../data/ml-latest-small/movies.csv")

# Rename column to match PostgreSQL schema
df = df.rename(columns={
    "movieId": "movie_id"
})

df.to_sql(
    "movies",
    engine,
    if_exists="append",
    index=False
)

print("Movies seeded successfully!")