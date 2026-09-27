---
name: transkrip
description: Skill transkrip tunggal dan mandiri. Dari transkrip mentah (ASR/YouTube/rekaman kuliah) yang ditempel atau diunggah, menghasilkan SATU file markdown berisi Rangkuman di atas lalu Transkrip Literal lengkap di bawah. Bila slide (PDF/PPT) ikut dikirim bersama transkrip, slide otomatis dipakai sebagai konteks pencocokan istilah tanpa prompt tambahan. Gunakan setiap kali pengguna menyebut "transkrip", "rangkum transkrip", "perbaiki/rapikan transkrip", "transkrip aka", "transkrip literal", atau menempel/mengunggah transkrip (dengan atau tanpa kata "rangkuman"/"literal"/"slide").
---

# Transkrip

Satu skill, satu hasil: file `_aka.md` = **Bagian 1 Rangkuman** + **Bagian 2 Transkrip Literal**. Tidak ada skill lain yang perlu dipicu. Urutan kerja: koreksi literal dulu, rangkuman dari hasil literal itu, tidak pernah sebaliknya, tidak ada yang dikerjakan dua kali.

**Literal** = isi ucapan utuh dan berurutan; tidak diringkas, tidak diparafrasa, tidak dibenarkan secara isi. Yang diperbaiki hanya artefak ASR. Detail keputusan: `references/aturan-literal.md` (baca hanya bila ragu). `<skill>` = folder skill ini; bila path tak diketahui: `find / -name tk.py -path '*transkrip*' 2>/dev/null | head -1`.

## Alur hemat token
Prinsip: teks penuh **tidak pernah** ditulis ulang Claude bila ada di disk. Skrip mengerjakan bagian mekanis; Claude hanya menulis patch kecil.

1. **Cek** hasil yang sudah ada: `ls /home/claude/tk/*/ /mnt/user-data/outputs/`. Pakai ulang, jangan diulang. Cari input: `ls /mnt/user-data/uploads`. Jangan `view`/cat file utuh.
2. **Slide** (bila ada): ikuti bagian "Konteks slide" di bawah sebelum mengoreksi.
3. **Pra-koreksi otomatis** (0 token output):
   `python3 <skill>/scripts/tk.py prep INPUT --out /home/claude/tk/<slug> --kamus <skill>/references/kamus-asr.tsv`
   Membuang bunyi jeda, menerapkan kamus, merapikan spasi/tanda baca, memecah `chunk_NN.txt` (~1400 kata).
4. **Tiap chunk**: `view` chunk itu, tulis `patch_NN.txt` (format di bawah). Jangan menyalin ulang teks yang sudah benar.
5. **Terapkan**: `python3 <skill>/scripts/tk.py apply DIR DIR/patch_*.txt --isi-saja --out /home/claude/tk/<slug>/literal_isi.md`
   "PATCH DITOLAK" = teks `cari` tidak persis sama dengan chunk; perbaiki baris itu lalu ulang.
6. **Rangkuman**: tulis dari chunk yang sudah dibaca (jangan baca ulang) ke `/home/claude/tk/<slug>/rangkuman.md` memakai template di bawah.
7. **Rakit tanpa menulis ulang**:
   `python3 <skill>/scripts/tk.py aka --judul "<judul>" --ringkasan .../rangkuman.md --literal .../literal_isi.md --sumber "<url/nama file>" --out /mnt/user-data/outputs/<slug>_aka.md`
8. `present_files` hanya untuk `_aka.md`. **Balasan akhir maksimal 4 baris**: nama file, jumlah segmen, jumlah `[tidak jelas]`, jumlah catatan verifikasi (+ "dicocokkan dengan slide" bila ada slide). Jangan menempel isi ke chat.

Jalur pendek: transkrip <600 kata, atau hanya ada di chat/konteks dan tidak ada file di disk, tulis literal langsung ke file (tanpa `prep`), lalu langkah 6-8. Sesi terputus: `ls DIR`, lanjutkan dari patch terakhir.

