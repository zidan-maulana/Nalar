import os
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from app.schemas.dialogue import DialogueTurnRequest, DialogueTurnResponse, TurnEvaluationDetail
from app.config import settings
from google import genai
from google.genai import types

class InternalLLMEvalResult(BaseModel):
    """Schema internal untuk menampung hasil evaluasi LLM per turn"""
    input_category: Literal["VALID_ATTEMPT", "EXPLICIT_REFUSAL", "NONSENSE_OR_OFFTOPIC"] = Field(
        "VALID_ATTEMPT",
        description="Klasifikasi input: VALID_ATTEMPT, EXPLICIT_REFUSAL, NONSENSE_OR_OFFTOPIC"
    )
    passed_current_level: bool = Field(..., description="True jika kriteria level saat ini sudah terpenuhi")
    evidence_trail: List[str] = Field(..., description="Kutipan bukti jawaban pengguna")
    criteria_met: List[str] = Field(default_factory=list, description="Kriteria yang berhasil dipenuhi")
    criteria_missing: List[str] = Field(default_factory=list, description="Kriteria yang belum dipenuhi")
    user_is_confused: bool = Field(False, description="True jika pengguna menyatakan bingung/minta bocoran")
    simplified_rephrased_question: Optional[str] = Field(None, description="Pertanyaan ulang yang lebih sederhana jika bingung")

def load_prompt() -> str:
    """Membaca system prompt evaluasi dialog dari file markdown."""
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/dialogue_evaluation.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Evaluasi jawaban pengguna terhadap master rubric secara objektif tanpa memberikan kunci jawaban."

