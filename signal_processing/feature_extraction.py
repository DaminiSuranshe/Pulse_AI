import numpy as np
import neurokit2 as nk

def extract_heart_rate(peaks, fs):
    """
    Compute average heart rate (BPM)
    """
    rr_intervals = np.diff(peaks) / fs
    hr = 60 / np.mean(rr_intervals)
    return hr, rr_intervals


def extract_hrv(rr_intervals):
    """
    HRV metrics: SDNN & RMSSD
    """
    sdnn = np.std(rr_intervals)

    diff_rr = np.diff(rr_intervals)
    rmssd = np.sqrt(np.mean(diff_rr ** 2))

    return sdnn, rmssd


def extract_amplitude_features(beats):
    """
    Pulse amplitude features
    """
    amplitudes = [np.max(beat) - np.min(beat) for beat in beats]

    return {
        "pulse_amplitude_mean": np.mean(amplitudes),
        "pulse_amplitude_std": np.std(amplitudes)
    }


def extract_rhythm_irregularity(rr_intervals):
    """
    Measures rhythm variability
    """
    coefficient_variation = np.std(rr_intervals) / np.mean(rr_intervals)
    return coefficient_variation


def extract_all_features(ppg_signal, fs, peaks, beats):
    """
    Master feature extractor
    """
    hr, rr_intervals = extract_heart_rate(peaks, fs)
    sdnn, rmssd = extract_hrv(rr_intervals)
    amp_features = extract_amplitude_features(beats)
    rhythm_irregularity = extract_rhythm_irregularity(rr_intervals)

    features = {
        "heart_rate": hr,
        "hrv_sdnn": sdnn,
        "hrv_rmssd": rmssd,
        "pulse_irregularity": rhythm_irregularity,
        **amp_features
    }

    return features