## Konteks slide (otomatis, tanpa prompt tambahan)
Bila ada file slide (`.pdf`/`.pptx`/`.ppt` di `/mnt/user-data/uploads` atau berupa dokumen konteks) di samping transkrip, langsung pakai; jangan bertanya, jangan tunggu diminta.
1. **Ekstrak hemat token**: `pdftotext -layout FILE /home/claude/tk/<slug>/slide.txt` (pptx: `python-pptx`, teks saja). Jangan render gambar kecuali teks kosong/scan.
2. **Glosarium**: dari slide.txt ambil judul, istilah medis/teknis, singkatan, nama dosen/tokoh/obat, angka penting; tulis `glosarium.txt` (satu baris per istilah). Pakai untuk patch `R` (mis. "Profon" -> nama dosen di slide, "pen generator" -> "pain generator").
3. **Batas**: slide hanya untuk mencocokkan ejaan istilah, nama, singkatan, angka ambigu. Jangan menambah isi slide ke Literal. Bila ucapan berbeda dari slide, ucapan **dipertahankan** dan selisih dicatat lewat `?`.
4. **Rangkuman**: boleh memakai slide untuk melengkapi urutan topik dan tabel istilah (tandai "slide"); selisih ucapan vs slide masuk "Perlu Dicek". `Sumber:` menyebut transkrip + slide.
5. Tanpa slide, lewati bagian ini.

## Format patch (satu perintah per baris)
```
R|00:05|mantum tes|Mantoux tes
R||teks salah|teks benar
S|38:28|Teks lengkap baru untuk segmen ini.
?|37:12|Catatan verifikasi: dosen menyebut X, padahal secara medis Y.
# baris berawalan # diabaikan
```
- `R|waktu|cari|ganti`: ganti kata/frasa di satu segmen (utama, paling murah). Waktu kosong = seluruh dokumen; hanya bila pasti aman.
- `S|waktu|teks`: tulis ulang satu segmen; hanya bila >25% rusak, usahakan <10% dari seluruh segmen.
- `?|waktu|catatan`: masuk "Catatan verifikasi" di akhir file.
- Teks tak terbaca: `[tidak jelas]`, jangan mengarang. Karakter `|` tidak boleh ada di `cari`/`ganti`.

## Template rangkuman
Panjang default ~10% kata sumber (min 200, maks 900); "singkat" 5%, "detail" 15% (maks 1500). Ikuti permintaan pengguna bila menyebut panjang/gaya.
```
# Rangkuman: {judul}
Sumber: {url/nama file} · Durasi: {mm:ss}

## Inti
3-5 kalimat: topik, tujuan, kesimpulan utama.

## Poin Utama
### {Topik 1} (mm:ss-mm:ss)
- poin padat, satu gagasan per baris

## Istilah, Angka & Definisi Penting
Tabel (istilah | keterangan | waktu) bila >4 item; jika tidak, daftar pendek.

## Perlu Dicek
Kekeliruan/keraguan pembicara, selisih dengan slide, [tidak jelas] yang memengaruhi isi. Hapus bila kosong.

## Administratif
Pengumuman, jadwal, tugas (1-3 baris). Hapus bila kosong.
```
Aturan rangkuman: setia pada sumber, tidak menambah fakta dari luar. Kekeliruan pembicara ditulis apa adanya + "(sesuai ucapan; perlu dicek)". Buang basa-basi/doa. Bahasa mengikuti sumber; angka, dosis, usia, nama persis. "Titik Ujian" (maks. 8 poin yang ditekankan pembicara) hanya bila diminta.

## Batas keras (literal)
- Jangan meringkas, menggabung, mengurutkan ulang, atau menambah kalimat.
- Kekeliruan isi pembicara dipertahankan dan dicatat lewat `?`, tidak diam-diam dibetulkan.
- Koreksi hanya bila yakin; bila tidak, biarkan atau `[tidak jelas]`.
- Kamus baru yang sering muncul boleh ditambah ke `references/kamus-asr.tsv` (regex, TAB, pengganti).

## Struktur hasil
```
# {Judul} — Transkrip Aka
Sumber: ...
## Bagian 1 — Rangkuman
### Inti / Poin Utama / ...
---
## Bagian 2 — Transkrip Literal
**(mm:ss)** teks ...   (tanpa penanda waktu: paragraf biasa)
### Catatan verifikasi
```
