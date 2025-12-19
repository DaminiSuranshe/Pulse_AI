import numpy as np

def sanitize_features(features: dict):
    """
    Ensure all features are valid numeric values.
    No NaN, No Inf, No NULL for numeric biomedical features.
    """
    clean = {}

    for k, v in features.items():
        # Missing value
        if v is None:
            clean[k] = 0.0

        # Numeric value
        elif isinstance(v, (int, float)):
            if np.isnan(v) or np.isinf(v):
                clean[k] = 0.0
            else:
                clean[k] = float(v)

        # Any unexpected type (should not happen)
        else:
            try:
                clean[k] = float(v)
            except Exception:
                clean[k] = 0.0

    return clean
