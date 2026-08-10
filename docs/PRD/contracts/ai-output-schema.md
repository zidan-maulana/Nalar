# AI Output Schema

**Status:** Active
**Owner:** Zidan (AI)
**Terakhir diupdate:** 2026-08-10

Dokumen ini mendefinisikan format data yang dihasilkan oleh setiap tahap pipeline AI. Backend dan Frontend merujuk ke dokumen ini untuk mengetahui struktur data yang akan diterima/disimpan. Semua respons dari AI Service **WAJIB** lolos validasi Pydantic sebelum dikirim atau disimpan.

---

## 1. Concept Graph (Output Stage 1: Document Ingestion & Concept Extraction)
**Endpoint AI:** `POST /extract-concepts`

```json
{
  "material_id": "uuid",
  "concepts": [
    {
      "concept_id": "c-001",
      "name": "Congestion Control",
      "definition": "Mekanisme jaringan untuk mencegah atau menangani kelebihan beban pada router dan link.",
      "source_reference": "Slide 12 (Bab 3: Transport Layer)",
      "related_concepts": ["c-002", "c-005"]
    }
  ]
}
```

---

## 2. Master Rubric (Output Stage 2: Question Generation)
**Endpoint AI:** `POST /generate-questions`

```json
{
  "concept_id": "c-001",
  "opening_question": "Bisakah kamu menjelaskan apa yang dimaksud dengan Congestion Control dan mengapa itu penting dalam jaringan komputer?",
  "levels": [
    {
      "level": "definisi",
      "criteria": [
        "Menjelaskan pengertian congestion control sebagai penanganan beban berlebih",
        "Membedakan antara flow control (receiver limit) dan congestion control (network limit)"
      ]
    },
    {
      "level": "sebab-akibat",
      "criteria": [
        "Menjelaskan dampak jika terjadi congestion (packet loss, delay spike)",
        "Menjelaskan pemicu terjadinya congestion (buffer overflow di router)"
      ]
    },
    {
      "level": "transfer",
      "criteria": [
        "Mampu menerapkan analisis ke studi kasus dunia nyata (misal: penanganan kemacetan di protokol TCP vs UDP)",
        "Mampu memberikan solusi perbaikan arsitektur jaringan jika terjadi bottleneck"
      ]
    }
  ]
}
```

---

## 3. Evaluasi Jawaban & Dialogue Turn (Output Stage 3: Adaptive Dialogue Engine)
**Endpoint AI:** `POST /dialogue/turn`

```json
{
  "session_id": "sess-uuid-001",
  "concept_id": "c-001",
  "current_level": "sebab-akibat",
  "rounds_used": 1,
  "is_completed": false,
  "next_question": "Bagaimana router memberi tahu sender bahwa jaringan mulai macet sebelum terjadi packet drop?",
  "evaluation": {
    "level_reached": "definisi",
    "evidence_trail": [
      "Pengguna menyebutkan: 'Congestion control itu pembatasan data dari pengirim agar router tidak penuh'"
    ],
    "criteria_met": [
      "Menjelaskan pengertian congestion control"
    ],
    "criteria_missing": [
      "Belum membedakan dengan flow control"
    ]
  }
}
```

---

## 4. Depth Score & Confidence Calibration (Output Stage 4: Scoring)
**Endpoint AI:** `POST /score`

```json
{
  "session_id": "sess-uuid-001",
  "concept_id": "c-001",
  "depth_score": 70.0,
  "confidence_input": 5,
  "confidence_normalized": 100.0,
  "delta": 30.0,
  "calibration_status": "overconfident",
  "summary_reason": "Pengguna merasa sangat yakin (skala 5/5 = 100%), namun pemahamannya baru mencapai level Sebab-Akibat (70%) dan belum menguasai level Transfer."
}
```

---

## Aturan Perubahan Skema
Setiap perubahan field atau tipe data pada dokumen ini **WAJIB**:
1. Dicatat terlebih dahulu pada [schema-change-log.md](file:///c:/Documents/Projects/Nalar/docs/PRD/context/schema-change-log.md).
2. Diinformasikan ke owner Backend (Lukman/Haikal) dan Frontend (Andika/Mahardika) sebelum kode di-update.