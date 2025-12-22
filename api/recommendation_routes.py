from fastapi import APIRouter
from recommendations.recommendation_engine import generate_recommendations

router = APIRouter()

@router.post("/recommendations/generate")
def get_recommendations(
    dominant_dosha: str,
    vata: float,
    pitta: float,
    kapha: float,
    season: str = None
):
    dosha_scores = {
        "vata": vata,
        "pitta": pitta,
        "kapha": kapha
    }

    return generate_recommendations(
        dominant_dosha=dominant_dosha,
        dosha_scores=dosha_scores,
        season=season
    )
