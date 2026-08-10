# PRD: Penguji Adaptif (Adaptive Interrogation Engine)

**Status:** Draft
**Owner:** Zidan (AI)
**Terakhir diupdate:** [tanggal]

## 1. Overview & Goals
Mesin utama yang menguji pengguna dengan pertanyaan lanjutan secara adaptif sampai terlihat jelas apakah pengguna paham konsep atau hanya menghafal. Ini adalah core differentiator produk.

## 2. Problem Statement & User Persona
Kuis konvensional (pilihan ganda, single-turn) tidak bisa membedakan pemahaman asli dari hafalan. Persona: mahasiswa yang butuh simulasi mirip sidang/ujian lisan sebelum ujian sesungguhnya.

## 3. Scope

**In (Fase 1):**
- Interaksi berbasis teks
- Drill-down berjenjang: definisi → sebab-akibat → transfer ke kasus lain
- Mode Ujian: AI tidak memberi jawaban langsung, hanya boleh mengulang pertanyaan dengan kalimat berbeda jika pengguna bingung

**Out (belum fase ini):**
- Interaksi berbasis suara (masuk backlog Simulasi Ujian Lisan)
- Dukungan soal matematika/rumus (masuk backlog)

## 4. User Flow / User Stories
- Sebagai mahasiswa, saya ingin ditanya lebih lanjut kalau jawaban saya masih dangkal, supaya AI bisa menilai pemahaman saya secara akurat
- Sebagai mahasiswa, saya ingin bisa minta pertanyaan diulang dengan kalimat lain kalau saya tidak paham maksud soalnya
- [TODO: tambahkan user story lain]

## 5. Functional Requirements
[TODO, contoh: jumlah maksimal drill-down per konsep, kriteria kapan AI naik level vs berhenti, kriteria mendeteksi permintaan "bocoran jawaban" dari pengguna]

## 6. Non-functional Requirements
- Rubric evaluasi dibuat statis per konsep (lihat `ai-output-schema.md`), cara bertanya tetap fleksibel
- [TODO: batas waktu/jumlah pertanyaan per konsep]

## 7. Acceptance Criteria
[TODO, contoh: "AI berhenti drill-down begitu pengguna mencapai level transfer, atau setelah maksimal N percobaan di level yang sama"]

## 8. Dependencies & Assumptions
- Bergantung pada master rubric dari tahap Question Generation
- Output evaluasi dipakai oleh Understanding Depth Score dan Gap Radar

## 9. Open Questions
- [TODO]