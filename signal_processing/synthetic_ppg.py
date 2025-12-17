import numpy as np

def generate_ppg(duration_sec=120, fs=125, pattern="vata"):
    t = np.linspace(0, duration_sec, duration_sec * fs)

    if pattern == "vata":
        base = np.sin(2 * np.pi * 1.4 * t)
        noise = np.random.normal(0, 0.15, len(t))
        signal = base + noise

    elif pattern == "pitta":
        base = 1.2 * np.sin(2 * np.pi * 1.8 * t)
        signal = base + np.random.normal(0, 0.08, len(t))

    elif pattern == "kapha":
        base = 0.8 * np.sin(2 * np.pi * 1.0 * t)
        signal = base + np.random.normal(0, 0.04, len(t))

    else:
        raise ValueError("Unknown pattern")

    return signal
