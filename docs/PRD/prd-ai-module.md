# PRD: AI Module — Nalar

**Status:** Active
**Owner:** Zidan
**Terakhir diupdate:** [tanggal]

Dokumen ini adalah acuan teknis detail untuk seluruh bagian AI yang jadi tanggung jawab Zidan: Concept Extraction, Question Generation, Adaptive Dialogue Engine (Penguji Adaptif), dan Scoring + Confidence Calibration. Ini dipakai sebagai konteks utama untuk coding agent (Antigravity) saat development.

**Di luar scope dokumen ini:** Gap Radar (visualisasi, punya FE), Mode Dosen (BE+FE), Academic Battle Mode, Simulasi Suara, dukungan Matematika (backlog, lihat `project-context.md`).

## 1. Overview & Goals

Modul ini adalah "otak" dari Nalar: membaca materi kuliah, mengekstrak konsep, membuat pertanyaan, menguji pengguna secara adaptif, dan menghasilkan skor pemahaman yang bisa dipertanggungjawabkan (ada evidence trail, bukan angka tanpa alasan).

## 2. Tech Stack

| Komponen | Pilihan | Catatan |
|---|---|---|
| Bahasa | Python | |
| API Framework | FastAPI | Modul ini jalan sebagai service terpisah, diakses backend lewat REST sesuai `api-contract.md` |
| LLM | Google Gemini API | Default: **Gemini 2.5 Flash**. Hindari 2.5 Pro untuk pemakaian rutin (limit free tier jauh lebih ketat, ~5 RPM/50 RPD vs Flash ~10-15 RPM/250-1000 RPD) |
| Agent Framework | Google ADK | Dipakai **khusus** untuk Stage 3 (Adaptive Dialogue Engine), pakai `LoopAgent` untuk logika drill-down |
| Validasi Output | Pydantic | Wajib untuk semua respons Gemini sebelum disimpan atau dikirim balik |
| Database | PostgreSQL (via Supabase) | Single source of truth, skema di `db-schema.md` |
| Math validation (backlog) | SymPy | Belum dibangun sekarang |

## 3. Arsitektur Layanan

- Modul AI berjalan sebagai service Python terpisah (bukan menyatu dengan backend utama Lukman/Haikal), berkomunikasi lewat REST endpoint sesuai `api-contract.md`
- Data hasil tiap stage disimpan langsung ke Postgres (bukan cuma di memory), sesuai `db-schema.md`
- ADK Session cuma dipakai sebagai working memory selama satu sesi tanya-jawab per konsep berlangsung. Begitu satu konsep selesai dievaluasi, hasil finalnya di-push ke Postgres

## 4. Functional Requirements per Stage

### Stage 1: Document Ingestion & Concept Extraction

- **Endpoint:** `POST /extract-concepts`
- **Input:** file (PDF/PPTX) + metadata (material_id)
- **Proses:** tiap halaman/slide dikonversi jadi gambar, dikirim ke Gemini sekaligus (native document understanding, tidak perlu OCR/parser teks terpisah), dengan prompt ekstraksi konsep
- **Output:** tervalidasi Pydantic sesuai skema concept graph di `ai-output-schema.md`, disimpan ke tabel `concepts`
- **Kriteria selesai:** tiap concept punya `name`, `definition`, `source_reference`, dan `related_concepts` (boleh kosong)
- **Guard rail:** prompt harus eksplisit melarang AI mengarang konsep yang tidak didukung materi. Kalau materi terlalu tipis/tidak terstruktur, AI tetap ekstrak sebanyak mungkin konsep yang valid, bukan menambah-nambah

### Stage 2: Question Generation & Master Rubric

- **Endpoint:** `POST /generate-questions`
- **Input:** `concept_id` (hasil Stage 1)
- **Proses:** generate 1 pertanyaan pembuka level "definisi" + master rubric 3 level (definisi → sebab-akibat → transfer) mengikuti Bloom's Taxonomy, per konsep
- **Output:** tervalidasi sesuai skema rubric di `ai-output-schema.md`, disimpan ke tabel `rubrics`
- **Sifat:** rubric ini statis, dibuat sekali dan dipakai berulang oleh Stage 3 (lihat keputusan desain "rubric hybrid" di `project-context.md`)

### Stage 3: Adaptive Dialogue Engine (Penguji Adaptif)

- **Endpoint:** `POST /dialogue/turn`
- **Dibangun dengan:** Google ADK, `LoopAgent` sebagai inti drill-down
- **Session:** satu ADK session per kombinasi (user_id, concept_id) aktif, menyimpan level saat ini dan rounds_used

