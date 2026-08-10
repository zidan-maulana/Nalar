from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from app.schemas.rubric import MasterRubricResponse

class TurnEvaluationDetail(BaseModel):
    """
    Rincian evaluasi terhadap satu giliran jawaban mahasiswa di Stage 3.
    """
    level_reached: Literal["none", "definisi", "sebab-akibat", "transfer"] = Field(
        ...,
        description="Level tertinggi yang saat ini diakui tercapai oleh mahasiswa"
    )
    evidence_trail: List[str] = Field(
        ...,
        description="Kutipan langsung/singkat dari jawaban pengguna yang mendasari alasan penilaian",
        example=["Pengguna menyebutkan: 'Congestion control itu pembatasan data dari pengirim agar router tidak penuh'"]
    )
    criteria_met: List[str] = Field(
        default_factory=list,
        description="Daftar poin kriteria rubrik yang berhasil dipenuhi pengguna pada giliran ini"
    )
    criteria_missing: List[str] = Field(
        default_factory=list,
        description="Daftar poin kriteria rubrik yang belum dipenuhi"
    )

class DialogueTurnRequest(BaseModel):
    """
    Payload request HTTP POST ke /dialogue/turn.
    """
    session_id: str = Field(..., description="ID sesi pengujian aktif")
    concept_id: str = Field(..., description="ID konsep yang sedang diuji")
    concept_name: Optional[str] = Field(None, description="Nama konsep (contoh: 'Transport Layer (Bab 3)')")
    user_answer: str = Field(..., description="Teks jawaban dari mahasiswa")
    current_level: Literal["definisi", "sebab-akibat", "transfer"] = Field(
        "definisi",
        description="Level yang sedang diuji pada giliran ini"
    )
    rounds_used: int = Field(
        1,
        description="Jumlah percobaan/round yang sudah terpakai pada level saat ini"
    )
    rubric: MasterRubricResponse = Field(..., description="Master Rubric statis dari Stage 2")

class DialogueTurnResponse(BaseModel):
    """
    Model skema output Stage 3: Adaptive Dialogue Turn & Next Question.
    """
    session_id: str = Field(..., description="ID sesi pengujian")
    concept_id: str = Field(..., description="ID konsep yang diuji")
    current_level: Literal["definisi", "sebab-akibat", "transfer"] = Field(
        ...,
        description="Level pemahaman saat ini setelah evaluasi giliran ini"
    )
    rounds_used: int = Field(..., description="Jumlah percobaan yang terpakai pada level saat ini")
    is_completed: bool = Field(
        ...,
        description="True jika sesi tanya-jawab untuk konsep ini sudah selesai (mencapai level Transfer atau Max Rounds)"
    )
    next_question: Optional[str] = Field(
        None,
        description="Pertanyaan lanjutan untuk giliran berikutnya (None jika is_completed = True)"
    )
    evaluation: TurnEvaluationDetail = Field(..., description="Rincian evaluasi dan evidence trail")
