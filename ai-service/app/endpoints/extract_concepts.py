import os
from fastapi import APIRouter, HTTPException, status
from app.schemas.concept import ExtractConceptsRequest, ConceptGraphResponse, ConceptItem
from app.config import settings
from google import genai
from google.genai import types

router = APIRouter(prefix="/extract-concepts", tags=["Stage 1: Concept Extraction"])

def load_prompt() -> str:
    """Membaca system prompt ekstraksi dari file markdown."""
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/concept_extraction.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Ekstrak semua konsep utama dari materi kuliah ini secara objektif."

@router.post("", response_model=ConceptGraphResponse, status_code=status.HTTP_200_OK)
async def extract_concepts(request: ExtractConceptsRequest):
    """
    Endpoint Stage 1: Menerima materi kuliah dan meng-extract Concept Graph.
    Menggunakan Gemini 2.5 Flash dengan Structured Output (Pydantic).
    """
    if not settings.GEMINI_API_KEY:
        # Jika API Key belum diset di .env, kita kembalikan mock data untuk testing lokal
        return ConceptGraphResponse(
            material_id=request.material_id,
            concepts=[
                ConceptItem(
                    concept_id="c-001",
                    name="Congestion Control (Mock)",
                    definition="Mekanisme jaringan untuk mencegah atau menangani kelebihan beban pada router dan link.",
                    source_reference="Slide 12 (Bab 3)",
                    related_concepts=["c-002"]
                ),
                ConceptItem(
                    concept_id="c-002",
                    name="Flow Control (Mock)",
                    definition="Mekanisme membatasi laju pengiriman data agar sesuai kapasitas receiver.",
                    source_reference="Slide 8 (Bab 3)",
                    related_concepts=["c-001"]
                )
            ]
        )

    try:
        # Inisialisasi Google GenAI Client dengan API Key
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        system_instruction = load_prompt()

        # Konfigurasi Structured Output menggunakan Pydantic Schema ConceptGraphResponse
        response = client.models.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            contents=[
                f"Tolong ekstrak konsep dari materi berikut (URL: {request.file_url}) untuk material_id: {request.material_id}"
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ConceptGraphResponse,
                temperature=0.2, # Low temperature agar output sangat objektif & deterministik
            ),
        )

        # Parse response langsung menjadi Pydantic model
        result = ConceptGraphResponse.model_validate_json(response.text)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal melakukan ekstraksi konsep: {str(e)}"
        )
