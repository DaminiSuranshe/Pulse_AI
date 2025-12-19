import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from ml.datasets.dataset_builder import build_dosha_dataset
from ml.datasets.synthetic_outcomes import attach_outcomes

df = build_dosha_dataset()
df = attach_outcomes(df)

X = df.drop(columns=["dominant_dosha", "improved"])
y = df["improved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = GradientBoostingClassifier(n_estimators=150)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
print("ROC AUC:", roc_auc_score(y_test, probs))

joblib.dump(model, "ml/models/outcome_predictor.pkl")
