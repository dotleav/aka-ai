---
name: softfiler
description: >-
  Mengubah isi PDF (terutama yang berisi gambar/scan/slide) atau foto materi kuliah menjadi satu file markdown ("softfile") yang menuliskan ulang isinya secara setia — teks, struktur, tabel, dan deskripsi gambar/diagram — tanpa meringkas atau menambah interpretasi. Ini prompt cepat, bukan pipeline bertahap: gunakan setiap kali pengguna menyebut "softfile", "jadikan softfile", "ubah pdf ini jadi markdown", "tulis ulang isi gambar/slide ini", atau mengunggah PDF/foto materi lalu minta versi teks/markdown-nya, tanpa perlu pengguna menjelaskan panjang lebar caranya.
---

# Softfiler

Catatan desain: dicoba dulu sebagai pipeline hemat token seperti `transkrip` (chunk + patch), tapi untuk PDF/foto tidak diperlukan — sumbernya sudah berupa halaman/gambar diskrit yang bisa dibaca satu-dua kali lewat `view`, bukan teks ASR panjang yang perlu dipotong dan dikoreksi bertahap. Jadi skill ini sengaja ringan: **prompt cepat**, bukan skrip.

## Alur
1. **Baca sumber langsung.** PDF: `view` tiap halaman relevan (pakai `view_range` bila PDF panjang dan hanya sebagian diminta). Foto: `view` gambarnya. Jangan OCR mentah dulu ke teks lalu dibaca lagi — cukup satu kali baca visual per halaman/foto.
2. **Tulis ulang isinya ke markdown, setia ke sumber**:
   - Pertahankan urutan dan struktur asli (heading/subheading materi, urutan poin, urutan tabel).
   - Tabel di sumber → tabel markdown.
   - Diagram/gambar/skema yang tidak bisa jadi teks → deskripsikan singkat dalam `[Gambar: ...]`, cukup untuk konteks, jangan mengarang detail yang tidak terbaca.
   - Rumus/istilah teknis disalin persis, jangan diparafrasa jadi bahasa lain kecuali diminta.
   - Jangan meringkas isi (beda dengan rangkuman di skill `transkrip`) — tujuannya softfile lengkap yang bisa dibaca ulang sebagai pengganti sumber asli, bukan intisari.
3. **Tulis langsung ke satu file** `/mnt/user-data/outputs/<nama>_softfile.md` dengan `create_file` (untuk sumber panjang/multi-halaman, tulis per batch halaman dengan `str_replace`/append, jangan tunggu semua halaman terbaca dulu baru menulis).
4. `present_files`. Balasan akhir singkat (nama file, jumlah halaman/gambar yang diproses) — jangan tempel isi softfile ke chat kecuali diminta.

## Batas
- Bukan alat ringkas — kalau pengguna memang minta ringkasan dari PDF/foto, itu request terpisah (boleh dikerjakan setelah softfile, atau pakai skill rangkuman yang sesuai).
- Halaman/bagian yang tidak terbaca jelas → tandai `[tidak terbaca]`, jangan menebak isinya.
