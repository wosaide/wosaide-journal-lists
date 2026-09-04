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
| `SCOPUS/` | Scopus source-title list | [`SCOPUS/README.md`](SCOPUS/README.md) |
| `SD/` | ScienceDirect active journals and all books | [`SD/README.md`](SD/README.md) |
| `PUBMED/` | NLM list of journals cited in PubMed | [`PUBMED/README.md`](PUBMED/README.md) |
| `EI/` | Ei Compendex serial/source list | [`EI/README.md`](EI/README.md) |
| `CNKI/` | PKU Core 2023 and CSSCI 2025–2026 journal lists | [`CNKI/README.md`](CNKI/README.md) |
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

- `SCOPUS/ext_list_Jul_2026.csv` — Scopus source-title list, converted from
  Elsevier's official July 2026 XLSX download

The previously tracked `SCOPUS/Scopus_book_list_Q2.xlsx` file has been
removed. The current Scopus source in this repository is limited to the
source-title list used for journal/source matching.

### ScienceDirect

- `SD/jnlactive.csv` — active ScienceDirect journal titles, converted from the
  official XLSX title list
- `SD/allbooks.csv` — all ScienceDirect book titles, converted from the
  official XLSX title list

The former XLSX copies are no longer tracked in this repository; the CSV files
are the maintained application-facing snapshots.

### PubMed

- `PUBMED/J_Medline.txt` — official NLM List of All Journals Cited in PubMed
- `PUBMED/J_Medline.csv` — generated CSV used for journal/source matching
- `PUBMED/update_pubmed.py` — downloads the latest TXT and converts it to CSV

The PubMed CSV is generated from the official NLM text file and contains
`JrId`, journal title and abbreviation fields, print/online ISSNs, ISO
abbreviation, and NLM ID. A scheduled GitHub Actions workflow checks for NLM
updates daily and commits a new TXT/CSV snapshot only when the source changes.

### Ei Compendex

- `EI/compendex_journals.csv` — journal-only Ei Compendex list (`Source Type =
  Journal`) used for journal matching
- `EI/compendex_serials.csv` — complete `SERIALS` worksheet from Elsevier's
  official Compendex Source List, converted to CSV
- `EI/source_url.txt` — exact official XLSX URL used for the current snapshot
- `EI/update_compendex.py` — resolves the current source list and converts it

The current August 2026 snapshot contains 4,613 `Journal` rows in the official
`SERIALS` worksheet. Book series and trade journals remain available in the
complete serials CSV but are excluded from `compendex_journals.csv`.

### Chinese core journal classifications

- `CNKI/PKU_Core_2023.csv` — 1,987 journals from the 2023 edition of
  《中文核心期刊要目总览》 (PKU Core)
- `CNKI/CSSCI_2025_2026.csv` — 674 CSSCI source journals for 2025–2026
- `CNKI/CSSCI_Extended_2025_2026.csv` — 261 CSSCI extended source journals
  for 2025–2026
- `CNKI/update_pku_core.py` — downloads and converts the public PKU Core XLSX

These files are grouped under `CNKI/` for WOS Aide's Chinese-journal matching
workflow. PKU Core and CSSCI are independent evaluation/indexing systems and
are not published by CNKI. The source CSSCI PDFs are not tracked because the
reference copies contain institutional watermarks; only normalized table data
is stored here.

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
- NLM List of All Journals Cited in PubMed:
  https://www.nlm.nih.gov/bsd/serfile_addedinfo.html
- NLM PubMed journal-list TXT:
  https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt
- Elsevier Engineering Village — Compendex:
  https://www.elsevier.com/products/engineering-village/databases/compendex
- Beijing Union University core-journal download/reference page:
  https://lib.buu.edu.cn/Home/ServiceDetail/23948?utm_source=chatgpt.com
- Peking University Library Core Journal project:
  http://hxqk.lib.pku.edu.cn/
- Nanjing University Chinese Social Sciences Research Evaluation Center:
  https://cssrac.nju.edu.cn/
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
organizations. Web of Science and Clarivate, Scopus, ScienceDirect,
Engineering Village, Compendex and Elsevier, CNKI, Peking University Library,
Nanjing University and CSSCI, Academic Journal Guide and Chartered ABS,
Financial Times, and The University of Texas at Dallas are marks/names of
their respective owners.
This repository is independent and is not affiliated with or endorsed by
those organizations.
