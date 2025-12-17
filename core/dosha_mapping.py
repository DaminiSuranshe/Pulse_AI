def normalize(value, min_val, max_val):
    return max(0, min(1, (value - min_val) / (max_val - min_val)))


def compute_dosha_scores(features):
    """
    Compute Vata, Pitta, Kapha scores based on pulse features
    """

    hr = features["heart_rate"]
    sdnn = features["hrv_sdnn"]
    rmssd = features["hrv_rmssd"]
    irregularity = features["pulse_irregularity"]
    amp_mean = features["pulse_amplitude_mean"]
    amp_std = features["pulse_amplitude_std"]

    # Normalized physiological indicators
    hr_norm = normalize(hr, 50, 120)
    hrv_norm = normalize((sdnn + rmssd) / 2, 0.02, 0.15)
    irr_norm = normalize(irregularity, 0.05, 0.3)
    amp_norm = normalize(amp_mean, 0.3, 2.0)
    amp_var_norm = normalize(amp_std, 0.05, 0.5)

    # Dosha Scores
    vata = (0.35 * hrv_norm +
            0.35 * irr_norm +
            0.20 * amp_var_norm +
            0.10 * hr_norm)

    pitta = (0.40 * amp_norm +
             0.30 * hr_norm +
             0.20 * (1 - irr_norm) +
             0.10 * amp_var_norm)

    kapha = (0.40 * (1 - hr_norm) +
             0.30 * (1 - hrv_norm) +
             0.20 * (1 - irr_norm) +
             0.10 * (1 - amp_var_norm))

    total = vata + pitta + kapha
    vata /= total
    pitta /= total
    kapha /= total

    dominant = max(
        {"Vata": vata, "Pitta": pitta, "Kapha": kapha},
        key=lambda x: {"Vata": vata, "Pitta": pitta, "Kapha": kapha}[x]
    )

    explanation = generate_explanation(vata, pitta, kapha, features)

    return {
        "vata": round(vata, 3),
        "pitta": round(pitta, 3),
        "kapha": round(kapha, 3),
        "dominant_dosha": dominant,
        "explanation": explanation
    }


def generate_explanation(v, p, k, features):
    reasons = []

    if v > 0.4:
        reasons.append("High rhythm variability and HRV suggest Vata dominance.")
    if p > 0.4:
        reasons.append("Strong pulse amplitude and higher heart rate suggest Pitta dominance.")
    if k > 0.4:
        reasons.append("Stable rhythm and lower variability suggest Kapha dominance.")

    if not reasons:
        reasons.append("Balanced pulse characteristics observed.")

    return " ".join(reasons)
