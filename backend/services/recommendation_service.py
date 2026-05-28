from recommender.popularity import (
    get_popular_recommendations
)

from recommender.personalized_content import (
    get_personalized_recommendations
)

from recommender.collaborative import (
    get_collaborative_recommendations
)

from recommender.content_based import (
    get_similar_movies
)

from recommender.hybrid import (
    get_hybrid_recommendations
)

# ---------------------------------
# HOMEPAGE RECOMMENDATIONS
# ---------------------------------
def get_homepage_recommendations(
    user_id: int
):

    # ---------------------------------
    # POPULAR MOVIES
    # ---------------------------------
    popular_movies = (
        get_popular_recommendations(
            user_id
        )
    )


    # ---------------------------------
    # PERSONALIZED CONTENT
    # ---------------------------------
    personalized_movies = (
        get_personalized_recommendations(
            user_id
        )
    )


    # ---------------------------------
    # COLLABORATIVE FILTERING
    # ---------------------------------
    collaborative_movies = (
        get_collaborative_recommendations(
            user_id
        )
    )

    # ---------------------------------
    # HYBRID MODEL
    # ---------------------------------
    hybrid_movies = (
        get_hybrid_recommendations(
            user_id
        )
    )

    return {

        "must_watch": {

            "title": "🔥 Must Watch",

            "movies": popular_movies
        },


        "personalized": {

            "title": "🧠 Personalized For You",

            "movies": personalized_movies
        },


        "users_also_liked": {

            "title": "👥 Users Also Liked",

            "movies": collaborative_movies
        },

        "hybrid": {

            "title": "🔄 Hybrid Recommendations",

            "movies": hybrid_movies
        }
    }


# ---------------------------------
# CONTENT-BASED ROW
# ---------------------------------
def get_content_based_recommendations(
    movie_title: str
):

    similar_movies = (
        get_similar_movies(
            movie_title
        )
    )


    return {

        "title": f"🎭 More Like {movie_title}",

        "movies": similar_movies
    }