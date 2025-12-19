import numpy as np
import neurokit2 as nk

# ----------------------------
# HEART RATE
# ----------------------------
def extract_heart_rate(peaks, fs):
    if peaks is None or len(peaks) < 2:
        raise ValueError("Not enough peaks to compute heart rate")

    rr_intervals = np.diff(peaks) / fs

    if np.mean(rr_intervals) <= 0:
        raise ValueError("Invalid RR intervals")

    hr = 60.0 / np.mean(rr_intervals)
    return hr, rr_intervals


# ----------------------------
# HRV FEATURES
# ----------------------------
def extract_hrv(rr_intervals):
    if rr_intervals is None or len(rr_intervals) < 2:
        return 0.0, 0.0  # clinically safer than NULL

    sdnn = float(np.std(rr_intervals))

    diff_rr = np.diff(rr_intervals)
    rmssd = float(np.sqrt(np.mean(diff_rr ** 2))) if len(diff_rr) > 0 else 0.0

    return sdnn, rmssd


# ----------------------------
# AMPLITUDE FEATURES
# ----------------------------
def extract_amplitude_features(beats):
    if beats is None or len(beats) == 0:
        return {
            "pulse_amplitude_mean": 0.0,
            "pulse_amplitude_std": 0.0
        }

    amplitudes = [
        float(np.max(beat) - np.min(beat))
        for beat in beats if len(beat) > 0
    ]

    if len(amplitudes) == 0:
        return {
            "pulse_amplitude_mean": 0.0,
            "pulse_amplitude_std": 0.0
        }

    return {
        "pulse_amplitude_mean": float(np.mean(amplitudes)),
        "pulse_amplitude_std": float(np.std(amplitudes))
    }


# ----------------------------
# RHYTHM IRREGULARITY
# ----------------------------
def extract_rhythm_irregularity(rr_intervals):
    if rr_intervals is None or len(rr_intervals) < 2:
        return 0.0

    mean_rr = np.mean(rr_intervals)
    if mean_rr <= 0:
        return 0.0

    return float(np.std(rr_intervals) / mean_rr)


# ----------------------------
# MASTER FEATURE EXTRACTOR
# ----------------------------
def extract_all_features(ppg_signal, fs, peaks, beats):
    hr, rr_intervals = extract_heart_rate(peaks, fs)
    sdnn, rmssd = extract_hrv(rr_intervals)
    amp_features = extract_amplitude_features(beats)
    rhythm_irregularity = extract_rhythm_irregularity(rr_intervals)

    features = {
        "heart_rate": float(hr),
        "hrv_sdnn": float(sdnn),
        "hrv_rmssd": float(rmssd),
        "pulse_irregularity": float(rhythm_irregularity),
        **amp_features
    }

    return features
