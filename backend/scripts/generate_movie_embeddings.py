import pandas as pd
import psycopg2

from psycopg2.extras import Json
from sentence_transformers import SentenceTransformer

import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Database Connection
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="movie_recommender",
    user="postgres",
    password=os.getenv("DATABASE_PASSWORD")
)

cursor = conn.cursor()

# -----------------------------
# Load Movies
# -----------------------------
movies = pd.read_sql(
    """
    SELECT *
    FROM movies
    """,
    conn
)

print(f"Loaded {len(movies)} movies")


# -----------------------------
# Load Tags
# -----------------------------
tags = pd.read_sql(
    """
    SELECT *
    FROM tags
    """,
    conn
)

print(f"Loaded {len(tags)} tags")


# -----------------------------
# Aggregate Tags Per Movie
# -----------------------------
tag_text = (
    tags.groupby("movie_id")["tag"]
    .apply(lambda x: " ".join(x.astype(str)))
    .reset_index()
)

print("Tags aggregated")


# -----------------------------
# Merge Movies + Tags
# -----------------------------
movies = movies.merge(
    tag_text,
    on="movie_id",
    how="left"
)

movies["tag"] = movies["tag"].fillna("")

print("Movies merged with tags")


# -----------------------------
# Build Movie Content
# -----------------------------
def build_movie_text(row):
    genres = row["genres"].replace("|", " ")

    return f"""
    {row['title']}
    {genres}
    {row['tag']}
    """


movies["content"] = movies.apply(
    build_movie_text,
    axis=1
)

print("Movie content created")


# -----------------------------
# Load Embedding Model
# -----------------------------
print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded")


# -----------------------------
# Test One Movie
# -----------------------------
print("Generating embeddings...")

movies["embedding"] = movies["content"].apply(
    lambda text: model.encode(text).tolist()
)

print("Embeddings generated")
print("Saving embeddings to database...")
for _, row in movies.iterrows():

    cursor.execute(
        """
        INSERT INTO movie_embeddings
        (
            movie_id,
            embedding
        )
        VALUES (%s, %s)

        ON CONFLICT (movie_id)
        DO UPDATE
        SET embedding = EXCLUDED.embedding
        """,
        (
            int(row["movie_id"]),
            Json(row["embedding"])
        )
    )
conn.commit()
print("Embeddings saved successfully")
cursor.close()
conn.close()