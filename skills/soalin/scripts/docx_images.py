#!/usr/bin/env python3
"""
docx_images.py — image crop persistence + placement audit for Soalin quiz docx.

Why: Google Docs' built-in crop only stores a *view window* (a:srcRect) over the
full original image. Copy/paste elsewhere may drop the window and the full image
(maybe with the answer-leaking part) comes back. Fix = bake the crop into pixels.

USAGE
  # 1. Bake Google-Docs crops into the image pixels (srcRect removed, full original dropped):
  python docx_images.py bake --docx in.docx --output out.docx

  # 2. Docx lost its crop but the PDF still shows it cropped: rebuild from the PDF.
  #    Images matched by reading order; PDF must have the same number of images as the docx.
  python docx_images.py sync-pdf --docx in.docx --pdf in.pdf --output out.docx

  # 3. Audit image placement (must be: centered, under question text, above option A):
  python docx_images.py check --docx in.docx
  python docx_images.py check --docx in.docx --fix --output out.docx

  # 4. Manual crop of one image (ONLY when it leaks the answer; box = 0-1 fractions L T R B):
  python docx_images.py trim --image q3_gambar.png --crop 0 0 1 0.85 --output q3_gambar.png
  python docx_images.py dump --docx in.docx --outdir imgs     # save every image as img_NN.png to inspect
  python docx_images.py replace --docx in.docx --index 3 --image q3_trim.png --output out.docx  # put trimmed image back

Notes: needs lxml + pillow (+ pypdfium2 for sync-pdf).
"""
import argparse, io, re, sys, zipfile
from pathlib import Path
from lxml import etree

NS = dict(
    w="http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    a="http://schemas.openxmlformats.org/drawingml/2006/main",
    r="http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
)
W, A, R, WP = ("{%s}" % NS[k] for k in ("w", "a", "r", "wp"))
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"
DOC, RELS, CTF = "word/document.xml", "word/_rels/document.xml.rels", "[Content_Types].xml"


