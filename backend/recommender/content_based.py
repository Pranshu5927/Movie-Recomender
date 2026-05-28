from recommender.engines.content_engine import (
    movies_df,
    similarity
)


def get_similar_movies(movie_title):

    movie_index = (
        movies_df[
            movies_df["title"] == movie_title
        ]
        .index[0]
    )

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for movie in movies_list:

        recommended_movie = (
            movies_df.iloc[movie[0]]
        )

        recommendations.append({
            "movie_id": int(
                recommended_movie["movie_id"]
            ),
            "title": recommended_movie["title"],
            "genres": recommended_movie["genres"]
        })

    return recommendations