**Loop logic:**
1. Ajukan pertanyaan sesuai level saat ini (mulai dari "definisi")
2. Terima jawaban pengguna
3. Evaluasi jawaban terhadap kriteria level tersebut di master rubric (bukan generate kriteria baru saat itu juga)
4. Kalau kriteria terpenuhi → naik level, reset rounds_used ke 0
5. Kalau belum terpenuhi → rounds_used bertambah 1. Kalau rounds_used < max (default 2) → drill-down di level yang sama. Kalau sudah mencapai max → tandai level itu "belum tercapai", keluar loop
6. Loop berhenti kalau level "transfer" tercapai, ATAU max rounds di level manapun terlampaui

**Mode Ujian (hard rule, wajib di system instruction agent):**
- AI TIDAK BOLEH memberi jawaban atau penjelasan konsep dalam bentuk apapun selama loop berjalan
- Kalau pengguna menyatakan bingung dengan pertanyaan, AI HANYA boleh mengulang pertanyaan dengan kalimat berbeda, tidak boleh menjelaskan konsepnya

**Evidence trail:** tiap evaluasi wajib menyertakan kutipan singkat dari jawaban pengguna yang jadi dasar penilaian, tidak boleh cuma kesimpulan tanpa bukti

**Output per turn:** pertanyaan berikutnya (kalau loop lanjut), ATAU hasil akhir konsep (`level_reached`, `rounds_used`, `evidence_trail` lengkap) kalau loop selesai

### Stage 4: Scoring & Confidence Calibration

- **Endpoint:** `POST /score`
- **Trigger:** begitu Stage 3 selesai untuk satu konsep
- **Input tambahan:** `confidence_input` (skala 1-5) yang dikirim FE setelah pengguna menjawab "seberapa yakin"
- **depth_score:** dihitung dari `level_reached` + `rounds_used`. Titik awal yang disarankan: Definisi=40, Sebab-akibat=70, Transfer=100, dikurangi penalti kecil per rounds_used ekstra. Formula ini perlu dituning berdasarkan hasil testing riil, bukan final
- **calibration_status:** dibandingkan `confidence_input` (dinormalisasi ke skala sama dengan depth_score) vs `depth_score`. Threshold awal yang disarankan: selisih >15 poin dianggap overconfident/underconfident, di bawah itu dianggap accurate. Perlu dituning juga
- **Output:** tervalidasi sesuai skema score di `ai-output-schema.md`, disimpan ke tabel `scores`

## 5. Non-Functional Requirements

- **Reliability:** jawaban dengan kualitas setara harus menghasilkan `level_reached` yang konsisten kalau dites berulang (lihat bagian testing)
- **Explainability:** semua evaluasi wajib punya evidence_trail, tidak boleh cuma angka tanpa konteks
- **Rate limit handling:** implementasikan retry dengan exponential backoff untuk error 429 dari Gemini API
- **Modularitas prompt:** semua prompt disimpan di folder `prompts/`, terpisah dari kode logic, supaya gampang diiterasi tanpa ubah kode

## 6. Testing & Validation

- **Unit test:** validasi Pydantic schema untuk tiap endpoint
- **Reliability harness:** script yang me-replay beberapa contoh jawaban (kualitas bagus/medium/lemah) berkali-kali lewat Stage 3 + 4, cek konsistensi `level_reached` dan `depth_score`. Manfaatkan eval framework bawaan ADK untuk testing skenario multi-turn

## 7. Struktur Folder yang Disarankan

```
ai-service/
  app/
    main.py                    # FastAPI entrypoint
    endpoints/
      extract_concepts.py
      generate_questions.py
      dialogue.py
      score.py
    agents/
      dialogue_loop_agent.py   # Definisi ADK LoopAgent
    schemas/                   # Pydantic models, mirror ai-output-schema.md
    prompts/
      concept_extraction.md
      question_generation.md
      dialogue_evaluation.md
      scoring.md
    db/                        # Koneksi Postgres, query functions
  tests/
  .env                         # GEMINI_API_KEY, DATABASE_URL
  requirements.txt
```

## 8. Dependencies & Assumptions

- Bergantung pada `ai-output-schema.md` dan `db-schema.md` tetap sinkron dengan implementasi ini
- Asumsi: 1 material = 1 mata kuliah/topik, belum ada penggabungan lintas mata kuliah (itu kebutuhan RAG, masuk backlog)

## 9. Open Questions

- Formula pasti `depth_score` dan threshold `calibration_status` masih perlu dituning berdasarkan hasil testing riil
- Nilai `max_rounds` per level yang paling pas (default 2, bisa disesuaikan setelah dicoba ke user asli)