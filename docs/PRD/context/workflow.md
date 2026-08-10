# Workflow Development Nalar

## Tahap 0: Alignment
1. Presentasiin dokumen konsep (`Nalar-Dokumen-Perancangan-Produk.md`) ke tim, pastiin semua align soal arah produk

## Tahap 1: Zidan Develop AI Duluan
2. Bikin PRD sendiri buat modul AI (Penguji Adaptif + Understanding Depth Score) pakai `how-to-draft-prd-with-ai.md`, jadi acuan dev sekaligus konteks ke coding agent
3. Develop sampai beneran kelar, gak perlu buru-buru karena gak ada deadline
4. Setelah kelar, update `project-context.md` dan `ai-output-schema.md` jadi versi final sesuai yang beneran dibangun (bukan lagi draft rencana)

## Tahap 2: Handoff ke Tim
5. Oper `project-context.md` + `ai-output-schema.md` (+ `db-schema.md` kalau relevan) ke Lukman, Bule, Kanjut, Delon, Thomas
6. Tiap orang upload dua file itu ke AI mereka, generate PRD modul masing-masing pakai template prompt di `how-to-draft-prd-with-ai.md` (termasuk instruksi audit gap yang udah ditambahin)
7. Tiap orang review hasil PRD dari AI sebelum dianggap final (cek bagian `[ASUMSI]`, requirement harus jelas dan bisa dites)

## Tahap 3: Development Paralel
8. Lukman, Bule, Kanjut, Delon, Thomas mulai development sesuai PRD masing-masing
9. Kalau nemu kebutuhan data tambahan yang gak ada di skema, catat di `schema-change-log.md` dan kabarin Zidan, bukan dianggap masalah
10. `agent-conventions.md` dilengkapin begitu struktur folder repo dan konvensi coding disepakatin bareng
11. Pastikan logging data sesi (jawaban, skor, evidence trail) aktif dari awal buat keperluan validasi nanti

## Tahap 4: Validasi (setelah MVP jalan)
12. Jalanin metodologi validasi (reliability test + validity test dari pilot study), pakai data yang udah kekumpul

## Referensi Dokumen
| Dokumen | Fungsi |
|---|---|
| `Nalar-Dokumen-Perancangan-Produk.md` | Konsep produk lengkap, buat presentasi |
| `docs/context/project-context.md` | Konteks padat, dipakai sebagai input ke AI |
| `docs/context/how-to-draft-prd-with-ai.md` | Panduan + template prompt bikin PRD |
| `docs/context/schema-change-log.md` | Catatan kebutuhan tambahan pas development |
| `docs/context/agent-conventions.md` | Konvensi coding buat semua agent |
| `docs/prd/*.md` | PRD per fitur, acuan development |
| `docs/contracts/*.md` | Skema teknis (API, output AI, database) |