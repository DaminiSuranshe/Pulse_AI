import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from ml.features.schema import MODEL_FEATURES

# ----------------------------
# TEMP SYNTHETIC DATA
# (MATCHING SIGNAL FEATURES)
# ----------------------------
data = pd.DataFrame({
    "heart_rate": [70, 82, 65, 90, 78],
    "hrv_rmssd": [45, 32, 50, 28, 40],
    "hrv_sdnn": [60, 48, 65, 42, 55],
    "pulse_amplitude_mean": [1.2, 1.6, 1.1, 1.8, 1.4],
    "pulse_amplitude_std": [0.2, 0.3, 0.15, 0.35, 0.25],
    "pulse_rate_variability": [0.3, 0.5, 0.2, 0.6, 0.4],
    "beat_interval_mean": [0.85, 0.72, 0.92, 0.68, 0.78],
    "dosha_label": ["Vata", "Pitta", "Kapha", "Pitta", "Kapha"],
    "improved": [1, 0, 1, 0, 1]
})

X = data[MODEL_FEATURES]
y_dosha = data["dosha_label"]
y_outcome = data["improved"]

dosha_model = RandomForestClassifier(random_state=42)
outcome_model = RandomForestClassifier(random_state=42)

dosha_model.fit(X, y_dosha)
outcome_model.fit(X, y_outcome)

joblib.dump(dosha_model, "ml/models/dosha_classifier.pkl")
joblib.dump(outcome_model, "ml/models/outcome_predictor.pkl")

print("✅ Models retrained with signal-derived features")
