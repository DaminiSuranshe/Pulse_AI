from database.db import Base, engine
from models.patient import Patient
# import other models later (PulseRecording, Features, etc.)

def init_db():
    Base.metadata.create_all(bind=engine)
