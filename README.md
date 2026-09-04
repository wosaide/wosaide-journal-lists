# WOS Aide journal-list sources

This repository contains optional journal/source lists used by WOS Aide for
title completion, source identification, and more accurate journal matching.
The data is organized by provider so additional title lists can be added or
refreshed without mixing unrelated schemas.

The files contain publication metadata only. They do not contain article full
text or article content.

## Directory layout

| Directory | Contents | Source documentation |
| --- | --- | --- |
| `WOS/` | SCIE, SSCI, AHCI, ESCI journal lists | [`WOS/README.md`](WOS/README.md) |
| `SCOPUS/` | Scopus source-title and book-title lists | [`SCOPUS/README.md`](SCOPUS/README.md) |
| `SD/` | ScienceDirect active journals and all books | [`SD/README.md`](SD/README.md) |
| `CNKI/` | Reserved for CNKI journal-list snapshots | [`CNKI/README.md`](CNKI/README.md) |
| `LIST/` | AJG 2024, UTD24, FT50 curated lists | [`LIST/README.md`](LIST/README.md) |

Each directory README records the official source/download address for the
files in that directory. Prefer those provider-specific READMEs when updating
a snapshot because direct asset URLs can change between releases.

## Current files

### Web of Science

- `WOS/SCIE.csv` — Science Citation Index Expanded
- `WOS/SSCI.csv` — Social Sciences Citation Index
- `WOS/AHCI.csv` — Arts & Humanities Citation Index
- `WOS/ESCI.csv` — Emerging Sources Citation Index

The Web of Science snapshots were refreshed from Clarivate's Master Journal
List Collection List Downloads in August 2026. The four files represent Web
of Science Core Collection journal lists and are separate from Clarivate's
"Additional Web of Science Indexes" downloads.

### Scopus

- `SCOPUS/ext_list_Jul_2026.xlsx` — Scopus source-title list
- `SCOPUS/Scopus_book_list_Q2.xlsx` — Scopus book-title list

### ScienceDirect

- `SD/jnlactive.xlsx` — active ScienceDirect journal titles
- `SD/allbooks.xlsx` — all ScienceDirect book titles

### Curated lists

- `LIST/AJG2024.csv` — Academic Journal Guide 2024
- `LIST/UTD24.csv` — UT Dallas 24-journal set
- `LIST/FT50.csv` — Financial Times business-school research journal list

## Main official source pages

- Clarivate Master Journal List downloads:
  https://mjl.clarivate.com/collection-list-downloads
- Scopus content/title-list downloads:
  https://www.elsevier.com/products/scopus/content
- ScienceDirect journals/title lists:
  https://www.elsevier.com/products/sciencedirect/journals
- ScienceDirect books/title lists:
  https://www.elsevier.com/products/sciencedirect/books
- CNKI Journal Navigation:
  https://navi.cnki.net/knavi/journals/index
- Academic Journal Guide 2024:
  https://charteredabs.org/academic-journal-guide/academic-journal-guide-2024
- Academic Journal Guide 2024 methodology:
  https://assets.charteredabs.org/ajg-2024-methodology.pdf
- UT Dallas Top 100 journal/ranking source:
  https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/
- Financial Times 2026 source:
  https://www.ft.com/content/db863a0a-6524-45f9-bc52-fee997634bdc

## App usage

WOS Aide can map enabled matching sources to the corresponding files in this
repository. A source can be downloaded or refreshed independently, allowing
users to control which journal lists participate in matching while keeping the
source-specific datasets maintainable and extensible.

## Attribution

The source lists remain associated with their respective publishers and
organizations. Web of Science and Clarivate, Scopus, ScienceDirect and
Elsevier, CNKI, Academic Journal Guide and Chartered ABS, Financial Times, and
The University of Texas at Dallas are marks/names of their respective owners.
This repository is independent and is not affiliated with or endorsed by
those organizations.
