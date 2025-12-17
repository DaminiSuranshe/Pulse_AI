from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    age = Column(Float)
    gender = Column(String)


class DoshaAnalysis(Base):
    __tablename__ = "dosha_analysis"
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    vata = Column(Float)
    pitta = Column(Float)
    kapha = Column(Float)
    dominant_dosha = Column(String)
    explanation = Column(String)
