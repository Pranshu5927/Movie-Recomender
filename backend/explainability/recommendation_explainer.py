class RecommendationExplainer:

    @staticmethod
    def generate(movie):

        reasons = []

        scores = [
            (
                "content",
                movie.get("content_score", 0)
            ),
            (
                "collaborative",
                movie.get("collaborative_score", 0)
            ),
            (
                "popularity",
                movie.get("popularity_score", 0)
            )
        ]

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        top_sources = scores[:2]

        for source, score in top_sources:

            if score <= 0:
                continue

            if source == "content":
                reasons.append(
                    "Similar to movies you've enjoyed"
                )

            elif source == "collaborative":
                reasons.append(
                    "Liked by users with similar tastes"
                )

            elif source == "popularity":
                reasons.append(
                    "Highly rated by the community"
                )

        return reasons