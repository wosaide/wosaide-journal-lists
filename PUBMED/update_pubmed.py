#!/usr/bin/env python3
"""Download NLM's PubMed journal list and convert it to CSV.

By default this script converts the existing PUBMED/J_Medline.txt file.
Pass --download to fetch the newest official TXT snapshot before converting.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE_URL = "https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt"
BASE_DIR = Path(__file__).resolve().parent
TXT_PATH = BASE_DIR / "J_Medline.txt"
CSV_PATH = BASE_DIR / "J_Medline.csv"

FIELD_MAP = [
    ("JrId", "JrId"),
    ("JournalTitle", "JournalTitle"),
    ("MedAbbr", "MedAbbr"),
    ("ISSN (Print)", "ISSN"),
    ("ISSN (Online)", "EISSN"),
    ("IsoAbbr", "IsoAbbr"),
    ("NlmId", "NlmId"),
]


def download_txt() -> bytes:
    request = Request(
        SOURCE_URL,
        headers={"User-Agent": "wosaide-journal-lists/1.0"},
    )
    with urlopen(request, timeout=60) as response:
        return response.read()


def parse_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}

    def flush() -> None:
        nonlocal current
        if current:
            if not current.get("JrId") or not current.get("JournalTitle"):
                raise ValueError(f"Incomplete PubMed journal record: {current!r}")
            records.append(current)
            current = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("---"):
            flush()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = value.strip()

    flush()
    return records


def write_if_changed(path: Path, data: bytes) -> bool:
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


def convert_txt_to_csv(txt_path: Path = TXT_PATH, csv_path: Path = CSV_PATH) -> int:
    text = txt_path.read_text(encoding="utf-8")
    records = parse_records(text)
    if not records:
        raise ValueError("No PubMed journal records were parsed from J_Medline.txt")

    rows: list[list[str]] = []
    rows.append([csv_name for _, csv_name in FIELD_MAP])
    for record in records:
        rows.append([record.get(source_name, "") for source_name, _ in FIELD_MAP])

    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerows(rows)
    csv_bytes = buffer.getvalue().encode("utf-8-sig")
    write_if_changed(csv_path, csv_bytes)
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert NLM's PubMed J_Medline.txt journal list to CSV."
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the latest official J_Medline.txt before converting.",
    )
    args = parser.parse_args()

    if args.download:
        raw = download_txt()
        write_if_changed(TXT_PATH, raw)
    elif not TXT_PATH.exists():
        parser.error("J_Medline.txt is missing; run again with --download")

    count = convert_txt_to_csv()
    print(f"Converted {count:,} PubMed journal records -> {CSV_PATH.name}")


if __name__ == "__main__":
    main()
