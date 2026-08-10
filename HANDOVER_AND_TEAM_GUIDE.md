# 🚀 Laporan Pencapaian Modul AI & Panduan Kerja Tim (Handover & Team Guide)

**Status Proyek:** Stage 1 s/d 5 AI Microservice Completed (100% Lulus QA & Verification)  
**Pemilik AI Microservice:** Zidan Maulana (AI Engineer)  
**Target Pembaca:** Lukman & Haikal (Backend), Andika & Mahardika (Frontend), Thomas (UI/UX)  
**Tanggal Handover:** 11 Agustus 2026  
**Git Branch:** `develop`  

---

## 📌 1. Ringkasan Pencapaian Zidan (AI Engineer)

Seluruh modul AI Nalar Microservice (Stage 1 s/d Stage 5) telah selesai dibangun, diuji secara otomatis dan manual, serta diperkuat terhadap berbagai *edge cases* pengguna dunia nyata.

### ✅ Pencapaian Per Stage:

1. **Stage 1 — Document Concept Extraction (`POST /extract-concepts`)**:
   - Berhasil mengekstraksi graf konsep (nama, definisi, rujukan slide, konsep terkait) dari materi PDF/teks.
   - Dilengkapi *graceful fallback* jika terjadi limit/kendala file.

2. **Stage 2 — Master Rubric & Question Generator (`POST /generate-questions`)**:
   - Menghasilkan **Master Rubric 3-Level** (*Definisi, Sebab-Akibat, Transfer*) dan **Soal Pembuka Ujian**.
   - Input konsep kini mendukung penyesuaian dinamis (*editable/custom concept input*).

3. **Stage 3 — Adaptive Oral Examiner Engine (`POST /dialogue/turn`)**:
   - Mesin Ujian Lisan Interaktif menggunakan LoopAgent dengan transisi 3-level Bloom's Taxonomy.
   - **Adversarial Input Guard**: Mampu mengklasifikasikan input menjadi `VALID_ATTEMPT`, `EXPLICIT_REFUSAL` ("gatau"/menyerah), atau `NONSENSE_OR_OFFTOPIC` ("bacot"/iseng/prompt injection).
   - **Toleransi Bahasa Gaul Teknis**: Mengenali bahasa gaul mahasiswa IT (contoh: *"L4 OSI bro, handle port multiplexing..."*) sebagai `VALID_ATTEMPT`.
   - **Penanganan Jawaban Nol**: Jawaban menyerah ("gatau") di-set `level_reached: "none"` (0% score).

4. **Stage 4 — Depth Score & Confidence Calibration (`POST /score`)**:
   - Menghitung **Depth Score (0-100%)** dengan penalti *extra rounds*.
   - Normalisasi rasa yakin (1-5 menjadi 0-100%) dan menghitung **Delta Kalibrasi**.
   - Mengkategorikan status kalibrasi (`ACCURATE`, `OVERCONFIDENT`, `UNDERCONFIDENT`).
   - Menyajikan narasi apresiatif hangat untuk mahasiswa pintar yang minder (Skor 100% tapi Yakin 1/5).

5. **Stage 5 — Diagnostic Remedial & Smart Action Chips (`POST /explain/diagnostic` & `/explain/chip`)**:
   - Menghasilkan **Penjelasan Diagnostik 3-Lapis**: *Mental Anchor Analogy*, *Dekonstruksi Misconception*, dan *Jembatan Teknis Slide Dosen*.
   - Menyediakan 3 tombol **Action Chips** (`💡 Bikin Analogi Lain`, `🔍 Bedah Istilah`, `🧪 Uji Ulang Mini`).
   - Pembatasan maksimal 3 turn interaksi dengan integrasi tombol **Uji Ulang Mini (Re-Test Mode)** langsung ke Stage 3.

6. **Interactive Sandbox & Testing UI**:
   - Menyediakan Web Sandbox di `ai-service/app/static/playground.html` (diakses di `http://127.0.0.1:8000/playground`) dengan desain *Swiss Minimalist 2-Color*.

---

## 🛠️ 2. Arahan Kerja & Dokumen WAJIB DIBACA Per Role

Seluruh tim diharapkan segera membaca dokumen panduan teknis yang sesuai dengan tanggung jawab masing-masing di bawah ini:

### ⚙️ A. Lukman & Haikal (Backend Engineers)

