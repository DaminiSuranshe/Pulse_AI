import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

def bandpass_filter(signal, fs, lowcut=0.5, highcut=8.0, order=4):
    """
    Bandpass filter for PPG signal
    Removes motion artifacts & high-frequency noise
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal


def detect_peaks(ppg_signal, fs):
    """
    Detect systolic peaks in PPG waveform
    """
    distance = int(0.4 * fs)  # minimum distance between beats
    peaks, _ = find_peaks(ppg_signal, distance=distance, prominence=0.2)

    return peaks


def segment_beats(ppg_signal, peaks):
    """
    Segment pulse waveform into individual beats
    """
    beats = []
    for i in range(len(peaks) - 1):
        beat = ppg_signal[peaks[i]:peaks[i + 1]]
        beats.append(beat)

    return beats
