# Create From Scratch — Full Rules

## Input Types and How to Handle Them

### From PowerPoint/PPTX slides
1. Extract key facts from each slide (concept, mechanism, clinical relevance, numbers)
2. For each major concept: write 1-3 MCQs at different difficulty levels
3. For diagrams/figures: write image-slot questions, reference slide number
4. Suggested density: 1-2 questions per content slide, 0 for title/header slides

### From PDF (lecture notes, textbook chapters)
1. Read headers as topic anchors
2. Extract: definitions, mechanisms, clinical presentations, normal values, anatomical relationships
3. For anatomy topics: assume images needed for spatial relationships → use image slots

### From topic list only
1. Generate questions covering all listed topics
2. Assume standard Indonesian medical curriculum (USMLE Step 1 equivalent depth)
3. Mix question types (see templates below)

### From student-provided messy notes
1. Identify distinct facts amid the noise
2. Turn each fact into at least one MCQ
3. Strip uncertainty markers before generating (don't make questions about uncertain content)

---

## Question Type Templates

### Type 1: Direct Recall (easy)
```
{N}. Apa {term/structure/function} dari {concept}?

A. {wrong — plausible}
B. {wrong — common misconception}
C. {correct}
D. {wrong — partially true}
E. {wrong — related but different}

Kunci: C
Penjelasan: {1-2 sentences. State the correct answer plainly, explain why.}
```

### Type 2: Application / Mechanism (medium)
```
{N}. Bagaimana {mechanism} terjadi ketika {condition}?

A-E: one correct + four wrong (cover common confusions)

Kunci: {letter}
Penjelasan: {explain the mechanism step-by-step briefly}
```

### Type 3: Clinical Scenario (hard — high value)
```
{N}. Seorang {age} tahun datang dengan {symptoms}. Pada pemeriksaan didapatkan {findings}. 
Apa {diagnosis/mechanism/finding/next step}?

A-E: include one answer that's close but wrong (e.g., similar disease, wrong side, wrong test)

Kunci: {letter}
Penjelasan: {Why this diagnosis/answer. What distinguishes it from the distractors.}
```

### Type 4: Image Reference (anatomy/histology)
```
{N}. Perhatikan gambar berikut. {Specific question about labeled structure/location}

[GAMBAR: {exact description of image needed}]

A. A
B. B
C. C
D. D
E. E

Kunci: {letter}
Penjelasan: {Structure is X because Y. Anatomical landmark.} [Lihat gambar]
```

### Type 5: Calculation (physiology values)
```
{N}. Diketahui {variable 1} = {value}, {variable 2} = {value}. Berapakah {calculated value}?

A. {wrong calculation}
B. {correct answer}
C. {wrong — common arithmetic error}
D. {wrong — different formula}
E. {wrong — units error}

Kunci: {letter}
Penjelasan: Rumus: {formula}. Perhitungan: {step by step} = {answer}.
```

### Type 6: Isian / Essay (jawaban singkat — no options)
Use when the concept is better tested as recall than recognition: definitions, "sebutkan",
lists to name, short explanations. Goes into the Bagian 3 table, not inline with Type 1-5.

```
No: {N}
Soal: {Sebutkan/Jelaskan singkat ... ?}
Jawaban: {complete answer key — a short list of points or a 1-2 sentence explanation,
          written so the student can self-check, not a single letter}
```

Don't invent a Kunci/Penjelasan pair for these — isian has no options and no letter answer.
If a Type 1-5 draft ends up needing more than one implausible filler distractor to reach 5
options, that's a signal it belongs here instead.

### Type 6b: Soal Isian Berbasis Kasus (case-based, default mode when user asks for "soal per kasus" / "soal berdasarkan kasus")

Default jawaban singkat (a short phrase, term, or bare list — never a paragraph explanation),
for every question in a case-based isian batch. This is a standing user preference, not a
one-off instruction: apply it automatically to every case-based isian batch. Only drop it —
write longer/explained jawaban — when the user says so explicitly in that chat (e.g. "gak usah
jawaban singkat", "boleh dijelasin"); the relaxation applies to that request only, revert to
short jawaban on the next case-based batch unless they repeat it.

**Soal cell structure — case and question are separate paragraphs, never concatenated into one
run-on string:**
```
[Paragraph, bold label + italic case text] Kasus {N}: {full vignette — presenting complaint,
  vital signs, exam findings, relevant results}
[Paragraph, blank]
[Paragraph, plain] {the question itself}
[Paragraph, image — only if this case has a linked figure, see below]
```
The full case vignette is repeated in EVERY row tied to that case, not written once and
referenced afterward — a student answering row 5 has not necessarily just read row 1, and
isian rows are meant to be self-contained.

**Question content — test solving the case, not recalling it:**
- Ask about diagnosis banding, diagnosis/etiologi paling mungkin, pemeriksaan konfirmasi,
  tata laksana, komplikasi, pemeriksaan lanjutan/pencitraan — i.e. what the case leads to.
- Never ask to recall a figure or finding already stated in the vignette itself (e.g. "berapa
  kadar glukosa LCS pada kasus ini?", "apa gejala pasien ini?") — that tests memorization of
  the stem, not clinical reasoning.
- Skip "mengapa"/"why" framing by default — it invites a long explanatory answer, which
  conflicts with the short-jawaban default above. A "makna klinis dari X" question is fine
  as long as the expected jawaban is still a short term/phrase, not a paragraph.

**Case-linked images:** if the source material has a figure tied to this specific case (e.g.
a cell-smear image referenced right after that case's own text, a case-specific ECG/X-ray),
embed that actual image in the Soal cell (Mode C allows images in the Soal cell) rather than
inventing a generic one or skipping images entirely. Match the image to its case by document
position/context, not just by topic — see the docx's own image anchors before picking one.

```
No: {N}
Soal: [bold]Kasus {N}:[/bold] [italic]{full vignette}[/italic]
      [blank line]
      {reasoning question — short-answer, not recall, not "mengapa"}
      [+ embedded case image if one is linked to this case]
Jawaban: {short phrase/term/bare list — not an explanation}
```

---

## Quality Checklist (apply to every generated question)

- [ ] Exactly 5 options (A-E)
- [ ] Only ONE correct answer — verify the others are definitively wrong
- [ ] Distractors are plausible (not obviously wrong), covering common misconceptions
- [ ] Options not guessable by form: similar length (±25%), no "( )"/clause only on the key, no absolute words only in distractors, key letters spread evenly (see `kualitas-opsi.md`)
- [ ] Penjelasan explains WHY the answer is correct, not just what it is
- [ ] Clinical scenario questions include enough context to be solvable
- [ ] Calculation questions: verify arithmetic before writing answer options
- [ ] Image-slot questions: `[GAMBAR: ...]` present + catatan gambar entry written
- [ ] Isian (Type 6) questions: Jawaban is a real self-checkable answer, not a placeholder; not stretched into fake MCQ options
- [ ] Language: Bahasa Indonesia throughout (anatomical Latin terms acceptable in options)

---

## Topic Coverage Strategy

For a full exam bank (>50 questions), aim for this distribution:
- Anatomy (gross + histology): 30%
- Physiology: 30%
- Biochemistry (heme, proteins, electrolytes): 15%
- Radiology/clinical examination: 15%
- Pharmacology (if in scope): 10%

For a targeted topic bank (<20 questions), cover:
- Core mechanism: 2-3 questions
- Clinical application: 2-3 questions  
- Normal values/structure: 1-2 questions
- Edge case / exception: 1 question

---

## Image Request Format (always emit at end of batch)

```
---CATATAN GAMBAR---

q{N} → Butuh: {precise image description}
       Sumber: Slide {topic} / Atlas {anatomical region} / {textbook}
       Nama file: q{N}_gambar.png
       Cara ambil: {Screenshot slide | Crop dari PDF hal {N} | Foto atlas hal {N}}

q{N2} → Butuh: ...
```
