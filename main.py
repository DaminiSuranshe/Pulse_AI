from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="AI-Powered Ayurvedic Wellness Platform",
    description="Clinical Decision Support System (Pilot)",
    version="1.0"
)

app.include_router(router)
