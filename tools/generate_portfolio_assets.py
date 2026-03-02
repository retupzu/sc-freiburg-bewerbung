from __future__ import annotations

import csv
import math
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape
import zipfile


ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = ROOT / "downloads"


DATA = [
    {"date": "2026-01-18", "matchday": "Yes", "category": "Trikots", "sessions": 1650, "orders": 96, "revenue": 8640, "returns": 4},
    {"date": "2026-01-18", "matchday": "Yes", "category": "Accessories", "sessions": 1240, "orders": 73, "revenue": 3285, "returns": 3},
    {"date": "2026-01-18", "matchday": "Yes", "category": "Kids", "sessions": 710, "orders": 31, "revenue": 1240, "returns": 1},
    {"date": "2026-01-22", "matchday": "No", "category": "Trikots", "sessions": 940, "orders": 39, "revenue": 3510, "returns": 2},
    {"date": "2026-01-22", "matchday": "No", "category": "Accessories", "sessions": 780, "orders": 28, "revenue": 1260, "returns": 1},
    {"date": "2026-01-22", "matchday": "No", "category": "Kids", "sessions": 420, "orders": 16, "revenue": 640, "returns": 1},
    {"date": "2026-01-26", "matchday": "No", "category": "Trikots", "sessions": 1080, "orders": 47, "revenue": 4230, "returns": 2},
    {"date": "2026-01-26", "matchday": "No", "category": "Accessories", "sessions": 860, "orders": 30, "revenue": 1350, "returns": 1},
    {"date": "2026-01-26", "matchday": "No", "category": "Kids", "sessions": 515, "orders": 19, "revenue": 760, "returns": 1},
    {"date": "2026-02-01", "matchday": "Yes", "category": "Trikots", "sessions": 1725, "orders": 102, "revenue": 9180, "returns": 5},
    {"date": "2026-02-01", "matchday": "Yes", "category": "Accessories", "sessions": 1330, "orders": 77, "revenue": 3465, "returns": 3},
    {"date": "2026-02-01", "matchday": "Yes", "category": "Kids", "sessions": 760, "orders": 34, "revenue": 1360, "returns": 2},
    {"date": "2026-02-06", "matchday": "No", "category": "Trikots", "sessions": 990, "orders": 43, "revenue": 3870, "returns": 2},
    {"date": "2026-02-06", "matchday": "No", "category": "Accessories", "sessions": 810, "orders": 29, "revenue": 1305, "returns": 1},
    {"date": "2026-02-06", "matchday": "No", "category": "Kids", "sessions": 470, "orders": 17, "revenue": 680, "returns": 1},
    {"date": "2026-02-15", "matchday": "Yes", "category": "Trikots", "sessions": 1840, "orders": 110, "revenue": 9900, "returns": 5},
    {"date": "2026-02-15", "matchday": "Yes", "category": "Accessories", "sessions": 1405, "orders": 82, "revenue": 3690, "returns": 4},
    {"date": "2026-02-15", "matchday": "Yes", "category": "Kids", "sessions": 820, "orders": 38, "revenue": 1520, "returns": 2},
]


def euro(value: float) -> str:
    return f"{value:,.0f} EUR".replace(",", ".")


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def compute_summary() -> dict[str, object]:
    total_sessions = sum(row["sessions"] for row in DATA)
    total_orders = sum(row["orders"] for row in DATA)
    total_revenue = sum(row["revenue"] for row in DATA)
    total_returns = sum(row["returns"] for row in DATA)

    conversion = total_orders / total_sessions
    aov = total_revenue / total_orders
    return_rate = total_returns / total_orders

    revenue_by_category: dict[str, int] = {}
    revenue_by_day: dict[str, int] = {}
    matchday_revenue = 0
    non_matchday_revenue = 0

    for row in DATA:
        revenue_by_category[row["category"]] = revenue_by_category.get(row["category"], 0) + row["revenue"]
        revenue_by_day[row["date"]] = revenue_by_day.get(row["date"], 0) + row["revenue"]
        if row["matchday"] == "Yes":
            matchday_revenue += row["revenue"]
        else:
            non_matchday_revenue += row["revenue"]

    return {
        "sessions": total_sessions,
        "orders": total_orders,
        "revenue": total_revenue,
        "returns": total_returns,
        "conversion": conversion,
        "aov": aov,
        "return_rate": return_rate,
        "revenue_by_category": revenue_by_category,
        "revenue_by_day": revenue_by_day,
        "matchday_revenue": matchday_revenue,
        "non_matchday_revenue": non_matchday_revenue,
    }


