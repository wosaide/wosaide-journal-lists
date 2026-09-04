# Chinese core journal lists: PKU Core and CSSCI

This directory stores Chinese journal-classification lists used by WOS Aide
for title matching and classification labels.

> **Naming note:** the files are kept under `CNKI/` because this is the app's
> Chinese-journal source group. **PKU Core and CSSCI are not CNKI lists.**
> PKU Core is associated with Peking University Library's *A Guide to the Core
> Journals of China* (《中文核心期刊要目总览》), while CSSCI is developed by
> Nanjing University's Chinese Social Sciences Research Evaluation Center.

## Current files

| File | List | Edition | Records |
| --- | --- | --- | ---: |
| `PKU_Core_2023.csv` | 中文核心期刊要目总览（北大核心） | 2023 | 1,987 |
| `CSSCI_2025_2026.csv` | CSSCI 来源期刊 | 2025–2026 | 674 |
| `CSSCI_Extended_2025_2026.csv` | CSSCI 扩展版来源期刊 | 2025–2026 | 261 |

## Beijing Union University download page

The public download/reference page supplied for these snapshots is:

https://lib.buu.edu.cn/Home/ServiceDetail/23948?utm_source=chatgpt.com

It currently links the following files:

### PKU Core 2023 XLSX

https://lib.buu.edu.cn/ContentDelivery/20260514/F1F57D455CD28C5D4E8BB476FFC10CCF_5632DF4F64444D44E871F13F3208E1B7.xlsx

### CSSCI source journals 2025–2026 PDF

https://lib.buu.edu.cn/ContentDelivery/20260514/689CE46C4DF28D15B7671032392F3A8B_33D7EB81FD5772E9EF3C3D21F6E6217A.pdf

### CSSCI extended journals 2025–2026 PDF

https://lib.buu.edu.cn/ContentDelivery/20260514/F731CDB0985AF0453652432625BBE1D0_0D0E6ACE0509FE8CFE5ADD5AE2C49D16.pdf

## PKU Core conversion

The source XLSX has four logical columns: overall sequence, category, journal
title, and sequence within category. Category cells are merged in the workbook,
so `update_pku_core.py` forward-fills the category before writing the normalized
CSV.

Regenerate the CSV directly from the public XLSX:

```bash
python3 CNKI/update_pku_core.py
```

Or convert a manually downloaded workbook:

```bash
python3 CNKI/update_pku_core.py --input /path/to/pku-core-2023.xlsx
```

The normalized columns are:

`JournalTitle, Category, List, Edition, OverallRank, CategoryRank`

## CSSCI normalization and PDF watermarks

The Beijing Union University CSSCI PDFs contain dense institutional/reference
watermarks. Those PDF files are **not stored or redistributed in this
repository, and the repository does not publish altered/de-watermarked copies**.
Only the journal-table fields are normalized into CSV for matching. Watermark
strings and page-decoration text are excluded from the datasets.

The CSSCI CSV columns are:

`JournalTitle, Discipline, List, Edition, Rank`

The current normalized lists have been checked against the 2025–2026 directory
counts: 674 CSSCI source journals and 261 CSSCI extended journals.

## Publisher / maintainer references

- Peking University Library Core Journal project:
  http://hxqk.lib.pku.edu.cn/
- Nanjing University Chinese Social Sciences Research Evaluation Center:
  https://cssrac.nju.edu.cn/
- CNKI Journal Navigation (separate database/navigation service):
  https://navi.cnki.net/knavi/journals/index

These datasets are maintained as identification/matching aids. Always consult
the relevant publisher/evaluation organization and its current terms when an
official classification decision is required.

