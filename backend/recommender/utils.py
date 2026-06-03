from typing import List


def normalize_scores(
    recommendations: List[dict],
    score_field: str = "score"
) -> List[dict]:
    """
    Normalizes scores into a 0-1 range.
    """

    if not recommendations:
        return recommendations

    max_score = max(
        item.get(score_field, 0)
        for item in recommendations
    )

    if max_score == 0:
        for item in recommendations:
            item["normalized_score"] = 0.0
        return recommendations

    for item in recommendations:
        item["normalized_score"] = (
            item.get(score_field, 0) / max_score
        )

    return recommendations