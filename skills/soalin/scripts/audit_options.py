#!/usr/bin/env python3
"""
audit_options.py — check MCQ quality of a Soalin bank (.txt or .docx) and rebalance key positions.

USAGE
  python audit_options.py audit   --input bank.docx            # report only
  python audit_options.py shuffle --input bank.docx --output out.docx [--seed 7]
  python audit_options.py shuffle --input bank.txt  --output out.txt

audit reports:
  - answer-letter distribution (chi-square vs uniform), same-letter streaks
  - "tells": correct option is the longest / only one with "( )" / only one with a comma clause,
    distractors that hold absolute words (selalu, tidak pernah, semua, hanya, pasti)
shuffle: moves the correct option to a balanced letter (options text re-lettered, Kunci updated).
  Skips: image-label options (A. A), numeric options (ordered), "semua/tidak ada/kombinasi/A dan B"
  options, and questions whose Penjelasan cites a letter ("opsi C", "jawaban B").
  Text-only edit: docx images and layout stay untouched. Rewriting LONG/PAREN tells needs Claude, not this script.
"""
import argparse, random, re, sys
from pathlib import Path

OPT = re.compile(r"^(\s*)([A-E])(\s*[.)]\s*)(.*)$", re.S)
NUM = re.compile(r"^\s*\d+\s*[.)]\s+\S")
KUNCI = re.compile(r"^(\s*Kunci\s*:\s*)([A-E])", re.I)
PENJ = re.compile(r"^\s*Penjelasan\s*:", re.I)
POSITIONAL = re.compile(r"\b(semua (jawaban )?(di atas )?(benar|salah)|tidak ada (jawaban )?(di atas|yang benar)|kecuali|kombinasi|[A-E] dan [A-E]|[A-E] semua|jawaban di atas|pilihan di atas)\b", re.I)
LETTER_REF = re.compile(r"\b(opsi|pilihan|jawaban|option)\s+[A-E]\b", re.I)
ABSOLUTE = re.compile(r"\b(selalu|tidak pernah|semua|seluruh|hanya|pasti|mutlak|satu-satunya)\b", re.I)


# ── item abstraction: a line (txt) or a paragraph (docx) with get/set text ────
class Item:
    def __init__(self, get, set_):
        self.get, self.set = get, set_


def load(path):
    if path.suffix.lower() == ".docx":
        from docx import Document
        doc = Document(str(path))

        def mk(p):
            def set_(t):
                runs = p.runs
                if not runs:
                    p.add_run(t); return
                runs[0].text = t
                for r in runs[1:]:
                    r.text = ""
            return Item(lambda: p.text, set_)
        return doc, [mk(p) for p in doc.paragraphs]
    lines = path.read_text(encoding="utf-8").split("\n")

    def mk(i):
        def set_(t):
            lines[i] = t
        return Item(lambda: lines[i], set_)
    return lines, [mk(i) for i in range(len(lines))]


def parse(items):
    qs, cur, state = [], None, "penj"

    def flush():
        if cur and len(cur["opts"]) == 5 and cur["kunci"]:
            qs.append(cur)

    for it in items:
        t = it.get()
        if not t.strip():
            continue
        m_opt, m_k = OPT.match(t), KUNCI.match(t)
        if NUM.match(t) or (state in ("penj", "kunci") and not m_opt and not m_k and not PENJ.match(t)):
            flush()
            cur, state = {"opts": {}, "kunci": None, "penj": "", "n": len(qs) + 1}, "stem"
            continue
        if cur is None:
            continue
        if m_k:
            cur["kunci"], state = (it, m_k.group(2).upper()), "kunci"
        elif PENJ.match(t):
            cur["penj"], state = t, "penj"
        elif m_opt and state in ("stem", "opt") and not KUNCI.match(t):
            cur["opts"][m_opt.group(2)] = it
            state = "opt"
    flush()
    return qs


def body(it):
    return OPT.match(it.get()).group(4).strip()


def is_label(q):
    return all(len(body(o)) <= 2 for o in q["opts"].values())


def is_numeric(q):
    return all(re.match(r"^[-+]?\d[\d.,]*\s*\S{0,8}$", body(o)) for o in q["opts"].values())


