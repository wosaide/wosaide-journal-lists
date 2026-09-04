# PubMed journal list

This directory stores the NLM journal list used for PubMed journal/source
matching in WOS Aide.

## Official source

NLM publishes **List of All Journals Cited in PubMed** as `J_Medline.txt`.
Despite the historical filename, this list is not limited to currently indexed
MEDLINE journals; it is the journal list cited in PubMed.

- NLM description:
  https://www.nlm.nih.gov/bsd/serfile_addedinfo.html
- Official TXT download:
  https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt

## Files

- `J_Medline.txt` — unmodified official NLM source snapshot.
- `J_Medline.csv` — application-facing CSV generated from the TXT file.
- `update_pubmed.py` — downloader and deterministic TXT-to-CSV converter.

The generated CSV contains these columns:

`JrId, JournalTitle, MedAbbr, ISSN, EISSN, IsoAbbr, NlmId`

`ISSN` comes from NLM's `ISSN (Print)` field and `EISSN` comes from
`ISSN (Online)`.

## Update manually

Download the newest official TXT and regenerate the CSV in one command:

```bash
python3 PUBMED/update_pubmed.py --download
```

If `J_Medline.txt` has already been replaced manually, regenerate only the CSV:

```bash
python3 PUBMED/update_pubmed.py
```

The converter uses only the Python standard library and writes the CSV in
UTF-8 with BOM for broad spreadsheet/application compatibility.

## Automatic updates

The repository workflow `.github/workflows/update-pubmed.yml` checks the NLM
source daily. It downloads the latest TXT, regenerates the CSV, and commits the
two files only when the resulting repository content has changed. The workflow
can also be started manually from GitHub Actions.

NLM updates this source independently, so the exact journal count can change
between snapshots.
