import asyncio
import json
from app.schemas.concept import ExtractConceptsRequest
from app.schemas.rubric import GenerateQuestionsRequest
from app.schemas.dialogue import DialogueTurnRequest
from app.schemas.score import ScoreRequest
from app.schemas.remedial import DiagnosticExplainRequest, ChipActionRequest

from app.endpoints.extract_concepts import extract_concepts
from app.endpoints.generate_questions import generate_questions
from app.endpoints.dialogue import dialogue_turn
from app.endpoints.score import score_concept
from app.endpoints.remedial import explain_diagnostic, process_chip_action

def print_banner(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

async def run_full_pipeline_test():
    print_banner("🚀 MEMULAI PENGUJIAN FULL PIPELINE NALAR AI SERVICE (STAGE 1 - 5)")

    # -------------------------------------------------------------
    # STAGE 1: Concept Extraction
    # -------------------------------------------------------------
    print_banner("1. STAGE 1: Concept Extraction (POST /extract-concepts)")
    req_s1 = ExtractConceptsRequest(
        material_id="mat-101",
        file_url="https://storage.supabase.co/materials/jaringan_komputer_bab3.pdf"
    )
    res_s1 = await extract_concepts(req_s1)
    print(json.dumps(res_s1.model_dump(), indent=2, ensure_ascii=False))

    first_concept = res_s1.concepts[0]
    concept_id = first_concept.concept_id
    concept_name = first_concept.name
    concept_def = first_concept.definition

    # -------------------------------------------------------------
    # STAGE 2: Question Generation & Master Rubric
    # -------------------------------------------------------------
    print_banner(f"2. STAGE 2: Question & Master Rubric Generation (POST /generate-questions) - [{concept_name}]")
    req_s2 = GenerateQuestionsRequest(
        concept_id=concept_id,
        name=concept_name,
        definition=concept_def,
        source_reference="Slide 12"
    )
    res_s2 = await generate_questions(req_s2)
    print(json.dumps(res_s2.model_dump(), indent=2, ensure_ascii=False))

    # -------------------------------------------------------------
    # STAGE 3: Adaptive Dialogue Engine (Mode Ujian Turn 1)
    # -------------------------------------------------------------
    print_banner(f"3. STAGE 3: Adaptive Interrogation Engine Turn 1 (POST /dialogue/turn)")
    user_answer_turn1 = "Congestion control itu pembatasan data dari pengirim agar router penerima tidak penuh."
    print(f" Pertanyaan AI  : {res_s2.opening_question}")
    print(f" Jawaban User   : '{user_answer_turn1}'")

    req_s3 = DialogueTurnRequest(
        session_id="sess-mvp-001",
        concept_id=concept_id,
        user_answer=user_answer_turn1,
        current_level="definisi",
        rounds_used=1,
        rubric=res_s2
    )
    res_s3 = await dialogue_turn(req_s3)
    print(json.dumps(res_s3.model_dump(), indent=2, ensure_ascii=False))

    # -------------------------------------------------------------
    # STAGE 4: Scoring & Confidence Calibration
    # -------------------------------------------------------------
    print_banner("4. STAGE 4: Scoring & Confidence Calibration (POST /score)")
    confidence_user = 5  # User merasa sangat yakin (5/5 = 100%)
    req_s4 = ScoreRequest(
        session_id="sess-mvp-001",
        concept_id=concept_id,
        confidence_input=confidence_user,
        level_reached=res_s3.evaluation.level_reached,
        rounds_used=res_s3.rounds_used
    )
    res_s4 = score_concept(req_s4)
    print(json.dumps(res_s4.model_dump(), indent=2, ensure_ascii=False))

    # -------------------------------------------------------------
    # STAGE 5: Diagnostic Remedial Engine & Smart Chips (Mode Belajar)
    # -------------------------------------------------------------
    print_banner("5. STAGE 5: Diagnostic Remedial 3-Layer Explanation (POST /explain/diagnostic)")
    req_s5 = DiagnosticExplainRequest(
        concept_id=concept_id,
        concept_name=concept_name,
        concept_definition=concept_def,
        evidence_trail=res_s3.evaluation.evidence_trail,
        criteria_missing=res_s3.evaluation.criteria_missing
    )
    res_s5 = await explain_diagnostic(req_s5)
    print(json.dumps(res_s5.model_dump(), indent=2, ensure_ascii=False))

    print_banner("5b. STAGE 5: Action Chip Click - '💡 Bikin Analogi Lain' (POST /explain/chip)")
    req_chip = ChipActionRequest(
        session_id="sess-mvp-001",
        concept_id=concept_id,
        chip_id="another_analogy",
        current_turn_count=1
    )
    res_chip = await process_chip_action(req_chip)
    print(json.dumps(res_chip.model_dump(), indent=2, ensure_ascii=False))

    print_banner("🎉 PENGUJIAN PIPELINE SELESAI & LULUS 100%!")

if __name__ == "__main__":
    asyncio.run(run_full_pipeline_test())
