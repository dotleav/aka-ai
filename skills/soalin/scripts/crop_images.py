#!/usr/bin/env python3
"""
crop_images.py — Extract and embed images into a Soalin quiz docx.

USAGE (Claude reads this and infers all args — no other docs needed):

  # Extract one image from a source file:
  python crop_images.py extract --source slides.pptx --slide 14 --output q13_gambar.png
  python crop_images.py extract --source notes.pdf  --page  7  --output q45_gambar.png
  python crop_images.py extract --source report.docx --page  3  --output q7_gambar.png

  # Optional: crop to a bounding box (left top right bottom, 0-1 fractions of page):
  python crop_images.py extract --source slides.pptx --slide 14 --crop 0.1 0.2 0.9 0.8 --output q13_gambar.png

  # Batch: process all [GAMBAR:] tags in a Soalin text file, extract images, embed into docx:
  python crop_images.py embed --quiz quiz_output.txt --images-dir ./images --output quiz_with_images.docx

  # List slides/pages in a source (helps identify which slide has the diagram):
  python crop_images.py list --source slides.pptx
  python crop_images.py list --source notes.pdf

WORKFLOW FOR CLAUDE:
  1. After writing quiz text with [GAMBAR: slide N, description] tags → run 'list' to confirm slide numbers
  2. Run 'extract' for each [GAMBAR:] tag, saving to q{N}_gambar.png
  3. Run 'embed' to produce final docx with images inserted at each [GAMBAR:] slot
     (image = own centered paragraph, under the question, above option A)
  Crop persistence / placement audit of an existing docx: see docx_images.py
"""

import argparse
import sys
import re
from pathlib import Path


# ── deps (lazy-import so missing deps give clean errors) ──────────────────────

def need(pkg, import_as=None):
    import importlib
    try:
        return importlib.import_module(import_as or pkg)
    except ImportError:
        print(f"Missing: pip install {pkg} --break-system-packages", file=sys.stderr)
        sys.exit(1)


# ── extract ───────────────────────────────────────────────────────────────────

def extract_pptx(source: Path, slide_n: int, crop, output: Path):
    _extract_via_pdf(source, slide_n, crop, output)


def _extract_via_pdf(source: Path, page_n: int, crop, output: Path, is_pptx=False):
    """Fallback: convert to PDF first, then rasterize."""
    import subprocess, tempfile
    convert = need("pdf2image", "pdf2image")
    Image = need("PIL", "PIL.Image").Image

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pdf_path = tmp / "converted.pdf"
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", str(source), "--outdir", str(tmp)],
            check=True, capture_output=True
        )
        # Find the pdf
        pdfs = list(tmp.glob("*.pdf"))
        if not pdfs:
            sys.exit("LibreOffice conversion failed — no PDF produced")
        pages = convert.convert_from_path(str(pdfs[0]), first_page=page_n, last_page=page_n, dpi=150)
        if not pages:
            sys.exit(f"Page {page_n} not found")
        img = pages[0]
        if crop:
            img = _apply_crop(img, crop)
        img.save(str(output))
    print(f"Saved: {output}")


def extract_pdf(source: Path, page_n: int, crop, output: Path):
    convert = need("pdf2image", "pdf2image")
    Image = need("PIL", "PIL.Image").Image
    pages = convert.convert_from_path(str(source), first_page=page_n, last_page=page_n, dpi=150)
    if not pages:
        sys.exit(f"Page {page_n} out of range")
    img = pages[0]
    if crop:
        img = _apply_crop(img, crop)
    img.save(str(output))
    print(f"Saved: {output}")


def extract_docx(source: Path, page_n: int, crop, output: Path):
    # Docx → PDF → image
    _extract_via_pdf(source, page_n, crop, output)


def _apply_crop(img, crop):
    """crop = (left top right bottom) as 0-1 fractions."""
    w, h = img.size
    box = (int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h))
    return img.crop(box)


# ── list ──────────────────────────────────────────────────────────────────────

