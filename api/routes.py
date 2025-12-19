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

router = APIRouter()

UPLOAD_DIR = "uploaded_pulses"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/pulse/upload/{patient_id}")
def upload_pulse(
    patient_id: str,
    sampling_rate: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    df = pd.read_csv(file_path)

    # Debug: inspect incoming dataset
    print("Uploaded CSV columns:", df.columns.tolist())

    # Robust column handling
    if "ppg_value" in df.columns:
        ppg_signal = df["ppg_value"].values
    elif "ppg" in df.columns:
        ppg_signal = df["ppg"].values
    elif "value" in df.columns:
        ppg_signal = df["value"].values
    else:
        # Handle single-column CSV without header
        ppg_signal = df.iloc[:, 0].values

    duration = len(ppg_signal) // sampling_rate


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
    peaks = detect_peaks(filtered, sampling_rate)
    beats = segment_beats(filtered, peaks)

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

