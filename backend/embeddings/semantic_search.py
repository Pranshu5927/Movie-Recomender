import json

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy import create_engine

from db.database import DATABASE_URL

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

engine = create_engine(DATABASE_URL)


def load_movie_embeddings():

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

    movies = pd.read_sql(query, engine)

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
            json.loads(row["embedding"])
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