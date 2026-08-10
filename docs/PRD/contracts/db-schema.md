# DB Schema (PostgreSQL / Supabase)

**Status:** Active
**Owner:** Lukman & Haikal (Backend)
**Terakhir diupdate:** 2026-08-10

Dokumen ini mendefinisikan skema database PostgreSQL di Supabase. Database ini adalah **Single Source of Truth** untuk aplikasi Nalar.

---

## Relasi Antar Tabel (ERD High-Level)

```
users (1) ───< materials (N) ───< concepts (N) ───< rubrics (1)
  │                                    │
  ├───< sessions (N) ──────────────────┤
  │        │                           │
  │        ├───< answers (N) ──────────┤
  │        │                           │
  │        └───< scores (1) ───────────┘
  │
  └───< class_enrollments (N) >─── classes (1)
```

---

## Detail Tabel

### 1. `users`
Tabel pengguna (mahasiswa & dosen). Integrasi dengan Supabase Auth (`auth.users`).

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'lecturer', 'admin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2. `materials`
Materi kuliah yang diunggah oleh pengguna (PDF/PPTX).

```sql
CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL, -- Supabase Storage Bucket Path
    file_type VARCHAR(50) NOT NULL, -- 'pdf', 'pptx'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3. `concepts`
Concept Graph hasil ekstraksi Stage 1.

```sql
CREATE TABLE concepts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    concept_code VARCHAR(50) NOT NULL, -- e.g. 'c-001'
    name VARCHAR(255) NOT NULL,
    definition TEXT NOT NULL,
    source_reference TEXT, -- e.g. 'Slide 12'
    related_concept_codes JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concepts_material_id ON concepts(material_id);
```

### 4. `rubrics`
Master Rubric statis hasil Stage 2.

```sql
CREATE TABLE rubrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    concept_id UUID UNIQUE NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    opening_question TEXT NOT NULL,
    levels JSONB NOT NULL, -- [{level: 'definisi', criteria: [...]}, ...]
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 5. `sessions`
Sesi pengujian aktif/lampau per pengguna per konsep.

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_sessions_user_concept ON sessions(user_id, concept_id);
```

### 6. `answers`
Riwayat jawaban pengguna per turn/round di Stage 3.

```sql
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    round_number INT NOT NULL,
    level_tested VARCHAR(50) NOT NULL, -- 'definisi', 'sebab-akibat', 'transfer'
    question_text TEXT NOT NULL,
    user_answer TEXT NOT NULL,
    evaluation JSONB NOT NULL, -- {criteria_met: [...], criteria_missing: [...], evidence_trail: [...]}
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 7. `scores`
Hasil depth score dan confidence calibration Stage 4.

```sql
CREATE TABLE scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID UNIQUE NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    depth_score NUMERIC(5,2) NOT NULL, -- 0.00 - 100.00
    confidence_input INT NOT NULL CHECK (confidence_input BETWEEN 1 AND 5),
    confidence_normalized NUMERIC(5,2) NOT NULL,
    delta NUMERIC(5,2) NOT NULL,
    calibration_status VARCHAR(50) NOT NULL CHECK (calibration_status IN ('overconfident', 'underconfident', 'accurate')),
    summary_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scores_user_calibration ON scores(user_id, calibration_status);
```

### 8. `classes` & `class_enrollments` (Mode Dosen)

```sql
CREATE TABLE classes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lecturer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE class_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    consent_given BOOLEAN DEFAULT FALSE NOT NULL,
    enrolled_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(class_id, student_id)
);
```