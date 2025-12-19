from fastapi import APIRouter
from ml.inference.predict import run_ml_inference
from api.schemas import PulseFeatures

router = APIRouter()

@router.post("/ml/predict")
def ml_predict(features: PulseFeatures):
    result = run_ml_inference(features.dict())
    return result
