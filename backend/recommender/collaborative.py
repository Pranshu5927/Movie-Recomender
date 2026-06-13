import pandas as pd
import numpy as np

from sqlalchemy import create_engine

from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix

from db.database import DATABASE_URL

from recommender.utils import normalize_scores


# ---------------------------------
# LOAD DATABASE
# ---------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------
# LOAD RATINGS
# ---------------------------------
try:
    ratings_df = pd.read_sql(
        "SELECT * FROM ml_ratings",
        engine
    )


    movies_df = pd.read_sql(
        "SELECT * FROM movies",
        engine
    )


    # ---------------------------------
    # CREATE USER-MOVIE MATRIX
    # ---------------------------------
    user_movie_matrix = ratings_df.pivot_table(
        index="user_id",
        columns="movie_id",
        values="rating"
    ).fillna(0)


    # ---------------------------------
    # SPARSE MATRIX
    # ---------------------------------
    sparse_matrix = csr_matrix(
        user_movie_matrix.values
    )


    # ---------------------------------
    # SVD MODEL
    # ---------------------------------
    svd = TruncatedSVD(
        n_components=50,
        random_state=42
    )

    matrix_decomposition = svd.fit_transform(
        sparse_matrix
    )


    # ---------------------------------
    # USER SIMILARITY
    # ---------------------------------
    user_similarity = cosine_similarity(
        matrix_decomposition
    )


    print(
        "Collaborative filtering engine loaded!"
    )
except Exception as e:
    print(f"Warning: Could not load collaborative filtering data at startup: {e}")
    ratings_df = None
    movies_df = None
    user_movie_matrix = None
    user_similarity = None

def get_collaborative_recommendations(
    user_id,
    top_n=20
):

    # ---------------------------------
    # FIND USER INDEX
    # ---------------------------------
    if user_movie_matrix is None or user_id not in user_movie_matrix.index:
        return []


    user_idx = (
        user_movie_matrix.index
        .tolist()
        .index(user_id)
    )


    # ---------------------------------
    # GET SIMILAR USERS
    # ---------------------------------
    similarity_scores = list(
        enumerate(user_similarity[user_idx])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:11]


    # ---------------------------------
    # MOVIES USER ALREADY WATCHED
    # ---------------------------------
    watched_movies = set(

        ratings_df[
            ratings_df["user_id"] == user_id
        ]["movie_id"]

    )


    # ---------------------------------
    # COLLECT RECOMMENDATIONS
    # ---------------------------------
    recommended_movies = {}


    for similar_user_idx, similarity_score in similarity_scores:

        similar_user_id = (
            user_movie_matrix.index[
                similar_user_idx
            ]
        )

        similar_user_movies = ratings_df[
            (ratings_df["user_id"] == similar_user_id)
            &
            (ratings_df["rating"] >= 4)
        ]


        for _, row in similar_user_movies.iterrows():

            movie_id = row["movie_id"]

            if movie_id in watched_movies:
                continue

            if movie_id not in recommended_movies:

                recommended_movies[movie_id] = {
                    "score": 0,
                    "count": 0
                }

            recommended_movies[movie_id][
                "score"
            ] += similarity_score

            recommended_movies[movie_id][
                "count"
            ] += 1


    # ---------------------------------
    # SORT MOVIES
    # ---------------------------------
    sorted_movies = sorted(
        recommended_movies.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )[:top_n]


    # ---------------------------------
    # BUILD RESPONSE
    # ---------------------------------
    recommendations = []


    for movie_id, data in sorted_movies:

        movie = movies_df[
            movies_df["movie_id"] == movie_id
        ].iloc[0]

        recommendations.append({

            "movie_id": int(movie_id),

            "title": movie["title"],

            "genres": movie["genres"],

            "score": float(data["score"]),

            "recommendation_source": "collaborative",

            "vote_count": None,

            "reasons": [
                "Liked by users with similar tastes"
            ],

            "metadata": {}

        })

    recommendations = normalize_scores(recommendations)

    return recommendations