from sqlalchemy import Column, String, Float, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from database.db import Base
class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
class PulseRecording(Base):
    __tablename__ = "pulse_recordings"
    recording_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    sampling_rate = Column(Integer)
    duration_sec = Column(Integer)
    raw_file_path = Column(String)
    recorded_at = Column(DateTime, default=datetime.utcnow)
class PulseFeatures(Base):
    __tablename__ = "pulse_features"
    feature_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recording_id = Column(UUID(as_uuid=True), ForeignKey("pulse_recordings.recording_id"))

    heart_rate = Column(Float)
    hrv_sdnn = Column(Float)
    hrv_rmssd = Column(Float)
    pulse_irregularity = Column(Float)
    pulse_amplitude_mean = Column(Float)
    pulse_amplitude_std = Column(Float)
class DoshaAnalysis(Base):
    __tablename__ = "dosha_analysis"
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recording_id = Column(UUID(as_uuid=True), ForeignKey("pulse_recordings.recording_id"))

    vata = Column(Float)
    pitta = Column(Float)
    kapha = Column(Float)
    dominant_dosha = Column(String)
    explanation = Column(String)
