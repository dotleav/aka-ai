# Kualitas Opsi — Kunci Tidak Boleh Bisa Ditebak dari Bentuknya

Tujuan: siswa yang tidak tahu materi tidak boleh bisa menang dengan menebak pola.

## Pola yang harus dihilangkan
| Pola | Perbaikan |
|---|---|
| Kunci paling panjang | Panjang lima opsi setara (selisih ≤ ±25%). Perpanjang distraktor dengan detail yang sama spesifiknya, atau ringkas kunci. |
| Hanya kunci yang diperjelas "( )" atau ", yaitu ..." | Beri semua opsi bentuk yang sama, atau tidak ada yang berkurung. Pindahkan penjelas ke Penjelasan. |
| Kunci paling spesifik/teknis, distraktor umum | Distraktor setingkat: istilah sama-sama baku, sama-sama spesifik. |
| Distraktor pakai "selalu/tidak pernah/semua/hanya" | Ganti dengan pernyataan bernuansa yang sama bentuknya dengan kunci. |
| Kunci memuat kata dari batang soal | Distraktor juga memakai kata dari batang soal. |
| Dua distraktor hampir kembar, satu berbeda (=kunci) | Buat kunci punya "saudara" yang sama dekatnya, atau samakan jarak antar opsi. |
| Kunci di tengah/huruf itu-itu saja | Jalankan `audit_options.py shuffle`. Target tiap huruf ≈ 20%, tanpa 3 kunci huruf sama berturut-turut. |
| "Semua benar"/"tidak ada" selalu jadi kunci | Jadikan sesekali distraktor, atau hindari format ini. |

## Cara menulis ulang
1. Tulis kunci dulu, lalu ukur panjang dan bentuknya.
2. Bentuk distraktor dari salah kaprah nyata (struktur mirip, mekanisme terbalik, lateralisasi tertukar, penyakit serupa), bukan opsi yang jelas salah.
3. Satu jawaban benar saja; verifikasi distraktor benar-benar salah.
4. Opsi numerik: urutkan naik, jangan diacak.
5. Jangan mengubah makna soal, kunci, atau fakta; ubah hanya bentuk. Bila Kunci berubah huruf, sesuaikan Penjelasan yang menyebut huruf.
6. Opsi berbahasa Indonesia; istilah Latin/Inggris baku boleh.

## Target sebelum diserahkan
- Kunci = opsi terpanjang di ≤ ~30% soal.
- Rasio panjang kunci/distraktor ≈ 1.0 (0.85–1.15).
- Chi-square distribusi kunci ≤ 9.49.
- Tidak ada soal dengan kunci satu-satunya yang berkurung.
