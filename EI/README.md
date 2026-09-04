# Ei Compendex source list

This directory stores journal/serial data from the **SERIALS** worksheet in
Elsevier's official Compendex Source List as CSV for WOS Aide matching.

## Official source

Compendex is an Elsevier Engineering Village database. Its official product
page provides a **View source list** XLSX download.

- Official Compendex page:
  https://www.elsevier.com/products/engineering-village/databases/compendex
- Current resolved XLSX URL:
  see [`source_url.txt`](source_url.txt)

The direct asset URL is versioned by Elsevier and can change when a new source
list is published, so the updater resolves the current link from the official
product page rather than hard-coding a release URL.

## Files

- `compendex_journals.csv` — journal-only CSV for EI/Compendex journal matching.
- `compendex_serials.csv` — complete CSV generated from the official `SERIALS`
  sheet, including journals, trade journals, and book series.
- `source_url.txt` — exact official XLSX asset URL used for the current CSV.
- `update_compendex.py` — downloader and XLSX-to-CSV converter.

For the current August 2026 source list, the `SERIALS` worksheet contains
4,613 rows with `Source Type = Journal`, 179 `Trade Journal` rows, and 1,059
`Book Series` rows. `compendex_journals.csv` contains only the 4,613 `Journal`
rows so it can be used as the EI/Compendex journal list without treating book
series or trade journals as scholarly journals.

The official workbook also contains separate non-serial and discontinued
source sheets. Those sheets are not included in the journal-only CSV.

## Update manually

Run:

```bash
python3 EI/update_compendex.py
```

The script uses only the Python standard library. It:

1. opens Elsevier's official Compendex product page;
2. resolves the current Compendex Source List XLSX link;
3. downloads the workbook in memory;
4. reads the `SERIALS` worksheet directly from the XLSX XML package;
5. writes both the complete serials CSV and the `Journal`-only CSV;
6. records the resolved source URL.

## Automatic updates

`.github/workflows/update-compendex.yml` checks the official source weekly and
commits new CSV/source URL files only when the generated content changes. It
can also be run manually from GitHub Actions.
