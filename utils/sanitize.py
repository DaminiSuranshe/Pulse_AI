import numpy as np

def sanitize_features(features: dict):
    clean = {}
    for k, v in features.items():
        if v is None:
            clean[k] = None
        elif isinstance(v, (float, int)):
            if np.isnan(v) or np.isinf(v):
                clean[k] = None
            else:
                clean[k] = float(v)
        else:
            clean[k] = v
    return clean
