from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from db.database import DATABASE_URL

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ml-latest-small"

engine = create_engine(DATABASE_URL)

df = pd.read_csv(DATA_DIR / "movies.csv")

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
