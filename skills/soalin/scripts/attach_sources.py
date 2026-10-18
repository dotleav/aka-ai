#!/usr/bin/env python3
"""Find candidate explaining pages for each question, and apply verified sources.

Step 1 (candidates):
  python attach_sources.py candidates --pdf materi.pdf --questions q.json --out cand.json [--top 3] [--render pages/]
  - Each question needs "cari": [keywords]. The kunci option text is added automatically.
  - Writes ranked candidate pages + snippets. If --render is given, also renders top pages to PNG.
  - Candidates are NOT sources yet. Open each rendered PNG and confirm the page explains the answer.

Step 2 (apply verified choices):
  python attach_sources.py apply --questions q.json --choices choices.json --pdf materi.pdf --out q_sourced.json
  - choices.json: {"12": {"pages": [541], "note": "subendocardial layer of Purkinje fibers"}, "5": {"pages": [], "note": "tidak ditemukan di slide"}}
  - Writes "sumber" = "{file} hal. N (note)". Empty pages -> "tidak ditemukan di slide; dijawab dari pengetahuan umum".
  - Refuses to write a page number that does not exist in the PDF.
"""
import argparse, json, re, subprocess, os, sys

def load_pages(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, check=True).stdout
    pages = out.decode("utf-8", errors="ignore").split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return [" ".join(p.split()) for p in pages]

def keywords_for(q):
    kws = list(q.get("cari", []))
    kunci = q.get("kunci")
    for o in q.get("opsi", []):
        if kunci and o.get("huruf") == kunci:
            kws += [w for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", o.get("teks", ""))]
    seen, out = set(), []
    for k in kws:
        if k.lower() not in seen:
            seen.add(k.lower()); out.append(k)
    return out

def cmd_candidates(a):
    pages = load_pages(a.pdf)
    qs = json.load(open(a.questions, encoding="utf-8"))
    result = {}
    for q in qs:
        if q.get("broken"):
            continue
        kws = keywords_for(q)
        scored = []
        for i, t in enumerate(pages):
            hits = [k for k in kws if re.search(re.escape(k), t, re.I)]
            if hits:
                scored.append((len(hits), i + 1, hits))
        scored.sort(key=lambda x: (-x[0], x[1]))
        top = scored[: a.top]
        cand = []
        for s, p, hits in top:
            m = re.search(re.escape(hits[0]), pages[p - 1], re.I)
            snip = pages[p - 1][max(0, m.start() - 120): m.end() + 120]
            cand.append({"page": p, "score": s, "hits": hits, "snippet": snip})
        result[str(q["no"])] = cand
        print(f"No {q['no']}: " + ", ".join(f"p{c['page']}({c['score']})" for c in cand) if cand else f"No {q['no']}: (tidak ada kandidat)")
    json.dump(result, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"candidates -> {a.out}")
    if a.render:
        os.makedirs(a.render, exist_ok=True)
        want = sorted({c["page"] for v in result.values() for c in v})
        for p in want:
            subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "60", "-png", "-singlefile", a.pdf, os.path.join(a.render, f"p{p:04d}")], check=True)
        print(f"rendered {len(want)} pages -> {a.render}  (buka tiap PNG dan konfirmasi sebelum apply)")

def cmd_apply(a):
    pages = load_pages(a.pdf)
    qs = json.load(open(a.questions, encoding="utf-8"))
    choices = json.load(open(a.choices, encoding="utf-8"))
    base = os.path.basename(a.pdf)
    for q in qs:
        c = choices.get(str(q["no"]))
        if not c:
            continue
        pg = c.get("pages", [])
        bad = [p for p in pg if not (1 <= p <= len(pages))]
        if bad:
            sys.exit(f"No {q['no']}: halaman {bad} tidak ada di PDF ({len(pages)} halaman)")
        note = c.get("note", "")
        if pg:
            ps = ", ".join(str(p) for p in pg)
            q["sumber"] = f"{base} hal. {ps}" + (f" ({note})" if note else "")
        else:
            q["sumber"] = f"{base} tidak ditemukan di slide; dijawab dari pengetahuan umum"
    json.dump(qs, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"sumber diterapkan -> {a.out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("candidates")
    c.add_argument("--pdf", required=True); c.add_argument("--questions", required=True); c.add_argument("--out", required=True)
    c.add_argument("--top", type=int, default=3); c.add_argument("--render", default="")
    c.set_defaults(f=cmd_candidates)
    p = sub.add_parser("apply")
    p.add_argument("--questions", required=True); p.add_argument("--choices", required=True); p.add_argument("--pdf", required=True); p.add_argument("--out", required=True)
    p.set_defaults(f=cmd_apply)
    a = ap.parse_args(); a.f(a)
