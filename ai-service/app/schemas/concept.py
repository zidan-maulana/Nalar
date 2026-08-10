from pydantic import BaseModel, Field
from typing import List, Optional

class ConceptItem(BaseModel):
    """
    Model representasi satu konsep yang diekstrak dari materi kuliah.
    """
    concept_id: str = Field(
        ...,
        description="ID unik untuk konsep dalam konteks materi ini, contoh: 'c-001'",
        example="c-001"
    )
    name: str = Field(
        ...,
        description="Nama konsep atau topik utama",
        example="Congestion Control"
    )
    definition: str = Field(
        ...,
        description="Penjelasan ringkas dan akurat tentang konsep tersebut sesuai materi",
        example="Mekanisme jaringan untuk mencegah atau menangani kelebihan beban pada router dan link."
    )
    source_reference: Optional[str] = Field(
        None,
        description="Referensi asal halaman/slide dari materi",
        example="Slide 12 (Bab 3: Transport Layer)"
    )
    related_concepts: List[str] = Field(
        default_factory=list,
        description="Daftar concept_id lain yang berkaitan erat dengan konsep ini",
        example=["c-002", "c-005"]
    )

class ConceptGraphResponse(BaseModel):
    """
    Model skema output Stage 1: Concept Graph untuk seluruh materi.
    Mencakup daftar konsep yang tervalidasi Pydantic.
    """
    material_id: str = Field(..., description="ID materi kuliah yang diproses")
    concepts: List[ConceptItem] = Field(..., description="Daftar konsep yang berhasil diekstrak")

class ExtractConceptsRequest(BaseModel):
    """
    Model payload input request HTTP POST ke /extract-concepts.
    """
    material_id: str = Field(..., description="ID materi kuliah dari database")
    file_url: str = Field(..., description="URL file PDF/PPTX di Supabase Storage")