# ── io ────────────────────────────────────────────────────────────────────────
def load(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def save(files, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(CTF, files[CTF])
        for n, b in files.items():
            if n != CTF:
                z.writestr(n, b)
    print(f"Saved: {path}")


def xml(files, name):
    return etree.fromstring(files[name])


def put(files, name, root):
    files[name] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def need_pil():
    try:
        from PIL import Image
        return Image
    except ImportError:
        sys.exit("Missing: pip install pillow --break-system-packages")


def media_path(target):
    t = target.lstrip("/")
    return t if t.startswith("word/") else "word/" + t


def set_png(files, rels, blip, img, tag):
    """Point blip at a new PNG part; register rel + content type."""
    name = f"word/media/{tag}.png"
    buf = io.BytesIO()
    img.save(buf, "PNG")
    files[name] = buf.getvalue()
    rid = f"rId{tag}"
    old = rels.xpath(f"//*[@Id='{blip.get(R + 'embed')}']")
    rel = etree.SubElement(rels, REL + "Relationship")
    rel.set("Id", rid)
    rel.set("Type", old[0].get("Type") if old else NS["r"] + "/image")
    rel.set("Target", f"media/{tag}.png")
    blip.set(R + "embed", rid)
    ct = xml(files, CTF)
    if not ct.xpath("//*[@Extension='png']"):
        e = etree.SubElement(ct, CT + "Default")
        e.set("Extension", "png")
        e.set("ContentType", "image/png")
        put(files, CTF, ct)


def prune_media(files, doc, rels):
    """Drop image rels/parts no longer referenced (removes leftover uncropped originals)."""
    used = {v for el in doc.iter() for k, v in el.attrib.items() if k.startswith(R)}
    for rel in list(rels):
        if rel.get("Type", "").endswith("/image") and rel.get("Id") not in used:
            files.pop(media_path(rel.get("Target")), None)
            rels.remove(rel)
    still = {media_path(r.get("Target")) for r in rels}
    for n in [n for n in files if n.startswith("word/media/") and n not in still]:
        del files[n]


def blips(doc):
    return [b for b in doc.iter(A + "blip") if b.get(R + "embed")]


def blip_image(files, rels, blip):
    Image = need_pil()
    rel = rels.xpath(f"//*[@Id='{blip.get(R + 'embed')}']")
    if not rel:
        return None
    return Image.open(io.BytesIO(files[media_path(rel[0].get("Target"))])).convert("RGBA")


# ── bake ──────────────────────────────────────────────────────────────────────
def bake(files):
    doc, rels = xml(files, DOC), xml(files, RELS)
    n = 0
    for i, blip in enumerate(blips(doc), 1):
        bf = blip.getparent()
        sr = bf.find(A + "srcRect")
        if sr is None:
            continue
        l, t, r, b = (int(sr.get(k) or 0) for k in "ltrb")  # 1/1000 of a percent
        if min(l, t, r, b) < 0:
            print(f"img#{i}: negative crop (padding) clamped to 0")
            l, t, r, b = (max(0, v) for v in (l, t, r, b))
        if not any((l, t, r, b)):
            bf.remove(sr)
            continue
        img = blip_image(files, rels, blip)
        if img is None:
            continue
        w, h = img.size
        box = (round(w * l / 1e5), round(h * t / 1e5), round(w * (1 - r / 1e5)), round(h * (1 - b / 1e5)))
        if box[2] - box[0] < 2 or box[3] - box[1] < 2:
            print(f"img#{i}: crop leaves nothing, skipped")
            continue
        set_png(files, rels, blip, img.crop(box), f"baked{i}")
        bf.remove(sr)
        n += 1
        print(f"img#{i}: baked crop {w}x{h} -> {box[2]-box[0]}x{box[3]-box[1]}")
    prune_media(files, doc, rels)
    put(files, DOC, doc)
    put(files, RELS, rels)
    print(f"{n} crop baked")


# ── sync-pdf ──────────────────────────────────────────────────────────────────
def pdf_images(pdf_path, scale=4):
    """Each image as VISIBLE in the PDF (clip/crop applied), in reading order.
    Visible area = pixels that change when that image object is removed (magenta backdrop)."""
    try:
        import pypdfium2 as pdfium
        import pypdfium2.raw as c
        from PIL import ImageChops
    except ImportError:
        sys.exit("Missing: pip install pypdfium2 pillow --break-system-packages")
    mg = (255, 0, 255, 255)
    pos = lambda o: (o.get_bounds if hasattr(o, "get_bounds") else o.get_pos)()  # l, b, r, t
    order = lambda page: sorted(page.get_objects(filter=[c.FPDF_PAGEOBJ_IMAGE]), key=lambda o: (-pos(o)[3], pos(o)[0]))
    out = []
    for pi in range(len(pdfium.PdfDocument(str(pdf_path)))):
        n = len(order(pdfium.PdfDocument(str(pdf_path))[pi]))
        for oi in range(n):
            page = pdfium.PdfDocument(str(pdf_path))[pi]
            with_img = page.render(scale=scale, fill_color=mg).to_pil().convert("RGB")
            o = order(page)[oi]
            page.remove_obj(o)
            page.gen_content()
            without = page.render(scale=scale, fill_color=mg).to_pil().convert("RGB")
            box = ImageChops.difference(with_img, without).getbbox()
            if box:
                out.append(with_img.crop(box))
    return out


def sync_pdf(files, pdf_path, tol=0.03):
    doc, rels = xml(files, DOC), xml(files, RELS)
    bl, pi = blips(doc), pdf_images(pdf_path)
    if len(bl) != len(pi):
        sys.exit(f"Image count mismatch: docx {len(bl)} vs pdf {len(pi)}. Cannot match by order.")
    n = 0
    for i, (blip, shown) in enumerate(zip(bl, pi), 1):
        img = blip_image(files, rels, blip)
        sr = blip.getparent().find(A + "srcRect")
        w, h = img.size
        if sr is not None:  # crop still stored in docx: effective aspect
            l, t, r, b = (int(sr.get(k) or 0) for k in "ltrb")
            w, h = w * (1 - (l + r) / 1e5), h * (1 - (t + b) / 1e5)
        have, want = w / h, shown.width / shown.height
        if abs(have - want) / want > tol:
            set_png(files, rels, blip, shown.convert("RGBA"), f"pdf{i}")
            if sr is not None:
                blip.getparent().remove(sr)
            n += 1
            print(f"img#{i}: aspect {have:.3f} != pdf {want:.3f} -> replaced with PDF crop")
    prune_media(files, doc, rels)
    put(files, DOC, doc)
    put(files, RELS, rels)
    print(f"{n} image replaced from PDF")


# ── check / fix placement ─────────────────────────────────────────────────────
OPT = re.compile(r"^\s*([A-E])\s*[.)]\s*\S?")
NUM = re.compile(r"^\s*\d+\s*[.)]\s+\S")
KUNCI = re.compile(r"^\s*Kunci\s*:", re.I)
PENJ = re.compile(r"^\s*Penjelasan\s*:", re.I)
PPR_AFTER_JC = {W + x for x in ("textDirection", "textAlignment", "textboxTightWrap", "outlineLvl",
                                "divId", "cnfStyle", "rPr", "sectPr", "pPrChange")}


def ptext(p):
    return "".join(t.text or "" for t in p.iter(W + "t")).strip()


def has_draw(p):
    return p.find(".//" + W + "drawing") is not None or p.find(".//" + W + "pict") is not None


def is_centered(p):
    jc = p.find(f"{W}pPr/{W}jc")
    return jc is not None and jc.get(W + "val") == "center"


def center(p):
    pPr = p.find(W + "pPr")
    if pPr is None:
        pPr = etree.Element(W + "pPr")
        p.insert(0, pPr)
    jc = pPr.find(W + "jc")
    if jc is None:
        jc = etree.Element(W + "jc")
        pos = next((i for i, ch in enumerate(pPr) if ch.tag in PPR_AFTER_JC), len(pPr))
        pPr.insert(pos, jc)
    jc.set(W + "val", "center")
    if pPr.find(W + "keepNext") is None:  # keep image with the options below it
        kn = etree.Element(W + "keepNext")
        pPr.insert(1 if pPr.find(W + "pStyle") is not None else 0, kn)


def split_drawing_par(p):
    """New paragraph holding only p's drawing runs (p keeps its text)."""
    runs = [r for r in p.iter(W + "r") if r.find(".//" + W + "drawing") is not None]
    q = etree.Element(W + "p")
    for r in runs:
        q.append(r)
    return q


def check(files, fix=False):
    doc = xml(files, DOC)
    body = doc.find(W + "body")
    paras = [p for p in body if p.tag == W + "p"]
    numbered = any(NUM.match(ptext(p)) for p in paras)
    state, qn, stem_text, opt_a, bad, k = "stem", 1, False, None, 0, 0
    for el in list(body):
        if el.tag == W + "tbl" and el.find(".//" + W + "drawing") is not None:
            print("! gambar di dalam tabel: cek manual"); bad += 1
            continue
        if el.tag != W + "p":
            continue
        txt, draw = ptext(el), has_draw(el)
        if txt:
            if NUM.match(txt):
                state, stem_text, opt_a, qn = "stem", True, None, (int(re.match(r"\s*(\d+)", txt).group(1)))
            elif OPT.match(txt) and not KUNCI.match(txt):
                if txt.lstrip()[0] == "A":
                    opt_a = el
                state = "opt"
            elif KUNCI.match(txt):
                state = "kunci"
            elif PENJ.match(txt):
                state = "penj"
            elif state in ("penj", "kunci") and not numbered:
                state, stem_text, opt_a = "stem", True, None; qn += 1
            elif state == "stem":
                stem_text = True
        if not draw:
            continue
        k += 1
        floating = el.find(".//" + WP + "anchor") is not None
        tag = f"img#{k} (soal ~{qn})"
        issues = []
        if floating:
            issues.append("FLOATING (bukan inline): cek manual")
        if state == "opt" and opt_a is not None:
            issues.append("DI BAWAH/ANTARA OPSI, harus di atas opsi A")
            if fix and not floating:
                tgt = split_drawing_par(el) if txt else el
                opt_a.addprevious(tgt)
                center(tgt)
        elif state in ("kunci", "penj"):
            print(f"{tag}: setelah Kunci/Penjelasan, dibiarkan (gambar penjelasan atau soal berikutnya? cek manual)")
            continue
        elif state == "stem":
            if not stem_text and not txt:
                issues.append("DI ATAS TEKS SOAL? harus di bawah soal, cek manual")
            elif txt and stem_text:
                issues.append("INLINE dalam paragraf soal, harus paragraf sendiri di bawah soal")
                if fix and not floating:
                    q = split_drawing_par(el)
                    el.addnext(q)
                    center(q)
        if not is_centered(el) and not txt:
            issues.append("TIDAK DI TENGAH")
            if fix:
                center(el)
        bad += bool(issues)
        print(f"{tag}: " + ("OK" if not issues else "; ".join(issues)))
    if fix:
        put(files, DOC, doc)
    print(f"{k} gambar, {bad} bermasalah" + (" (diperbaiki yang otomatis)" if fix else ""))


# ── trim / dump ───────────────────────────────────────────────────────────────
def trim(image, crop, output):
    Image = need_pil()
    img = Image.open(image)
    w, h = img.size
    img.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h))).save(output)
    print(f"Saved: {output}")


