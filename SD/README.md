# ScienceDirect title lists

This directory stores ScienceDirect journal and book title-list snapshots used
for source matching. The repository keeps the data as CSV for simpler parsing
in WOS Aide.

## Files and download addresses

### `jnlactive.csv`

Active journal titles available on ScienceDirect.

The repository CSV was converted from Elsevier's official XLSX title list.

- Official journals/title-list page:
  https://www.elsevier.com/products/sciencedirect/journals
- Official XLSX used to produce the CSV snapshot:
  https://legacyfileshare.elsevier.com/promis_misc/sd-content/journals/jnlactive.xlsx

### `allbooks.csv`

All book titles available on ScienceDirect.

The repository CSV was converted from Elsevier's official XLSX title list.

- Official books/title-list page:
  https://www.elsevier.com/products/sciencedirect/books
- Official XLSX used to produce the CSV snapshot:
  https://legacyfileshare.elsevier.com/promis_misc/sd-content/books/allbooks.xlsx

Elsevier updates these title lists over time. Use the official product pages
to confirm the latest lists before replacing the repository snapshots, then
convert the required data to CSV before committing it here.
