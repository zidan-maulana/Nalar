import os
from fastapi import APIRouter, HTTPException, status
from app.schemas.remedial import (
    DiagnosticExplainRequest,
    DiagnosticExplainResponse,
    ChipActionRequest,
    ChipActionResponse,
    ActionChip
)
from app.config import settings
from google import genai
from google.genai import types

router = APIRouter(prefix="/explain", tags=["Stage 5: Diagnostic Remedial Engine"])

def load_prompt() -> str:
    """Membaca system prompt remedial dari file markdown."""
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/diagnostic_remedial.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Berikan penjelasan diagnostik 3-lapis (analogi dunia nyata, koreksi salah kaprah, dan jembatan teknis)."

def get_default_chips() -> list[ActionChip]:
    return [
        ActionChip(
            chip_id="another_analogy",
            label="💡 Bikin Analogi Lain",
            description="Minta analogi dunia nyata lain yang berbeda"
        ),
        ActionChip(
            chip_id="breakdown_term",
            label="🔍 Bedah Bagian Spesifik ini",
            description="Bedah istilah atau kalimat spesifik yang belum dipahami"
        ),
        ActionChip(
            chip_id="mini_retest",
            label="🧪 Uji Ulang Mini",
            description="Lakukan uji pemahaman singkat 1 soal untuk memvalidasi pemahaman baru"
        )
    ]

@router.post("/diagnostic", response_model=DiagnosticExplainResponse, status_code=status.HTTP_200_OK)
async def explain_diagnostic(request: DiagnosticExplainRequest):
    """
    Endpoint Stage 5: Menghasilkan Penjelasan Diagnostik 3-Lapis (Analogi + Koreksi Salah Kaprah + Jembatan Teknis)
    berdasarkan bukti kesalahan jawaban pengguna di Stage 3.
    """
    if not settings.GEMINI_API_KEY:
        # Mock Response jika API Key belum diset
        return DiagnosticExplainResponse(
            concept_id=request.concept_id,
            mental_anchor_analogy=f"Bayangkan {request.concept_name} seperti polisi lalu lintas di perempatan jalan tol yang mengatur debit kendaraan...",
            misconception_deconstruction=f"Saat ujian tadi kamu menyebutkan: '{request.evidence_trail[0] if request.evidence_trail else 'jawaban kurang pas'}'. Kekeliruannya adalah...",
            technical_bridge=f"Di materi slide dosenmu, {request.concept_name} dijelaskan sebagai: {request.concept_definition}",
            available_action_chips=get_default_chips()
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        system_instruction = load_prompt()

        prompt_input = (
            f"Nama Konsep: {request.concept_name}\n"
            f"Definisi Asli Dosen: {request.concept_definition}\n"
            f"Bukti Kesalahan Jawaban Pengguna Saat Ujian: {request.evidence_trail}\n"
            f"Kriteria Yang Belum Dikuasai: {request.criteria_missing}\n\n"
            f"Tolong buatkan Penjelasan Diagnostik 3-Lapis (Analogi Dunia Nyata, Dekonstruksi Salah Kaprah, dan Jembatan Teknis) "
            f"untuk concept_id: {request.concept_id}."
        )

        response = client.models.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            contents=[prompt_input],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=DiagnosticExplainResponse,
                temperature=0.3, # Temperature 0.3 untuk keluwesan analogi yang hangat & faktual
            ),
        )

        result = DiagnosticExplainResponse.model_validate_json(response.text)
        # Pastikan chips selalu ada
        result.available_action_chips = get_default_chips()
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal generate penjelasan diagnostik: {str(e)}"
        )

@router.post("/chip", response_model=ChipActionResponse, status_code=status.HTTP_200_OK)
async def process_chip_action(request: ChipActionRequest):
    """
    Endpoint Stage 5: Memproses klik tombol aksi cepat (Action Chip).
    Menghasilkan jawaban ringkas (~200 token) dan membatasi sisa kuota interaksi (Max 3 turns).
    """
    max_turns = 3
    turns_remaining = max(0, max_turns - request.current_turn_count)
    suggest_retest = turns_remaining == 0

    if not settings.GEMINI_API_KEY:
        content_mock = {
            "another_analogy": f"Analogi alternatif lain: Bayangkan {request.concept_id} seperti sistem pendaftaran antrean di rumah sakit...",
            "breakdown_term": f"Penjelasan istilah '{request.selected_text or 'spesifik'}': Ini mengacu pada...",
            "mini_retest": f"Pertanyaan Uji Ulang Mini: Jika terjadi lonjakan trafik 2x lipat, apa langkah pertama yang dilakukan {request.concept_id}?"
        }.get(request.chip_id, "Penjelasan bantuan tambahan.")

        return ChipActionResponse(
            chip_id=request.chip_id,
            content=content_mock,
            turns_remaining=turns_remaining,
            suggest_retest=suggest_retest
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        chip_prompts = {
            "another_analogy": f"Berikan 1 analogi dunia nyata lain yang BERBEDA dan sangat mudah dibayangkan untuk konsep {request.concept_id}. Maksimal 2 paragraf ringkas.",
            "breakdown_term": f"Jelaskan istilah/kalimat berikut secara sangat sederhana dan to-the-point: '{request.selected_text or request.concept_id}'. Maksimal 2 paragraf.",
            "mini_retest": f"Berikan 1 pertanyaan uji pemahaman singkat (1 soal open-ended) untuk menguji apakah pengguna sudah paham konsep {request.concept_id} sekarang."
        }

        prompt = chip_prompts.get(request.chip_id, f"Jelaskan bantuan untuk {request.concept_id}")

        response = client.models.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.3,
            ),
        )

        return ChipActionResponse(
            chip_id=request.chip_id,
            content=response.text,
            turns_remaining=turns_remaining,
            suggest_retest=suggest_retest
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal memproses aksi chip: {str(e)}"
        )
