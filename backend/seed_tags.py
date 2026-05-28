import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

import os


# ---------------------------------
# LOAD ENV VARIABLES
# ---------------------------------
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


# ---------------------------------
# CREATE ENGINE
# ---------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------
# LOAD CSV
# ---------------------------------
df = pd.read_csv(
    "../data/ml-latest-small/tags.csv"
)


# ---------------------------------
# RENAME COLUMNS
# ---------------------------------
df.columns = [
    "user_id",
    "movie_id",
    "tag",
    "timestamp"
]


# ---------------------------------
# INSERT INTO POSTGRES
# ---------------------------------
df.to_sql(
    "tags",
    engine,
    if_exists="append",
    index=False
)

print("Tags seeded successfully!")