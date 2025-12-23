def attach_recommendation_context(df, dominant_dosha):
    df = df.copy()

    df["warming"] = 1 if dominant_dosha == "Vata" else 0
    df["cooling"] = 1 if dominant_dosha == "Pitta" else 0
    df["light"] = 1 if dominant_dosha == "Kapha" else 0
    df["calming"] = 1 if dominant_dosha in ["Vata", "Pitta"] else 0

    return df
