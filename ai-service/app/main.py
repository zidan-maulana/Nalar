import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.config import settings
from app.endpoints import extract_concepts, generate_questions, dialogue, score, remedial

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="Nalar AI Service API",
    description="Microservice AI untuk Nalar: Concept Extraction, Question Generation, Adaptive Interrogation Engine, Scoring, & Diagnostic Remedial",
    version="1.0.0",
)

# Konfigurasi CORS (Cross-Origin Resource Sharing) agar API bisa diakses Backend/Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi Router Endpoints
app.include_router(extract_concepts.router)
app.include_router(generate_questions.router)
app.include_router(dialogue.router)
app.include_router(score.router)
app.include_router(remedial.router)

@app.get("/playground", response_class=HTMLResponse)
def get_playground():
    """
    Endpoint Visual Playground untuk testing interaktif 5 Stage Pipeline Nalar AI Service di Browser.
    """
    playground_path = os.path.join(os.path.dirname(__file__), "static/playground.html")
    if os.path.exists(playground_path):
        with open(playground_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Playground HTML file tidak ditemukan.</h1>"

@app.get("/")
def read_root():
    """
    Endpoint utama untuk mengecek status service.
    """
    return {
        "status": "online",
        "service": "Nalar AI Service",
        "model_default": settings.DEFAULT_LLM_MODEL,
        "environment": settings.ENVIRONMENT,
        "playground_url": "http://127.0.0.1:8000/playground"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint untuk monitoring sistem.
    """
    return {"status": "healthy"}





