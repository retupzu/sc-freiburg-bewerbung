from __future__ import annotations

import csv
import math
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = ROOT / "downloads"
WEBSITE_URL = "https://retupzu.github.io/sc-freiburg-bewerbung/"


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


def ascii_safe(value: str) -> str:
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
        "·": "-",
        "–": "-",
        "—": "-",
        "’": "'",
        "“": '"',
        "”": '"',
    }
    return "".join(replacements.get(char, char if ord(char) < 128 else "") for char in value)


def escape_pdf(value: str) -> str:
    return ascii_safe(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def pdf_text(x: int, y: int, text: str, *, size: int = 11, font: str = "F1") -> str:
    return f"BT /{font} {size} Tf {x} {y} Td ({escape_pdf(text)}) Tj ET"


def pdf_fill(x: int, y: int, width: int, height: int, *, rgb: tuple[float, float, float]) -> str:
    red, green, blue = rgb
    return f"{red:.2f} {green:.2f} {blue:.2f} rg\n{x} {y} {width} {height} re f"


def build_pdf(pages: list[bytes]) -> bytes:
    page_count = len(pages)
    catalog_id = 1
    pages_id = 2
    regular_font_id = 3
    bold_font_id = 4
    page_ids = [5 + index for index in range(page_count)]
    content_ids = [5 + page_count + index for index in range(page_count)]

    objects: dict[int, bytes] = {
        catalog_id: f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii"),
        pages_id: (
            f"<< /Type /Pages /Count {page_count} /Kids [{' '.join(f'{page_id} 0 R' for page_id in page_ids)}] >>"
        ).encode("ascii"),
        regular_font_id: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        bold_font_id: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    }

    for index, content in enumerate(pages):
        page_id = page_ids[index]
        content_id = content_ids[index]
        objects[page_id] = (
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {regular_font_id} 0 R /F2 {bold_font_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")
        objects[content_id] = b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream"

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for object_id in range(1, max(objects) + 1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_id} 0 obj\n".encode("ascii"))
        pdf.extend(objects[object_id])
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {max(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {max(objects) + 1} /Root {catalog_id} 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)


def kpi_pdf_stream() -> bytes:
    revenue_by_category = SUMMARY["revenue_by_category"]
    revenue_by_day = SUMMARY["revenue_by_day"]

    lines = [
        "q",
        pdf_fill(36, 744, 523, 56, rgb=(0.05, 0.05, 0.05)),
        "Q",
        pdf_text(48, 772, "KPI Dashboard Uebersicht", size=24, font="F2"),
        pdf_text(48, 752, "Bewerbungsprojekt zu Umsatz, AOV, Conversion, Retourenquote und Matchday-Effekt.", size=11),
        pdf_fill(48, 676, 116, 52, rgb=(0.72, 0.12, 0.14)),
        pdf_fill(168, 676, 116, 52, rgb=(0.72, 0.12, 0.14)),
        pdf_fill(288, 676, 116, 52, rgb=(0.72, 0.12, 0.14)),
        pdf_fill(408, 676, 116, 52, rgb=(0.72, 0.12, 0.14)),
        pdf_text(60, 710, "Revenue", size=10),
        pdf_text(60, 690, euro(float(SUMMARY["revenue"])), size=17, font="F2"),
        pdf_text(180, 710, "Orders", size=10),
        pdf_text(180, 690, str(int(SUMMARY["orders"])), size=17, font="F2"),
        pdf_text(300, 710, "AOV", size=10),
        pdf_text(300, 690, euro(float(SUMMARY["aov"])), size=17, font="F2"),
        pdf_text(420, 710, "Conversion", size=10),
        pdf_text(420, 690, pct(float(SUMMARY["conversion"])), size=17, font="F2"),
        pdf_text(48, 648, "Umsatz nach Kategorie", size=13, font="F2"),
        pdf_text(310, 648, "Umsatz nach Datum", size=13, font="F2"),
    ]

    y = 626
    for category, value in revenue_by_category.items():
        lines.append(pdf_text(56, y, category, size=11))
        lines.append(pdf_text(180, y, euro(float(value)), size=11, font="F2"))
        y -= 20

    y = 626
    for day, value in revenue_by_day.items():
        lines.append(pdf_text(318, y, day, size=11))
        lines.append(pdf_text(418, y, euro(float(value)), size=11, font="F2"))
        y -= 20

    lines.extend([
        pdf_text(48, 490, "Matchday Vergleich", size=13, font="F2"),
        pdf_text(56, 468, f"Matchday revenue: {euro(float(SUMMARY['matchday_revenue']))}", size=11),
        pdf_text(56, 448, f"Non-matchday revenue: {euro(float(SUMMARY['non_matchday_revenue']))}", size=11),
        pdf_text(56, 428, f"Return rate: {pct(float(SUMMARY['return_rate']))}", size=11),
        pdf_text(48, 82, "Erstellt fuer die Bewerbungswebsite. Beispielwerte fuer ein E-Commerce-Reporting-Projekt.", size=10),
    ])
    return "\n".join(lines).encode("ascii")


def kpi_pdf_insights_stream() -> bytes:
    lines = [
        "q",
        pdf_fill(36, 744, 523, 56, rgb=(0.05, 0.05, 0.05)),
        "Q",
        pdf_text(48, 772, "KPI Dashboard - Insights & Ableitungen", size=22, font="F2"),
        pdf_text(48, 752, "Die zweite Seite macht aus Kennzahlen konkrete Shop-Empfehlungen.", size=11),
        pdf_text(48, 712, "1. Kategorie-Fokus", size=14, font="F2"),
        pdf_text(48, 692, "Trikots sind die mit Abstand staerkste Kategorie und sollten auf Startseite,", size=11),
        pdf_text(48, 676, "Landingpages und Matchday-Aktionsflaechen noch staerker priorisiert werden.", size=11),
        pdf_text(48, 638, "2. Matchday-Effekt", size=14, font="F2"),
        pdf_text(48, 618, "Der Umsatzsprung an Heimspieltagen spricht fuer klar getimte Angebote,", size=11),
        pdf_text(48, 602, "Bundling, Hero-Produkte und mehr Sichtbarkeit am Spieltag.", size=11),
        pdf_text(48, 564, "3. Conversion & Warenkorbwert", size=14, font="F2"),
        pdf_text(48, 544, "Mit solider Conversion und gutem AOV lohnen sich Cross-Selling und Zubehör", size=11),
        pdf_text(48, 528, "wie Schals, Caps oder Geschenkartikel als Add-on-Produkte.", size=11),
        pdf_text(48, 490, "4. Service & Datenqualitaet", size=14, font="F2"),
        pdf_text(48, 470, "Auch bei guter Performance bleiben Produktdaten und Retourenquote wichtige", size=11),
        pdf_text(48, 454, "Hebel fuer ein professionelles Shop-Setup.", size=11),
        pdf_text(48, 416, "Nutzen fuer die Bewerbung", size=14, font="F2"),
        pdf_text(48, 396, "Das Projekt zeigt nicht nur Zahlenverstaendnis, sondern auch die Faehigkeit,", size=11),
        pdf_text(48, 380, "Shop-Entscheidungen aus Reporting strukturiert abzuleiten.", size=11),
        pdf_text(48, 82, "Seite 2 ergaenzt die Uebersicht um operative Prioritaeten fuer E-Commerce-Teams.", size=10),
    ]
    return "\n".join(lines).encode("ascii")


def resume_pdf_stream() -> bytes:
    lines = [
        "q",
        pdf_fill(36, 756, 523, 50, rgb=(0.05, 0.05, 0.05)),
        pdf_fill(36, 734, 523, 6, rgb=(0.72, 0.12, 0.14)),
        "Q",
        pdf_text(48, 781, "Kassem Jaffal", size=25, font="F2"),
        pdf_text(48, 761, "Bewerbung fuer die Ausbildung Kaufmann im E-Commerce", size=11),
        pdf_text(48, 718, "Freiburg im Breisgau | 0174 9683772 | Hassan1.jaffal1@outlook.de", size=10),
        pdf_text(48, 702, f"Website und Portfolio: {WEBSITE_URL}", size=10),
        pdf_text(48, 670, "Kurzprofil", size=14, font="F2"),
        pdf_text(48, 652, "Digital affiner Bewerber mit technischem Hintergrund, strukturierter Arbeitsweise", size=10),
        pdf_text(48, 638, "und grossem Interesse an Onlinehandel, Shop-Systemen, Produktdarstellung und Daten.", size=10),
        pdf_text(48, 624, "Private Projekte zu digitalen Brands, Social Media Marketing und Funnel-Ideen", size=10),
        pdf_text(48, 610, "haben mein Verstaendnis fuer E-Commerce, Angebotslogik und Zielgruppen weiter vertieft.", size=10),
        pdf_text(48, 580, "Schulbildung", size=14, font="F2"),
        pdf_text(48, 562, "07/2025 | Abitur | Wentzinger Gymnasium, Freiburg", size=10),
        pdf_text(48, 532, "Praktische Erfahrung", size=14, font="F2"),
        pdf_text(48, 514, "09/2022 | Praktikum bei Bechtle AG", size=10, font="F2"),
        pdf_text(48, 500, "Einblicke in technische Prozesse, systematisches Arbeiten und strukturierte Umsetzung.", size=10),
        pdf_text(48, 482, "2023 | Soziales Praktikum im Kindergarten St. Elisabeth, Stuehlinger", size=10, font="F2"),
        pdf_text(48, 468, "Staerkung von Teamfaehigkeit, Kommunikation, Verlaesslichkeit und Verantwortungsbewusstsein.", size=10),
        pdf_text(48, 450, "Laufend | Private E-Commerce- und Marketing-Projekte", size=10, font="F2"),
        pdf_text(48, 436, "Beschaeftigung mit digitalen Brands, Angebotsseiten, Social Media Marketing und Content-Planung.", size=10),
        pdf_text(48, 418, "Projektbeispiele", size=14, font="F2"),
        pdf_text(48, 400, "KPI Dashboard: Umsatz, AOV, Conversion, Retourenquote und Matchday-Vergleich.", size=10),
        pdf_text(48, 386, "Interaktive Shop-Demo: Produktkarten, Suche, Filter, Warenkorb und vorbereiteter Checkout.", size=10),
        pdf_text(48, 372, "Matchday-Funnel: Content-Route vom Teaser bis zum Sale mit Vereins- und Kampagnenbezug.", size=10),
        pdf_text(48, 358, "Social-Funnel: Landingpage mit Lead-Capture und vorbereiteter Welcome-Mail-Automation.", size=10),
        pdf_text(48, 342, "Kenntnisse", size=14, font="F2"),
        pdf_text(48, 324, "Interesse an E-Commerce, Online-Shops und digitalen Geschaeftsmodellen", size=10),
        pdf_text(48, 310, "Sorgfaeltige und strukturierte Arbeitsweise, technisches Grundverstaendnis", size=10),
        pdf_text(48, 296, "Interesse an Kennzahlen, Reporting, Zielgruppen und digitaler Kommunikation", size=10),
        pdf_text(48, 282, "Teamfaehig, lernbereit, zuverlaessig und motiviert, Neues schnell aufzunehmen", size=10),
        pdf_text(48, 252, "Sprachen", size=14, font="F2"),
        pdf_text(48, 234, "Deutsch: Muttersprache | Englisch: B2 | Franzoesisch: B2 | Spanisch: B1", size=10),
        pdf_text(48, 204, "Hinweis", size=14, font="F2"),
        pdf_text(48, 186, "Die Website ergaenzt den Lebenslauf um konkrete E-Commerce-Arbeitsproben und eine Shop-Demo.", size=10),
        pdf_text(48, 82, "Stand: Maerz 2026 | Bewerbungswebsite und PDF wurden als zusammengehoeriges Portfolio aufgebaut.", size=9),
    ]
    return "\n".join(lines).encode("ascii")


def write_pdfs() -> None:
    (DOWNLOADS / "SCF_Ecommerce_KPI_Dashboard.pdf").write_bytes(build_pdf([kpi_pdf_stream(), kpi_pdf_insights_stream()]))
    (DOWNLOADS / "Kassem_Jaffal_Lebenslauf.pdf").write_bytes(build_pdf([resume_pdf_stream()]))


def main() -> None:
    write_csv()
    write_xlsx()
    write_pdfs()


if __name__ == "__main__":
    main()
