from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class RubricLevel(BaseModel):
    """
    Kriteria penilaian statis untuk satu level Bloom's Taxonomy.
    """
    level: Literal["definisi", "sebab-akibat", "transfer"] = Field(
        ...,
        description="Level taksonomi pemahaman: 'definisi', 'sebab-akibat', atau 'transfer'"
    )
    criteria: List[str] = Field(
        ...,
        description="Daftar poin kriteria kunci yang harus ada pada jawaban mahasiswa untuk lolos level ini",
        example=[
            "Menjelaskan pengertian congestion control sebagai penanganan beban berlebih di router",
            "Membedakan antara flow control (receiver limit) dan congestion control (network limit)"
        ]
    )

class MasterRubricResponse(BaseModel):
    """
    Model skema output Stage 2: Master Rubric untuk satu konsep.
    """
    concept_id: str = Field(..., description="ID konsep terkait, contoh: 'c-001'")
    opening_question: str = Field(
        ...,
        description="Pertanyaan pembuka open-ended level 'definisi' untuk memulai interogasi",
        example="Bisakah kamu menjelaskan apa yang dimaksud dengan Congestion Control dan mengapa itu penting dalam jaringan komputer?"
    )
    levels: List[RubricLevel] = Field(
        ...,
        description="Daftar kriteria rubrik statis 3 level (definisi, sebab-akibat, transfer)"
    )

class GenerateQuestionsRequest(BaseModel):
    """
    Model payload input HTTP POST ke /generate-questions.
    """
    concept_id: str = Field(..., description="ID konsep dari Stage 1")
    name: str = Field(..., description="Nama konsep, contoh: 'Congestion Control'")
    definition: str = Field(..., description="Definisi konsep dari Stage 1")
    source_reference: Optional[str] = Field(None, description="Referensi slide/halaman asal")
