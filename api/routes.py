from fastapi import APIRouter
from core.dosha_mapping import compute_dosha_scores
from api.schemas import PulseFeatures, DoshaResponse

router = APIRouter()


@router.post("/dosha/analyze", response_model=DoshaResponse)
def analyze_dosha(features: PulseFeatures):
    result = compute_dosha_scores(features.dict())
    return result
