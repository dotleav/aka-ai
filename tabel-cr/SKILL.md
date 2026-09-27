---
name: tabel-cr
description: >-
  Pembuat tabel kasus (CR) universal untuk OSCE/CBT kedokteran: satu kasus = satu baris pada tabel Word (docx) sungguhan dengan kolom tetap No, KASUS, Ax, Pf, PP, Tx, EDUKASI, untuk topik gangguan medis apa pun. Sumber bundel saat ini hanya neurologi (59 kasus FK UKDW, level SKDI 2024, PERDOSSI 2023); topik lain ditambah bertahap. Gunakan setiap kali pengguna minta "tabel CR", "CR neurologi/kardiologi/…", "buatkan tabel kasus", ringkasan kasus per diagnosis beserta resep lege artis dan edukasi, atau menyebut SKDI/PERDOSSI untuk simulasi OSCE. Jika materi topik belum dibundel, skill ini mencari manual lewat web atau connector PubMed/Consensus.
---

# Tabel CR (Kasus per Diagnosis)

Output: **file `.docx` berisi tabel Word sungguhan** (bukan markdown/pipe-table) untuk topik gangguan medis pilihan pengguna — satu baris per kasus. Format kolom dan gaya tabel tetap (lihat `references/format-tabel-cr.md`), isi bergantung topik.

## Spesifikasi tabel (wajib, tidak boleh menyimpang)
- **Header baris pertama, selalu persis 7 kolom dalam urutan ini**: `No | KASUS | Ax | Pf | PP | Tx | EDUKASI` (Ax = Anamnesis, Pf = Pemeriksaan Fisik, Tx = Tata Laksana). Bila skill/referensi lain menyebut nama kolom berbeda (mis. "GEJALA/ANAMNESIS", "TATA LAKSANA"), tetap tulis header sebagai di atas.
- **Gaya tabel**: Table Grid (semua sel bergaris, border tunggal hitam tipis) — di docx-js: beri tiap sel `borders` single pada keempat sisi (top/bottom/left/right, size ~4, color "000000"), bukan tabel tanpa garis.
- **Repeat Header Rows menyala**: baris header berulang di tiap halaman saat tabel panjang — di docx-js: set `tableHeader: true` pada `TableRow` header.
- **Font seluruh isi tabel**: Comic Sans MS, ukuran 12pt (docx-js: `size: 24` — satuan half-point) — berlaku untuk header maupun isi baris, tanpa terkecuali.
- Satu kasus = satu baris tabel (bukan satu blok heading per kasus seperti versi markdown lama).

## Topik tersedia (sumber bundel)
| Topik | Folder | Isi |
|---|---|---|
| Neurologi | `references/neurologi/` | 59 kasus terverifikasi (9 Tabel CR + 50 SKDI), indeks PERDOSSI 2023, peta cakupan, PDF sumber |

Topik lain: belum ada. Pengguna akan menambah bertahap (cara: `references/tambah-topik.md`).

## Referensi (baca sesuai kebutuhan, jangan sekaligus)
- `references/format-tabel-cr.md` — struktur 6 kolom + 2 contoh asli. Acuan format semua topik.
- `references/neurologi/daftar-kasus-59-terverifikasi.md` — daftar & level kasus neurologi. Sumber kebenaran level; jangan re-OCR SKDI.
- `references/neurologi/peta-cakupan-kasus.md` — kasus mana ada di PERDOSSI (+ halaman) vs cari manual.
- `references/neurologi/daftar-isi-perdossi.md` — indeks halaman PERDOSSI.
- `references/neurologi/PERDOSSI_2023.pdf` — sumber klinis neurologi.

## Alur kerja per kasus
1. **Tentukan topik & daftar kasus.** Topik ada di tabel di atas → pakai daftar kasusnya. Topik belum ada → minta pengguna daftar kasus (atau usulkan dari SKDI/kurikulum, lalu konfirmasi) dan lanjut ke langkah 3.
2. **Materi bundel ada?** Cek peta cakupan topik. Ada → ekstrak HANYA halaman relevan (±10 halaman dari indeks) dengan `bash_tool` + pypdf; `view` dengan `view_range` hanya bila tabel/gambar dibutuhkan. Jangan `view` seluruh PDF.
3. **Materi tidak ada / kurang → cari manual.** Urutan:
   - Connector **PubMed** dan **Consensus**: panggil `tool_search` dulu (deferred tools), pakai bila terhubung. Query spesifik ke celah klinis (kriteria diagnosis, dosis dewasa/anak, algoritma), bukan query umum.
   - Connector tidak tersedia → `web_search` / `web_fetch`. Utamakan PPK/guideline nasional (Kemenkes, perhimpunan profesi), lalu guideline internasional, lalu review terindeks. Hindari forum dan blog.
   - Catat sumber tiap kasus di baris kecil di akhir kasus; ini bukan bagian tabel.
   - Dosis dan kriteria yang tidak bisa diverifikasi → tandai `[verifikasi]`, jangan ditebak.
