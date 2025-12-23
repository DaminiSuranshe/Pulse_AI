import joblib
import pandas as pd

model = joblib.load("ml/models/recommendation_personalizer.pkl")

def personalize_recommendations(features, base_recommendations, dominant_dosha):
    df = pd.DataFrame([features])

    df["warming"] = 1 if dominant_dosha == "Vata" else 0
    df["cooling"] = 1 if dominant_dosha == "Pitta" else 0
    df["light"] = 1 if dominant_dosha == "Kapha" else 0
    df["calming"] = 1 if dominant_dosha in ["Vata", "Pitta"] else 0

    probability = model.predict_proba(df)[0][1]

    if probability > 0.7:
        strength = "Strongly Recommended"
    elif probability > 0.5:
        strength = "Recommended"
    else:
        strength = "Optional"

    return {
        "personalization_score": round(probability, 3),
        "recommendation_strength": strength,
        "base_recommendations": base_recommendations
    }
