import pandas as pd
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import PulseFeatures, DoshaAnalysis

def build_dosha_dataset():
    db: Session = SessionLocal()

    query = (
        db.query(
            PulseFeatures.heart_rate,
            PulseFeatures.hrv_sdnn,
            PulseFeatures.hrv_rmssd,
            PulseFeatures.pulse_irregularity,
            PulseFeatures.pulse_amplitude_mean,
            PulseFeatures.pulse_amplitude_std,
            DoshaAnalysis.dominant_dosha
        )
        .join(DoshaAnalysis, PulseFeatures.recording_id == DoshaAnalysis.recording_id)
    )

    df = pd.read_sql(query.statement, db.bind)
    db.close()

    return df
