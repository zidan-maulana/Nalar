# API Contract

**Status:** Active
**Owner:** Lukman & Bule (Backend)
**Terakhir diupdate:** 2026-08-10

Dokumen ini adalah sumber kebenaran tunggal untuk seluruh endpoint API di Nalar (baik API Backend Utama untuk Frontend maupun API Internal AI Service).

---

## Konvensi Umum
- **Backend Base URL:** `https://api.nalar.app/v1`
- **AI Service Internal URL:** `http://ai-service.internal:8000`
- **Format Response Standard:**
  ```json
  {
    "success": true,
    "data": { ... },
    "error": null
  }
  ```
- **Error Response Standard:**
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "INVALID_INPUT",
      "message": "Detail pesan kesalahan"
    }
  }
  ```
- **Auth:** Bearer JWT (Supabase Auth).

---

## Endpoint AI Service (Internal REST - FastAPI)

### 1. `POST /extract-concepts`
- **Deskripsi:** Menerima file materi (PDF/PPTX) dan meng-extract Concept Graph.
- **Request Body:**
  ```json
  {
    "material_id": "uuid-string",
    "file_url": "https://storage.supabase.co/..."
  }
  ```
- **Response `data`:** Mengembalikan JSON [Concept Graph](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/ai-output-schema.md#1-concept-graph-output-stage-1-document-ingestion--concept-extraction).

### 2. `POST /generate-questions`
- **Deskripsi:** Menghasilkan 1 pertanyaan pembuka & Master Rubric 3 level untuk suatu konsep.
- **Request Body:**
  ```json
  {
    "concept_id": "c-001",
    "name": "Congestion Control",
    "definition": "Mekanisme jaringan...",
    "source_reference": "Slide 12"
  }
  ```
- **Response `data`:** Mengembalikan JSON [Master Rubric](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/ai-output-schema.md#2-master-rubric-output-stage-2-question-generation).

### 3. `POST /dialogue/turn`
- **Deskripsi:** Memproses 1 turn dialog pengujian adaptif via ADK LoopAgent.
- **Request Body:**
  ```json
  {
    "session_id": "sess-uuid-001",
    "concept_id": "c-001",
    "user_answer": "Congestion control itu mengatur agar data pengirim tidak bikin router macet.",
    "rubric": { ... }
  }
  ```
- **Response `data`:** Mengembalikan JSON [Evaluasi Turn & Next Question](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/ai-output-schema.md#3-evaluasi-jawaban--dialogue-turn-output-stage-3-adaptive-dialogue-engine).

### 4. `POST /score`
- **Deskripsi:** Menghitung Depth Score & Confidence Calibration setelah Stage 3 selesai.
- **Request Body:**
  ```json
  {
    "session_id": "sess-uuid-001",
    "concept_id": "c-001",
    "confidence_input": 5,
    "level_reached": "sebab-akibat",
    "rounds_used": 1
  }
  ```
- **Response `data`:** Mengembalikan JSON [Depth Score & Calibration](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/ai-output-schema.md#4-depth-score--confidence-calibration-output-stage-4-scoring).

---

## Endpoint Backend Utama (Eksternal REST)

### 1. `POST /materials/upload`
- **Deskripsi:** Mengunggah file materi kuliah pengguna ke Supabase Storage.
- **Form Data:** `file` (Multipart), `title` (String).

### 2. `GET /materials/:material_id/concepts`
- **Deskripsi:** Mengambil daftar konsep yang diekstrak dari materi.

### 3. `POST /sessions/start`
- **Deskripsi:** Memulai sesi tanya-jawab untuk konsep tertentu.

### 4. `POST /sessions/:session_id/turn`
- **Deskripsi:** Mengirim jawaban mahasiswa per giliran.

### 5. `POST /sessions/:session_id/score`
- **Deskripsi:** Mengirim nilai rasa yakin pengguna (1-5) dan mendapatkan skor akhir + grafik kesadaran diri.

---

## Perubahan
Setiap perubahan pada endpoint wajib di-update di dokumen ini dan diinfokan ke tim terkait.