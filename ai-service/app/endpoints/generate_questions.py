import os
from fastapi import APIRouter, HTTPException, status
from app.schemas.rubric import GenerateQuestionsRequest, MasterRubricResponse, RubricLevel
from app.config import settings
from google import genai
from google.genai import types

router = APIRouter(prefix="/generate-questions", tags=["Stage 2: Question & Rubric Generation"])

def load_prompt() -> str:
    """Membaca system prompt pembuatan pertanyaan & rubrik dari file markdown."""
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/question_generation.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Buat pertanyaan pembuka dan master rubric 3 level (definisi, sebab-akibat, transfer) secara objektif."

@router.post("", response_model=MasterRubricResponse, status_code=status.HTTP_200_OK)
async def generate_questions(request: GenerateQuestionsRequest):
    """
    Endpoint Stage 2: Menghasilkan Pertanyaan Pembuka & Master Rubric 3 Level (Definisi, Sebab-Akibat, Transfer).
    Menggunakan Gemini 2.5 Flash dengan Structured Output Pydantic.
    """
    if not settings.GEMINI_API_KEY:
        # Jika API Key belum diset di .env, kita kembalikan mock data untuk testing lokal
        return MasterRubricResponse(
            concept_id=request.concept_id,
            opening_question=f"Bisakah kamu menjelaskan apa yang dimaksud dengan {request.name} dan mengapa itu penting?",
            levels=[
                RubricLevel(
                    level="definisi",
                    criteria=[
                        f"Menjelaskan pengertian mendasar dari {request.name}",
                        "Menyebutkan komponen atau batasan utama konsep"
                    ]
                ),
                RubricLevel(
                    level="sebab-akibat",
                    criteria=[
                        f"Menjelaskan dampak jika {request.name} tidak berjalan dengan baik",
                        "Menjelaskan alur pemicu masalah pada konsep ini"
                    ]
                ),
                RubricLevel(
                    level="transfer",
                    criteria=[
                        f"Menerapkan konsep {request.name} pada studi kasus nyata",
                        "Memberikan analisis pemecahan masalah berbasis skenario baru"
                    ]
                )
            ]
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        system_instruction = load_prompt()

        prompt_input = (
            f"Konsep: {request.name}\n"
            f"Definisi Asal: {request.definition}\n"
            f"Referensi: {request.source_reference or 'Tidak ada'}\n\n"
            f"Tolong buatkan pertanyaan pembuka dan master rubric 3 level (definisi, sebab-akibat, transfer) "
            f"untuk concept_id: {request.concept_id}."
        )

        response = client.models.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            contents=[prompt_input],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=MasterRubricResponse,
                temperature=0.2, # Low temperature untuk konsistensi rubrik
            ),
        )

        result = MasterRubricResponse.model_validate_json(response.text)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal generate pertanyaan & rubrik: {str(e)}"
        )
