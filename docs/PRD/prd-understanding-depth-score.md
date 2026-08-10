# PRD: Understanding Depth Score

**Status:** Draft
**Owner:** Zidan (AI) + Lukman (BE) + Delon (FE)
**Terakhir diupdate:** [tanggal]

## 1. Overview & Goals
Fitur yang memberikan skor kedalaman pemahaman pengguna per konsep, bukan sekadar penilaian benar/salah. Tujuan: pengguna tahu secara spesifik seberapa dalam pemahamannya di tiap konsep dari materi yang diuji.

## 2. Problem Statement & User Persona
Mahasiswa sering merasa sudah paham materi setelah belajar, tapi tidak punya cara objektif mengukur kedalaman pemahaman tersebut sebelum ujian sesungguhnya. Persona utama: mahasiswa S1 yang sedang mempersiapkan UTS/UAS/sidang dengan materi kuliah spesifik.

## 3. Scope

**In (Fase 1):**
- Skor per konsep, ditampilkan setelah sesi tanya-jawab untuk konsep tersebut selesai
- Skor dihitung berdasarkan hasil evaluasi dari Penguji Adaptif (lihat `prd-penguji-adaptif.md`)

**Out (belum fase ini):**
- Skor gabungan lintas mata kuliah
- Perbandingan skor antar waktu (progress tracking historis)

## 4. User Flow / User Stories
- Sebagai mahasiswa, saya ingin melihat skor pemahaman saya per konsep, supaya saya tahu bagian mana yang perlu dipelajari lagi
- [TODO: tambahkan user story lain sesuai kebutuhan]

## 5. Functional Requirements
[TODO: diisi bersama owner AI dan FE, contoh: format skor 0-100%, threshold kategori kuat/sedang/lemah, dst]

## 6. Non-functional Requirements
- Skor harus disertai evidence trail (alasan/kutipan jawaban yang mendasari penilaian)
- [TODO: requirement performa, misal waktu tampil skor setelah sesi selesai]

## 7. Acceptance Criteria
[TODO: kriteria konkret dan bisa dites, misal "skor tampil dalam X detik setelah sesi konsep selesai, disertai minimal 1 evidence trail"]

## 8. Dependencies & Assumptions
- Bergantung pada output evaluasi dari Penguji Adaptif
- Skema data mengikuti `ai-output-schema.md`

## 9. Open Questions
- [TODO]