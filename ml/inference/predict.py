import joblib
import pandas as pd
from pathlib import Path

# -------- Path Resolution (IMPORTANT) --------
BASE_DIR = Path(__file__).resolve().parents[2]
DOSHA_MODEL_PATH = BASE_DIR / "ml" / "models" / "dosha_classifier.pkl"
OUTCOME_MODEL_PATH = BASE_DIR / "ml" / "models" / "outcome_predictor.pkl"

# -------- Lazy-loaded Models --------
dosha_model = None
outcome_model = None


def load_models():
    global dosha_model, outcome_model

    if dosha_model is None:
        if not DOSHA_MODEL_PATH.exists():
            raise FileNotFoundError(f"Dosha model not found at {DOSHA_MODEL_PATH}")
        dosha_model = joblib.load(DOSHA_MODEL_PATH)

    if outcome_model is None:
        if not OUTCOME_MODEL_PATH.exists():
            raise FileNotFoundError(f"Outcome model not found at {OUTCOME_MODEL_PATH}")
        outcome_model = joblib.load(OUTCOME_MODEL_PATH)


def run_ml_inference(features: dict):
    """
    Runs ML inference for Dosha classification
    and treatment outcome prediction
    """

    load_models()

    df = pd.DataFrame([features])

    ml_dosha = dosha_model.predict(df)[0]
    improvement_prob = outcome_model.predict_proba(df)[0][1]

    if improvement_prob < 0.4:
        risk = "High Risk (Low Improvement Probability)"
    elif improvement_prob < 0.65:
        risk = "Moderate Response Expected"
    else:
        risk = "Likely Improvement"

    return {
        "ml_predicted_dosha": ml_dosha,
        "improvement_probability": round(float(improvement_prob), 3),
        "risk_level": risk
    }
