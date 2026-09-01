# WOS Aide Bar journal-list sources

This repository contains optional journal-list CSV sources that WOS Aide Bar
can download and parse on demand. The app also accepts user-selected CSV files
for the same supported collections.

## Available lists

- `SCIE.csv`, `SSCI.csv`, `AHCI.csv`, and `ESCI.csv` provide the corresponding
  Web of Science Core Collection journal-list data used by journal completion.
- `AJG2024.csv` provides the Academic Journal Guide 2024 journal-list data and
  rating field used by the app's optional AJG source.
- `UTD24.csv` contains the 24 journal titles displayed by the University of
  Texas at Dallas for its Top 100 Business School Research Rankings.
- `FT50.csv` contains the Financial Times journal list announced on
  April 29, 2026.

The files contain journal-list metadata used for title completion, matching,
and journal details. They do not contain article full text or article content.

## Web of Science data snapshot

The `SCIE.csv`, `SSCI.csv`, `AHCI.csv`, and `ESCI.csv` files were refreshed
from Clarivate's Collection List Downloads on August 17, 2026.

On that download page, **Additional Web of Science Indexes** is a separate
section and was also shown as **Last Updated: August 17, 2026**. The four files
above represent Web of Science Core Collection journal lists; they should not
be interpreted as mirrors of the separate Additional Web of Science Indexes
downloads.

## App usage

WOS Aide Bar maps each supported collection to its corresponding file in this
repository. A list is downloaded only when the user chooses to install or
refresh it. The downloaded data is validated and then stored locally for
journal completion. Users can also replace a source with a compatible CSV
selected from disk.

## Source attribution

- UTD Top 100 journal list:
  https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/
- Financial Times 2026 list:
  https://www.ft.com/content/db863a0a-6524-45f9-bc52-fee997634bdc
- Clarivate Master Journal List downloads:
  https://mjl.clarivate.com/collection-list-downloads
- Academic Journal Guide 2024 methodology:
  https://assets.charteredabs.org/ajg-2024-methodology.pdf

The lists are provided for identification and interoperability. Financial
Times, FT, University of Texas at Dallas, Web of Science, and Clarivate are
marks of their respective owners. This project is independent and is not
affiliated with or endorsed by those organizations.
