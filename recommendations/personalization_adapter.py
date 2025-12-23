import os

ENABLE_ML = os.getenv("ENABLE_ML_PERSONALIZATION", "false").lower() == "true"


def apply_ml_personalization(
    features,
    dominant_dosha,
    base_recommendations
):
    """
    Optional ML-based personalization.
    Safe for pilot mode: never crashes the system.
    """

    # --- Pilot mode: ML disabled ---
    if not ENABLE_ML:
        return {
            "recommendations": base_recommendations,
            "note": "ML personalization disabled (pilot mode)."
        }

    # --- Lazy import to prevent startup failure ---
    try:
        from ml.personalization.personalize import personalize_recommendations
    except Exception as e:
        return {
            "recommendations": base_recommendations,
            "note": f"ML personalization unavailable: {str(e)}"
        }

    # --- ML execution with safety ---
    try:
        return personalize_recommendations(
            features=features,
            base_recommendations=base_recommendations,
            dominant_dosha=dominant_dosha
        )
    except Exception as e:
        return {
            "recommendations": base_recommendations,
            "note": f"ML personalization failed gracefully: {str(e)}"
        }
