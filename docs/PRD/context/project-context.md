# Project Context: Nalar

**Status:** Living document, update kalau ada perubahan keputusan
**Terakhir diupdate:** [tanggal]

Dokumen ini adalah sumber konteks tunggal untuk seluruh anggota tim, dipakai sebagai input ke AI saat menyusun PRD, technical design, atau dokumen kerja lain. Kalau ada perubahan keputusan project, update dokumen ini duluan sebelum dipakai lagi.

## 1. Apa itu Nalar
Platform AI yang mensimulasikan ujian berbasis materi kuliah milik pengguna sendiri (PPT/PDF/modul/notes), mengukur seberapa dalam pemahaman seseorang (bukan sekadar benar/salah), dan memberi tahu kalau pengguna merasa sudah paham padahal sebenarnya belum.

**Tagline:** "Bukan sekadar benar. Tapi seberapa paham."

## 2. Target Pengguna
Mahasiswa S1 yang sedang mempersiapkan UTS/UAS/sidang, dengan materi kuliah spesifik dari dosen masing-masing. Fase lanjut: dosen yang ingin memantau pemahaman kelasnya (lihat Mode Dosen).

## 3. Masalah yang Diselesaikan
Mahasiswa belajar berjam-jam tapi tidak punya cara objektif mengetahui apakah mereka benar-benar paham atau hanya menghafal. Alat evaluasi yang ada (kuis, flashcard, pilihan ganda) hanya mengukur benar-salah, bukan kedalaman pemahaman.

## 4. Kenapa Ini Beda dari Kompetitor
Kompetitor global (Trainexus, AiLearn360, Probe, Viva Master) sudah punya mekanisme serupa (upload materi, AI menguji adaptif). Yang membedakan Nalar:
- Mengukur confidence calibration (gap antara rasa yakin dan kompetensi asli), belum ada di kompetitor manapun
- Lokal untuk konteks Indonesia (bahasa, gaya ujian ala sidang Indonesia)
- Punya Mode Dosen (institusional), kompetitor lain murni B2C

## 5. Fitur Fase 1 (yang sedang dibangun)

1. **Understanding Depth Score** — skor kedalaman pemahaman per konsep, disertai evidence trail (alasan penilaian, bukan angka tanpa konteks)
2. **Penguji Adaptif (Adaptive Interrogation Engine)** — AI memberi pertanyaan lanjutan sampai jelas apakah pengguna paham atau menghafal. Drill-down berjenjang: definisi → sebab-akibat → transfer ke kasus lain. Mode Ujian: AI tidak memberi jawaban langsung, hanya boleh mengulang pertanyaan dengan kalimat lain
3. **Knowledge Gap Radar** — visualisasi status kuat/lemah/belum diuji per konsep, prioritas tertinggi untuk konsep yang overconfident
4. **Confidence Calibration** — pengguna ditanya "seberapa yakin" (skala 1-5) setelah menjawab satu konsep, sebelum skor ditampilkan. Dibandingkan dengan depth score aktual untuk mendeteksi overconfident/underconfident
5. **Mode Dosen (versi minimal)** — dosen membuat kelas, assign materi, melihat dashboard agregat dan individual. Bukan pengganti nilai resmi. Mahasiswa wajib memberi consent sebelum ikut

## 6. Fitur Fase 2 / Backlog (belum dibangun sekarang)
- Academic Battle Mode (duel pemahaman antar mahasiswa)
- Simulasi Ujian Lisan berbasis suara
- Dukungan materi matematika (rumus, validasi pakai Computer Algebra System)
- Cakupan universal (SD-perguruan tinggi, materi non-akademik) — visi jangka panjang, bukan scope sekarang

## 7. Arsitektur Pipeline Teknis (High-Level)
1. Document Ingestion & Concept Extraction — materi diparsing jadi concept graph (konsep, definisi, relasi, referensi sumber), disimpan di Postgres
2. Question Generation — generate pertanyaan per konsep (Bloom's Taxonomy) + master rubric
3. Adaptive Dialogue Engine — AI bertanya, evaluasi jawaban berdasar rubric, drill-down atau lanjut
4. Scoring & Explainability — depth score + evidence trail
5. Gap Radar — visualisasi hasil

**Keputusan desain kunci:**
- Rubric hybrid: kriteria dibuat sekali di awal per konsep (statis), cara AI menggali jawaban tetap fleksibel (dinamis)
- Drill-down berbasis level pemahaman yang dicapai, bukan jumlah pertanyaan tetap
- Satu model AI dipakai untuk semua tahap, dengan instruksi/prompt berbeda per tahap (bukan sistem terpisah per tahap)

## 8. Prinsip Data
- Database (Postgres) adalah single source of truth
- Semua data sesi (jawaban, skor, evidence trail) wajib disimpan sejak awal development untuk keperluan validasi nanti

## 9. Struktur Tim

| Anggota | Fokus |
|---|---|
| Zidan | AI: concept extraction, question generation, adaptive dialogue engine, scoring, confidence calibration |
| Lukman & Bule | Backend: core (DB, API, concept graph, rubric, scoring) dan Mode Dosen (auth, consent, multi-kelas, dashboard data) |
| Kanjut & Delon | Frontend: flow mahasiswa (upload, sesi tanya-jawab, hasil) dan dashboard dosen + visualisasi |
| Thomas | UI/UX: wireframe, flow, persona/tone AI examiner |

## 10. Dokumen Terkait
- PRD per fitur: `/docs/prd/`
- Contract teknis (API, skema output AI, skema database): `/docs/contracts/`
- Konvensi coding agent: `/docs/context/agent-conventions.md`