# WOS Aide Bar journal-list sources

This repository contains small, optional journal-title lists that WOS Aide Bar
can download and parse on demand. The app also accepts user-selected CSV files.

## Published lists

- `utd24.csv` contains the 24 journal titles displayed by the University of
  Texas at Dallas for its Top 100 Business School Research Rankings.
- `FT50.csv` contains the Financial Times journal list announced on
  April 29, 2026.

Each CSV deliberately contains journal titles and source attribution only. It
does not contain articles, abstracts, metrics, publisher addresses, or a copy
of a commercial journal database.

## Web of Science Core Collection lists

SCIE, SSCI, AHCI, and ESCI exports downloaded from Clarivate may be kept beside
these files for local development, but they are excluded by `.gitignore`.
Clarivate describes the Master Journal List as free to browse and permits
account holders to download collection lists; that does not by itself establish
permission to republish the exported datasets in a public repository.

WOS Aide Bar therefore does not bundle or publicly mirror those exports.
People who want Core Collection autocomplete can download the current CSV files
from Clarivate and import them locally in the app.

The Academic Journal Guide 2024 export is likewise not mirrored here. People
who are entitled to use that file can import their local CSV into WOS Aide Bar.

## Source attribution

- UTD Top 100 journal list:
  https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/
- Financial Times 2026 list:
  https://www.ft.com/content/db863a0a-6524-45f9-bc52-fee997634bdc
- Clarivate Master Journal List downloads:
  https://mjl.clarivate.com/collection-list-downloads

The lists are provided for identification and interoperability. Financial
Times, FT, University of Texas at Dallas, Web of Science, and Clarivate are
marks of their respective owners. This project is independent and is not
affiliated with or endorsed by those organizations.
