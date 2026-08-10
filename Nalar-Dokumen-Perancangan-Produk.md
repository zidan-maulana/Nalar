# Nalar — Dokumen Perancangan Produk

## 1. Latar Belakang Masalah

Mahasiswa sering belajar berjam-jam untuk UTS, UAS, atau sidang, tapi tidak punya cara objektif untuk tahu apakah mereka benar-benar paham materi atau hanya merasa paham (menghafal tanpa pemahaman mendalam). Alat evaluasi yang ada sekarang (kuis, flashcard, pilihan ganda) mengukur benar-salah, bukan kedalaman pemahaman.

## 2. Solusi & Positioning

**Nama:** Nalar

**Tagline:** "Bukan sekadar benar. Tapi seberapa paham."

**Positioning statement:**
Nalar adalah platform AI yang mensimulasikan ujian berbasis materi kuliah milik pengguna sendiri, mengukur seberapa dalam pemahaman seseorang (bukan sekadar benar/salah), dan memberi tahu jika seseorang merasa sudah siap padahal sebenarnya belum.

**Kategori produk:** Pre-exam understanding verification tool / AI oral examiner. Bukan platform belajar dari nol (beda dari Zenius/RuangGuru), tapi alat verifikasi pemahaman sebelum menghadapi ujian sesungguhnya, menggunakan materi yang sudah dipelajari dari sumber manapun.

**Target pengguna awal:** Mahasiswa S1 dengan materi kuliah spesifik dari dosen masing-masing (bukan pasar massal K12/UTBK yang sudah dikuasai RuangGuru/Zenius).

## 3. Diferensiasi dari Kompetitor

Riset menemukan beberapa kompetitor dengan mekanisme serupa (AI examiner berbasis materi upload, follow-up question, tracking gap): Trainexus, AiLearn360, Probe (Oncourse AI), Viva Master, MyAnswer, Geeky Medics AI Tutor. Mekanisme inti "upload materi lalu AI menguji secara adaptif" sudah bukan hal baru di pasar global.

Celah yang belum digarap kompetitor:
- Tidak ada yang secara eksplisit mengukur confidence calibration (gap antara rasa yakin dan kompetensi aktual)
- Tidak ada yang lokal untuk konteks Indonesia (bahasa, gaya "dosen killer" khas sidang Indonesia, kurikulum lokal)
- Semua kompetitor bersifat B2C murni (mahasiswa latihan sendiri), belum ada yang punya mode institusional untuk dosen

## 4. Fitur Utama

### Fase 1 (MVP inti)
1. **Understanding Depth Score** — skor kedalaman pemahaman per konsep, bukan sekadar benar/salah
2. **Penguji Adaptif (Adaptive Interrogation Engine)** — AI terus memberi pertanyaan lanjutan sampai terlihat jelas apakah pengguna paham atau hanya menghafal
3. **Knowledge Gap Radar** — memetakan konsep mana yang sudah dikuasai dan mana yang masih jadi celah
4. **Confidence Calibration** — mengukur seberapa akurat pengguna menilai pemahamannya sendiri (overconfident vs underconfident)
5. **Mode Dosen (versi minimal)** — dosen membuat kelas, assign materi, melihat dashboard rekap pemahaman kelas

### Fase 2 / Backlog (modul tambahan, bisa jadi topik TA anggota tim lain nantinya)
- Academic Battle Mode (duel pemahaman antar mahasiswa)
- Simulasi Ujian Lisan berbasis suara (voice input/output)
- Dukungan materi matematika (rumus, perhitungan, lihat bagian 7)
- Cakupan universal (SD sampai perguruan tinggi, materi non-akademik seperti saham atau sejarah BTC) — dicatat sebagai visi jangka panjang, bukan bagian yang dibangun dan divalidasi sekarang

## 5. Arsitektur Pipeline Teknis

