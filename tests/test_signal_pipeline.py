from signal_processing.preprocessing import bandpass_filter, detect_peaks, segment_beats
from signal_processing.feature_extraction import extract_all_features
from signal_processing.synthetic_ppg import generate_ppg

FS = 125

ppg = generate_ppg(pattern="vata")
filtered = bandpass_filter(ppg, FS)
peaks = detect_peaks(filtered, FS)
beats = segment_beats(filtered, peaks)

features = extract_all_features(filtered, FS, peaks, beats)

print("Extracted Features:")
for k, v in features.items():
    print(f"{k}: {v:.3f}")