#### 🎯 Tugas Utama:
1. Menghubungkan REST API FastAPI AI Microservice ini ke Database PostgreSQL Supabase.
2. Mempersiapkan skema database untuk menyimpan `materials`, `concepts`, `rubrics`, `sessions`, `answers`, dan `scores`.
3. Memasang middleware Autentikasi (JWT Supabase Auth) pada endpoint.

#### 📚 Dokumen WAJIB DIBACA:
1. 📄 [docs/context/project-context.md](file:///c:/Documents/Projects/Nalar/docs/context/project-context.md) — *Konteks Produk & Visi Keseluruhan Nalar.*
2. 📄 [docs/contracts/db-schema.md](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/db-schema.md) — *Skema Database PostgreSQL / Supabase (Single Source of Truth).*
3. 📄 [docs/contracts/api-contract.md](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/api-contract.md) — *Format Endpoint REST API & Payload Request/Response.*
4. 📄 [docs/contracts/ai-output-schema.md](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/ai-output-schema.md) — *Skema Validasi Output AI (Pydantic Models).*

---

### 🎨 B. Andika & Mahardika (Frontend Engineers - Next.js)

#### 🎯 Tugas Utama:
1. Mengintegrasikan endpoint AI Service (Stage 1 s/d Stage 5) ke dalam antarmuka Next.js.
2. Membangun alur **Dual Flow**:
   - **Mode Ujian**: Tampilan ketat tanpa membocorkan jawaban, menampilkan soal pembuka & drill-down.
   - **Mode Belajar**: Tampilan penjelasan 3-lapis + tombol interaktif Action Chips (Maks 3 turns) + tombol Uji Ulang Mini.

#### 📚 Dokumen WAJIB DIBACA:
1. 📄 [docs/context/project-context.md](file:///c:/Documents/Projects/Nalar/docs/context/project-context.md) — *Visi User Journey & Alur Dual Flow.*
2. 📄 [docs/prd/prd-ai-module.md](file:///c:/Documents/Projects/Nalar/docs/PRD/prd-ai-module.md) — *PRD Detail Modul AI (Stage 1 s/d Stage 5).*
3. 📄 [docs/contracts/api-contract.md](file:///c:/Documents/Projects/Nalar/docs/PRD/contracts/api-contract.md) — *Spesifikasi Endpoint HTTP.*
4. 🖥️ [ai-service/app/static/playground.html](file:///c:/Documents/Projects/Nalar/ai-service/app/static/playground.html) — *Referensi Implementasi Interaktif Web Sandbox (Akses via http://127.0.0.1:8000/playground).*

---

### 🎨 C. Thomas (UI/UX Designer)

#### 🎯 Tugas Utama:
1. Finalisasi desain visual UI/UX Next.js untuk alur Mode Ujian & Mode Belajar.
2. Memastikan komponen *Action Chips*, indikator *Confidence Slider* (1-5), dan *Badge Kalibrasi* (`ACCURATE`, `OVERCONFIDENT`, `UNDERCONFIDENT`) tampak sangat elegan, intuitif, dan tidak *crowded*.

#### 📚 Dokumen WAJIB DIBACA:
1. 📄 [docs/context/project-context.md](file:///c:/Documents/Projects/Nalar/docs/context/project-context.md) — *Filosofi Desain & Karakter Nalar (Oral Examiner & Diagnostic Explanation).*
2. 📄 [docs/prd/prd-ai-module.md](file:///c:/Documents/Projects/Nalar/docs/PRD/prd-ai-module.md) — *Spesifikasi Penjelasan 3-Lapis & Alur Action Chips.*

---

## 🚀 3. Panduan Menjalankan AI Service di Lokal

Untuk mencoba dan menguji AI Service di komputer lokal Anda:

1. **Jalankan Uvicorn Server**:
   ```bash
   cd ai-service
   python -m uvicorn app.main:app --reload --port 8000
   ```
2. **Akses Web Testing Sandbox**:
   Buka browser di 👉 **`http://127.0.0.1:8000/playground`**
3. **Akses Swagger / OpenAPI Documentation**:
   Buka browser di 👉 **`http://127.0.0.1:8000/docs`**

---

## 🌿 4. Aturan Git Workflow

- **Branch `main`**: DIKUNCI KHUSUS rilis milestone / produksi akhir. DILARANG push langsung ke `main`.
- **Branch `develop`**: Tempat integrasi harian seluruh tim. Seluruh fitur baru wajib di-merge ke branch `develop`.

---

*Dokumen ini disusun oleh Zidan Maulana (AI Engineer) untuk memastikan transisi integrasi tim berjalan mulus dan efisien.*
