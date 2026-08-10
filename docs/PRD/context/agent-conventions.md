# Agent Conventions

**Status:** Draft
**Owner:** Seluruh tim
**Terakhir diupdate:** [tanggal]

Dokumen ini adalah rujukan tetap untuk semua coding agent (Antigravity, Codex, Hermes, dll) yang dipakai anggota tim, supaya output tiap orang tetap konsisten walau tools berbeda-beda.

## Referensi Wajib
Sebelum mengerjakan task apapun, agent harus merujuk ke:
- PRD fitur terkait di `/docs/prd/`
- Contract teknis di `/docs/contracts/`

## Struktur Folder Project
[TODO: definisikan struktur folder repo, contoh: `/frontend`, `/backend`, `/ai`]

## Konvensi Penamaan
[TODO: penamaan file, variable, komponen]

## Konvensi Commit
[TODO: format commit message, contoh: `feat(ai): tambah rubric generation untuk konsep baru`]

## Aturan Perubahan Contract
Setiap perubahan pada `api-contract.md`, `ai-output-schema.md`, atau `db-schema.md` wajib:
1. Diinfokan ke owner modul lain yang terdampak
2. Disetujui sebelum diimplementasikan di kode

## Review
Output dari coding agent, terutama untuk bagian Adaptive Dialogue Engine dan Scoring, wajib direview manusia sebelum merge, tidak langsung dipercaya begitu saja.