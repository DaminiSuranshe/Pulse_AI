from recommendations.ayurveda_rules import AYURVEDIC_DIET_RULES
from recommendations.confidence_scoring import compute_confidence
from recommendations.explanations import generate_explanation

def generate_recommendations(
    dominant_dosha: str,
    dosha_scores: dict,
    prakriti: dict = None,
    season: str = None
):
    rules = AYURVEDIC_DIET_RULES[dominant_dosha]

    recommendations = {
        "diet_prefer": rules["prefer"],
        "diet_avoid": rules["avoid"],
        "lifestyle": rules["lifestyle"]
    }

    confidence = compute_confidence(dosha_scores, dominant_dosha)

    explanation = generate_explanation(
        dominant_dosha,
        dosha_scores,
        season
    )

    return {
        "dominant_dosha": dominant_dosha,
        "recommendations": recommendations,
        "confidence_score": confidence,
        "explanation": explanation
    }
