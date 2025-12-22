from fastapi import FastAPI

from api.routes import router as core_router
from api.ml_routes import router as ml_router
from database.init_db import init_db
from api.recommendation_routes import router as recommendation_router

app = FastAPI(
    title="AI-Powered Ayurvedic Wellness Platform",
    description="Clinical Decision Support System (Pilot)",
    version="2.0"
)

# -------- Routers --------
app.include_router(core_router)
app.include_router(ml_router)
app.include_router(recommendation_router)

# -------- Root Health Check --------
@app.get("/")
def root():
    return {"status": "Pulse AI backend is running"}

# -------- Startup Lifecycle --------
@app.on_event("startup")
def startup_event():
    init_db()

    # Load ML models safely at startup
    from ml.inference.predict import load_models
    load_models()

@app.get("/health")
def health():
    return {
        "database": "ok",
        "ml_models": "loaded"
    }
