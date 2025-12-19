import pandas as pd

def preprocess_dosha_data(df: pd.DataFrame):
    X = df.drop(columns=["dominant_dosha"])
    y = df["dominant_dosha"]

    return X, y
