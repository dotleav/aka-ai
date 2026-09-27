#!/usr/bin/env python3
"""
parse_bank.py — Soalin quiz bank parser

Usage:
    python parse_bank.py input.txt [--output questions.json] [--report]

Parses a messy Soalin-format text file into structured dicts.
Classifies each question as: valid | salvage | broken
Strips student noise. Outputs JSON for Claude to process in batches.
"""

import re
import json
import sys
from pathlib import Path

NOISE_PATTERNS = [
    r"😁|🤣|😅|😭|😂|👍|❓",              # emoji
    r"Kaga tau.*",                          # student confusion notes
    r"tidak bisa baca.*",
    r"buku SL.*",
    r"\[PERLU VERIFIKASI.*?\]",             # verifikasi flags (keep for classification)
    r"harusnya\s+\w+\s*\(.*?\)",           # "harusnya X" notes
]

VERIFIKASI_RE = re.compile(r"\[PERLU VERIFIKASI[^\]]*\]", re.IGNORECASE)
IMAGE_OPTION_RE = re.compile(r"^[A-E]\.\s+[A-E1-5]$", re.MULTILINE)  # options like "A. A"


def strip_noise(text: str) -> str:
    for pat in NOISE_PATTERNS:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)
    return text.strip()


def parse_questions(raw: str) -> list[dict]:
    """Split raw text into question blocks."""
    # Questions start with digit(s) followed by period
    blocks = re.split(r"\n(?=\d+\. )", raw.strip())
    questions = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        q = parse_single(block)
        if q:
            questions.append(q)

    return questions


def parse_single(block: str) -> dict | None:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    if not lines:
        return None

    # Number + question text
    m = re.match(r"^(\d+)\.\s+(.+)", lines[0])
    if not m:
        return None

    number = int(m.group(1))
    question = m.group(2)
    # Multi-line question text (lines before first A.)
    i = 1
    while i < len(lines) and not re.match(r"^[A-E]\.", lines[i]):
        question += " " + lines[i]
        i += 1

    options = {}
    while i < len(lines) and re.match(r"^([A-E])\.", lines[i]):
        opt_m = re.match(r"^([A-E])\.\s*(.*)", lines[i])
        if opt_m:
            letter = opt_m.group(1)
            opt_text = opt_m.group(2)
            # Strip inline student notes after "/"
            opt_text = re.sub(r"\s*/[^A-Z].*$", "", opt_text).strip()
            options[letter] = strip_noise(opt_text)
        i += 1

    kunci = None
    penjelasan = None
    needs_verifikasi = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("Kunci:"):
            kunci_raw = line.replace("Kunci:", "").strip()
            # Take first letter only
            km = re.search(r"[A-E]", kunci_raw)
            kunci = km.group(0) if km else None
        elif line.startswith("Penjelasan:"):
            penjelasan = line.replace("Penjelasan:", "").strip()
            if VERIFIKASI_RE.search(penjelasan):
                needs_verifikasi = True
                penjelasan = VERIFIKASI_RE.sub("", penjelasan).strip()
            # Collect continuation lines
            j = i + 1
            while j < len(lines) and not re.match(r"^[A-E]\.|^Kunci:|^Penjelasan:", lines[j]):
                penjelasan += " " + lines[j]
                j += 1
            i = j
            continue
        i += 1

    # Classify
    is_image_options = bool(IMAGE_OPTION_RE.search(block))
    status = classify(number, question, options, kunci, penjelasan, needs_verifikasi, is_image_options)

    return {
        "number": number,
        "question": strip_noise(question.strip()),
        "options": options,
        "kunci": kunci,
        "penjelasan": strip_noise(penjelasan or ""),
        "needs_verifikasi": needs_verifikasi,
        "is_image_dependent": is_image_options,
        "status": status,
    }


def classify(n, q, opts, kunci, penjelasan, needs_verifikasi, is_image) -> str:
    if len(opts) < 4:
        return "broken"
    if not kunci and is_image:
        return "broken"
    if not kunci and needs_verifikasi:
        return "broken"
    if needs_verifikasi and not kunci:
        return "broken"
    # Calculation mismatch: if penjelasan says "tidak menghasilkan angka yang sesuai"
    if penjelasan and "tidak menghasilkan" in penjelasan.lower():
        return "broken"
    if not kunci:
        return "salvage"  # might be able to infer
    if not penjelasan:
        return "salvage"  # needs penjelasan written
    return "valid"


def report(questions: list[dict]) -> str:
    valid = [q for q in questions if q["status"] == "valid"]
    salvage = [q for q in questions if q["status"] == "salvage"]
    broken = [q for q in questions if q["status"] == "broken"]
    image = [q for q in questions if q["is_image_dependent"]]

    lines = [
        f"Total: {len(questions)} questions",
        f"  Valid:   {len(valid)}",
        f"  Salvage: {len(salvage)} (need Penjelasan or Kunci inference)",
        f"  Broken:  {len(broken)} (→ broken table)",
        f"  Image-dependent: {len(image)}",
        "",
        "BROKEN:",
    ]
    for q in broken:
        reason = []
        if q["is_image_dependent"] and not q["kunci"]:
            reason.append("image+no kunci")
        if q["needs_verifikasi"]:
            reason.append("verifikasi flag")
        if len(q["options"]) < 4:
            reason.append(f"only {len(q['options'])} options")
        lines.append(f"  [{q['number']}] {q['question'][:60]}... — {', '.join(reason)}")

    return "\n".join(lines)


def to_soalin(q: dict, new_number: int) -> str:
    """Format a valid/salvage question as Soalin plain text."""
    lines = [f"{new_number}. {q['question']}", ""]
    if q["is_image_dependent"]:
        lines += ["[GAMBAR: gambar diperlukan — isi dengan screenshot materi]", ""]
    for letter in "ABCDE":
        if letter in q["options"]:
            lines += [f"{letter}. {q['options'][letter]}", ""]
    if q["kunci"]:
        lines += [f"Kunci: {q['kunci']}", ""]
    penj = q["penjelasan"] or "[Penjelasan dibuatkan]"
    lines += [f"Penjelasan: {penj}", ""]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_bank.py input.txt [--output out.json] [--report]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    raw = input_path.read_text(encoding="utf-8")
    questions = parse_questions(raw)

    do_report = "--report" in sys.argv
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_path = Path(sys.argv[idx + 1])

    if do_report:
        print(report(questions))

    if output_path:
        output_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {len(questions)} questions to {output_path}")
    else:
        print(json.dumps(questions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
