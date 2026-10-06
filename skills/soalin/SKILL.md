---
name: soalin
description: "Build medical quiz banks in Soalin's exact plain-text docx format. Use this skill whenever the user wants to: (1) convert raw/messy quiz banks into clean Soalin format, (2) create quizzes from scratch from lecture slides, PDFs, or source material, (3) process last year's exam banks with student comments and fix salvageable questions, (4) generate a broken-question recovery table for image-dependent or ambiguous questions, (5) embed image references or crop markers, (6) fix images/answer options in an existing docx bank: permanent crops, image placement, rebalance answer-option patterns, or (7) create or triage short-answer/essay (\"isian\") recall questions that don't fit MCQ. Trigger on: \"soalin\", \"quiz bank\", \"soal UB\", \"soal ujian\", \"buat soal\", \"convert soal\", \"kunci jawaban\", \"penjelasan\", \"crop gambar\", \"distribusi jawaban\", \"soal isian\", \"essay\", \"jawaban singkat\", \"soal minites\", any .docx quiz file, or medical MCQ with Indonesian anatomy/physiology.\n"
---

# Soalin

Builds quiz content in **Soalin's plain-text `.docx` format** — the format the Soalin
web app parses to generate interactive quizzes.

## First: Detect Input Mode

Read the user's input and classify immediately — do not ask unless truly ambiguous:

| Signal | Mode |
|--------|------|
| Numbered questions with A-E options already present | **MODE A: Triage existing bank** |
| Raw lecture material, PDF outline, topic list, no question structure | **MODE B: Create from scratch** |
| Both ("here's old soal + slides for broken ones") | **MODE A** then **MODE B** for gaps |
| Explicit ask for "soal isian"/"essay"/"jawaban singkat", or a question is genuinely open-ended recall with no honest 5-option MCQ possible | **MODE C: Soal Isian/Essay** — runs alongside A/B, not instead of |
| Trigger **"Soal minites"** | Tambahan gaya, berlaku di MODE A/B: baca `references/minites-pattern.md` dulu |

MODE C questions never live inline with MODE A/B output — they always go into the separate **Bagian 3** table (see below), same document, own section.

**Soal minites**: soal kasus klinis MCQ bergaya vignette. `references/minites-pattern.md` berisi ciri pola + beberapa contoh sampel. Pakai sebagai gambaran gaya saja: JANGAN menyalin soal persis, JANGAN meniru nomor soal bergambar / nomor soal kasus / nomor soal non-kasus dari bank sumber. Isi dan sebaran ditentukan materi pengguna. **Soal bergambar harus dibanyakkan** bila relevan untuk belajar materi (radiologi CT/MRI/foto polos, EKG, histologi/apusan, anatomi, lesi kulit/mata/telinga, funduskopi, dst.): jadikan gambar bagian dari petunjuk klinis, bukan hiasan. Pakai slot `[GAMBAR: ...]` dan sertakan daftar gambar yang dibutuhkan; jangan menghindari soal bergambar hanya karena gambarnya harus dicari pengguna.

---

## Soalin Format Spec (memorize this — do not deviate)

```
{N}. {Question text}

A. {option}

B. {option}

C. {option}

D. {option}

E. {option}

Kunci: {letter}

Penjelasan: {explanation text}

Sumber: {nama materi} hal. {nomor halaman/slide} ({ID kuliah bila ada})

```

**Rules:**
- One blank line between every element (question, each option, Kunci, Penjelasan, next question)
- `Kunci:` line is REQUIRED for every valid question. If missing → question goes to broken table.
- `Sumber:` line is REQUIRED (standing rule) — its own paragraph directly under `Penjelasan:`, format `Sumber: Binder2 hal. 614-616 (K13)`. `Sumber:` points to the slide/page that EXPLAINS THE ANSWER (the pages that justify the Kunci and Penjelasan: definition, criteria, table, dose, mechanism), NOT the page the vignette or image was taken from. Image-origin pages go only in the CATATAN GAMBAR list. Use the binder2-blok2h skill to find and read the explaining pages; for other source files use their own page/slide number. Only omit when the source truly has no page numbers (e.g. pasted text); then write `Sumber: {nama materi}`. Knowledge not in the source is still flagged inside Penjelasan.
- `Penjelasan:` line is REQUIRED. If missing but question is salvageable → write one from medical knowledge.
- Options always A through E (5 options). If fewer → broken table.
- MODE A/triage: keep any existing source reference; if the question has none and the page is unknown, write `Sumber: rekapan lama`.
- No bold, no markdown, no extra formatting — pure plain text.
- Numbering is sequential from 1 for the whole file.