def list_source(source: Path):
    ext = source.suffix.lower()
    if ext == ".pptx":
        Presentation = need("pptx", "pptx").presentation.Presentation
        prs = Presentation(str(source))
        for i, slide in enumerate(prs.slides, 1):
            # Grab title if available
            title = ""
            for shape in slide.shapes:
                if shape.has_text_frame and shape.shape_type == 13:
                    continue
                if shape.has_text_frame:
                    title = shape.text_frame.paragraphs[0].text.strip()
                    if title:
                        break
            print(f"Slide {i:3d}: {title[:70]}")
    elif ext == ".pdf":
        import subprocess
        result = subprocess.run(["pdfinfo", str(source)], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Pages" in line:
                    print(line)
        else:
            print("(pdfinfo unavailable — install poppler-utils)")
    else:
        print(f"Listing not supported for {ext}")


# ── embed ─────────────────────────────────────────────────────────────────────

def embed(quiz_txt: Path, images_dir: Path, output: Path):
    """
    Read quiz plain-text, find [GAMBAR: filename.png] tags,
    build a docx with images embedded at those positions.
    """
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import io

    doc = Document()
    text = quiz_txt.read_text(encoding="utf-8")
    # Split on [GAMBAR: ...] tags
    parts = re.split(r"(\[GAMBAR:[^\]]*\])", text)

    for part in parts:
        m = re.match(r"\[GAMBAR:\s*(.*?)\]", part)
        if m:
            tag_content = m.group(1).strip()
            # tag_content may be "q13_gambar.png" or "description — q13_gambar.png"
            # Extract filename: last token ending in .png/.jpg
            fname_m = re.search(r"(q\d+_\w+\.(?:png|jpg|jpeg))", tag_content)
            if fname_m:
                img_path = images_dir / fname_m.group(1)
                if img_path.exists():
                    doc.add_picture(str(img_path), width=Inches(5))
                    pic = doc.paragraphs[-1]  # image: own paragraph, centered, kept with options below
                    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    pic.paragraph_format.keep_with_next = True
                else:
                    doc.add_paragraph(f"[GAMBAR TIDAK DITEMUKAN: {img_path.name}]")
            else:
                doc.add_paragraph(f"[GAMBAR: {tag_content}]")
        else:
            # Plain text block — split by newlines, add paragraphs
            for line in part.split("\n"):
                doc.add_paragraph(line)

    doc.save(str(output))
    print(f"Saved docx: {output}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    # extract
    ex = sub.add_parser("extract", help="Extract one image from a source file")
    ex.add_argument("--source", required=True, type=Path, help="PPTX, PDF, or DOCX file")
    ex.add_argument("--slide", type=int, help="Slide number (PPTX)")
    ex.add_argument("--page",  type=int, help="Page number (PDF/DOCX)")
    ex.add_argument("--crop",  type=float, nargs=4, metavar=("L","T","R","B"),
                    help="Crop box as 0-1 fractions: left top right bottom")
    ex.add_argument("--output", required=True, type=Path, help="Output PNG filename")

    # list
    ls = sub.add_parser("list", help="List slides/pages in a source file")
    ls.add_argument("--source", required=True, type=Path)

    # embed
    em = sub.add_parser("embed", help="Embed extracted images into a Soalin quiz docx")
    em.add_argument("--quiz",       required=True, type=Path, help="Quiz plain-text file with [GAMBAR:] tags")
    em.add_argument("--images-dir", required=True, type=Path, help="Directory containing q{N}_gambar.png files")
    em.add_argument("--output",     required=True, type=Path, help="Output .docx path")

    args = p.parse_args()

    if args.cmd == "extract":
        source = args.source
        page = args.slide or args.page
        if not page:
            sys.exit("Provide --slide (PPTX) or --page (PDF/DOCX)")
        ext = source.suffix.lower()
        if ext == ".pptx":
            extract_pptx(source, page, args.crop, args.output)
        elif ext == ".pdf":
            extract_pdf(source, page, args.crop, args.output)
        else:
            extract_docx(source, page, args.crop, args.output)

    elif args.cmd == "list":
        list_source(args.source)

    elif args.cmd == "embed":
        embed(args.quiz, args.images_dir, args.output)


if __name__ == "__main__":
    main()
