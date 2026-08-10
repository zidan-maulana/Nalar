# PRD: Confidence Calibration

**Status:** Draft
**Owner:** Zidan (AI) + Delon (FE)
**Terakhir diupdate:** [tanggal]

## 1. Overview & Goals
Mengukur seberapa akurat pengguna menilai pemahamannya sendiri, dengan membandingkan rasa yakin (self-reported) terhadap depth score aktual. Fitur ini menjawab langsung masalah "merasa paham vs paham beneran" yang jadi motivasi awal produk.

## 2. Problem Statement & User Persona
Mahasiswa sering overconfident (merasa yakin padahal lemah) atau underconfident (merasa tidak yakin padahal sebenarnya paham). Overconfidence lebih berbahaya karena pengguna tidak sadar perlu belajar lagi.

## 3. Scope

**In (Fase 1):**
- Pertanyaan "seberapa yakin" (skala 1-5) ditanyakan setelah pengguna selesai menjawab satu konsep, sebelum depth score ditampilkan
- Grafik confidence vs depth score aktual
- Skor ringkasan "Skor Kesadaran Diri"

**Out:**
- [TODO]

## 4. User Flow / User Stories
- Sebagai mahasiswa, saya ingin tahu apakah saya overconfident atau underconfident di suatu konsep, supaya saya bisa mengoreksi cara belajar saya
- [TODO]

## 5. Functional Requirements
[TODO, contoh: skala input (1-5), rumus "Skor Kesadaran Diri", threshold overconfident/underconfident]

## 6. Non-functional Requirements
[TODO]

## 7. Acceptance Criteria
[TODO]

## 8. Dependencies & Assumptions
- Bergantung pada Understanding Depth Score sebagai pembanding
- Output dipakai Gap Radar untuk menentukan prioritas

## 9. Open Questions
- [TODO]