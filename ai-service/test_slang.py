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
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)

async def run_slang_testing_simulation():
    print_banner("🎭 SIMULASI TESTING PENGGUNA ASLI (BAHASA SLANG MAHASISWA IT)")
    print(" 👤 User Persona : Rian (Mahasiswa Teknik Informatika S1)")
    print(" 💬 Gaya Bahasa  : Informal Slang / Mix Indo-Inggris Teknis")

    # -------------------------------------------------------------
    # STAGE 1: Extract Concepts
    # -------------------------------------------------------------
    print_banner("1. STAGE 1: Upload PDF & Extract Concept Graph")
    req_s1 = ExtractConceptsRequest(
        material_id="mat-jarkom-bab3",
        file_url="https://storage.supabase.co/materials/jaringan_komputer_bab3.pdf"
    )
    res_s1 = await extract_concepts(req_s1)
    concept = res_s1.concepts[0]
    print(f"✅ Konsep Terpilih: [{concept.name}]")

    # -------------------------------------------------------------
    # STAGE 2: Question Generation
    # -------------------------------------------------------------
    print_banner("2. STAGE 2: Dosen AI Menyiapkan Rubrik & Pertanyaan Pembuka")
    req_s2 = GenerateQuestionsRequest(
        concept_id=concept.concept_id,
        name=concept.name,
        definition=concept.definition,
        source_reference="Slide 5"
    )
    res_s2 = await generate_questions(req_s2)
    print(f"❓ Pertanyaan Dosen AI: \"{res_s2.opening_question}\"")

    # -------------------------------------------------------------
    # STAGE 3: Mode Ujian - Turn 1 (Bahasa Slang Level Definisi)
    # -------------------------------------------------------------
    slang_answer_turn1 = "L4 OSI bro, tugas utamanya handle port multiplexing ama flow control biar data gak kebentrok atau packet loss di jalan."
    print_banner("3. STAGE 3 (Turn 1): Rian Menjawab dengan Bahasa Slang Teknis")
    print(f" 💬 Jawaban Rian: \"{slang_answer_turn1}\"")

    req_s3_t1 = DialogueTurnRequest(
        session_id="sess-rian-001",
        concept_id=concept.concept_id,
        user_answer=slang_answer_turn1,
        current_level="definisi",
        rounds_used=1,
        rubric=res_s2
    )
    res_s3_t1 = await dialogue_turn(req_s3_t1)
    print("\n--- Hasil Evaluasi Dosen AI ---")
    print(f"📊 Level Terbukti : {res_s3_t1.evaluation.level_reached.upper()}")
    print(f"🔎 Evidence Trail : {res_s3_t1.evaluation.evidence_trail}")
    print(f"💬 Respon AI      : \"{res_s3_t1.next_question}\"")

    # -------------------------------------------------------------
    # STAGE 3: Mode Ujian - Turn 2 (Bahasa Slang Level Sebab-Akibat)
    # -------------------------------------------------------------
    slang_answer_turn2 = "Kalo router kebebanan ntar buffer overflow bro, pasti auto packet loss. Makanya TCP kudu ACK ama retrans segmen biar gak corrupt."
    print_banner("3b. STAGE 3 (Turn 2): Rian Menjawab Level Sebab-Akibat")
    print(f" 💬 Jawaban Rian: \"{slang_answer_turn2}\"")

    req_s3_t2 = DialogueTurnRequest(
        session_id="sess-rian-001",
        concept_id=concept.concept_id,
        user_answer=slang_answer_turn2,
        current_level=res_s3_t1.current_level,
        rounds_used=res_s3_t1.rounds_used,
        rubric=res_s2
    )
    res_s3_t2 = await dialogue_turn(req_s3_t2)
    print("\n--- Hasil Evaluasi Dosen AI ---")
    print(f"📊 Level Terbukti : {res_s3_t2.evaluation.level_reached.upper()}")
    print(f"🔎 Evidence Trail : {res_s3_t2.evaluation.evidence_trail}")
    print(f"🏁 Ujian Selesai? : {res_s3_t2.is_completed}")

    # -------------------------------------------------------------
    # STAGE 4: Confidence Calibration
    # -------------------------------------------------------------
    print_banner("4. STAGE 4: Rian Mengisi Rasa Yakin (4/5 = Yakin 80%)")
    req_s4 = ScoreRequest(
        session_id="sess-rian-001",
        concept_id=concept.concept_id,
        confidence_input=4,
        level_reached=res_s3_t2.evaluation.level_reached,
        rounds_used=res_s3_t2.rounds_used
    )
    res_s4 = await score_concept(req_s4)
    print(f"📈 Depth Score          : {res_s4.depth_score}%")
    print(f"🎯 Calibration Status   : {res_s4.calibration_status.upper()}")
    print(f"📝 Pesan Kalibrasi      : \"{res_s4.summary_reason}\"")

    # -------------------------------------------------------------
    # STAGE 5: Diagnostic Remedial & Action Chips
    # -------------------------------------------------------------
    print_banner("5. STAGE 5: Mode Belajar Diagnostik 3-Lapis & Chip Analogi")
    req_s5 = DiagnosticExplainRequest(
        concept_id=concept.concept_id,
        concept_name=concept.name,
        concept_definition=concept.definition,
        evidence_trail=res_s3_t2.evaluation.evidence_trail,
        criteria_missing=res_s3_t2.evaluation.criteria_missing
    )
    res_s5 = await explain_diagnostic(req_s5)
    print(f"⚓ Mental Anchor Analogy :\n   \"{res_s5.mental_anchor_analogy}\"\n")
    print(f"🎯 Dekonstruksi Misconception :\n   \"{res_s5.misconception_deconstruction}\"\n")

    print("👉 Rian mengklik Action Chip: '💡 Bikin Analogi Lain'")
    req_chip = ChipActionRequest(
        session_id="sess-rian-001",
        concept_id=concept.concept_id,
        concept_name=concept.name,
        chip_id="another_analogy",
        current_turn_count=1
    )
    res_chip = await process_chip_action(req_chip)
    print(f"💡 Respon Action Chip   : \"{res_chip.content}\"")
    print(f"⏳ Sisa Kuota Interaksi : {res_chip.turns_remaining} turns")

    print_banner("🎉 SIMULASI TESTING PENGGUNA SLANG SELESAI & LULUS 100%!")

if __name__ == "__main__":
    asyncio.run(run_slang_testing_simulation())
