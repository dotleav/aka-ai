#!/usr/bin/env python3
"""tk.py - alat hemat-token untuk transkrip literal (tanpa dependensi).
  prep  INPUT --out DIR [--kamus F] [--kata 1400]        pra-koreksi otomatis + pecah chunk
  apply DIR PATCH... --out F.md [--judul T] [--isi-saja]  terapkan patch -> markdown literal
  aka   --judul T --ringkasan R.md --literal L.md --out F.md [--sumber S]
Format input: baris "(mm:ss) teks" atau "(h:mm:ss) teks"; tanpa penanda waktu -> tiap paragraf jadi segmen §n.
"""
import re, os, sys, json, argparse

SEG = re.compile(r'^\(((?:\d+:)?\d{1,2}:\d{2})\)\s*(.*)$')
FILL = re.compile(r'\b(?:ee+h?|heeh|hee+|hmm+|emm+|umm+|ehm+)\b', re.I)

def load_kamus(path):
    out = []
    if path and os.path.exists(path):
        for l in open(path, encoding='utf-8'):
            l = l.rstrip('\n')
            if not l.strip() or l.startswith('#') or '\t' not in l:
                continue
            a, b = l.split('\t', 1)
            out.append((re.compile(r'\b(?:%s)\b' % a, re.I), b))
    return out

