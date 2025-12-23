import joblib
from sklearn.linear_model import LogisticRegression
from ml.personalization.dataset_builder import build_personalization_dataset
from ml.personalization.feature_builder import attach_recommendation_context
from ml.datasets.synthetic_outcomes import attach_outcomes

df = build_personalization_dataset()
df = attach_recommendation_context(df, dominant_dosha="Vata")
df = attach_outcomes(df)

X = df.drop(columns=["improved"])
y = df["improved"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "ml/models/recommendation_personalizer.pkl")