SUMMARY = compute_summary()


def write_csv() -> None:
    DOWNLOADS.mkdir(exist_ok=True)
    target = DOWNLOADS / "scf_ecommerce_daily_data.csv"
    headers = ["date", "matchday", "category", "sessions", "orders", "revenue", "returns"]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, headers)
        writer.writeheader()
        writer.writerows(DATA)


def cell_reference(row: int, column: int) -> str:
    letters = ""
    index = column
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return f"{letters}{row}"


def text_cell(ref: str, value: str) -> str:
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'


def number_cell(ref: str, value: float) -> str:
    if math.isclose(value, round(value)):
        shown = str(int(round(value)))
    else:
        shown = f"{value:.4f}".rstrip("0").rstrip(".")
    return f'<c r="{ref}"><v>{shown}</v></c>'


def build_sheet(rows: list[list[object]]) -> str:
    row_xml: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        cells: list[str] = []
        for col_index, value in enumerate(row, start=1):
            ref = cell_reference(row_index, col_index)
            if isinstance(value, (int, float)):
                cells.append(number_cell(ref, float(value)))
            else:
                cells.append(text_cell(ref, str(value)))
        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    dimension = f"A1:{cell_reference(len(rows), max(len(row) for row in rows))}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        '</worksheet>'
    )


