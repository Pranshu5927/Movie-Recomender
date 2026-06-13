from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from db.database import DATABASE_URL

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ml-latest-small"

engine = create_engine(DATABASE_URL)

# Read ratings CSV
df = pd.read_csv(DATA_DIR / "ratings.csv")

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
    index=False,
    chunksize=1000,
    method="multi"
)

print("Ratings seeded successfully!")
