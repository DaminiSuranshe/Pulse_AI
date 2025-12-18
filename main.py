from fastapi import FastAPI
from api.routes import router
from database.init_db import init_db

app = FastAPI(
    title="AI-Powered Ayurvedic Wellness Platform",
    description="Clinical Decision Support System (Pilot)",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Pulse AI backend is running"}

@app.on_event("startup")
def startup_event():
    init_db()