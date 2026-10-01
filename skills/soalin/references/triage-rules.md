# Triage Rules — Full Decision Tree

## Step 1: Strip Noise

Remove before classifying:
- Student comments: "Kaga tau 😁", "buku SL", "harusnya X", "tidak bisa baca gambar", emoji, parenthetical asides in answers like `D. 4 /Duktus Alveolaris` → keep `D. Duktus Alveolaris`
- Duplicate answer markers from annotation tools (when same letter appears twice with different text)
- `[PERLU VERIFIKASI KUNCI JAWABAN MANUAL]` prefix from explanation — note the reason, then decide classification

## Step 2: Classify Each Question

### KEEP (output as valid)

| Condition | Action |
|-----------|--------|
| Has 5 options + Kunci + Penjelasan | Output as-is (clean noise) |
| Has 5 options + Kunci, no Penjelasan | Write Penjelasan, add `[Penjelasan dibuatkan]` |
| Student challenges Kunci but medical consensus is clear | Correct Kunci, note in Penjelasan: "Jawaban dikoreksi dari {old} ke {new}: {reason}" |
| Image-dependent, Kunci known, standard image (diagram/histology known type) | Keep + `[GAMBAR: ...]` slot + catatan gambar entry |

### SALVAGE (fix then output as valid)

| Condition | Fix |
|-----------|-----|
| Options A-E present but one contains extra student annotation text | Strip annotation, keep option text |
| Penjelasan says "PERLU VERIFIKASI" but medical answer is unambiguous | Write correct Penjelasan, keep question |
| Question has 4 options (E missing), answer not E | If text is a 4-option question by design: add `E. Tidak ada di atas` or reconstruct missing option if inferable |
| Kunci says one letter but Penjelasan text implies different answer | Align Kunci with Penjelasan logic, note discrepancy |

### ISIAN (→ Bagian 3 table, not broken)

| Condition | Reason to route to isian instead of broken |
|-----------|---------------------------------------------|
| Question asks to enumerate/explain ("sebutkan", "jelaskan singkat", "apa saja") with a clear correct answer, but no natural set of wrong options | Forcing 5 MCQ options here means writing fake distractors — isian keeps the real answer without the pretense |
| Original source was already a short-answer/essay item (no A-E ever existed, not a transcription gap) | Not "broken" — it was never meant to be MCQ |
| Calculation/definition question where the only honest options would be "benar" and 4 near-duplicates of the same number | Isian keeps the actual value as the answer key instead of gaming an MCQ shape |

Distinguish from BROKEN: broken = *should* be MCQ but the transcription/image/kunci is
missing or unrecoverable. Isian = *was never* meant to be MCQ, or forcing it into MCQ would
require inventing content that isn't in the source. When unsure and Kunci is genuinely known,
prefer isian over broken — it's not a dead end.

### BROKEN (→ broken table)

| Condition | Reason for broken table |
|-----------|------------------------|
| Image-dependent AND no Kunci | Cannot answer without image |
| Options are `A. A`, `B. B` etc. (pure label options) AND Kunci missing | Image-only question, needs slide screenshot |
| Calculation soal where no answer option matches any calculation route | Typo in source, needs instructor verification |
| `PERLU VERIFIKASI` AND question is ambiguous (multiple defensible answers) | Needs instructor input |
| Less than 4 complete options | Incomplete transcription |
| Question text is truncated mid-sentence | Incomplete transcription |

## Step 3: Renumber

After triaging all questions, renumber all KEEP+SALVAGE questions sequentially from 1.
Broken table references original numbers from source.

## Edge Cases

**Duplicate questions** (same concept, different wording — common in Indonesian exam banks):
- Keep both if wording differs meaningfully (tests same concept from different angle)
- Remove exact duplicate, keep first occurrence

**Questions with `Kunci: A` but options show `A. A` (image reference)**:
- This means question 12 type: asks "di manakah serabut Purkinje?" and shows labeled diagram
- Classification: image-dependent with known Kunci → SALVAGE with `[GAMBAR: ...]` slot

**Student-added explanation hints** in Penjelasan field (e.g., "Rumus: VA = VT-VD × F"):
- These are helpful — keep them, clean formatting

**Bilingual terms** in options (Indonesian + Latin anatomy):
- Keep as-is. Soalin audience is medical students who need both.

**Soal klinis** (clinical vignette format starting with "Seorang pasien..."):
- These are high value — prioritize keeping them
- If clinical context is present but options are incomplete, attempt to reconstruct from medical logic