1. **Document Ingestion & Concept Extraction** — parsing materi (PPT/PDF/modul/notes), ekstraksi concept graph (konsep, definisi, relasi antar konsep, referensi ke slide/halaman asal), disimpan sebagai structured JSON di Postgres
2. **Question Generation** — generate pertanyaan open-ended per konsep berdasarkan Bloom's Taxonomy (understand, apply, analyze), sekaligus generate master rubric per konsep
3. **Adaptive Dialogue Engine** — AI bertanya, mengevaluasi jawaban berdasarkan rubric, memutuskan drill-down atau lanjut ke konsep lain. Ini bagian paling riset-heavy dan jadi core differentiator
4. **Scoring & Explainability** — depth score dengan evidence trail (kutipan jawaban pengguna yang jadi alasan penilaian)
5. **Gap Radar** — visualisasi status kuat/lemah/belum diuji per konsep

### Keputusan desain kunci
- **Rubric hybrid**: master rubric (kriteria kunci) dibuat sekali di awal per konsep dan disimpan (statis), sementara cara AI menggali jawaban tetap fleksibel dan natural (dinamis)
- **Drill-down berbasis level pemahaman**, bukan jumlah pertanyaan tetap: AI mengejar sampai pengguna mencapai level tertentu (definisi → penjelasan sebab-akibat → transfer ke kasus lain), bukan sekadar "tanya 3 kali lalu berhenti"
- **Satu model AI dengan instruksi/prompt berbeda tiap tahap**, bukan sistem terpisah per tahap. Lebih sederhana dan cukup untuk scope MVP

### Mode Ujian vs Mode Belajar
Selama sesi pengujian berlangsung, AI tidak memberi jawaban langsung meski pengguna meminta penjelasan (hanya boleh mengulang pertanyaan dengan kalimat lain). Penjelasan detail konsep yang lemah baru diberikan di Mode Belajar setelah sesi ujian selesai, berdasarkan hasil Gap Radar.

## 6. Confidence Calibration (Detail)

- Ditanyakan setelah pengguna menyelesaikan seluruh drill-down untuk satu konsep, sebelum depth score ditampilkan: "Seberapa yakin kamu dengan pemahamanmu di topik ini?" (skala 1-5)
- Divisualisasikan sebagai grafik confidence (sumbu X) vs depth score aktual (sumbu Y). Titik di atas garis diagonal = underconfident, titik di bawah garis = overconfident (paling berisiko karena pengguna tidak sadar perlu belajar lagi)
- Konsep yang overconfident diberi prioritas tertinggi di Gap Radar
- Ada skor tambahan "Skor Kesadaran Diri" sebagai ringkasan rata-rata akurasi confidence sepanjang sesi

## 7. Mode Dosen (Detail)

**Alur:**
1. Dosen membuat kelas, upload materi/silabus
2. Dosen memilih: AI generate semua pertanyaan otomatis, atau dosen menentukan konsep wajib yang harus diuji (override sebagian rubric)
3. Dosen membagikan kode kelas/link ke mahasiswa
4. Mahasiswa mengikuti sesi seperti biasa
5. Hasil semua mahasiswa masuk ke dashboard dosen

**Dua level tampilan untuk dosen:**
- Level kelas (agregat): misalnya "68% mahasiswa lemah di Congestion Control"
- Level individu (drill-down): grafik confidence-vs-depth score dan history jawaban per mahasiswa, hanya untuk mahasiswa yang terdaftar di kelas dosen tersebut

**Batasan penting:**
- Bukan pengganti nilai ujian resmi, diposisikan sebagai alat diagnostik tambahan untuk dosen
- Mahasiswa wajib memberi consent eksplisit sebelum mengikuti sesi Mode Dosen (beda dari Mode Belajar mandiri yang privat)

## 8. Edge Case: Materi Matematika (Backlog)

