from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ScoreRequest(BaseModel):
    """
    Payload input HTTP POST ke /score setelah Stage 3 (Adaptive Interrogation) selesai.
    """
    session_id: str = Field(..., description="ID sesi pengujian pengguna")
    concept_id: str = Field(..., description="ID konsep yang diuji")
    confidence_input: int = Field(
        ...,
        description="Nilai rasa yakin yang diisi pengguna (skala 1-5)",
        example=5
    )
    level_reached: Literal["none", "definisi", "sebab-akibat", "transfer"] = Field(
        ...,
        description="Level tertinggi Bloom's Taxonomy yang berhasil dicapai pengguna di Stage 3"
    )
    rounds_used: int = Field(
        1,
        description="Total jumlah percobaan/round yang digunakan di Stage 3",
        example=2
    )

    @field_validator("confidence_input")
    @classmethod
    def check_confidence_range(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError("confidence_input harus berupa angka bulat antara 1 sampai 5")
        return v

class ScoreResponse(BaseModel):
    """
    Model skema output Stage 4: Depth Score & Confidence Calibration.
    """
    session_id: str = Field(..., description="ID sesi pengujian")
    concept_id: str = Field(..., description="ID konsep terkait")
    depth_score: float = Field(
        ...,
        description="Skor kedalaman pemahaman aktual (skala 0.00 - 100.00)",
        example=70.0
    )
    confidence_input: int = Field(..., description="Input rasa yakin asli (1-5)")
    confidence_normalized: float = Field(
        ...,
        description="Input rasa yakin yang dinormalisasi ke skala 0-100",
        example=100.0
    )
    delta: float = Field(
        ...,
        description="Selisih antara Confidence Normalized dan Depth Score",
        example=30.0
    )
    calibration_status: Literal["overconfident", "underconfident", "accurate"] = Field(
        ...,
        description="Kategori akurasi kesadaran diri pemahaman pengguna"
    )
    summary_reason: str = Field(
        ...,
        description="Penjelasan naratif ringkas mengenai hasil evaluasi kesadaran diri"
    )