### Image-dependent questions (questions referring to a figure/diagram)

When a question says "huruf A/B/C/D" or "gambar nomor 1/2/3" or options are literally `A. A`, `B. B`:

```
{N}. {Question text}

[GAMBAR: {brief image description — e.g., "Histologi alveolus berlabel A-E"}]

A. A

B. B

C. C

D. D

E. E

Kunci: {letter if known}

Penjelasan: {explanation} [Lihat gambar: {filename or slide ref}]

Sumber: {materi} hal. {N}

```

`[GAMBAR: q{N}_gambar.png — {brief description}]` is the image slot contract. Script handles extraction.

---

## MODE A: Triage Existing Quiz Bank

See `references/triage-rules.md` for full decision tree. Short version:

### Pass → Keep (fix minimally)
- Has numbered question, 5 A-E options, a Kunci, a Penjelasan (or one can be written)
- Student comments like "Kaga tau 😁", "harusnya X", "buku SL" → strip silently
- Minor typos/inconsistency in Kunci → fix if medically obvious, flag in Penjelasan if uncertain

### Salvage → Fix and Keep
- Missing Penjelasan only → write one from medical knowledge, mark it `[Penjelasan dibuatkan]`
- Wrong Kunci suspected by student note → verify medically, correct if confident
- Image-dependent but Kunci is known → keep, add `[GAMBAR: ...]` slot + tell user which image

### Broken → Broken Table
Before filing here, check MODE C below — if the answer is known but no honest 5-option MCQ
exists, it's isian, not broken.
Broken conditions (ANY one):
- `[PERLU VERIFIKASI KUNCI JAWABAN MANUAL]` flag present AND image unavailable
- Options are incomplete (less than 5 or truncated)
- Question depends entirely on an image AND no Kunci exists
- Calculation soal with no valid matching answer option

**Broken Table format** (append after all valid questions) — exactly 3 columns, matching
what Soalin's converter actually parses (`No` | `Soal Asli` | `Gambar Penjelasan`; a 4th
"Masalah" column is not read by the app — fold the reason into the `Soal Asli` text in
brackets if it's worth keeping):

```
| No | Soal Asli (dari rekapan) | Gambar Penjelasan |
|----|--------------------------|--------------------|
| 6  | Impuls jantung paling cepat [kunci konflik A vs D] | [kosong — isi screenshot slide dosen] |
| 13 | Sel pertukaran udara (histologi) [butuh gambar, tidak tersedia] | [kosong — isi screenshot slide dosen] |
```