def prep(a):
    os.makedirs(a.out, exist_ok=True)
    raw = open(a.input, encoding='utf-8', errors='replace').read().splitlines()
    head, segs = [], []
    for l in raw:
        s = l.strip()
        m = SEG.match(s)
        if m:
            segs.append([m.group(1), m.group(2)])
        elif s and segs:
            segs[-1][1] += ' ' + s
        elif s:
            head.append(s)
    if not segs:  # fallback tanpa timestamp
        paras = [p.strip() for p in re.split(r'\n\s*\n|\n', '\n'.join(raw)) if p.strip()]
        segs = [['§%d' % i, p] for i, p in enumerate(paras, 1)]
        head = []
    kam = load_kamus(a.kamus)
    n_sub = w_in = w_out = 0
    for s in segs:
        t = s[1]
        w_in += len(t.split())
        t = FILL.sub('', t)
        for rx, r in kam:
            t, c = rx.subn(r, t)
            n_sub += c
        t = re.sub(r'\s+', ' ', t)
        t = re.sub(r'\s+([,.?!;:])', r'\1', t)
        t = re.sub(r'([,.?!])(?:\s*[,.])+', r'\1', t)
        t = t.strip(' ,')
        if t:
            t = t[0].upper() + t[1:]
        s[1] = t
        w_out += len(t.split())
    segs = [s for s in segs if s[1]]
    with open(os.path.join(a.out, 'bersih.tsv'), 'w', encoding='utf-8') as f:
        for ts, t in segs:
            f.write('%s\t%s\n' % (ts, t))
    judul = re.sub(r'\s*-\s*YouTube\s*$', '', head[0]) if head else os.path.splitext(os.path.basename(a.input))[0]
    sumber = next((h for h in head if h.startswith('http')), '')
    json.dump({'judul': judul, 'sumber': sumber, 'segmen': len(segs)},
              open(os.path.join(a.out, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    n, cnt, ch, files = 1, 0, [], []
    def flush():
        nonlocal n, cnt, ch
        if ch:
            p = os.path.join(a.out, 'chunk_%02d.txt' % n)
            open(p, 'w', encoding='utf-8').write('\n'.join(ch) + '\n')
            files.append(p); n += 1; ch = []; cnt = 0
    for ts, t in segs:
        ch.append('%s | %s' % (ts, t)); cnt += len(t.split())
        if cnt >= a.kata:
            flush()
    flush()
    print('segmen=%d kata_masuk=%d kata_bersih=%d ganti_kamus=%d chunk=%d dir=%s'
          % (len(segs), w_in, w_out, n_sub, len(files), a.out))

def apply(a):
    d = a.dir
    segs = [l.rstrip('\n').split('\t', 1) for l in open(os.path.join(d, 'bersih.tsv'), encoding='utf-8') if l.strip()]
    meta = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8'))
    idx = {}
    for i, s in enumerate(segs):
        idx.setdefault(s[0], i)
    notes, bad, n_patch = [], [], 0
    for pf in a.patch:
        for ln, l in enumerate(open(pf, encoding='utf-8'), 1):
            l = l.rstrip('\n')
            if not l.strip() or l.lstrip().startswith('#'):
                continue
            try:
                k = l[0]
                if k == 'S':
                    _, ts, txt = l.split('|', 2)
                    segs[idx[ts.strip()]][1] = txt.strip()
                elif k == 'R':
                    _, ts, cari, ganti = l.split('|', 3)
                    ts = ts.strip()
                    tg = [idx[ts]] if ts else range(len(segs))
                    hit = 0
                    for i in tg:
                        if cari in segs[i][1]:
                            segs[i][1] = segs[i][1].replace(cari, ganti); hit += 1
                    if not hit:
                        raise KeyError('tidak ketemu')
                elif k == '?':
                    _, ts, cat = l.split('|', 2)
                    notes.append((ts.strip(), cat.strip()))
                else:
                    raise ValueError('kode?')
                n_patch += 1
            except Exception:
                bad.append('%s:%d' % (os.path.basename(pf), ln))
    out = []
    if not a.isi_saja:
        out += ['# ' + (a.judul or meta['judul']), '']
        if meta['sumber']:
            out += ['Sumber: ' + meta['sumber'], '']
    for ts, t in segs:
        out += [t if ts.startswith('§') else '**(%s)** %s' % (ts, t), '']
    if notes:
        out += ['### Catatan verifikasi', '']
        out += ['%d. (%s) %s' % (i, ts, c) for i, (ts, c) in enumerate(notes, 1)]
    open(a.out, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    tj = sum(t.count('[tidak jelas]') for _, t in segs)
    print('OK segmen=%d patch=%d ditolak=%d tidak_jelas=%d catatan=%d file=%s'
          % (len(segs), n_patch, len(bad), tj, len(notes), a.out))
    if bad:
        print('PATCH DITOLAK (perbaiki lalu jalankan ulang apply):', ', '.join(bad[:20]))

def aka(a):
    rk = open(a.ringkasan, encoding='utf-8').read().strip().splitlines()
    if rk and rk[0].startswith('# '):
        rk = rk[1:]
    rk = ['#' + l if l.startswith('#') else l for l in rk]
    lit = open(a.literal, encoding='utf-8').read().strip()
    out = ['# %s — Transkrip Aka' % a.judul, '']
    if a.sumber:
        out += ['Sumber: ' + a.sumber, '']
    out += ['## Bagian 1 — Rangkuman', ''] + rk + ['', '---', '', '## Bagian 2 — Transkrip Literal', '', lit, '']
    open(a.out, 'w', encoding='utf-8').write('\n'.join(out))
    print('OK aka=%s' % a.out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('prep'); p.add_argument('input'); p.add_argument('--out', required=True)
    p.add_argument('--kamus'); p.add_argument('--kata', type=int, default=1400); p.set_defaults(f=prep)
    p = sp.add_parser('apply'); p.add_argument('dir'); p.add_argument('patch', nargs='*')
    p.add_argument('--out', required=True); p.add_argument('--judul'); p.add_argument('--isi-saja', action='store_true'); p.set_defaults(f=apply)
    p = sp.add_parser('aka'); p.add_argument('--judul', required=True); p.add_argument('--ringkasan', required=True)
    p.add_argument('--literal', required=True); p.add_argument('--out', required=True); p.add_argument('--sumber', default=''); p.set_defaults(f=aka)
    a = ap.parse_args(); a.f(a)
