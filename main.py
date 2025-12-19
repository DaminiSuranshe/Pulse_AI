from fastapi import FastAPI
from api.routes import router
from database.init_db import init_db
from api.routes import router as core_router
from api.ml_routes import router as ml_router

app = FastAPI(
    title="AI-Powered Ayurvedic Wellness Platform",
    description="Clinical Decision Support System (Pilot)",
    version="2.0"
)

app.include_router(router)
app.include_router(core_router)
app.include_router(ml_router)

@app.get("/")
def root():
    return {"status": "Pulse AI backend is running"}

@app.on_event("startup")
def startup_event():
    init_db()