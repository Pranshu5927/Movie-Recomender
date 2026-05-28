import pandas as pd
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Get DB password
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Create database URL safely
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=DATABASE_PASSWORD,
    host="127.0.0.1",
    port=5432,
    database="movie_recommender"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Read ratings CSV
df = pd.read_csv("../data/ml-latest-small/ratings.csv")

# Rename columns to match PostgreSQL schema
df = df.rename(columns={
    "userId": "user_id",
    "movieId": "movie_id"
})

# Insert into PostgreSQL
df.to_sql(
    "ml_ratings",
    engine,
    if_exists="append",
    index=False
)

print("Ratings seeded successfully!")