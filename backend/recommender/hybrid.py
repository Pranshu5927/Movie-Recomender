from recommender.popularity import (
    get_popular_recommendations
)

from recommender.personalized_content import (
    get_personalized_recommendations
)

from recommender.collaborative import (
    get_collaborative_recommendations
)

from explainability.recommendation_explainer import (
    RecommendationExplainer
)


# ---------------------------------
# WEIGHTS
# ---------------------------------

POPULARITY_WEIGHT = 0.2

CONTENT_WEIGHT = 0.4

COLLABORATIVE_WEIGHT = 0.4


# ---------------------------------
# HYBRID RECOMMENDER
# ---------------------------------

def get_hybrid_recommendations(
    user_id,
    top_n=20
):

    popularity_movies = (
        get_popular_recommendations(
            user_id
        )
    )

    content_movies = (
        get_personalized_recommendations(
            user_id
        )
    )

    collaborative_movies = (
        get_collaborative_recommendations(
            user_id
        )
    )

    movie_scores = {}

    # ---------------------------------
    # POPULARITY
    # ---------------------------------

    for rank, movie in enumerate(
        popularity_movies
    ):

        movie_id = movie["movie_id"]

        score = (
            (len(popularity_movies) - rank)
            * POPULARITY_WEIGHT
        )

        if movie_id not in movie_scores:

            movie_scores[movie_id] = {
                **movie,
                "hybrid_score": 0,
                "popularity_score": 0,
                "content_score": 0,
                "collaborative_score": 0
            }

        movie_scores[movie_id][
            "hybrid_score"
        ] += score

        movie_scores[movie_id][
            "popularity_score"
        ] += score

    # ---------------------------------
    # CONTENT
    # ---------------------------------

    for rank, movie in enumerate(
        content_movies
    ):

        movie_id = movie["movie_id"]

        score = (
            (len(content_movies) - rank)
            * CONTENT_WEIGHT
        )

        if movie_id not in movie_scores:

            movie_scores[movie_id] = {
                **movie,
                "hybrid_score": 0,
                "popularity_score": 0,
                "content_score": 0,
                "collaborative_score": 0
            }

        movie_scores[movie_id][
            "hybrid_score"
        ] += score

        movie_scores[movie_id][
            "content_score"
        ] += score

    # ---------------------------------
    # COLLABORATIVE
    # ---------------------------------

    for rank, movie in enumerate(
        collaborative_movies
    ):

        movie_id = movie["movie_id"]

        score = (
            (len(collaborative_movies) - rank)
            * COLLABORATIVE_WEIGHT
        )

        if movie_id not in movie_scores:

            movie_scores[movie_id] = {
                **movie,
                "hybrid_score": 0,
                "popularity_score": 0,
                "content_score": 0,
                "collaborative_score": 0
            }

        movie_scores[movie_id][
            "hybrid_score"
        ] += score

        movie_scores[movie_id][
            "collaborative_score"
        ] += score

    # ---------------------------------
    # SORT
    # ---------------------------------

    ranked_movies = sorted(

        movie_scores.values(),

        key=lambda x: x["hybrid_score"],

        reverse=True

    )

    # ---------------------------------
    # ADD EXPLANATIONS
    # ---------------------------------

    final_movies = []

    for movie in ranked_movies[:top_n]:

        movie[
            "recommendation_source"
        ] = "hybrid"

        movie[
            "reasons"
        ] = (
            RecommendationExplainer.generate(
                movie
            )
        )

        final_movies.append(movie)

    return final_movies