# ── audit ─────────────────────────────────────────────────────────────────────
def audit(qs):
    usable = [q for q in qs if not is_label(q)]
    keys = [q["kunci"][1] for q in qs]
    n = len(keys)
    if not n:
        sys.exit("No complete questions parsed (need numbered stem, A-E, Kunci).")
    counts = {L: keys.count(L) for L in "ABCDE"}
    exp = n / 5
    chi = sum((c - exp) ** 2 / exp for c in counts.values())
    print(f"Soal: {n} | distribusi kunci: " + "  ".join(f"{L}={c} ({c/n:.0%})" for L, c in counts.items()))
    print(f"Chi-square={chi:.2f} (>9.49 = timpang, p<0.05)" + ("  TIMPANG" if chi > 9.49 and n >= 10 else "  ok"))
    streak, best, run = None, 0, 0
    for i, k in enumerate(keys):
        run = run + 1 if i and k == keys[i - 1] else 1
        if run >= 3 and run > best:
            best, streak = run, (i - run + 2, keys[i])
    if streak:
        print(f"Streak kunci sama: {best}x huruf {streak[1]} mulai soal {streak[0]}")

    tells = {"panjang": [], "kurung": [], "koma": [], "absolut": []}
    ratios = []
    for q in usable:
        k = q["kunci"][1]
        txt = {L: body(o) for L, o in q["opts"].items()}
        others = [v for L, v in txt.items() if L != k]
        lens = {L: len(v) for L, v in txt.items()}
        if lens[k] > max(len(v) for v in others):
            tells["panjang"].append(q["n"])
        ratios.append(lens[k] / (sum(len(v) for v in others) / 4 or 1))
        if "(" in txt[k] and not any("(" in v for v in others):
            tells["kurung"].append(q["n"])
        if "," in txt[k] and not any("," in v for v in others):
            tells["koma"].append(q["n"])
        if not ABSOLUTE.search(txt[k]) and sum(bool(ABSOLUTE.search(v)) for v in others) >= 2:
            tells["absolut"].append(q["n"])
    m = len(usable)
    if m:
        print(f"\nRata-rata panjang kunci / panjang distraktor = {sum(ratios)/m:.2f} (ideal ~1.00; >1.15 = kunci cenderung lebih panjang)")
        share = len(tells["panjang"]) / m
        print(f"Kunci = opsi terpanjang: {len(tells['panjang'])}/{m} ({share:.0%}), acak murni ~20%" + ("  POLA TERLIHAT" if share > 0.35 else "  ok"))
        for name, label in (("kurung", "Hanya kunci yang punya '( )'"), ("koma", "Hanya kunci yang punya klausa berkoma"),
                            ("absolut", "Kunci bebas kata absolut, >=2 distraktor pakai")):
            if tells[name]:
                print(f"{label}: soal {', '.join(map(str, tells[name]))}")
    bad = sorted({n for v in tells.values() for n in v})
    print(f"\nSoal perlu ditulis ulang opsinya (oleh Claude): {', '.join(map(str, bad)) or '-'}")
    skipped = n - m
    if skipped:
        print(f"({skipped} soal opsi-label gambar dilewati)")


# ── shuffle ───────────────────────────────────────────────────────────────────
def safe(q):
    txt = [body(o) for o in q["opts"].values()]
    return not (is_label(q) or is_numeric(q) or any(POSITIONAL.search(t) for t in txt) or LETTER_REF.search(q["penj"]))


def shuffle(qs, seed):
    rnd = random.Random(seed)
    counts = {L: 0 for L in "ABCDE"}
    for q in qs:
        if not safe(q):
            counts[q["kunci"][1]] += 1
    todo = [q for q in qs if safe(q)]
    rnd.shuffle(todo)
    moved, plan = 0, {}
    for q in todo:
        low = min(counts.values())
        cands = [L for L in "ABCDE" if counts[L] == low] or list("ABCDE")
        L = rnd.choice(cands)
        counts[L] += 1
        plan[q["n"]] = L
    # break streaks of 3+ by swapping targets between neighbours where possible
    order = sorted(plan)
    for i in range(2, len(order)):
        a, b, c = (plan[order[j]] for j in (i - 2, i - 1, i))
        if a == b == c:
            for j in range(len(order)):
                if j not in (i - 1, i, i + 1) and plan[order[j]] != c:
                    plan[order[i]], plan[order[j]] = plan[order[j]], plan[order[i]]
                    break
    for q in qs:
        if q["n"] not in plan:
            continue
        target, old = plan[q["n"]], q["kunci"][1]
        bodies = {L: body(o) for L, o in q["opts"].items()}
        others = [bodies[L] for L in "ABCDE" if L != old]
        rnd.shuffle(others)
        new = {}
        for L in "ABCDE":
            new[L] = bodies[old] if L == target else others.pop()
        for L, o in q["opts"].items():
            m = OPT.match(o.get())
            o.set(f"{m.group(1)}{L}{m.group(3)}{new[L]}")
        it, _ = q["kunci"]
        it.set(KUNCI.sub(lambda m: m.group(1) + target, it.get(), count=1))
        moved += target != old
    print(f"Diacak: {len(plan)} soal aman ({moved} berubah posisi), {len(qs) - len(plan)} dilewati (label gambar / numerik / 'semua benar' / rujuk huruf)")
    return counts


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["audit", "shuffle"])
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--seed", type=int, default=7)
    a = p.parse_args()
    container, items = load(a.input)
    qs = parse(items)
    if a.cmd == "audit":
        return audit(qs)
    if not a.output:
        sys.exit("--output required")
    shuffle(qs, a.seed)
    if a.input.suffix.lower() == ".docx":
        container.save(str(a.output))
    else:
        a.output.write_text("\n".join(container), encoding="utf-8")
    print(f"Saved: {a.output}\n-- after shuffle --")
    audit(parse(load(a.output)[1]))


if __name__ == "__main__":
    main()
