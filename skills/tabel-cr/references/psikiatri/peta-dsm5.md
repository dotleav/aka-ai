# Peta DSM-5 (APA 2013, 970 hlm PDF)

PDF **tidak dibundel** (±32 MB, hak cipta APA). Berkas ini hanya peta. Semua nomor = **halaman PDF (1-based)** dari bookmark dan teks PDF, bukan nomor cetak (selisih cetak→PDF 31–38, berubah antar bab). Akurasi ±1 halaman.

## Cara pakai
1. Cari berkas di `/mnt/user-data/uploads/` (nama berisi "DSM"). Tidak ada → minta pengguna unggah; tetap tidak ada → pakai peta ini sebagai petunjuk dan lengkapi lewat web/PubMed.
2. Ekstrak hanya halaman kriteria (3–5 halaman): `pdftotext -f N -l M -layout DSM-5.pdf -`. PDF punya lapisan teks OCR, bisa berderau; rasterisasi halaman bila kriteria tampak rusak.
3. DSM-5 hanya memuat **kriteria diagnostik, spesifier, kode ICD-10-CM**, tanpa terapi. Terapi/dosis tetap dari Kaplan & Sadock. Diagnosis klinis Indonesia tetap mengacu PPDGJ-III (kode F); DSM-5 dipakai melengkapi kriteria. Kode ICD-10-CM DSM-5 bisa beda dari ICD-10 PPDGJ: tulis kode PPDGJ di kolom KASUS.

## Navigasi bagian (hlm PDF)
Klasifikasi 13 · Dasar DSM-5 45 · Neurodevelopmental 69 · Spektrum skizofrenia 125 · Bipolar 161 · Depresif 193 · Anxietas 227 · OCD & terkait 272 · Trauma & stresor 302 · Disosiatif 328 · Gejala somatik 345 · Makan 364 · Eliminasi 390 · Tidur-bangun 396 · Disfungsi seksual 458 · Disforia gender 486 · Disruptif/impuls/konduk 495 · Zat & adiktif 515 · Neurokognitif 624 · Kepribadian 677 · Parafilik 717 · Efek samping obat 740 · Kondisi perhatian klinis 746 · Alat ukur 761 · Formulasi budaya 777 · Model alternatif kepribadian 788 · Daftar kode ICD-10-CM abjad 862, numerik 900.

## Diagnosis → halaman kriteria (PDF)
| Diagnosis | DSM-5 | Diagnosis | DSM-5 |
|---|---|---|---|
| Delirium | 629 | Skizofrenia | 137 |
| Gangguan neurokognitif mayor (Alzheimer, vaskular, dll.) | 635 | Skizofreniform | 134 |
| Gangguan neurokognitif ringan | ±638 | Psikotik singkat | 132 |
| Gangguan penggunaan alkohol | 524 | Waham (delusional) | 128 |
| Kanabis | 543 | Skizoafektif | 143 |
| Opioid | 575 | Bipolar I | 161 |
| Sedatif/hipnotik/ansiolitik | 584 | Bipolar II | 170 |
| Stimulan | 595 | Siklotimia | 177 |
| Depresi mayor (MDD) | 198 | Distimia (depresif persisten) | 206 |
| DMDD | 194 | Panik | 246 |
| Fobia sosial | 240 | Agorafobia | 255 |
| Fobia spesifik | 235 | GAD | 260 |
| OCD | 274 | PTSD | 308 |
| Stres akut | 317 | Gangguan penyesuaian | 323 |
| Disosiatif identitas | 329 | Gejala somatik | 347 |
| Cemas penyakit | 351 | Konversi (gejala neurologis fungsional) | 354 |
| Anoreksia nervosa | 373 | Bulimia nervosa | 380 |
| Makan berlebihan (BED) | 385 | Insomnia | 397 |
| Disfungsi ereksi | 461 | Disforia gender | 487 |
| ODD | 496 | Gangguan konduk | 500 |
| Kepribadian paranoid | 681 | Kepribadian skizoid | 684 |
| Antisosial | 691 | Borderline | 695 |
| Histrionik | 699 | Cemas-menghindar | 704 |
| Dependen | 707 | Obsesif-kompulsif (OCPD) | 710 |
| Disabilitas intelektual | 71 | ASD | 82 |
| ADHD | 97 | | |

Katatonia dan diagnosis lain tidak ada di tabel: cari lewat daftar abjad hlm 862 atau `grep` pada hasil `pdftotext`.
