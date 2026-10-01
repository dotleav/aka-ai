# Pola "Soal Minites" (soal kasus klinis MCQ)

Dipakai saat pengguna memakai trigger **"Soal minites"**. Sumber pola: bank `Minites 1 - 2H` (30 soal neurologi, vignette klinis ala UKMPPD/OSCE FK).

## ATURAN UTAMA (baca dulu)

- Contoh di bawah = **sampel gaya**, BUKAN template yang disalin. Jangan tiru kalimat, nama pasien, angka, atau pasangan diagnosis-distraktor yang sama persis.
- **Jangan tiru posisi/urutan** dari bank sumber: nomor soal bergambar, nomor soal kasus, dan nomor soal non-kasus di bank sumber hanyalah kebetulan. Tentukan sendiri sebaran per bank baru (soal bergambar diperbanyak bila relevan dengan materi; sebagian kecil soal boleh pendek tanpa vignette panjang).
- Topik/skenario selalu diambil dari materi pengguna, bukan dari contoh.
- Tetap ikuti Soalin Format Spec di SKILL.md (A-E, `Kunci:`, `Penjelasan:`, sebaran kunci merata, `references/kualitas-opsi.md`).

## Ciri pola (diamati dari bank sumber)

1. **Vignette satu paragraf**, diakhiri SATU kalimat tanya. Urutan isi: identitas (Ny./Tn./An./"Seorang laki-laki ... tahun") + tempat (UGD/puskesmas/poli) → keluhan utama + onset → ciri khas gejala/pencetus → riwayat penting (RPD, pekerjaan, obat, trauma) → tanda vital bila relevan → temuan pemeriksaan kunci. Panjang bervariasi: 1-2 kalimat (soal pendek) sampai 6-8 kalimat.
2. **Nama pasien** fiktif dan sering "nyeleneh" (Tn. Kejut, Tn. Mercury, Tn. Wakwaw); sebagian tanpa nama ("Seorang perempuan berusia 24 tahun").
3. **Petunjuk bertingkat**: jawaban jarang langsung disebut; pasien harus mengenali diagnosis dulu, baru menjawab langkah berikutnya (diagnosis → tes/terapi/patomekanisme/lokasi lesi).
4. **Variasi pertanyaan** (jangan semua "diagnosis"): diagnosis, tatalaksana/terapi abortif, pemeriksaan penunjang terbaik, pemeriksaan fisik lanjutan, patomekanisme, lokasi lesi, neurotransmitter, stadium penyakit, temuan cairan LP, jenis nyeri, tingkat kesadaran, nama kelainan.
5. **Distraktor** = diagnosis banding / pilihan yang sekelas dan masuk akal (Erb vs Klumpke; TTH vs migren vs cluster; MRI vs CT vs foto polos). Panjang dan bentuk opsi seragam; opsi pendek (satu istilah) atau pola gabungan "Diagnosis, terapi" bila ingin menguji dua langkah.
6. **Penjelasan 2-4 kalimat**: (a) kunci klinis → diagnosis, (b) mengapa kunci benar, (c) mengapa 1-2 distraktor terpenting salah. Tanpa menyebut huruf opsi.
7. **Gambar: dibanyakkan bila relevan untuk pembelajaran** (bank sumber hanya sedikit bergambar, itu BUKAN patokan). Topik yang pada praktiknya dikenali lewat visual (CT/MRI, EKG, histologi, apusan, anatomi, lesi kulit, funduskopi, dll.) sebaiknya diberi gambar sebagai bagian dari petunjuk klinis. Satu gambar per soal, slot `[GAMBAR: ...]` di bawah soal dan di atas opsi A; daftar gambar yang dibutuhkan diserahkan ke pengguna di akhir batch.

## Contoh sampel gaya (ringkas, bukan untuk disalin)

**Contoh 1 — tatalaksana, petunjuk bertingkat (CT sign → stroke iskemik → terapi)**

Ny. Fahria, 55 tahun, datang diantar keluarga dengan keluhan kelemahan pada anggota gerak. Keluhan dirasakan saat pasien bangun tidur. Riwayat darah tinggi dan DM tidak diketahui. Kesadaran compos mentis, TD 160/90 mmHg, Nadi 82x/menit, RR 18x/menit. Kekuatan motorik ekstremitas kanan 3/3, ekstremitas kiri 5/5. Pada pemeriksaan CT scan didapatkan Sylvian fissure sign atau hyperdense MCA dot sign. Apakah penatalaksanaan yang tepat untuk pasien ini?
A. Methylprednisolone 30 mg/kgBB bolus IV / B. Nicardipin 2-10 mcg/kgBB/menit IV / C. Terapi trombolitik dengan r-TPA / D. Konsul bedah saraf cito / E. Manitol 20% 0.5-1 gram/kgBB IV — Kunci: C
Penjelasan: Hemiparesis mendadak dengan hyperdense MCA dot sign dan Sylvian fissure sign menunjukkan trombus akut pada arteri serebri media, yaitu stroke iskemik. Tatalaksana reperfusi pada stroke iskemik akut adalah trombolisis dengan r-tPA bila tidak ada kontraindikasi. Nicardipin, manitol, dan kortikosteroid bukan terapi utama, sedangkan bedah saraf tidak diperlukan karena tidak ada perdarahan atau massa.

**Contoh 2 — diagnosis + terapi digabung dalam opsi**

