# Template Format Tabel CR

Kolom & contoh isi diekstrak dari dokumen asli Tabel CR Neurologi (hlm 167–180); struktur yang sama berlaku untuk topik apa pun (neurologi hanyalah topik pertama). Output SELALU tabel Word (`.docx`) sungguhan — satu baris = satu kasus, header 7 kolom tetap, gaya Table Grid, header berulang tiap halaman, font Comic Sans MS 12pt di seluruh tabel.

## Kolom output (urutan & nama header tetap dipakai — wajib persis ini)
1. **No** — nomor urut kasus
2. **KASUS** — nama diagnosis + level SKDI dalam kurung, lalu daftar DD (diagnosis banding)
3. **Ax** (Anamnesis) — nama-usia-pekerjaan pasien (ilustratif), keluhan utama (dalam tanda kutip), RPS (kronologi lengkap dgn onset/durasi/pemberat-peringan/keluhan penyerta), RPD, RPK, kadang Lifestyle
4. **Pf** (Pemeriksaan Fisik) — KU, kesadaran (GCS bila relevan), vital sign, status gizi bila relevan, lalu **pemeriksaan spesifik kasus** (mis. nervus kranialis, refleks fisiologis/patologis, meningeal sign, tes provokasi seperti Dix-Hallpike, dsb untuk neurologi) dengan **temuan yang KHAS untuk diagnosis tsb** — bukan cuma "dbn" semua
5. **PP** — pemeriksaan penunjang (boleh "-" bila tidak diperlukan untuk diagnosis klinis, tapi isi kalau memang lazim: rontgen, CT/MRI, LP, EMG, dst — sebutkan temuan khas yang diharapkan)
6. **Tx** (Tata Laksana) — resep lege artis format `R/ <obat> <bentuk> <kekuatan> No. <romawi>` + `S <signatura>`, dikelompokkan per kategori obat (mis. "Vertigo", "Antiemetik", "NSAID", "Antispasmodic") kalau lebih dari satu golongan. Sertakan **algoritma tata laksana ringkas** kalau kasusnya punya alur keputusan klinis penting (mis. kapan rujuk, kapan trombolisis, tahapan status epileptikus, eskalasi krisis miastenia)
7. **EDUKASI** — poin edukasi yang **spesifik untuk kasus itu** (bukan generik "istirahat cukup" untuk semua kasus kecuali memang relevan), termasuk instruksi non-farmakologis bertahap kalau ada (mis. Brandt-Daroff exercise untuk BPPV, ditulis sebagai langkah bernomor)

Ada juga bagian **Lampiran** di akhir dokumen sumber berisi gambar/tabel referensi bersama (contoh neurologi: skala GCS & kekuatan otot, tabel beda vertigo perifer-sentral, gambar CT scan evolusi perdarahan, dst) — ini TIDAK diulang per kasus/baris, cukup sekali sebagai paragraf biasa (bukan sel tabel) setelah tabel selesai, kalau relevan dengan beberapa kasus sekaligus.

## Kerangka docx-js (kasus pertama / dokumen baru)
Poin kunci yang wajib ada — isi detail (jumlah baris, teks) menyesuaikan batch kasus:

```javascript
const { Document, Table, TableRow, TableCell, Paragraph, TextRun, WidthType, BorderStyle, HeadingLevel } = require("docx");

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
const FONT = "Comic Sans MS";
const SIZE = 24; // 12pt, dalam half-point

function cell(text, { header = false, width } = {}) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: SIZE, bold: header })],
    })],
  });
}

const headerRow = new TableRow({
  tableHeader: true, // -> Repeat Header Rows menyala
  children: ["No", "KASUS", "Ax", "Pf", "PP", "Tx", "EDUKASI"].map((h, i) =>
    cell(h, { header: true, width: colWidths[i] })),
});

// satu TableRow per kasus, 7 TableCell sesuai urutan kolom di atas
const caseRow = new TableRow({
  children: [
    cell(String(no), { width: colWidths[0] }),
    cell(kasusText, { width: colWidths[1] }),
    cell(axText, { width: colWidths[2] }),
    cell(pfText, { width: colWidths[3] }),
    cell(ppText, { width: colWidths[4] }),
    cell(txText, { width: colWidths[5] }),
    cell(edukasiText, { width: colWidths[6] }),
  ],
});

const table = new Table({
  width: { size: 15840, type: WidthType.DXA }, // A4 landscape lebar penuh
  columnWidths: colWidths, // harus sejumlah 7 dan menjumlah ke width tabel
  rows: [headerRow, ...caseRows],
});
```

