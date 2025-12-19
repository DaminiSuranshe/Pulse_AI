from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
import os
from database.models import Patient
from database.db import SessionLocal
from database.models import PulseRecording, PulseFeatures, DoshaAnalysis
from signal_processing.preprocessing import bandpass_filter, detect_peaks, segment_beats
from signal_processing.feature_extraction import extract_all_features
from core.dosha_mapping import compute_dosha_scores
from utils.sanitize import sanitize_features
import numpy as np
from uuid import UUID

router = APIRouter()

UPLOAD_DIR = "uploaded_pulses"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_ppg_from_csv(file_path: str) -> np.ndarray:
    df = pd.read_csv(file_path)

    # Case 1: One row, many columns (your dataset)
    if df.shape[0] == 1:
        signal = df.iloc[0]

    # Case 2: One column, many rows
    elif df.shape[1] == 1:
        signal = df.iloc[:, 0]

    # Case 3: Mixed columns → take numeric only
    else:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            raise ValueError("No numeric PPG data found")
        signal = numeric_df.iloc[:, 0]

    signal = signal.dropna().astype(float).values

    if len(signal) < 50:
        raise ValueError("PPG signal too short")

    return signal

@router.post("/pulse/upload/{patient_id}")
def upload_pulse(
    patient_id: str,
    sampling_rate: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        patient_id = str(UUID(patient_id.strip()))
    except ValueError:
        return {"error": "Invalid patient ID format"}
    
    # Save file
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    ppg_signal = load_ppg_from_csv(file_path)

    print("PPG signal length:", len(ppg_signal))
    print("PPG signal preview:", ppg_signal[:10])

    duration = int(len(ppg_signal) / sampling_rate)

    # Store recording
    recording = PulseRecording(
        patient_id=patient_id,
        sampling_rate=sampling_rate,
        duration_sec=duration,
        raw_file_path=file_path
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)

    # Signal processing
    filtered = bandpass_filter(ppg_signal, sampling_rate)
    print("Filtered signal min/max:", filtered.min(), filtered.max())
    peaks = detect_peaks(filtered, sampling_rate)
    print("Number of detected peaks:", len(peaks))
    beats = segment_beats(filtered, peaks)
    print("Peaks sample:", peaks[:10] if len(peaks) > 0 else "NO PEAKS")
    print("Number of beats:", len(beats))

    features = extract_all_features(filtered, sampling_rate, peaks, beats)
    features = sanitize_features(features)
    feature_row = PulseFeatures(
        recording_id=recording.recording_id,
        **features
    )
    db.add(feature_row)

    dosha = compute_dosha_scores(features)

    dosha_row = DoshaAnalysis(
        recording_id=recording.recording_id,
        vata=dosha["vata"],
        pitta=dosha["pitta"],
        kapha=dosha["kapha"],
        dominant_dosha=dosha["dominant_dosha"],
        explanation=dosha["explanation"]
    )
    db.add(dosha_row)

    db.commit()

    return {
        "recording_id": recording.recording_id,
        "features": features,
        "dosha_analysis": dosha
    }

@router.post("/patients/register")
def register_patient(name: str, age: int, gender: str, db: Session = Depends(get_db)):
    patient = Patient(name=name, age=age, gender=gender)
    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {
        "patient_id": patient.patient_id,
        "message": "Patient registered successfully"
    }

