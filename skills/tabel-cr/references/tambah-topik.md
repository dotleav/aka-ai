# Menambah Topik Baru

Satu topik = satu folder `references/<topik>/` (slug huruf kecil, mis. `kardiologi`, `pediatri`).

Isi minimum (semua opsional kecuali daftar kasus):
- `daftar-kasus.md` — daftar kasus + level kompetensi (SKDI) terverifikasi pengguna. Sumber kebenaran level.
- `<sumber>.pdf` — buku/PPK/guideline utama topik itu.
- `daftar-isi-<sumber>.md` — indeks halaman per kondisi (hemat token, tidak perlu baca ulang PDF).
- `peta-cakupan.md` — kasus mana ada di sumber (+ halaman) vs harus cari manual.

Cara menambah: pengguna kirim sumber → buat folder → susun `daftar-kasus.md` dan indeks halaman → tambahkan baris topik di tabel "Topik tersedia" pada `SKILL.md`.
Topik tanpa folder tetap bisa dikerjakan: SKILL.md mengarahkan ke pencarian manual.
