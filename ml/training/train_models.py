import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_FEATURES = [
    "heart_rate",
    "hrv_sdnn",
    "hrv_rmssd",
    "pulse_irregularity",
    "pulse_amplitude_mean",
    "pulse_amplitude_std"
]

# Dummy / pilot data (replace later)
data = pd.DataFrame([
    [90, 0.12, 0.18, 0.25, 0.9, 0.15, "Vata", 1],
    [110, 0.05, 0.07, 0.10, 1.6, 0.30, "Pitta", 1],
    [70, 0.03, 0.05, 0.08, 1.1, 0.10, "Kapha", 0],
], columns=MODEL_FEATURES + ["dosha", "improved"])

X = data[MODEL_FEATURES]
y_dosha = data["dosha"]
y_outcome = data["improved"]

dosha_model = RandomForestClassifier(random_state=42)
outcome_model = RandomForestClassifier(random_state=42)

dosha_model.fit(X, y_dosha)
outcome_model.fit(X, y_outcome)

joblib.dump(dosha_model, "ml/models/dosha_classifier.pkl")
joblib.dump(outcome_model, "ml/models/outcome_predictor.pkl")

print("✅ Models retrained using canonical pulse features")
