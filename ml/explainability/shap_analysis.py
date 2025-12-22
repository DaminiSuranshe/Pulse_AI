import shap
import joblib
import pandas as pd

model = joblib.load("ml/models/outcome_predictor.pkl")
explainer = shap.Explainer(model)

def explain_prediction(X_sample: pd.DataFrame):
    shap_values = explainer(X_sample)
    return shap_values
