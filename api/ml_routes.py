from fastapi import APIRouter
from ml.inference.predict import run_ml_inference
from api.schemas import PulseFeatures
from typing import Dict, Any

router = APIRouter()

@router.post("/ml/predict")
def ml_predict(features: Dict[str, Any]):
    result = run_ml_inference(features)
    return result