4. **Susun kasus** memakai `references/format-tabel-cr.md`, dengan penekanan:
   - **PF & PP wajib berisi temuan KHAS/pembeda** diagnosis ini dari DD-nya. "dbn" hanya untuk pemeriksaan yang memang tidak relevan.
   - **Tata Laksana**: resep lege artis penuh (`R/`, bentuk, kekuatan, jumlah angka Romawi, signatura), bukan cuma nama obat. Nama generik; dosis sesuai sumber; jumlah = signatura × durasi. Pakai skill resep lege artis bila tersedia.
   - **Algoritma ringkas** untuk kasus dengan alur keputusan (kapan rujuk, eskalasi, kriteria rawat).
   - **Edukasi spesifik kasus**, bukan generik. Instruksi non-farmakologis bertahap ditulis bernomor.
5. **Susun isi tiap kasus dulu sebagai teks per kolom** (lihat sub-bagian isi per kolom di bawah) — ini yang dipikirkan Claude. Baru setelah 5–8 kasus siap dalam satu batch, tulis skrip docx-js (lihat `references/format-tabel-cr.md` untuk kerangka kode) yang menambahkan baris-baris itu ke tabel. Untuk kasus pertama: buat dokumen baru dengan header + baris-baris batch pertama. Batch berikutnya: `unzip` docx yang sudah ada, sisipkan `<w:tr>` baris baru sebelum penutup `<w:tbl>` di `word/document.xml` (ikuti gotcha edit-existing-docx pada skill `docx`), lalu `zip` ulang — jangan generate ulang seluruh dokumen dari nol tiap batch. Jangan cetak ulang isi kasus yang sudah ditulis ke chat.
6. Setelah batch selesai, render cepat ke PDF untuk memastikan border/font/header-repeat tampil benar (lihat skill `docx`), lalu `present_files` untuk file `.docx`-nya. Lampiran bersama (skala, tabel pembeda, dsb.) ditulis SEKALI di akhir dokumen, di luar tabel (paragraf biasa setelah tabel, font sama).

## Isi per kolom (satu kasus = satu baris, 7 sel)
- **No**: nomor urut kasus.
- **KASUS**: nama diagnosis + level SKDI dalam kurung, lalu daftar DD (diagnosis banding).
- **Ax**: nama-usia-pekerjaan pasien (ilustratif), keluhan utama (dalam tanda kutip), RPS (kronologi lengkap onset/durasi/pemberat-peringan/keluhan penyerta), RPD, RPK (opsional).
- **Pf**: KU, kesadaran (GCS bila relevan), vital sign, status gizi bila relevan, lalu pemeriksaan fisik spesifik kasus dengan temuan KHAS — bukan "dbn" semua.
- **PP**: pemeriksaan penunjang (boleh "-" bila memang tidak diperlukan untuk diagnosis klinis), sebutkan temuan khas yang diharapkan bila relevan.
- **Tx**: resep lege artis (`R/ <obat> <bentuk> <kekuatan> No. <romawi>` + `S <signatura>`), dikelompokkan per kategori obat bila lebih dari satu golongan; sertakan algoritma tata laksana ringkas bila kasus punya alur keputusan klinis penting.
- **EDUKASI**: poin edukasi spesifik kasus (bukan generik), termasuk instruksi non-farmakologis bertahap bila ada.

Dalam satu sel, pisahkan sub-bagian dengan paragraf/baris baru di dalam sel (bukan tabel bersarang); semua tetap Comic Sans MS 12pt.

## Urutan kasus
Topik bundel: ikuti urutan di daftar kasus topik itu (neurologi: 9 kasus Tabel CR dulu untuk kalibrasi gaya, lalu 50 kasus SKDI per kategori). Bila pengguna minta sebagian, tetap ikuti urutan itu agar mudah disambung.

## Jangan
- Jangan buka `SKDI_2024_-_OCR.pdf` untuk verifikasi level; OCR tidak reliabel, level final ada di daftar kasus.
- Jangan tulis identitas dokter/SIP/paraf/data pasien lengkap. Nama-usia-pekerjaan ilustratif saja.
- Jangan salin isi sumber panjang ke tiap kasus; parafrase secukupnya, ambil poin yang mengisi kolom.