The right column stays empty for the user to paste a screenshot into. This must be built as
a **real Word table** preceded by a **real Word Heading** paragraph ("Bagian 2" or "Soal yang
Gagal Diperbaiki") — see Output below; a pipe-style table typed as plain paragraph text is
just text to the parser and will not render as a card in the app.

---

## MODE B: Create From Scratch

Read `references/create-rules.md` for full guidance. Quick path:

1. **From lecture slides/PDFs**: Extract key facts → generate MCQs covering each concept.
   For concepts best shown visually (anatomy diagrams, histology): make image-slot question.
2. **From topic list**: Generate questions covering all topics, ~2-4 per major concept.
3. **Difficulty**: Mix recall (easy), application (medium), clinical scenario (hard).
4. **Indonesian**: All questions and answers in Bahasa Indonesia (anatomical terms bilingual ok).
5. **Options**: write per `references/kualitas-opsi.md` (equal length/form, no tells), spread key letters evenly across A–E.

### Image slot in scratch questions

When the question genuinely needs a figure, write:

```
{N}. Perhatikan gambar berikut. Struktur manakah yang ditunjukkan oleh huruf C?

[GAMBAR: {describe what image is needed — e.g., "Potongan koronal jantung berlabel A-E"}]

A. ...
...
Kunci: C
Penjelasan: ... [Lihat gambar yang disertakan]
```

Then tell the user: **"Butuh gambar: {precise description}. Screenshot dari slide {topic} atau crop dari atlas."**

---

## MODE C: Soal Isian / Essay (Bagian 3)

Soalin's app has a third question type besides MCQ (Bagian 1) and broken/tap-to-reveal
(Bagian 2): **soal isian** — free-text recall questions with no options, graded by the
student themselves against a revealed answer key. Use this instead of Bagian 1 when:

- The user explicitly asks for "soal isian", "essay", "jawaban singkat", or flashcard-style
  recall practice.
- During MODE A triage, a question is inherently open-ended (e.g. "Sebutkan 3 gejala klasik
  gagal ginjal pra renal") and forcing 5 MCQ options would mean inventing fake distractors
  just to fill slots — route it to Bagian 3 instead of the broken table. This is a real
  recovery path, not a dead end: prefer it over broken-table whenever the question has a
  clear answer, just not a clean set of wrong options.
- During MODE B creation, a concept is better tested as recall than recognition (definitions,
  "sebutkan", "jelaskan singkat", lists to name) — don't stretch it into an artificial MCQ.

**Soal isian is NOT the same shape as Bagian 1.** It is a literal 3-column Word table, same
mechanism as the Bagian 2 broken table, and it is parsed only when the docx actually contains
a Word **Heading** paragraph reading "Bagian 3" or "Soal Isian" immediately before the table —
see the docx table + heading requirements under Output below. A plain text line that merely
looks like a heading does not work.

**Table columns (exactly 3, in this order):** `No` | `Soal` | `Jawaban`
- `No`: original/sequential question number (used to build the id `QI{No}`)
- `Soal`: the question text (free text, images allowed in this cell)
- `Jawaban`: the answer key as free text — not a single letter, can be a short list of
  points ("Oliguria, azotemia, hipotensi"). Not graded automatically; write it complete
  enough to self-check against.

Rules:
- No `Kunci:`/`Penjelasan:` lines — isian questions don't have those fields.
- Numbering in the `No` column continues the same running sequence as Bagian 1/2, it does
  not restart at 1.
- Isian questions never enter Mode Tentamen (timed exam mode) or answer-distribution
  rebalancing — both are MCQ-only mechanics, skip them entirely for this section.
- See `references/create-rules.md` Type 6 for a generation template, and
  `references/triage-rules.md` ISIAN bucket for the triage decision.

**Case-based isian ("soal per kasus"/"soal berdasarkan kasus"):** see `references/create-rules.md`
Type 6b — standing preference, apply by default. Short version: jawaban singkat always (unless
user drops it for that one chat); case vignette and question are separate paragraphs in the Soal
cell, never concatenated into one run-on string; repeat the full case in every row tied to it;
ask questions that solve the case (DD, diagnosis, etiologi, tata laksana, komplikasi) rather than
recall figures already stated in the vignette; skip "mengapa" framing; embed the case's own
linked image (e.g. a cell-smear tied to that specific case) in the Soal cell when the source has
one, matched by its position in the source document.

---

## Gambar & Opsi: aturan wajib untuk bank docx

### 1. Crop harus permanen
Crop bawaan Google Docs hanya menyimpan "jendela" (srcRect) di atas gambar utuh. Saat gambar di-copy-paste, jendela bisa hilang dan gambar utuh muncul lagi. Solusi: crop dibakar ke piksel.

1. `python scripts/docx_images.py bake --docx in.docx --output out.docx` — semua crop di docx dibakar; gambar asli utuh dibuang dari file.
2. Bila pengguna juga memberi **PDF** dan gambar di docx sudah kehilangan crop tetapi di PDF masih ter-crop: `docx_images.py sync-pdf --docx in.docx --pdf in.pdf --output out.docx`. PDF adalah acuan tampilan; gambar dicocokkan menurut urutan (jumlah gambar harus sama; bila beda, laporkan, jangan menebak).
3. Aturan: **bila di PDF gambar sudah ter-crop, hasil akhir harus ter-crop persis seperti itu.** Jangan crop ulang dengan selera sendiri.

### 2. Crop manual hanya bila gambar membocorkan kunci
Setelah langkah 1, `docx_images.py dump --docx out.docx --outdir imgs`, lalu `view` tiap gambar berdampingan dengan soal, Kunci, dan Penjelasan. Crop manual HANYA bila gambar membocorkan jawaban, misalnya: keterangan/label/legenda yang menyebut diagnosis atau struktur yang ditanyakan, judul gambar berisi jawaban, panah berlabel jawaban di luar yang ditanyakan. Bukan bocor: label huruf A–E yang memang dipakai opsi.
Bocor → `docx_images.py trim --image imgs/img_NN.png --crop L T R B --output x.png` (fraksi 0–1), lalu `docx_images.py replace --docx out.docx --index NN --image x.png --output out.docx`. Sebutkan ke pengguna soal mana yang di-crop manual dan bagian apa yang dibuang. Tidak bocor → jangan sentuh.

### 3. Penempatan gambar
Gambar SELALU: paragraf sendiri, **rata tengah**, **di bawah teks soal, di atas opsi A**. Tidak boleh di bawah/antara opsi, tidak di atas soal, tidak inline dalam paragraf soal.
- Cek: `docx_images.py check --docx out.docx`
- Perbaiki otomatis: `docx_images.py check --docx out.docx --fix --output out.docx`
- Gambar setelah `Kunci:`/`Penjelasan:` dan gambar floating/di dalam tabel hanya dilaporkan (ambigu); periksa manual.
Slot `[GAMBAR: ...]` pada teks Soalin sudah berada di posisi benar (di bawah soal, di atas A). `crop_images.py embed` menaruhnya di tengah.

### 4. Distribusi & pola opsi
Cek: `python scripts/audit_options.py audit --input bank.docx` (atau .txt). Laporan: distribusi huruf kunci, streak, kunci selalu terpanjang, hanya kunci yang berkurung "( )" atau berklausa koma, kata absolut di distraktor.
Perbaiki dalam dua tahap:
1. **Tulis ulang opsi bermasalah** (Claude, bukan script) mengikuti `references/kualitas-opsi.md`: samakan panjang dan struktur, hilangkan penjelas hanya di kunci, beri distraktor tingkat detail yang sama.
2. **Acak posisi kunci**: `audit_options.py shuffle --input bank.docx --output out.docx`. Script hanya mengubah teks opsi dan huruf Kunci; gambar dan layout aman. Soal opsi-label gambar, opsi numerik berurutan, "semua/tidak ada jawaban benar", dan Penjelasan yang menyebut huruf dilewati otomatis; bila Penjelasan menyebut huruf, ubah manual.
Jalankan `audit` lagi setelah selesai dan laporkan angka sebelum/sesudah dalam 2–3 baris.

### Urutan kerja bank docx yang sudah ada
`bake` (atau `sync-pdf`) → `dump` + cek bocor → `check --fix` → `audit` → tulis ulang opsi → `shuffle` → `audit` ulang → serahkan file.
Semua perintah `--output` menulis file baru; jangan menimpa file asli pengguna.

### Ekstraksi gambar dari sumber (slide/PDF)
`python scripts/crop_images.py --help`. Nama gambar `q{N}_gambar.png`. Perintah: `list`, `extract`, `embed` (embed menaruh gambar di tengah, satu paragraf sendiri).

---

## Token-Saving Rules (apply always)

- Do NOT restate the source material back verbatim before converting — just output the Soalin format.
- Do NOT explain what you're doing for each question — just output them.
- For large banks (>30 questions): process in batches of 30, write batch to the docx (see below), ask "lanjut?" before next.
- For broken table: list broken questions AFTER all valid output, not inline.
- Image slots: emit `[GAMBAR: ...]` inline — don't pause to describe each one separately.

---

## Output: SELALU file `.docx`, tidak pernah markdown atau teks polos di chat

Final output ini WAJIB berupa file `.docx` — bukan `.md`, bukan ditempel sebagai teks di chat. Ini berlaku untuk MODE A (triage) maupun MODE B (create from scratch); MODE A biasanya sudah bekerja langsung di atas docx pengguna lewat pipeline gambar, tapi bila hasil MODE A hanya berupa teks tanpa gambar, tetap tulis ke `.docx` sebelum `present_files`, jangan tempel plain text.

- **MODE B / bank baru tanpa docx sumber**: setelah teks Soalin (struktur di bawah) selesai untuk satu batch, tulis ke `.docx` dengan `docx` (npm, lihat skill `docx`). Bagian 1 (soal MCQ): tiap baris pada spec (soal, tiap opsi, `Kunci:`, `Penjelasan:`, baris kosong pemisah) jadi satu `Paragraph` polos (tanpa bold/heading/formatting lain). Bagian 2 (rusak) dan Bagian 3 (isian), bila ada: masing-masing WAJIB satu `Paragraph` ber-`heading: HeadingLevel.HEADING_2` berisi teks persis "Bagian 2" / "Bagian 3" (bukan teks biasa, bukan bold-manual — harus style Heading asli, ini yang dibaca parser lewat tag `<h1-3>` hasil convert), diikuti satu `Table` sungguhan (`Table`/`TableRow`/`TableCell` dari `docx`) dengan kolom sesuai spec di atas (3 kolom masing-masing). Tanpa Heading asli ini, parser Soalin tidak akan pernah mendeteksi Bagian 3, dan kalau Bagian 2 + Bagian 3 sama-sama ada tanpa heading keduanya bisa ketuker (baris isian ke-parse sebagai soal rusak). Kasus pertama: `create_file` skrip docx-js baru. Batch berikutnya: buka docx yang sudah ada dan tambahkan paragraf/table di akhir `word/document.xml` (unzip → edit → zip, lihat skill `docx`) — jangan generate ulang dari nol.
- **MODE A dengan docx sumber**: ikuti pipeline gambar (`bake`/`sync-pdf` → `dump` → `check --fix` → `audit` → `shuffle`) seperti biasa; hasil akhirnya sudah docx. Kalau sumbernya sudah punya tabel rusak/isian tapi tanpa Heading "Bagian 2"/"Bagian 3" di atasnya (umum kalau bank lama ditulis sebelum aturan ini), sisipkan Heading itu langsung ke `word/document.xml` sebelum tabel yang bersangkutan — jangan biarkan tabel tanpa heading kalau lebih dari satu tabel non-MCQ ada di dokumen.
- Struktur isi (urutan di dalam docx, tetap sama seperti sebelumnya, sekarang dengan Bagian 3):

```
{valid MCQ questions in Soalin format, renumbered from 1}                — Bagian 1, plain paragraphs

[Heading: "Bagian 2"]                                                    — only if any broken questions exist
{broken table — real Table, 3 cols: No | Soal Asli | Gambar Penjelasan}

[Heading: "Bagian 3"]                                                    — only if any isian questions exist
{isian table — real Table, 3 cols: No | Soal | Jawaban}

---CATATAN GAMBAR--- (only if any image slots exist, plain paragraphs, after everything else)
{list: q{N} → source-file: {filename} --slide/--page {N} [--crop L T R B if needed]}
```

`present_files` untuk file `.docx` akhir. Balasan chat cukup ringkasan (jumlah soal MCQ, jumlah rusak, jumlah isian) — jangan tempel isi bank ke chat.

---

## Reference Files

- `references/triage-rules.md` — Full decision tree for classifying questions (read when bank has >10 broken questions or complex edge cases)
- `references/create-rules.md` — Full guidance for generating new questions (read when creating >15 questions from scratch or from complex source material)
- `scripts/parse_bank.py` — Python parser: extracts questions from messy text into structured dicts (use for large banks >50 questions)
- `references/kualitas-opsi.md` — Aturan menulis opsi agar kunci tidak mudah ditebak (baca saat menulis ulang opsi atau membuat soal baru)
- `scripts/crop_images.py` — Image pipeline: `list` slides, `extract` crops, `embed` into docx. Run `--help` for full usage — do NOT load this file into context, just run it.
- `scripts/docx_images.py` — Crop permanen (`bake`, `sync-pdf`), audit/perbaikan penempatan (`check`), `dump`, `trim`, `replace`. Run `--help`; do NOT load into context.
- `scripts/audit_options.py` — `audit` distribusi kunci & pola opsi, `shuffle` seimbangkan huruf kunci. Run `--help`; do NOT load into context.
