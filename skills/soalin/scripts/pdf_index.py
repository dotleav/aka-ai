#!/usr/bin/env python3
"""Index a PDF per page (text) and optionally render pages to PNG for visual checking.

Usage:
  python pdf_index.py index  --pdf materi.pdf --out index.json
  python pdf_index.py render --pdf materi.pdf --pages 168,175 --outdir pages/ [--dpi 60]

Page numbers are 1-based PDF page indices (the page you see in a PDF viewer).
"""
import argparse, json, os, subprocess, sys

def page_texts(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, check=True).stdout
    txt = out.decode("utf-8", errors="ignore")
    pages = txt.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages

def cmd_index(a):
    pages = page_texts(a.pdf)
    data = [{"page": i + 1, "text": " ".join(p.split())} for i, p in enumerate(pages)]
    json.dump(data, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"indexed {len(data)} pages -> {a.out}")

def cmd_render(a):
    os.makedirs(a.outdir, exist_ok=True)
    for p in [int(x) for x in a.pages.split(",") if x.strip()]:
        prefix = os.path.join(a.outdir, f"p{p:04d}")
        subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(a.dpi), "-png", "-singlefile", a.pdf, prefix], check=True)
        print(prefix + ".png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("index"); s.add_argument("--pdf", required=True); s.add_argument("--out", required=True); s.set_defaults(f=cmd_index)
    r = sub.add_parser("render"); r.add_argument("--pdf", required=True); r.add_argument("--pages", required=True); r.add_argument("--outdir", default="pages"); r.add_argument("--dpi", type=int, default=60); r.set_defaults(f=cmd_render)
    a = ap.parse_args(); a.f(a)
