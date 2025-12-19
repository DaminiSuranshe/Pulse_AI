import numpy as np
import neurokit2 as nk
from scipy.signal import butter, filtfilt, find_peaks

def bandpass_filter(signal, fs, lowcut=0.5, highcut=5.0, order=3):
    """
    Bandpass filter for PPG signal
    Removes motion artifacts & high-frequency noise
    """
    if len(signal) < 30:
        raise ValueError(
            f"Signal too short for filtering. Need at least 30 samples, got {len(signal)}"
        )
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal

def detect_peaks(ppg_signal, fs):
    try:
        signals, info = nk.ppg_process(ppg_signal, sampling_rate=fs)
        peaks = info["PPG_Peaks"]
        return np.array(peaks, dtype=int)
    except Exception as e:
        print("Peak detection failed:", e)
        return np.array([])

def segment_beats(signal, peaks, window=50):
    beats = []
    for p in peaks:
        start = max(0, p - window)
        end = min(len(signal), p + window)
        beat = signal[start:end]
        if len(beat) > 10:
            beats.append(beat)
    return beats