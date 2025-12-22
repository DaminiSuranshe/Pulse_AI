import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ----------------------------
# TEMP DATA (for pipeline validation)
# ----------------------------
data = pd.DataFrame({
    "pulse_rate": [72, 85, 60, 95, 78],
    "pulse_variability": [0.3, 0.6, 0.2, 0.7, 0.4],
    "amplitude": [1.2, 1.6, 1.1, 1.8, 1.4],
    "irregularity": [0, 1, 0, 1, 0],
    "age": [25, 45, 30, 55, 40],
    "gender_encoded": [0, 1, 0, 1, 0],
    "prakriti_encoded": [0, 1, 2, 1, 2],
    "dosha_label": ["Vata", "Pitta", "Kapha", "Pitta", "Kapha"],
    "improved": [1, 0, 1, 0, 1]
})

X = data.drop(columns=["dosha_label", "improved"])
y_dosha = data["dosha_label"]
y_outcome = data["improved"]

dosha_model = RandomForestClassifier(random_state=42)
outcome_model = RandomForestClassifier(random_state=42)

dosha_model.fit(X, y_dosha)
outcome_model.fit(X, y_outcome)

# ----------------------------
# SAVE MODELS (CORRECTLY)
# ----------------------------
joblib.dump(dosha_model, "ml/models/dosha_classifier.pkl")
joblib.dump(outcome_model, "ml/models/outcome_predictor.pkl")

print("✅ Models trained and saved successfully")
