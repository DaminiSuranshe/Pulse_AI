import os
import joblib
import pandas as pd

DOSHA_MODEL_PATH = "ml/models/dosha_classifier.pkl"
OUTCOME_MODEL_PATH = "ml/models/outcome_predictor.pkl"

dosha_model = None
outcome_model = None

# ----------------------------
# SAFE MODEL LOADING
# ----------------------------
def load_models():
    global dosha_model, outcome_model

    if os.path.exists(DOSHA_MODEL_PATH) and os.path.getsize(DOSHA_MODEL_PATH) > 0:
        try:
            dosha_model = joblib.load(DOSHA_MODEL_PATH)
            print("Dosha ML model loaded")
        except Exception as e:
            print("Failed to load dosha model:", e)
            dosha_model = None
    else:
        print("Dosha model missing or empty")

    if os.path.exists(OUTCOME_MODEL_PATH) and os.path.getsize(OUTCOME_MODEL_PATH) > 0:
        try:
            outcome_model = joblib.load(OUTCOME_MODEL_PATH)
            print("Outcome ML model loaded")
        except Exception as e:
            print("Failed to load outcome model:", e)
            outcome_model = None
    else:
        print("Outcome model missing or empty")


# Load once at startup
load_models()


# ----------------------------
# ML INFERENCE (SAFE)
# ----------------------------
def run_ml_inference(features: dict):
    df = pd.DataFrame([features])

    # ---- Dosha Prediction ----
    if dosha_model is not None:
        ml_dosha = dosha_model.predict(df)[0]
    else:
        ml_dosha = "Rule-Based (Fallback)"

    # ---- Outcome Prediction ----
    if outcome_model is not None:
        improvement_prob = float(outcome_model.predict_proba(df)[0][1])
    else:
        improvement_prob = 0.5  # neutral fallback

    # ---- Risk Interpretation ----
    if improvement_prob < 0.4:
        risk = "High Risk (Low Improvement Probability)"
    elif improvement_prob < 0.65:
        risk = "Moderate Response Expected"
    else:
        risk = "Likely Improvement"

    return {
        "ml_predicted_dosha": ml_dosha,
        "improvement_probability": round(improvement_prob, 3),
        "risk_level": risk,
        "inference_mode": "ML" if dosha_model and outcome_model else "Rule-Based Fallback"
    }
