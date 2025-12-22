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
    Optional ML advisory inference.
    Uses available pulse features only.
    Never blocks core pulse analysis.
    """

    try:
        load_models()
    except Exception as e:
        return {
            "ml_predicted_dosha": "Unavailable",
            "confidence": "Low",
            "note": f"ML models not loaded: {str(e)}"
        }

    # Ensure DataFrame
    df = pd.DataFrame([features])

    # Adapt to model expectations
    model_features = list(dosha_model.feature_names_in_)
    available_features = [f for f in model_features if f in df.columns]

    if len(available_features) < 3:
        return {
            "ml_predicted_dosha": "Insufficient data",
            "confidence": "Low",
            "note": "Not enough pulse features for ML inference"
        }

    try:
        X = df[available_features]

        ml_dosha = dosha_model.predict(X)[0]

        improvement_prob = (
            outcome_model.predict_proba(X)[0][1]
            if hasattr(outcome_model, "predict_proba")
            else None
        )

        return {
            "ml_predicted_dosha": ml_dosha,
            "improvement_probability": (
                round(float(improvement_prob), 3)
                if improvement_prob is not None
                else None
            ),
            "confidence": "Medium" if improvement_prob is not None else "Low",
            "note": "ML advisory based on available pulse features"
        }

    except Exception as e:
        return {
            "ml_predicted_dosha": "Unavailable",
            "confidence": "Low",
            "note": f"ML inference failed gracefully: {str(e)}"
        }
