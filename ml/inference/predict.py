import joblib
import pandas as pd

dosha_model = joblib.load("ml/models/dosha_classifier.pkl")
outcome_model = joblib.load("ml/models/outcome_predictor.pkl")

def run_ml_inference(features: dict):
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
        "improvement_probability": round(improvement_prob, 3),
        "risk_level": risk
    }
