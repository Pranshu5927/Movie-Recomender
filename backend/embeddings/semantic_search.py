import numpy as np
import pandas as pd
import psycopg2

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import os 
from dotenv import load_dotenv

load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="movie_recommender",
        user="postgres",
        password=DATABASE_PASSWORD
    )


def load_movie_embeddings():

    conn = get_connection()

    query = """
    SELECT
        m.movie_id,
        m.title,
        m.genres,
        me.embedding
    FROM movies m
    JOIN movie_embeddings me
        ON m.movie_id = me.movie_id
    """

    movies = pd.read_sql(query, conn)

    conn.close()

    return movies

def semantic_search(
    query: str,
    top_k: int = 10
):
    query_embedding = model.encode(query)
    movies = load_movie_embeddings()
    scores = []
    for _, row in movies.iterrows():
        movie_embedding = np.array(
            row["embedding"]
        )

        score = cosine_similarity(
            [query_embedding],
            [movie_embedding]
        )[0][0]

        scores.append({
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "genres": row["genres"],
            "score": round(float(score), 4)
        })
    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    return scores[:top_k]

if __name__ == "__main__":

    results = semantic_search(
        "movies about loneliness in space"
    )

    for result in results:
        print(result)