def dump(files, outdir):
    doc, rels = xml(files, DOC), xml(files, RELS)
    outdir.mkdir(parents=True, exist_ok=True)
    for i, blip in enumerate(blips(doc), 1):
        img = blip_image(files, rels, blip)
        sr = blip.getparent().find(A + "srcRect")
        if sr is not None:
            l, t, r, b = (int(sr.get(k) or 0) for k in "ltrb")
            w, h = img.size
            img = img.crop((round(w * l / 1e5), round(h * t / 1e5), round(w * (1 - r / 1e5)), round(h * (1 - b / 1e5))))
        img.save(outdir / f"img_{i:02d}.png")
    print(f"Saved images to {outdir}")


def replace(files, index, image):
    """Swap image #index with a file (e.g. manually trimmed); keep width, fix height to new aspect."""
    Image = need_pil()
    doc, rels = xml(files, DOC), xml(files, RELS)
    bl = blips(doc)
    if not 1 <= index <= len(bl):
        sys.exit(f"index out of range 1-{len(bl)}")
    blip, img = bl[index - 1], Image.open(image).convert("RGBA")
    drawing = blip
    while drawing.tag != W + "drawing":
        drawing = drawing.getparent()
    set_png(files, rels, blip, img, f"manual{index}")
    sr = blip.getparent().find(A + "srcRect")
    if sr is not None:
        blip.getparent().remove(sr)
    for ext in list(drawing.iter(WP + "extent")) + list(drawing.iter(A + "ext")):
        if ext.get("cx") and ext.get("cy"):
            ext.set("cy", str(round(int(ext.get("cx")) * img.height / img.width)))
    prune_media(files, doc, rels)
    put(files, DOC, doc)
    put(files, RELS, rels)
    print(f"img#{index} replaced")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    for name in ("bake", "sync-pdf", "check", "dump"):
        x = s.add_parser(name)
        x.add_argument("--docx", required=True, type=Path)
        if name != "dump":
            x.add_argument("--output", type=Path)
        if name == "sync-pdf":
            x.add_argument("--pdf", required=True, type=Path)
        if name == "check":
            x.add_argument("--fix", action="store_true")
        if name == "dump":
            x.add_argument("--outdir", required=True, type=Path)
    rp = s.add_parser("replace")
    rp.add_argument("--docx", required=True, type=Path)
    rp.add_argument("--index", required=True, type=int, help="image number as printed by check/dump (1-based)")
    rp.add_argument("--image", required=True, type=Path)
    rp.add_argument("--output", required=True, type=Path)
    t = s.add_parser("trim")
    t.add_argument("--image", required=True, type=Path)
    t.add_argument("--crop", required=True, type=float, nargs=4, metavar=("L", "T", "R", "B"))
    t.add_argument("--output", required=True, type=Path)
    a = p.parse_args()

    if a.cmd == "trim":
        return trim(a.image, a.crop, a.output)
    files = load(a.docx)
    if a.cmd == "replace":
        replace(files, a.index, a.image)
        return save(files, a.output)
    if a.cmd == "dump":
        return dump(files, a.outdir)
    if a.cmd == "check" and not a.fix:
        return check(files)
    if not a.output:
        sys.exit("--output required")
    {"bake": lambda: bake(files), "sync-pdf": lambda: sync_pdf(files, a.pdf),
     "check": lambda: check(files, fix=True)}[a.cmd]()
    save(files, a.output)


if __name__ == "__main__":
    main()
