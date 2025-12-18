from database.db import Base, engine
from database.models import Patient

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
