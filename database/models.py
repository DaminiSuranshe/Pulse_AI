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
    recording_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pulse_recordings.recording_id"),
        nullable=False
    )

    heart_rate = Column(Float, nullable=False)
    hrv_sdnn = Column(Float, nullable=False)
    hrv_rmssd = Column(Float, nullable=False)
    pulse_irregularity = Column(Float, nullable=False)
    pulse_amplitude_mean = Column(Float, nullable=False)
    pulse_amplitude_std = Column(Float, nullable=False)
class DoshaAnalysis(Base):
    __tablename__ = "dosha_analysis"
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recording_id = Column(UUID(as_uuid=True), ForeignKey("pulse_recordings.recording_id"))

    vata = Column(Float, nullable=False)
    pitta = Column(Float, nullable=False)
    kapha = Column(Float, nullable=False)
    dominant_dosha = Column(String, nullable=False)
    explanation = Column(String)
