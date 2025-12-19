import numpy as np
import pandas as pd

def generate_outcome_label(row):
    score = 0

    if row["vata"] < 0.5:
        score += 1
    if row["pitta"] < 0.5:
        score += 1
    if row["kapha"] < 0.6:
        score += 1

    score += np.random.choice([0, 1])

    return 1 if score >= 2 else 0


def attach_outcomes(df):
    df["improved"] = df.apply(generate_outcome_label, axis=1)
    return df