Ingat gotcha umum docx-js (lihat skill `docx`): `columnWidths` pada tabel HARUS diisi selain `width` per sel; landscape butuh `orientation: PageOrientation.LANDSCAPE` di section; jangan pakai `\n` di dalam teks — pecah jadi beberapa `TextRun`/`Paragraph` di dalam sel yang sama untuk sub-bagian (mis. RPS/RPD dalam sel Ax).

## Batch berikutnya (menambah baris ke docx yang sudah ada)
Jangan generate ulang seluruh dokumen. `unzip` docx yang ada, tambahkan blok `<w:tr>` baris baru (7 `<w:tc>`, tiap run pakai `<w:rFonts w:ascii="Comic Sans MS" .../>` dan `<w:sz w:val="24"/>`, border sudah ada di `<w:tblBorders>` tabel) sebelum penutup `</w:tbl>` di `word/document.xml`, lalu `zip` ulang. Ikuti alur edit-docx-existing pada skill `docx` (termasuk `merge_runs.py` dan `validate.py`).

Contoh di bawah menunjukkan isi teks per bagian (persis apa yang masuk ke sel KASUS/Ax/Pf/PP/Tx/EDUKASI) — bukan format output; format output-nya tabel docx di atas.

## Contoh isi asli (Cluster Headache, level 3A)

```
KASUS: Cluster Headache (3A)
DD: Tension Headache, Migrain

GEJALA/ANAMNESIS:
Yudi, 25 tahun, bekerja (** bisa pria/wanita 50 tahun)
RPS:
- Nyeri kepala, seluruh kepala, 6 minggu lalu, semakin memburuk
  malam hari, 1 minggu lalu mata mulai berair
- Nyeri hilang timbul, menjalar, nyeri berdenyut, skala nyeri 9
- Keluhan lain: mata kemerahan & keluar air mata (1 minggu yll),
  sudah konsumsi obat warung
RPD: 6 bulan yll pernah mengalami keluhan yang sama, kambuh lagi. Dulu durasi 6 ...

PF:
KU: CM, vital sign dbn
PF Nervus Kranialis -> dbn
Refleks Fisiologis dan Patologis -> dbn
Meningeal sign (-): Kaku kuduk -> dbn, Brudzinski -> dbn, Kernig -> dbn

PP: -

TATA LAKSANA:
R/ Sumatriptan inj 6mg/0,5ml vial No. I
      s.pro. inj. SC

EDUKASI:
- Berhenti merokok dan konsumsi alkohol
- Istirahat yang cukup
```

## Contoh isi asli (BPPV, level 3A — perhatikan algoritma edukasi bernomor)

```
KASUS: BPPV (3A)
DD: Neuritis Vestibular, Meniere's Disease, Vertigo Central, Labirintis

GEJALA/ANAMNESIS:
Rio, 30 tahun, Mahasiswa + Kerja, "Pusing Berputar"
RPS: pusing berputar sejak 3 jam lalu, tiba-tiba, muncul 3 hari sebelum
  berobat, makin kesini makin berat, mual muntah, perut mual, nafsu
  makan menurun
RPD: 6 bulan yll pernah, sembuh sendiri; riwayat opname, operasi, trauma
RPK: -
Lifestyle: sedang skripsi

PF:
KU: sakit sedang, Kesadaran E4V5M6
Vital sign: HR 82x/min, TD 140/70, RR 20x/min, Suhu 37C
Status gizi: TB 170cm, BB 50kg (underweight)
Head: menggunakan kacamata, melihat jauh/dekat kesulitan

PP: (N/A)

TATA LAKSANA:
Vertigo
R/ Betahistine mesylate tab 6mg No. XXI
      s.3.d.d tab I
Antiemetik
R/ Domperidone tab 10mg No. X
      s.p.r.n. 3.d.d tab I

EDUKASI:
Brandt-Daroff Exercises
1. Posisikan badan duduk di kasur dengan kaki di lantai
2. Kemudian, tengok ke kanan sebesar 45 derajat
3. Kepala tetap pada posisi yang sama, kemudian baringkan tubuh ke
   kiri. Tahan posisi selama 30 detik
4. Setelah itu, kembali ke posisi awal. Tahan ...
```
