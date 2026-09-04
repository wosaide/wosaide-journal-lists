# Scopus source list

This directory stores the Scopus source-title snapshot used for journal and
source matching. The repository keeps the data as CSV for simpler parsing in
WOS Aide.

## Files and download addresses

### `ext_list_Jul_2026.csv`

Scopus source-title list, including active/inactive status, ISSN/EISSN,
coverage, source type, publisher, ASJC classifications, and related metadata.

The CSV in this repository was converted from Elsevier's official July 2026
XLSX source-title list. The official download is currently provided as XLSX;
there is no separate official CSV download for this snapshot.

- Official content/download page:
  https://www.elsevier.com/products/scopus/content
- Official XLSX used to produce the current CSV snapshot:
  https://downloads.ctfassets.net/o78em1y1w4i4/7xtaTxNiNcWRTeZkV86eNy/8df9934a6138c7e15817214c098deaf2/ext_list_Jul_2026.xlsx

## Removed files

`Scopus_book_list_Q2.xlsx` is no longer stored in this repository. The current
Scopus dataset is intentionally limited to the source-title list used for
journal/source matching.

Elsevier updates the Scopus source information regularly. Direct asset URLs
are versioned and may change. When refreshing, obtain the newest source list
from the official content page, convert the required data to CSV, and update
both the snapshot and this README.
