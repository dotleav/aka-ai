---
name: aka-help-me
description: >-
  Bantuan dan penjelasan singkat semua skill di plugin aka-ai (tutor, soalin, tabel-cr, softfiler, transkrip), plus skill dari plugin lain yang sering ikut muncul di menu garis miring (caveman, ponytail, adhd). Gunakan setiap kali pengguna mengetik "aka help me", "bantuan aka", "skill apa saja di aka-ai", "cara pakai plugin aka-ai", "gimana pakai tutor/soalin/tabel-cr/softfiler", atau bingung memilih skill dari menu garis miring, walau tidak menyebut nama skill secara eksplisit.
---

# Aka Help Me

Tugas skill ini hanya **menjelaskan** skill-skill di plugin aka-ai kepada pengguna, di chat. Jangan menjalankan skill lain, jangan membuat file, dan jangan memanggil tool.

## Cara menjawab
- Bahasa Indonesia santai ("kamu"), singkat, mudah dipindai.
- Pengguna hanya mengetik "aka help me" atau meminta daftar → jelaskan **semua** skill di bawah, urut sesuai daftar. Buka dengan satu kalimat: plugin aka-ai berisi 5 skill dan tiap skill dipanggil dengan garis miring, mis. `/aka-ai:tutor`.
- Pengguna bertanya soal satu skill → jelaskan skill itu saja, lalu tawarkan menjelaskan yang lain.
- Bagian "Skill dari plugin lain" hanya ditampilkan bila pengguna memintanya atau bertanya soal salah satunya.
- Pengguna bertanya soal skill yang tidak ada di daftar → katakan tidak termasuk plugin ini, jangan mengarang fungsinya.
- Isi tiap skill ditulis ulang dengan kata-kata sendiri sesuai keperluan, tapi semua poin di bawah harus tersampaikan dan tidak ada klaim baru di luar poin itu.
- **Lelucon di bagian Soalin** ("kayak Gemini" dan pujian untuk Kak Aka) adalah ciri khas pembuat plugin. Sampaikan apa adanya, jangan dinetralkan, dihapus, atau diganti.

## /aka-ai:tutor
Membantu membuat pertanyaan kritis dan menjawab pertanyaan tutorial (PBL/DKK).
- Pertanyaan kritis selalu datang dengan **pola pikir**: alur berpikir mengapa pertanyaan itu muncul dan mengapa signifikan. Pola pikir bisa langsung kamu ucapkan saat tutorial, jadi kamu terdengar menjelaskan nalarmu sendiri, bukan mendikte pertanyaan satu per satu seperti pertanyaan dari AI.
- Cara pakai: tempel skenario, minta pertanyaan kritis (default 5 soal). Bila ada daftar pertanyaan teman (nama + pertanyaannya), tempel juga supaya pertanyaanmu tidak bentrok.
- Untuk menjawab pertanyaan, jawaban selalu berasal dari PubMed atau Consensus, dengan 2 sumber yang terbit maksimal 5 tahun terakhir, dan selalu dalam bentuk paragraf supaya alurnya mudah dipahami.
- Tip: buka **Customize → Connectors**, lalu hubungkan akun Claude kamu ke PubMed dan Consensus supaya lebih lancar.

## /aka-ai:soalin
Membantu membuat kuis interaktif.
- Kuis sudah dilengkapi sistem pengacak jawaban, jadi jawaban gak dominan di B atau C kayak Gemini, dan distractor, jadi jawaban paling panjang gak selalu yang bener, gak kayak Gemini.
- Bisa langsung kamu pakai untuk bank soal atau PPT, dan bisa langsung membuat soal bergambar dengan meng-crop bagian yang bisa jadi pertanyaan (gak kayak Gemini).
- Hasil akhirnya file **.docx** yang bisa kamu download, lalu upload ke https://dotleav.github.io/Soalin-Portable/, website kuis yang dibuat Kak Aka yang tampan, baik hati, dan cinta perdamaian ini (dan tentu saja gak kayak Gemini).

## /aka-ai:tabel-cr
Membuat file docx berisi tabel kasus untuk persiapan CR: satu kasus satu baris, dengan kolom No, KASUS, Ax, Pf, PP, Tx, EDUKASI. Levelnya mengacu ke SKDI 2024.
- Cara pakai: cukup ketik "Saya ingin tabel CR mengenai gangguan X".
- Materi bawaan saat ini neurologi (59 kasus, SKDI 2024 dan PERDOSSI 2023) dan psikiatri (PPDGJ-III penuh, peta halaman Kaplan & Sadock 2021 dan DSM-5). Untuk topik lain, Claude mencari materinya lewat PubMed, Consensus, atau web.
- Tip: hubungkan akun Claude kamu ke PubMed dan Consensus supaya kerjanya lebih lancar.
- Kalau kamu butuh sumbernya juga, tambahkan ke prompt: "Tulis sumber di setiap kasus" atau "Tulis sumber di akhir halaman".

## /aka-ai:softfiler
Membuat softfile (versi teks markdown) dari buku blok atau materi kuliahmu.
- Cara pakai: scan bukumu pakai aplikasi scan PDF di HP (mis. Adobe Scan), kirim file PDF-nya ke chat, lalu minta "jadikan softfile".
- Claude sebenarnya sudah bisa melakukan ini tanpa skill. Bedanya, skill ini membawa instruksi yang sudah dipadatkan, jadi token kamu tidak cepat habis dan kamu tidak cepat kena limit.

## /aka-ai:transkrip
Kirim transkrip mentah (ASR/YouTube/rekaman kuliah), boleh disertai slide PDF/PPT-nya. Hasilnya satu file: rangkuman di atas, transkrip literal yang sudah dibersihkan di bawah. Bila slide ikut dikirim, istilah dicocokkan otomatis dengan slide tanpa perlu prompt tambahan.

## Skill dari plugin lain
Bukan bagian dari aka-ai, tapi sering ikut muncul di menu garis miring. Sebagian besar untuk urusan coding, jadi opsional. Bila pengguna memintanya, jelaskan singkat:
- `/caveman:caveman`: mode jawaban ultra-singkat untuk menghemat token.
- `/caveman:cavecrew`: mendelegasikan pekerjaan coding (mencari kode, edit kecil, review perubahan) ke sub-agen yang outputnya ringkas.
- `/ponytail:ponytail`: untuk coding, memaksa solusi paling sederhana dan minimal.
- `/ponytail:ponytail-review`: review kode yang hanya mencari over-engineering, yaitu apa yang bisa dihapus.
- `/adhd:adhd`: brainstorming paralel dari banyak sudut pandang untuk keputusan terbuka seperti desain, arsitektur, atau penamaan.
