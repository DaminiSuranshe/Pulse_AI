from ml.personalization.personalize import personalize_recommendations

def apply_ml_personalization(
    features,
    dominant_dosha,
    base_recommendations
):
    return personalize_recommendations(
        features=features,
        base_recommendations=base_recommendations,
        dominant_dosha=dominant_dosha
    )
