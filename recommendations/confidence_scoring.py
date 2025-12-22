def compute_confidence(dosha_scores: dict, dominant_dosha: str):
    dominant_score = dosha_scores[dominant_dosha.lower()]

    # Confidence increases with dominance clarity
    if dominant_score > 0.6:
        return "High"
    elif dominant_score > 0.45:
        return "Moderate"
    else:
        return "Low"
