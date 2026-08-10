from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

class ActionChip(BaseModel):
    """
    Model representasi satu tombol aksi cepat (Action Chip) untuk interaksi terpandu di Mode Belajar.
    """
    chip_id: str = Field(..., description="ID unik tombol, contoh: 'another_analogy'", example="another_analogy")
    label: str = Field(..., description="Teks label tombol", example="💡 Bikin Analogi Lain")
    description: str = Field(..., description="Penjelasan singkat fungsi tombol", example="Minta analogi dunia nyata lain yang berbeda")

class DiagnosticExplainRequest(BaseModel):
    """
    Payload input HTTP POST ke /explain/diagnostic setelah Mode Ujian selesai.
    """
    concept_id: str = Field(..., description="ID konsep yang terdeteksi lemah/overconfident")
    concept_name: str = Field(..., description="Nama konsep, contoh: 'Congestion Control'")
    concept_definition: str = Field(..., description="Definisi teknis asli dari materi dosen")
    evidence_trail: List[str] = Field(
        ...,
        description="Kutipan bukti jawaban salah/kurang pas dari pengguna di Stage 3",
        example=["Pengguna menyebutkan: 'Congestion control itu sama saja dengan flow control untuk penerima'"]
    )
    criteria_missing: List[str] = Field(
        ...,
        description="Daftar poin kriteria rubrik yang belum dikuasai pengguna",
        example=["Belum membedakan antara flow control dan congestion control"]
    )

class DiagnosticExplainResponse(BaseModel):
    """
    Model skema output Penjelasan Diagnostik 3-Lapis (Stage 5).
    """
    concept_id: str = Field(..., description="ID konsep terkait")
    mental_anchor_analogy: str = Field(
        ...,
        description="Analogi dunia nyata yang mudah dibayangkan untuk membangun intuisi awal",
        example="Bayangkan Congestion Control seperti polisi lalu lintas yang mengatur debit kendaraan di perempatan..."
    )
    misconception_deconstruction: str = Field(
        ...,
        description="Penjelasan spesifik mengenai letak kekeliruan logika pengguna pada ujian tadi",
        example="Saat ujian tadi kamu menganggap flow control dan congestion control sama..."
    )
    technical_bridge: str = Field(
        ...,
        description="Penjelasan teknis yang menghubungkan kembali ke materi slide dosen",
        example="Di slide dosenmu, mekanisme ini diatur lewat Window Size di protokol TCP..."
    )
    available_action_chips: List[ActionChip] = Field(
        ...,
        description="Daftar 3 tombol aksi cepat yang tersedia untuk pendalaman terpandu"
    )

class ChipActionRequest(BaseModel):
    """
    Payload input HTTP POST ke /explain/chip saat pengguna mengklik tombol aksi cepat.
    """
    session_id: str = Field(..., description="ID sesi pengujian aktif")
    concept_id: str = Field(..., description="ID konsep yang sedang dipelajari")
    concept_name: Optional[str] = Field(None, description="Nama konsep (contoh: 'Transport Layer')")
    chip_id: Literal["another_analogy", "breakdown_term", "mini_retest"] = Field(
        ...,
        description="ID tombol yang diklik pengguna"
    )
    current_turn_count: int = Field(
        1,
        description="Jumlah turn interaksi yang sudah terpakai di Mode Belajar (Max 3)",
        example=1
    )
    selected_text: Optional[str] = Field(
        None,
        description="Kalimat atau istilah spesifik yang ingin dibedah (khusus chip 'breakdown_term')"
    )

    @field_validator("current_turn_count")
    @classmethod
    def check_turn_limit(cls, v: int) -> int:
        if v < 1:
            raise ValueError("current_turn_count minimal adalah 1")
        return v

class ChipActionResponse(BaseModel):
    """
    Model skema output respon tombol aksi cepat.
    """
    chip_id: str = Field(..., description="ID tombol yang diproses")
    content: str = Field(..., description="Teks jawaban/penjelasan ringkas (~200 token) dari AI")
    turns_remaining: int = Field(..., description="Sisa kuota interaksi di Mode Belajar untuk konsep ini (3 - current_turn_count)")
    suggest_retest: bool = Field(..., description="True jika kuota interaksi sudah habis dan pengguna disarankan Re-Test")
