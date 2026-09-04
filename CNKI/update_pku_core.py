#!/usr/bin/env python3
"""Download and normalize the 2023 PKU Core journal list to CSV.

The source workbook is the public copy linked by Beijing Union University
Library. Parsing uses only the Python standard library so the converter can
run without openpyxl.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


SOURCE_URL = (
    "https://lib.buu.edu.cn/ContentDelivery/20260514/"
    "F1F57D455CD28C5D4E8BB476FFC10CCF_5632DF4F64444D44E871F13F3208E1B7.xlsx"
)
OUTPUT_PATH = Path(__file__).resolve().parent / "PKU_Core_2023.csv"
EXPECTED_COUNT = 1987

MAIN_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def download(url: str = SOURCE_URL) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "wosaide-journal-lists/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in archive.namelist():
        return []
    root = ET.fromstring(archive.read(path))
    values: list[str] = []
    for item in root.findall(MAIN_NS + "si"):
        values.append("".join(node.text or "" for node in item.iter(MAIN_NS + "t")))
    return values


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    kind = cell.attrib.get("t")
    if kind == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(MAIN_NS + "t")).strip()
    value = cell.find(MAIN_NS + "v")
    if value is None:
        return ""
    text = value.text or ""
    if kind == "s":
        text = strings[int(text)]
    return text.strip()


def first_sheet_path(archive: zipfile.ZipFile) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    relation_map = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
    sheets = workbook.find(MAIN_NS + "sheets")
    if sheets is None or not list(sheets):
        raise ValueError("PKU Core workbook does not contain a worksheet")
    first = list(sheets)[0]
    relationship_id = first.attrib[REL_NS + "id"]
    target = relation_map[relationship_id]
    return target if target.startswith("xl/") else "xl/" + target


def parse_workbook(data: bytes) -> list[list[str]]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        strings = shared_strings(archive)
        sheet = ET.fromstring(archive.read(first_sheet_path(archive)))

    sheet_data = sheet.find(MAIN_NS + "sheetData")
    if sheet_data is None:
        raise ValueError("PKU Core worksheet has no sheetData")

    records: list[list[str]] = []
    category = ""
    for row in list(sheet_data)[2:]:  # title row + header row
        values: dict[str, str] = {}
        for cell in row.findall(MAIN_NS + "c"):
            ref = cell.attrib.get("r", "")
            match = re.match(r"[A-Z]+", ref)
            if match:
                values[match.group()] = cell_value(cell, strings)

        if values.get("B"):
            category = values["B"]
        if not values.get("A") or not values.get("C"):
            continue
        if not category:
            raise ValueError(f"Missing category for row {values!r}")

        records.append(
            [
                values["C"],
                category,
                "PKU Core",
                "2023",
                values["A"],
                values.get("D", ""),
            ]
        )

    if len(records) != EXPECTED_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_COUNT} PKU Core journals, parsed {len(records)}"
        )
    return records


def write_csv(records: list[list[str]], output: Path = OUTPUT_PATH) -> None:
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            ["JournalTitle", "Category", "List", "Edition", "OverallRank", "CategoryRank"]
        )
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert the 2023 PKU Core XLSX journal list to CSV."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Use a local XLSX instead of downloading the public source copy.",
    )
    args = parser.parse_args()

    data = args.input.read_bytes() if args.input else download()
    records = parse_workbook(data)
    write_csv(records)
    print(f"Converted {len(records):,} PKU Core journals -> {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
