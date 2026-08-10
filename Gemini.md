# GEMINI.md — Rules untuk Modul AI Nalar

## Baca Dulu Sebelum Kerja
- `docs/context/project-context.md` — konteks produk secara keseluruhan
- `docs/prd/prd-ai-module.md` — PRD detail modul AI, acuan utama
- `docs/contracts/ai-output-schema.md` — skema data yang WAJIB diikuti persis
- `docs/contracts/db-schema.md` — skema database
- `docs/contracts/api-contract.md` — format endpoint yang harus konsisten dengan yang dipakai backend

## Stack
- Bahasa: Python
- API framework: FastAPI
- LLM: Google Gemini API — default Gemini 2.5 Flash, JANGAN pakai 2.5 Pro untuk pemakaian rutin (limit free tier jauh lebih ketat)
- Agent framework: Google ADK, khusus untuk Adaptive Dialogue Engine (Stage 3), pakai LoopAgent
- Validasi output: Pydantic, wajib untuk semua respons LLM sebelum disimpan atau dikirim balik
- Database: PostgreSQL (Supabase)

## Aturan Kerja
1. Semua output dari Gemini WAJIB divalidasi lewat Pydantic sebelum disimpan atau dikirim balik. Jangan pernah percaya JSON dari LLM secara langsung tanpa validasi.
2. Prompt disimpan di folder `prompts/`, terpisah dari kode logic.
3. Kalau menemukan kebutuhan field/data yang tidak ada di `ai-output-schema.md` atau `db-schema.md`, JANGAN mengarang field baru sendiri. Tulis dulu di `docs/context/schema-change-log.md`.
4. Selama Mode Ujian (Stage 3), agent TIDAK BOLEH memberi jawaban atau penjelasan konsep dalam bentuk apapun kepada pengguna, hanya boleh mengulang pertanyaan dengan kalimat berbeda kalau pengguna menyatakan bingung.
5. Rubric (kriteria penilaian per level) bersifat statis, dibuat sekali di Stage 2, tidak boleh digenerate ulang saat evaluasi di Stage 3.
6. Setiap hasil evaluasi wajib menyertakan evidence trail (kutipan singkat dari jawaban pengguna), tidak boleh cuma kesimpulan tanpa bukti.

## Struktur Folder
Lihat bagian "Struktur Folder yang Disarankan" di `docs/prd/prd-ai-module.md`.