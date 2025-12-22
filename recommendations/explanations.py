def generate_explanation(dominant_dosha, scores, season=None):
    explanation = (
        f"Based on pulse-derived features, {dominant_dosha} dosha shows higher activity. "
        f"The recommendations aim to balance this imbalance using classical Ayurvedic principles."
    )

    if season:
        explanation += f" Seasonal considerations for {season} have been applied."

    explanation += (
        " These suggestions support lifestyle regulation and dietary balance, "
        "and should be interpreted alongside practitioner judgment."
    )

    return explanation