def write_xlsx() -> None:
    data_rows: list[list[object]] = [["Date", "Matchday", "Category", "Sessions", "Orders", "Revenue", "Returns"]]
    for row in DATA:
        data_rows.append([
            row["date"],
            row["matchday"],
            row["category"],
            row["sessions"],
            row["orders"],
            row["revenue"],
            row["returns"],
        ])

    dashboard_rows: list[list[object]] = [
        ["SCF Ecommerce KPI Dashboard", "", ""],
        ["Metric", "Value", "Note"],
        ["Revenue", SUMMARY["revenue"], "Total sample revenue"],
        ["Orders", SUMMARY["orders"], "Total orders"],
        ["Sessions", SUMMARY["sessions"], "Traffic"],
        ["AOV", round(float(SUMMARY["aov"]), 2), "Average order value"],
        ["Conversion", round(float(SUMMARY["conversion"]) * 100, 2), "Percent"],
        ["Return rate", round(float(SUMMARY["return_rate"]) * 100, 2), "Percent"],
        ["Matchday revenue", SUMMARY["matchday_revenue"], "Home game days"],
        ["Non-matchday revenue", SUMMARY["non_matchday_revenue"], "Regular days"],
        ["", "", ""],
        ["Category", "Revenue", ""],
    ]
    for category, revenue in SUMMARY["revenue_by_category"].items():
        dashboard_rows.append([category, revenue, ""])

    dashboard_rows.extend([
        ["", "", ""],
        ["Date", "Revenue", ""],
    ])
    for day, revenue in SUMMARY["revenue_by_day"].items():
        dashboard_rows.append([day, revenue, ""])

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets>'
        '<sheet name="DailyData" sheetId="1" r:id="rId1"/>'
        '<sheet name="Dashboard" sheetId="2" r:id="rId2"/>'
        '</sheets>'
        '</workbook>'
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>'
    )
    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )
    package_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    )
    core_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>SCF Ecommerce Portfolio Excel Pack</dc:title>'
        '<dc:creator>Codex</dc:creator>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{date.today().isoformat()}T00:00:00Z</dcterms:created>'
        '</cp:coreProperties>'
    )
    app_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Codex</Application>'
        '</Properties>'
    )

    target = DOWNLOADS / "SCF_Ecommerce_Portfolio_ExcelPack.xlsx"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", package_rels)
        archive.writestr("docProps/core.xml", core_xml)
        archive.writestr("docProps/app.xml", app_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/styles.xml", styles_xml)
        archive.writestr("xl/worksheets/sheet1.xml", build_sheet(data_rows))
        archive.writestr("xl/worksheets/sheet2.xml", build_sheet(dashboard_rows))


def pdf_stream() -> bytes:
    revenue_by_category = SUMMARY["revenue_by_category"]
    revenue_by_day = SUMMARY["revenue_by_day"]

    lines = [
        "q",
        "0.07 0.07 0.07 rg",
        "36 740 523 56 re f",
        "Q",
        "BT /F1 24 Tf 48 774 Td (SCF Ecommerce KPI Dashboard) Tj ET",
        "BT /F1 11 Tf 48 752 Td (Revenue, orders, AOV, conversion, return rate and matchday comparison.) Tj ET",
        "0.72 0.12 0.14 rg",
        "48 676 116 52 re f",
        "168 676 116 52 re f",
        "288 676 116 52 re f",
        "408 676 116 52 re f",
        "0 0 0 rg",
        f"BT /F1 10 Tf 60 710 Td (Revenue) Tj ET",
        f"BT /F1 17 Tf 60 690 Td ({euro(float(SUMMARY['revenue']))}) Tj ET",
        f"BT /F1 10 Tf 180 710 Td (Orders) Tj ET",
        f"BT /F1 17 Tf 180 690 Td ({int(SUMMARY['orders'])}) Tj ET",
        f"BT /F1 10 Tf 300 710 Td (AOV) Tj ET",
        f"BT /F1 17 Tf 300 690 Td ({euro(float(SUMMARY['aov']))}) Tj ET",
        f"BT /F1 10 Tf 420 710 Td (Conversion) Tj ET",
        f"BT /F1 17 Tf 420 690 Td ({pct(float(SUMMARY['conversion']))}) Tj ET",
        "BT /F1 13 Tf 48 648 Td (Category revenue) Tj ET",
    ]

    y = 626
    for category, value in revenue_by_category.items():
        lines.append(f"BT /F1 11 Tf 56 {y} Td ({category}) Tj ET")
        lines.append(f"BT /F1 11 Tf 180 {y} Td ({euro(float(value))}) Tj ET")
        y -= 20

    lines.extend([
        "BT /F1 13 Tf 310 648 Td (Revenue by date) Tj ET",
    ])

    y = 626
    for day, value in revenue_by_day.items():
        lines.append(f"BT /F1 11 Tf 318 {y} Td ({day}) Tj ET")
        lines.append(f"BT /F1 11 Tf 418 {y} Td ({euro(float(value))}) Tj ET")
        y -= 20

    lines.extend([
        "BT /F1 13 Tf 48 490 Td (Matchday comparison) Tj ET",
        f"BT /F1 11 Tf 56 468 Td (Matchday revenue: {euro(float(SUMMARY['matchday_revenue']))}) Tj ET",
        f"BT /F1 11 Tf 56 448 Td (Non-matchday revenue: {euro(float(SUMMARY['non_matchday_revenue']))}) Tj ET",
        f"BT /F1 11 Tf 56 428 Td (Return rate: {pct(float(SUMMARY['return_rate']))}) Tj ET",
        "BT /F1 10 Tf 48 82 Td (Created for the application portfolio website. Sample data for presentation purposes.) Tj ET",
    ])

    return "\n".join(lines).encode("ascii")


def write_pdf() -> None:
    content = pdf_stream()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF\n"
        ).encode("ascii")
    )

    (DOWNLOADS / "SCF_Ecommerce_KPI_Dashboard.pdf").write_bytes(pdf)


def main() -> None:
    write_csv()
    write_xlsx()
    write_pdf()


if __name__ == "__main__":
    main()