Materi berbasis rumus dan angka butuh penyesuaian pipeline:
- **Ekstraksi materi**: model vision cukup baik membaca rumus ketikan (LaTeX/equation editor), tapi akurasi turun untuk tulisan tangan/scan
- **Jenis pertanyaan** perlu menambah dimensi prosedural (bisa menerapkan rumus ke soal baru) dan transfer (menerapkan konsep ke konteks berbeda), tidak cukup hanya "jelaskan kenapa"
- **Input jawaban**: foto hasil kerjaan tulisan tangan lebih natural daripada mengetik notasi matematika di HP
- **Validasi jawaban numerik**: menggunakan Computer Algebra System (CAS) seperti SymPy untuk menghitung ulang jawaban yang benar dan membandingkan dengan jawaban pengguna, bukan mengandalkan LLM menilai sendiri. Untuk soal pembuktian atau geometri yang tidak bisa dihitung otomatis, tetap pakai rubric manual seperti materi teori

## 9. Metodologi Validasi

**Reliability (konsistensi sistem):**
- Uji beberapa contoh jawaban (kualitas bagus/medium/lemah) berulang kali, cek stabilitas skor
- Bandingkan skor untuk dua jawaban setara kualitas tapi beda kalimat

**Validity (apakah skor mencerminkan pemahaman asli):**
- Pilot study kecil (10-15 mahasiswa) menggunakan materi mata kuliah yang sedang berjalan, bandingkan depth score dengan nilai ujian riil
- Bandingkan penilaian AI dengan penilaian manusia (asisten dosen/kating/dosen) untuk sekumpulan jawaban yang sama

**Catatan implementasi:** semua data sesi (jawaban, skor, evidence trail) harus disimpan sejak awal development, supaya validasi ini bisa langsung dijalankan begitu MVP berjalan, tanpa perlu membangun ulang sistem logging.

## 10. Struktur Tim & Pembagian Modul

| Anggota | Fokus |
|---|---|
| Zidan | AI: concept extraction, question generation, adaptive dialogue engine, scoring + confidence calibration |
| Lukman & Haikal | Backend: satu fokus ke core (DB, API, concept graph, rubric, scoring), satu fokus ke Mode Dosen (auth, consent, multi-kelas, dashboard data) |
| Andika & Mahardika | Frontend: satu fokus ke flow mahasiswa (upload, sesi tanya-jawab, hasil), satu fokus ke dashboard dosen + visualisasi (Gap Radar, confidence graph) |
| Thomas | UI/UX: wireframe, flow, persona/tone AI examiner, berjalan paralel dari awal bareng Zidan |

**Catatan prioritas:**
- Zidan berpotensi jadi bottleneck karena AI adalah bagian terberat dan dikerjakan sendiri. Prioritaskan adaptive dialogue engine + scoring dulu; concept extraction dan question generation boleh versi sederhana di awal
- Bentuk "kontrak data" (format output AI) dan bagikan ke tim backend/frontend secepat mungkin, supaya mereka bisa mulai bangun dengan data dummy tanpa menunggu AI selesai sepenuhnya

## 11. Catatan untuk Tugas Akhir (Nanti)

Tim baru semester 5, jadi TA belum jadi driver pengembangan saat ini. Ketika waktunya tiba dan tiap anggota mengambil skripsi individual, tiap orang perlu rumusan masalah dan sudut riset yang berbeda meski sistemnya sama. Referensi arah topik per modul (AI, data architecture, akses/keamanan, visualisasi, usability, psikologi interaksi) bisa disusun ulang saat itu berdasarkan progres nyata yang sudah berjalan.

## 12. Langkah Berikutnya

- Cek ketersediaan domain dan username sosial media untuk nama "Nalar"
- Mulai Stage 1 pipeline (concept extraction) sebagai prioritas AI
- Thomas mulai wireframe dan persona AI examiner secara paralel
- Pastikan sistem logging data sesi sudah aktif sejak awal development untuk keperluan validasi nanti