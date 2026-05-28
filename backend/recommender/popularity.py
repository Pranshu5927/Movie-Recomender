from sqlalchemy import text

from db.database import engine


def get_popular_recommendations(user_id):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    movies.movie_id,
                    movies.title,
                    movies.genres,

                    AVG(ml_ratings.rating) AS avg_rating,
                    COUNT(ml_ratings.rating) AS rating_count

                FROM ml_ratings

                JOIN movies
                ON ml_ratings.movie_id = movies.movie_id

                WHERE movies.movie_id NOT IN (

                    SELECT movie_id
                    FROM ratings
                    WHERE user_id = :user_id
                )

                GROUP BY
                    movies.movie_id,
                    movies.title,
                    movies.genres

                HAVING COUNT(ml_ratings.rating) > 50

                ORDER BY avg_rating DESC

                LIMIT 20
            """),
            {
                "user_id": user_id
            }
        )

        recommendations = []

        for row in result:

            recommendations.append({
                "movie_id": row.movie_id,
                "title": row.title,
                "genres": row.genres,
                "avg_rating": round(float(row.avg_rating), 2),
                "rating_count": row.rating_count
            })

    return recommendations