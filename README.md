# aka-ai-plugin

Plugin Claude Code berisi 6 skill untuk kebutuhan koas kedokteran (UKDW): tutorial PBL, bank soal, tabel kasus OSCE, konversi materi ke markdown, dan rapikan transkrip kuliah.

## Instalasi

```
/plugin marketplace add <owner>/<repo>
/plugin install aka-ai-plugin
```

Atau untuk pengembangan lokal:

```
claude --plugin-dir /path/ke/aka-ai-plugin
```

## Skill yang tersedia

| Skill | Fungsi |
|---|---|
| `aka-help-me` | Menjelaskan skill-skill di plugin ini saat pengguna bingung/minta bantuan memilih. |
| `soalin` | Membuat & memperbaiki bank soal kuis medis format docx (termasuk soal isian/essay). |
| `softfiler` | Mengubah PDF/foto materi kuliah jadi satu file markdown yang setia ke sumber. |
| `tabel-cr` | Membuat tabel kasus (CR) untuk OSCE/CBT — satu kasus per baris, docx. |
| `transkrip` | Merapikan transkrip kuliah mentah jadi ringkasan + transkrip literal. |
| `tutor` | Bantu sesi tutorial PBL/DKK: bikin pertanyaan kritis & jawab pertanyaan runtut. |

Detail trigger & cara kerja tiap skill ada di `skills/<nama-skill>/SKILL.md` masing-masing.

## Struktur

```
aka-ai-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── aka-help-me/
│   ├── soalin/
│   ├── softfiler/
│   ├── tabel-cr/
│   ├── transkrip/
│   └── tutor/
└── README.md
```

## Update versi

Naikkan field `version` (semver) di `.claude-plugin/plugin.json` tiap kali ada perubahan yang ingin dibedakan.
