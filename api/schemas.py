from pydantic import BaseModel
from typing import Dict


class PulseFeatures(BaseModel):
    signal_valid: bool
    detected_peaks: int

    heart_rate: float
    hrv_sdnn: float
    hrv_rmssd: float
    pulse_irregularity: float
    pulse_amplitude_mean: float
    pulse_amplitude_std: float

class DoshaResponse(BaseModel):
    vata: float
    pitta: float
    kapha: float
    dominant_dosha: str
    explanation: str
