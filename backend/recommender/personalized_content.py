import numpy as np

from sqlalchemy import text

from db.database import engine

from sklearn.metrics.pairwise import cosine_similarity

from recommender.engines.content_engine import (
    movies_df,
    vectors
)

from recommender.utils import normalize_scores


def get_personalized_recommendations(
    user_id,
    top_n=20
):

    # ---------------------------------
    # FETCH USER'S HIGHLY RATED MOVIES
    # ---------------------------------
    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT movie_id
                FROM ratings
                WHERE user_id = :user_id
                AND rating >= 4
            """),
            {
                "user_id": user_id
            }
        )

        liked_movie_ids = [
            row.movie_id
            for row in result
        ]


    # ---------------------------------
    # HANDLE COLD START
    # ---------------------------------
    if len(liked_movie_ids) == 0:

        return []


    # ---------------------------------
    # GET MOVIE INDICES
    # ---------------------------------
    liked_movies = movies_df[
        movies_df["movie_id"].isin(
            liked_movie_ids
        )
    ]


    liked_indices = liked_movies.index.tolist()


    # ---------------------------------
    # BUILD USER PROFILE VECTOR
    # ---------------------------------
    liked_vectors = vectors[liked_indices]

    user_profile = np.mean(
        liked_vectors,
        axis=0
    ).reshape(1, -1)


    # ---------------------------------
    # CALCULATE SIMILARITY
    # ---------------------------------
    similarity_scores = cosine_similarity(
        user_profile,
        vectors
    )[0]


    # ---------------------------------
    # SORT MOVIES BY SCORE
    # ---------------------------------
    scored_movies = list(
        enumerate(similarity_scores)
    )

    scored_movies = sorted(
        scored_movies,
        key=lambda x: x[1],
        reverse=True
    )


    # ---------------------------------
    # REMOVE ALREADY WATCHED MOVIES
    # ---------------------------------
    watched_set = set(
        liked_movie_ids
    )


    recommendations = []


    for movie_index, score in scored_movies:

        movie = movies_df.iloc[movie_index]

        if movie["movie_id"] in watched_set:
            continue

        recommendations.append({
            "movie_id": int(
                movie["movie_id"]
            ),
            "title": movie["title"],
            "genres": movie["genres"],

            "score": float(score),

            "recommendation_source": "personalized_content",

            "vote_count": None,

            "reasons": [
                "Matches your viewing preferences"
            ],

            "metadata": {}
        })

        if len(recommendations) >= top_n:
            break

    recommendations = normalize_scores(recommendations)

    return recommendations