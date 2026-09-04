#!/usr/bin/env python3
"""Download Elsevier's current Compendex source list and convert SERIALS to CSV."""

from __future__ import annotations

import csv
import html
import re
import sys
from io import BytesIO, StringIO
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from zipfile import ZipFile


BASE_DIR = Path(__file__).resolve().parent
SERIALS_CSV_PATH = BASE_DIR / "compendex_serials.csv"
JOURNALS_CSV_PATH = BASE_DIR / "compendex_journals.csv"
SOURCE_URL_PATH = BASE_DIR / "source_url.txt"

PRODUCT_PAGE = (
    "https://www.elsevier.com/products/engineering-village/databases/compendex"
)

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "wosaide-journal-lists/1.0"})
    with urlopen(request, timeout=90) as response:
        return response.read()


def find_current_xlsx_url() -> str:
    page = fetch(PRODUCT_PAGE).decode("utf-8", "replace")
    page = html.unescape(page).replace("\\u002F", "/")

    candidates = re.findall(
        r"(?:https?:)?//[^\"'<>\s]+\.xlsx(?:\?[^\"'<>\s]*)?",
        page,
        flags=re.IGNORECASE,
    )
    candidates += re.findall(
        r"href=[\"']([^\"']+\.xlsx(?:\?[^\"']*)?)[\"']",
        page,
        flags=re.IGNORECASE,
    )

    normalized: list[str] = []
    for candidate in candidates:
        candidate = candidate.replace("\\/", "/")
        if candidate.startswith("//"):
            candidate = "https:" + candidate
        candidate = urljoin(PRODUCT_PAGE, candidate)
        if "compendex" in candidate.lower():
            normalized.append(candidate)

    if not normalized:
        raise RuntimeError(
            "Could not find the Compendex XLSX link on Elsevier's product page"
        )

    # Prefer links explicitly named as a source list, then the first Compendex XLSX.
    normalized.sort(key=lambda u: ("source" not in u.lower(), u))
    return normalized[0]


def column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref.upper())
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def shared_strings(book: ZipFile) -> list[str]:
    name = "xl/sharedStrings.xml"
    if name not in book.namelist():
        return []
    root = ET.fromstring(book.read(name))
    result: list[str] = []
    for item in root.findall(f"{{{MAIN_NS}}}si"):
        result.append(
            "".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t"))
        )
    return result


def worksheet_path(book: ZipFile, wanted_name: str) -> str:
    workbook = ET.fromstring(book.read("xl/workbook.xml"))
    relationships = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
    targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in relationships.findall(f"{{{PKG_REL_NS}}}Relationship")
    }

    for sheet in workbook.findall(f".//{{{MAIN_NS}}}sheet"):
        if sheet.attrib.get("name", "").strip().upper() != wanted_name.upper():
            continue
        rel_id = sheet.attrib[f"{{{REL_NS}}}id"]
        target = targets[rel_id].lstrip("/")
        return target if target.startswith("xl/") else f"xl/{target}"

    available = [
        sheet.attrib.get("name", "")
        for sheet in workbook.findall(f".//{{{MAIN_NS}}}sheet")
    ]
    raise RuntimeError(f"Worksheet {wanted_name!r} not found; available: {available}")


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(
            node.text or "" for node in cell.iter(f"{{{MAIN_NS}}}t")
        )

    value = cell.find(f"{{{MAIN_NS}}}v")
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        return strings[int(value.text)]
    if cell_type == "b":
        return "TRUE" if value.text == "1" else "FALSE"
    return value.text


def serial_rows(xlsx: bytes) -> list[list[str]]:
    with ZipFile(BytesIO(xlsx)) as book:
        strings = shared_strings(book)
        sheet = ET.fromstring(book.read(worksheet_path(book, "SERIALS")))

    rows: list[list[str]] = []
    for row in sheet.findall(f".//{{{MAIN_NS}}}sheetData/{{{MAIN_NS}}}row"):
        values: dict[int, str] = {}
        for cell in row.findall(f"{{{MAIN_NS}}}c"):
            index = column_index(cell.attrib.get("r", "A1"))
            values[index] = cell_value(cell, strings)
        if not values:
            continue
        width = max(values) + 1
        rendered = [values.get(index, "") for index in range(width)]
        while rendered and rendered[-1] == "":
            rendered.pop()
        if rendered:
            rows.append(rendered)

    if not rows:
        raise RuntimeError("No rows were found in the Compendex SERIALS worksheet")

    header_index = next(
        (
            index
            for index, row in enumerate(rows)
            if "Source title" in row and "Source Type" in row
        ),
        None,
    )
    if header_index is None:
        raise RuntimeError("Could not identify the SERIALS column header row")
    return rows[header_index:]


def journal_rows(rows: list[list[str]]) -> list[list[str]]:
    header = rows[0]
    try:
        type_index = header.index("Source Type")
    except ValueError as exc:
        raise RuntimeError("SERIALS data has no Source Type column") from exc

    journals = [
        row
        for row in rows[1:]
        if len(row) > type_index and row[type_index].strip().casefold() == "journal"
    ]
    return [header, *journals]


def csv_bytes(rows: list[list[str]]) -> bytes:
    output = StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def write_if_changed(path: Path, data: bytes) -> bool:
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


def main() -> None:
    source_url = find_current_xlsx_url()
    xlsx = fetch(source_url)
    serials = serial_rows(xlsx)
    journals = journal_rows(serials)

    serials_changed = write_if_changed(SERIALS_CSV_PATH, csv_bytes(serials))
    journals_changed = write_if_changed(JOURNALS_CSV_PATH, csv_bytes(journals))
    source_changed = write_if_changed(
        SOURCE_URL_PATH, (source_url + "\n").encode("utf-8")
    )

    print(f"Compendex source: {source_url}")
    print(
        f"Converted {len(serials) - 1:,} serials -> {SERIALS_CSV_PATH.name}; "
        f"{len(journals) - 1:,} journals -> {JOURNALS_CSV_PATH.name}"
    )
    print(
        "Changed: "
        f"serials={serials_changed}, journals={journals_changed}, "
        f"source_url={source_changed}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
