from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from db.database import DATABASE_URL


# ---------------------------------
# PATHS
# ---------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ml-latest-small"


# ---------------------------------
# CREATE ENGINE
# ---------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------
# LOAD CSV
# ---------------------------------
df = pd.read_csv(DATA_DIR / "tags.csv")


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