Ny. Geni, 34 tahun, datang dengan keluhan nyeri kepala di kedua sisi disertai kekakuan leher. Nyeri kepala terasa mengikat, namun tidak disertai keluhan neurologis lainnya. Pasien mengaku masih bisa beraktivitas seperti biasa, namun keluhan ini sering muncul saat menghadapi tenggat waktu pekerjaan di kantor. Apakah diagnosis dan terapi abortif yang tepat pada pasien ini?
A. Migraine, amitriptyline / B. Migraine, sumatriptan / C. Cluster headache, oksigen 100% / D. TTH, ibuprofen / E. TTH, propranolol — Kunci: D
Penjelasan: Nyeri kepala bilateral, seperti diikat, intensitas ringan-sedang, dipicu stres, dan tidak memburuk dengan aktivitas merupakan tension type headache (TTH). Terapi abortifnya adalah analgesik sederhana seperti parasetamol atau NSAID misalnya ibuprofen. Propranolol dan amitriptilin adalah terapi profilaksis, bukan abortif.

**Contoh 3 — pemeriksaan (langkah berikutnya), pasien tanpa nama**

Ny. Lani, 36 tahun, datang ke praktik dokter umum dengan keluhan pusing berputar sejak 1 hari yang lalu. Keluhan semakin memberat bila pasien menoleh ke kiri, disertai mual dan muntah. Keluhan terutama terjadi saat pasien ingin tidur atau baru saja bangun tidur. Setahun lalu pernah mengalami keluhan serupa, namun sembuh dalam 1 minggu. Hasil pemeriksaan telinga dan pendengaran normal. Pemeriksaan apa yang harus dilakukan?
A. Tes Mini-Mental State / B. Tes kalori / C. Dix-Hallpike maneuver / D. Doll's eye maneuver / E. Epley maneuver — Kunci: C
Penjelasan: Vertigo yang dicetuskan perubahan posisi kepala, singkat, berulang, dengan pendengaran normal mengarah ke BPPV. Pemeriksaan untuk menegakkan diagnosis adalah manuver Dix-Hallpike. Manuver Epley adalah terapi, bukan pemeriksaan diagnostik.

**Contoh 4 — diagnosis banding sekelas (Erb vs Klumpke)**

An. Panji, 8 bulan, dibawa ke poli dengan keluhan bahwa tangan kanan memiliki posisi abnormal. Riwayat lahir sungsang dan lengan tertinggal. Pada pemeriksaan fisik, didapatkan pada lengan kanan: posisi lengan atas bergerak normal, lengan bawah fleksi, dorsum tangan fleksi, dan claw hand. Apakah diagnosis yang paling mungkin?
A. Erb's palsy / B. Palsi nervus radialis / C. Palsi pleksus brakialis total / D. Klumpke's palsy / E. Carpal tunnel syndrome — Kunci: D
Penjelasan: Klumpke's palsy melibatkan akar saraf C8-T1 sehingga otot intrinsik tangan lumpuh dan timbul claw hand, sedangkan gerak lengan atas masih normal. Erb's palsy (C5-C6) justru mengenai lengan atas dengan posisi waiter's tip. Palsi total akan melumpuhkan seluruh ekstremitas atas.

**Contoh 5 — soal pendek (vignette 2 kalimat)**

Ny. Wati, 39 tahun, datang dengan keluhan pusing berputar dan telinga berdenging. Pada pemeriksaan fisik ditemukan tuli sensorineural. Apakah diagnosis yang paling tepat?
A. Neuritis vestibularis / B. Meniere's disease / C. Benign Paroxysmal Positional Vertigo / D. Labirintitis / E. Vertigo sentral — Kunci: B
Penjelasan: Trias vertigo, tinitus, dan tuli sensorineural fluktuatif adalah gambaran khas penyakit Meniere akibat hidrops endolimfatik. BPPV dan neuritis vestibularis tidak menimbulkan gangguan pendengaran.

**Contoh 6 — patomekanisme / konsep di balik kasus**

Ny. Gempi, usia 60 tahun, datang ke UGD dengan keluhan nyeri kepala kiri sejak 5 jam yang lalu. Nyeri dirasakan seperti berdenyut. Pasien juga mengeluhkan mual, muntah dan silau jika terkena cahaya. Pemeriksaan fisik dan tanda vital dalam batas normal. Bagaimana patomekanisme penyakit di atas?
(opsi: kombinasi vasodilatasi/vasokonstriksi × intrakranial/ekstrakranial + peningkatan TIK)
Penjelasan: model: sebut diagnosis dari gejala, jelaskan mekanisme benar, lalu bedakan dari opsi kembar yang terbalik.

## Checklist sebelum menyerahkan bank Soal minites

- Tidak ada soal yang kalimat/nama/angkanya menyalin contoh di atas.
- Jenis pertanyaan bervariasi (tidak semua "diagnosis").
- Panjang vignette bervariasi; soal pendek dibolehkan.
- Distraktor sekelas; opsi seragam bentuk & panjang.
- Sebaran huruf kunci merata; jalankan `audit_options.py audit`.
- Posisi soal bergambar/kasus/non-kasus ditentukan oleh kebutuhan materi, bukan meniru bank sumber.
- Soal bergambar sudah dibanyakkan untuk topik yang relevan secara visual, dan daftar gambar dilampirkan.
