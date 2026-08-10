# Cara Menyusun PRD dengan Bantuan AI

Panduan ini buat anggota tim yang belum familiar dengan PRD. Tetap baca bagian "Apa itu PRD" di bawah walau nanti AI yang bantu menulis, karena kamu tetap perlu bisa menilai apakah hasil AI-nya masuk akal atau enggak.

## Apa itu PRD dan Kenapa Penting

PRD (Product Requirements Document) itu dokumen yang menjawab "apa yang dibangun dan kenapa", supaya semua orang di tim ngerjain hal yang sama persis, bukan interpretasi masing-masing. Tanpa PRD, gampang kejadian dua orang bikin asumsi beda soal cara kerja satu fitur, dan baru ketauan pas fitur-fiturnya digabung.

## Langkah-Langkah

### 1. Baca konteks project
Buka `docs/context/project-context.md`. Ini rangkuman seluruh keputusan project. Kamu gak perlu hafal semuanya, tapi baca dulu supaya ngerti gambaran besar sebelum minta bantuan AI.

### 2. Buka template PRD fitur kamu
Sesuai pembagian modul, cek file PRD yang jadi tanggung jawabmu di `docs/prd/`. Tiap file sudah ada strukturnya, sebagian sudah diisi konteks awal, sisanya masih `[TODO]`.

### 3. Pakai template prompt di bawah ini

Copy-paste ke AI (ChatGPT, Claude, atau AI yang kamu pakai di coding agent kamu), lalu tempelkan isi `project-context.md` dan isi PRD fitur kamu yang masih ada bagian `[TODO]`-nya:

```
Kamu adalah asisten yang membantu menyusun PRD (Product Requirements Document)
untuk sebuah fitur dari platform bernama Nalar.

Berikut konteks lengkap project (baca dulu sebelum menjawab):
[TEMPEL ISI project-context.md DI SINI]

Berikut draft PRD untuk fitur yang saya kerjakan, sebagian sudah terisi,
bagian yang bertanda [TODO] perlu kamu lengkapi:
[TEMPEL ISI FILE PRD KAMU DI SINI]

Tugasmu:
1. Lengkapi bagian [TODO] dengan requirement yang SPESIFIK dan BISA DITES
   (hindari kalimat vague seperti "sistem harus cepat", ganti dengan kriteria
   terukur seperti "sistem menampilkan hasil dalam maksimal 2 detik")
2. Kalau kamu terpaksa membuat asumsi karena informasi di konteks tidak cukup,
   tandai jelas dengan format: [ASUMSI: penjelasan asumsi]
3. Jangan menambahkan fitur atau scope baru yang tidak ada di konteks project
4. Tulis dalam Bahasa Indonesia, gaya to the point
5. Setelah PRD selesai, cek juga skema data yang saya kasih (ai-output-schema.md
   atau db-schema.md kalau relevan): berdasarkan fitur yang saya bangun ini,
   ada field atau data yang menurutmu kemungkinan kurang atau ambigu? Saya
   tidak selalu tahu ini karena saya masih belajar, jadi tolong bantu saya
   ngenalin kalau ada gap, walau kamu tidak yakin 100%.
```

### 4. Review hasil AI, jangan langsung dipakai mentah

Setelah AI kasih hasil, cek dengan pertanyaan ini sebelum dianggap final:
- Apakah ada bagian bertanda `[ASUMSI: ...]`? Diskusikan ke tim, jangan diloloskan begitu saja
- Apakah requirement-nya bisa dites/diukur, atau masih abstrak?
- Apakah ada yang bertentangan sama fitur lain (cek ke `project-context.md` atau PRD fitur lain yang terkait)?
- Kalau ada bagian yang kamu sendiri gak paham kenapa AI menulis begitu, tanya balik ke AI "kenapa kamu menentukan ini", jangan diterima kalau kamu sendiri belum ngerti alasannya

### 5. Diskusikan bareng tim sebelum dianggap final

PRD bukan dokumen yang selesai sendirian. Setelah draft dari AI kamu rasa cukup, bahas bareng anggota tim lain yang modulnya berkaitan (lihat bagian "Dependencies & Assumptions" di PRD kamu), pastikan gak ada mismatch sebelum mulai coding.

## Kalau Nemu Kebutuhan Tambahan Pas Development

Wajar banget kalau pas mulai coding kamu baru sadar butuh field atau data yang gak ada di skema dari Zidan. Ini bukan tanda ada yang salah, itu emang bagian normal dari proses. Kamu gak perlu bisa memprediksi ini dari awal.

Yang perlu dilakukan cuma:
1. Catat di `docs/context/schema-change-log.md` — apa yang kamu butuhkan, kenapa, dan tanggalnya
2. Kabarin ke Zidan biar dia tahu ada perubahan yang perlu disesuaikan

## Kalau Bingung

Kalau ada bagian PRD yang kamu sendiri gak yakin cara jawabnya (bahkan setelah tanya AI), lebih baik tulis pertanyaan itu di bagian "Open Questions" di PRD kamu dan bahas bareng tim, daripada dipaksa diisi asal supaya "kelihatan lengkap".