def process_dialogue_turn(request: DialogueTurnRequest) -> DialogueTurnResponse:
    """
    Logika Inti Drill-Down LoopAgent Stage 3 (Adversarial Guard Hardened):
    1. Mengklasifikasikan input (VALID_ATTEMPT, EXPLICIT_REFUSAL, NONSENSE_OR_OFFTOPIC).
    2. Jika EXPLICIT_REFUSAL ("gatau", "pass") -> Langsung selesaikan sesi ujian (is_completed = True).
    3. Jika NONSENSE_OR_OFFTOPIC ("asdfg", "wkwk") -> Berikan teguran dosen & penalti round.
    4. Jika VALID_ATTEMPT -> Evaluasi normal terhadap Master Rubric level saat ini.
    """
    if not settings.GEMINI_API_KEY:
        # Mock Response jika API Key belum diset
        return DialogueTurnResponse(
            session_id=request.session_id,
            concept_id=request.concept_id,
            current_level="sebab-akibat",
            rounds_used=1,
            is_completed=False,
            next_question="Bisakah kamu menjelaskan apa dampak jika router mengalami buffer overflow?",
            evaluation=TurnEvaluationDetail(
                level_reached="definisi",
                evidence_trail=[f"Pengguna menjawab: '{request.user_answer}'"],
                criteria_met=["Menjelaskan pengertian dasar"],
                criteria_missing=["Belum menjelaskan dampak sebab-akibat"]
            )
        )

    # 1. Cari kriteria rubrik untuk level saat ini
    current_level_rubric = next(
        (lvl for lvl in request.rubric.levels if lvl.level == request.current_level),
        None
    )
    criteria_list = current_level_rubric.criteria if current_level_rubric else []

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    system_instruction = load_prompt()

    eval_prompt = (
        f"Level Yang Sedang Diuji: {request.current_level}\n"
        f"Kriteria Rubrik Level Ini: {criteria_list}\n"
        f"Jawaban Mahasiswa: '{request.user_answer}'\n\n"
        f"Tolong klasifikasikan input_category dan evaluasi apakah jawaban mahasiswa memenuhi kriteria di atas. "
        f"Ingat aturan Mode Ujian: Jangan berikan penjelasan materi."
    )

    try:
        response = client.models.generate_content(
            model=settings.DEFAULT_LLM_MODEL,
            contents=[eval_prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=InternalLLMEvalResult,
                temperature=0.2, # Temperature 0.2 untuk ketegasan evaluasi & anti-hallucination
            ),
        )

        eval_res = InternalLLMEvalResult.model_validate_json(response.text)

    except Exception as e:
        # Fallback cerdas jika terjadi rate limit 429 / error LLM
        user_text = request.user_answer.lower()
        if any(w in user_text for w in ["gatau", "tidak tahu", "pass", "skip", "gelap", "gak tau", "ndak tahu"]):
            cat = "EXPLICIT_REFUSAL"
            passed = False
        elif len(user_text.strip()) < 3 or any(w in user_text for w in ["asdf", "qwerty", "1234", "zzzz"]):
            cat = "NONSENSE_OR_OFFTOPIC"
            passed = False
        else:
            cat = "VALID_ATTEMPT"
            # Cek apakah jawaban mengandung kata kunci teknis
            passed = any(w in user_text for w in ["l4", "layer 4", "port", "multiplex", "flow control", "transport", "tcp", "udp", "ack", "buffer", "overflow", "retrans"])

        eval_res = InternalLLMEvalResult(
            input_category=cat,
            passed_current_level=passed,
            evidence_trail=[f"Jawaban pengguna: '{request.user_answer}'"],
            criteria_met=criteria_list[:1] if passed else [],
            criteria_missing=[] if passed else criteria_list,
            user_is_confused=False
        )


    # 2. Logika Penentuan State LoopAgent (State Transition Hardened)
    level_order = ["definisi", "sebab-akibat", "transfer"]
    curr_idx = level_order.index(request.current_level) if request.current_level in level_order else 0

    max_rounds = 2
    is_completed = False
    next_question = None
    new_level = request.current_level
    new_rounds = request.rounds_used

    if eval_res.input_category == "EXPLICIT_REFUSAL":
        # Pengguna menyerah ("gatau", "pass", "skip", "tidak tahu") -> Langsung selesaikan sesi ujian!
        is_completed = True
        next_question = "Baik, karena kamu menyatakan belum mempelajari materi ini, mari kita langsung masuk ke Mode Belajar Diagnostik untuk mempelajarinya dari nol."
        highest_level_reached = level_order[curr_idx - 1] if curr_idx > 0 else "none"

    elif eval_res.input_category == "NONSENSE_OR_OFFTOPIC":
        # Pengguna iseng / ngasal / prompt injection -> Berikan teguran tegas & penalti round!
        new_rounds = request.rounds_used + 1
        if new_rounds > max_rounds:
            is_completed = True
            next_question = "Sesi ujian dihentikan karena jawaban tidak relevan secara berturut-turut. Mari masuk ke Mode Belajar."
        else:
            next_question = f"Jawabanmu ('{request.user_answer[:30]}...') tidak relevan dengan pertanyaan ujian. Harap jawab pertanyaan ujian secara serius!"
        highest_level_reached = level_order[curr_idx - 1] if curr_idx > 0 else "none"

    else:
        # VALID_ATTEMPT -> Evaluasi normal
        if eval_res.user_is_confused and eval_res.simplified_rephrased_question:
            next_question = eval_res.simplified_rephrased_question
            new_rounds += 1
        elif eval_res.passed_current_level:
            if curr_idx < len(level_order) - 1:
                new_level = level_order[curr_idx + 1]
                new_rounds = 1
                next_question = f"Bagus! Sekarang untuk level {new_level.upper()}: Bisakah kamu menganalisis lebih jauh mengenai {request.rubric.concept_id} dalam konteks {new_level}?"
            else:
                is_completed = True
                next_question = None
        else:
            if request.rounds_used < max_rounds:
                new_rounds = request.rounds_used + 1
                next_question = f"Jawabanmu sudah memuat beberapa poin, namun bisakah kamu menjelaskan lebih spesifik mengenai: {', '.join(eval_res.criteria_missing)}?"
            else:
                is_completed = True
                next_question = None

        if eval_res.passed_current_level:
            highest_level_reached = request.current_level
        else:
            highest_level_reached = level_order[curr_idx - 1] if curr_idx > 0 else "none"

    return DialogueTurnResponse(
        session_id=request.session_id,
        concept_id=request.concept_id,
        current_level=new_level,
        rounds_used=new_rounds,
        is_completed=is_completed,
        next_question=next_question,
        evaluation=TurnEvaluationDetail(
            level_reached=highest_level_reached,
            evidence_trail=eval_res.evidence_trail,
            criteria_met=eval_res.criteria_met,
            criteria_missing=eval_res.criteria_missing
        )
    )


