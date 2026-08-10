from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.endpoints import extract_concepts, generate_questions, dialogue, score

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="Nalar AI Service API",
    description="Microservice AI untuk Nalar: Concept Extraction, Question Generation, Adaptive Interrogation Engine, & Scoring",
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

@app.get("/")
def read_root():
    """
    Endpoint utama untuk mengecek status service.
    """
    return {
        "status": "online",
        "service": "Nalar AI Service",
        "model_default": settings.DEFAULT_LLM_MODEL,
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
def health_check():
    """
    Health check endpoint untuk monitoring sistem.
    """
    return {"status": "healthy"}




