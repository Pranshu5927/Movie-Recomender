from recommender.hybrid import (
    get_hybrid_recommendations
)

recommendations = (
    get_hybrid_recommendations(
        user_id=1
    )
)

print(recommendations[:5])