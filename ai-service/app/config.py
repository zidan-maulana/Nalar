import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Kelas konfigurasi aplikasi Nalar AI Service.
    Membaca environment variables dari file .env secara terstruktur dan aman.
    """
    GEMINI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gemini-3.6-flash"
    ENVIRONMENT: str = "development"
    PORT: int = 8000

    # Paramater Scoring Baseline (Configurable)
    SCORE_DEFINISI: float = 40.0
    SCORE_SEBAB_AKIBAT: float = 70.0
    SCORE_TRANSFER: float = 100.0
    PENALTY_EXTRA_ROUND: float = 5.0
    CALIBRATION_THRESHOLD: float = 15.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
