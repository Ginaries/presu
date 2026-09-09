from __future__ import annotations

import json
import mimetypes
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import uuid
from datetime import datetime
from html import escape as html_escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "presupuestos.db"
PAGE_WIDTH = 595.28
PAGE_HEIGHT = 841.89


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def new_id() -> str:
    return uuid.uuid4().hex


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                company TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                phone TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS quotes (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                number TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                project_type TEXT NOT NULL,
                mode TEXT NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Borrador',
                scope TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                terms TEXT NOT NULL DEFAULT '',
                config_json TEXT NOT NULL DEFAULT '{}',
                items_json TEXT NOT NULL DEFAULT '[]',
                recurring_items_json TEXT NOT NULL DEFAULT '[]',
                subtotal REAL NOT NULL DEFAULT 0,
                discount REAL NOT NULL DEFAULT 0,
                tax REAL NOT NULL DEFAULT 0,
                total REAL NOT NULL DEFAULT 0,
                monthly_total REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            );
            """
        )


def row_to_dict(row: sqlite3.Row) -> dict:
    return {key: row[key] for key in row.keys()}


def quote_number(conn: sqlite3.Connection) -> str:
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"COT-{today}-"
    row = conn.execute(
        "SELECT COUNT(*) AS total FROM quotes WHERE number LIKE ?",
        (f"{prefix}%",),
    ).fetchone()
    return f"{prefix}{int(row['total']) + 1:03d}"


def clean_text(value: object, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def clean_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_json_list(value: str) -> list:
    try:
        parsed = json.loads(value or "[]")
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def parse_json_obj(value: str) -> dict:
    try:
        parsed = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def htmlish_text(value: object) -> str:
    return clean_text(value).replace("\r\n", "\n").replace("\r", "\n")


def pdf_safe(value: object) -> str:
    text = clean_text(value)
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\n", " ")
    )


def money(value: object, currency: str = "ARS") -> str:
    symbol = {"ARS": "$", "USD": "US$", "EUR": "EUR"}.get(currency, "$")
    amount = f"{clean_float(value):,.0f}".replace(",", ".")
    return f"{symbol} {amount}"


def text_width(text: str, size: float) -> float:
    wide = sum(1.0 if ch in "MW@#%&" else 0.72 if ch.isupper() else 0.52 for ch in text)
    return wide * size


def wrap_text(text: object, max_width: float, size: float) -> list[str]:
    lines: list[str] = []
    paragraphs = htmlish_text(text).split("\n") or [""]
    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if text_width(candidate, size) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def initials(value: str) -> str:
    parts = [part for part in clean_text(value).split() if part]
    return "".join(part[0] for part in parts[:2]).upper() or "PW"


class PdfDocument:
    def __init__(self) -> None:
        self.pages: list[str] = []
        self.commands: list[str] = []
        self.y = PAGE_HEIGHT - 42

    def add_page(self) -> None:
        if self.commands:
            self.pages.append("\n".join(self.commands))
        self.commands = []
        self.y = PAGE_HEIGHT - 42

    def ensure(self, height: float) -> None:
        if self.y - height < 46:
            self.add_page()

    def color(self, rgb: tuple[int, int, int]) -> str:
        return " ".join(f"{channel / 255:.3f}" for channel in rgb)

    def rect(
        self,
        x: float,
        y_top: float,
        width: float,
        height: float,
        fill: tuple[int, int, int] | None = None,
        stroke: tuple[int, int, int] | None = None,
        line_width: float = 1,
    ) -> None:
        y = y_top - height
        if fill and stroke:
            self.commands.append(f"{self.color(fill)} rg {self.color(stroke)} RG {line_width} w {x:.2f} {y:.2f} {width:.2f} {height:.2f} re B")
        elif fill:
            self.commands.append(f"{self.color(fill)} rg {x:.2f} {y:.2f} {width:.2f} {height:.2f} re f")
        elif stroke:
            self.commands.append(f"{self.color(stroke)} RG {line_width} w {x:.2f} {y:.2f} {width:.2f} {height:.2f} re S")

    def line(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int]) -> None:
        self.commands.append(f"{self.color(color)} RG 1 w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def text(
        self,
        x: float,
        y: float,
        value: object,
        size: float = 10,
        bold: bool = False,
        color: tuple[int, int, int] = (31, 41, 51),
    ) -> None:
        font = "F2" if bold else "F1"
        self.commands.append(
            f"BT {self.color(color)} rg /{font} {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({pdf_safe(value)}) Tj ET"
        )

    def wrapped(
        self,
        x: float,
        y_top: float,
        value: object,
        width: float,
        size: float = 10,
        line_height: float = 13,
        bold: bool = False,
        color: tuple[int, int, int] = (31, 41, 51),
    ) -> float:
        y = y_top - size
        for line in wrap_text(value, width, size):
            self.text(x, y, line, size=size, bold=bold, color=color)
            y -= line_height
        return y + line_height

    def section_title(self, title: str) -> None:
        self.ensure(34)
        self.text(42, self.y - 12, title.upper(), size=10, bold=True, color=(37, 95, 79))
        self.line(42, self.y - 20, 553, self.y - 20, (217, 226, 220))
        self.y -= 32

    def finish(self) -> bytes:
        self.pages.append("\n".join(self.commands))
        objects: list[bytes] = []
        page_object_numbers = [5 + index * 2 for index in range(len(self.pages))]
        content_object_numbers = [6 + index * 2 for index in range(len(self.pages))]

        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        kids = " ".join(f"{num} 0 R" for num in page_object_numbers)
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(self.pages)} >>".encode("ascii"))
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

        for page_num, content_num, content in zip(page_object_numbers, content_object_numbers, self.pages):
            objects.append(
                (
                    f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH:.2f} {PAGE_HEIGHT:.2f}] "
                    f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_num} 0 R >>"
                ).encode("ascii")
            )
            stream = content.encode("cp1252", errors="replace")
            objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")

        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(output))
            output.extend(f"{index} 0 obj\n".encode("ascii"))
            output.extend(obj)
            output.extend(b"\nendobj\n")

        xref_pos = len(output)
        output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        output.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        output.extend(
            (
                f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
                f"startxref\n{xref_pos}\n%%EOF"
            ).encode("ascii")
        )
        return bytes(output)


def quote_pdf_native(payload: dict) -> bytes:
    quote = payload.get("quote", {}) if isinstance(payload.get("quote"), dict) else {}
    client = payload.get("client", {}) if isinstance(payload.get("client"), dict) else {}
    config = quote.get("config", {}) if isinstance(quote.get("config"), dict) else {}
    issuer = config.get("issuer", {}) if isinstance(config.get("issuer"), dict) else {}
    items = quote.get("items", []) if isinstance(quote.get("items"), list) else []
    recurring = quote.get("recurring_items", []) if isinstance(quote.get("recurring_items"), list) else []
    currency = clean_text(quote.get("currency"), "ARS")
    subtotal = sum(clean_float(item.get("qty"), 1) * clean_float(item.get("unit_price")) for item in items if isinstance(item, dict))
    monthly = sum(clean_float(item.get("qty"), 1) * clean_float(item.get("unit_price")) for item in recurring if isinstance(item, dict))
    discount = min(clean_float(quote.get("discount")), subtotal)
    tax = clean_float(quote.get("tax"))
    total = max(0, subtotal - discount) + tax
    quote_number = clean_text(quote.get("number"), "Sin guardar") or "Sin guardar"
    title = clean_text(quote.get("title"), "Presupuesto") or "Presupuesto"
    project_type = clean_text(quote.get("project_type"), "Proyecto")
    status = clean_text(quote.get("status"), "Borrador")
    brand = clean_text(issuer.get("brand"), "Presupuestos Web") or "Presupuestos Web"
    tagline = clean_text(issuer.get("tagline"), "Desarrollo web, apps y automatizaciones")
    issue_date = datetime.now().strftime("%d/%m/%Y")

    pdf = PdfDocument()

    def meta_line(label: str, value: object) -> None:
        if clean_text(value):
            pdf.text(318, pdf.y, label, size=8, bold=True, color=(101, 114, 124))
            pdf.wrapped(392, pdf.y + 8, value, 154, size=9, line_height=11, color=(31, 41, 51))
            pdf.y -= 16

    pdf.rect(42, pdf.y, 38, 38, fill=(37, 95, 79))
    pdf.text(53, pdf.y - 24, initials(brand), size=12, bold=True, color=(255, 255, 255))
    pdf.text(92, pdf.y - 13, brand, size=14, bold=True)
    pdf.wrapped(92, pdf.y - 17, tagline, 270, size=9, line_height=11, color=(101, 114, 124))
    pdf.text(430, pdf.y - 8, quote_number, size=9, color=(101, 114, 124))
    pdf.text(430, pdf.y - 24, status.upper(), size=9, bold=True, color=(37, 95, 79))
    pdf.text(430, pdf.y - 38, issue_date, size=9, color=(101, 114, 124))
    pdf.y -= 60

    pdf.rect(42, pdf.y, 511, 106, fill=(243, 247, 245), stroke=(217, 226, 220))
    pdf.rect(42, pdf.y, 7, 106, fill=(37, 95, 79))
    pdf.text(62, pdf.y - 22, "PROPUESTA COMERCIAL", size=8, bold=True, color=(37, 95, 79))
    hero_bottom = pdf.wrapped(62, pdf.y - 32, title, 315, size=22, line_height=24, bold=True, color=(22, 33, 38))
    client_name = clean_text(client.get("company")) or clean_text(client.get("name")) or "Cliente"
    pdf.wrapped(62, hero_bottom - 2, f"Preparada para {client_name}", 315, size=10, line_height=12, color=(63, 75, 83))
    pdf.line(382, pdf.y - 16, 382, pdf.y - 90, (217, 226, 220))
    pdf.text(402, pdf.y - 28, "INVERSIÓN ESTIMADA", size=8, bold=True, color=(101, 114, 124))
    pdf.text(402, pdf.y - 53, money(total, currency), size=19, bold=True, color=(37, 95, 79))
    monthly_text = f"+ {money(monthly, currency)} mensuales" if monthly else "Sin abono mensual incluido"
    pdf.wrapped(402, pdf.y - 62, monthly_text, 125, size=9, line_height=11, color=(63, 75, 83))
    pdf.y -= 126

    card_w = 120
    cards = [
        ("Tipo de proyecto", project_type),
        ("Servicios cotizados", str(len(items) + len(recurring))),
        ("Moneda", currency),
        ("Validez", "Ver condiciones"),
    ]
    for index, (label, value) in enumerate(cards):
        x = 42 + index * (card_w + 10)
        pdf.rect(x, pdf.y, card_w, 48, fill=(251, 252, 251), stroke=(217, 226, 220))
        pdf.text(x + 10, pdf.y - 16, label.upper(), size=7, bold=True, color=(101, 114, 124))
        pdf.wrapped(x + 10, pdf.y - 24, value, card_w - 20, size=10, line_height=11, bold=True)
    pdf.y -= 66

    party_y = pdf.y
    pdf.rect(42, party_y, 248, 92, fill=(255, 255, 255), stroke=(217, 226, 220))
    pdf.rect(305, party_y, 248, 92, fill=(255, 255, 255), stroke=(217, 226, 220))
    pdf.text(56, party_y - 18, "CLIENTE", size=9, bold=True, color=(37, 95, 79))
    left_y = party_y - 34
    for value in [client.get("company"), client.get("name"), client.get("email"), client.get("phone")]:
        if clean_text(value):
            pdf.text(56, left_y, value, size=9)
            left_y -= 13
    pdf.text(319, party_y - 18, "EMITIDO POR", size=9, bold=True, color=(37, 95, 79))
    right_y = party_y - 34
    for value in [brand, issuer.get("email"), issuer.get("phone"), issuer.get("website"), issuer.get("location")]:
        if clean_text(value):
            pdf.text(319, right_y, value, size=9, bold=value == brand)
            right_y -= 13
    pdf.y -= 110

    scope = htmlish_text(quote.get("scope")) or "Según detalle de servicios."
    scope_lines = wrap_text(scope, 475, 10)
    scope_h = 36 + len(scope_lines) * 13
    pdf.ensure(scope_h)
    pdf.rect(42, pdf.y, 511, scope_h, fill=(251, 253, 255), stroke=(217, 226, 220))
    pdf.rect(42, pdf.y, 5, scope_h, fill=(40, 95, 143))
    pdf.text(58, pdf.y - 18, "ALCANCE", size=9, bold=True, color=(37, 95, 79))
    pdf.wrapped(58, pdf.y - 30, scope, 475, size=10, line_height=13)
    pdf.y -= scope_h + 12

    def draw_table(title_text: str, rows: list[dict], monthly_label: bool = False) -> None:
        if not rows:
            return
        pdf.section_title(title_text)
        cols = [28, 116, 205, 40, 58, 64]
        x_positions = [42]
        for width in cols[:-1]:
            x_positions.append(x_positions[-1] + width)

        def header() -> None:
            pdf.ensure(32)
            pdf.rect(42, pdf.y, 511, 26, fill=(238, 244, 241), stroke=(217, 226, 220))
            labels = ["#", "Concepto", "Detalle", "Cant.", "Mensual" if monthly_label else "Unitario", "Total"]
            for x, label, width in zip(x_positions, labels, cols):
                pdf.text(x + 6, pdf.y - 17, label.upper(), size=7, bold=True, color=(37, 95, 79))
            pdf.y -= 26

        header()
        for index, item in enumerate(rows, start=1):
            name = clean_text(item.get("name"), "Servicio")
            detail = clean_text(item.get("description"))
            qty = clean_float(item.get("qty"), 1)
            unit = clean_float(item.get("unit_price"))
            name_lines = wrap_text(name, cols[1] - 12, 8.5)
            detail_lines = wrap_text(detail, cols[2] - 12, 8.5)
            row_h = max(34, 14 + max(len(name_lines), len(detail_lines), 1) * 11)
            if pdf.y - row_h < 46:
                pdf.add_page()
                header()
            pdf.rect(42, pdf.y, 511, row_h, fill=(255, 255, 255), stroke=(217, 226, 220))
            pdf.text(x_positions[0] + 9, pdf.y - 18, str(index), size=8.5, color=(101, 114, 124))
            pdf.wrapped(x_positions[1] + 6, pdf.y - 9, name, cols[1] - 12, size=8.5, line_height=11, bold=True)
            pdf.wrapped(x_positions[2] + 6, pdf.y - 9, detail, cols[2] - 12, size=8.5, line_height=11, color=(63, 75, 83))
            pdf.text(x_positions[3] + 10, pdf.y - 18, f"{qty:g}", size=8.5)
            pdf.text(x_positions[4] + 3, pdf.y - 18, money(unit, currency), size=8.5)
            pdf.text(x_positions[5] + 3, pdf.y - 18, money(qty * unit, currency), size=8.5, bold=True)
            pdf.y -= row_h
        pdf.y -= 10

    draw_table("Detalle del proyecto", items)
    draw_table("Servicios mensuales", recurring, monthly_label=True)

    pdf.ensure(116)
    top = pdf.y
    pdf.rect(42, top, 511, 104, fill=(248, 250, 249), stroke=(217, 226, 220))
    pdf.text(58, top - 20, "RESUMEN ECONÓMICO", size=10, bold=True, color=(37, 95, 79))
    pdf.wrapped(58, top - 34, "Los valores se calculan según los conceptos detallados en esta propuesta.", 220, size=9, line_height=12, color=(101, 114, 124))
    x = 318
    row_y = top - 18
    for label, value, bold in [
        ("Subtotal", subtotal, False),
        ("Descuento", discount, False),
        ("Impuestos", tax, False),
        ("Total proyecto", total, True),
        ("Total mensual", monthly, False),
    ]:
        if label == "Total mensual" and not monthly:
            continue
        if bold:
            pdf.rect(x - 10, row_y + 10, 214, 22, fill=(37, 95, 79))
            pdf.text(x, row_y - 6, label, size=9, bold=True, color=(255, 255, 255))
            pdf.text(x + 105, row_y - 6, money(value, currency), size=9, bold=True, color=(255, 255, 255))
        else:
            pdf.text(x, row_y, label, size=9, color=(63, 75, 83))
            pdf.text(x + 105, row_y, money(value, currency), size=9, bold=True)
        row_y -= 18
    pdf.y -= 120

    for title_text, value in [("Notas", quote.get("notes")), ("Condiciones", quote.get("terms"))]:
        text = htmlish_text(value)
        if not text:
            continue
        lines = wrap_text(text, 475, 9.5)
        height = 34 + len(lines) * 12
        pdf.ensure(height)
        pdf.rect(42, pdf.y, 511, height, fill=(255, 255, 255), stroke=(217, 226, 220))
        pdf.text(58, pdf.y - 18, title_text.upper(), size=9, bold=True, color=(37, 95, 79))
        pdf.wrapped(58, pdf.y - 30, text, 475, size=9.5, line_height=12)
        pdf.y -= height + 10

    pdf.ensure(22)
    pdf.line(42, 36, 553, 36, (217, 226, 220))
    pdf.text(42, 22, brand, size=8, color=(101, 114, 124))
    pdf.text(470, 22, quote_number, size=8, color=(101, 114, 124))
    return pdf.finish()


def normalize_pdf_context(payload: dict) -> dict:
    quote = payload.get("quote", {}) if isinstance(payload.get("quote"), dict) else {}
    client = payload.get("client", {}) if isinstance(payload.get("client"), dict) else {}
    config = quote.get("config", {}) if isinstance(quote.get("config"), dict) else {}
    issuer = config.get("issuer", {}) if isinstance(config.get("issuer"), dict) else {}
    items = quote.get("items", []) if isinstance(quote.get("items"), list) else []
    recurring = quote.get("recurring_items", []) if isinstance(quote.get("recurring_items"), list) else []
    currency = clean_text(quote.get("currency"), "ARS")

    def normalize_item(item: object) -> dict:
        data = item if isinstance(item, dict) else {}
        qty = clean_float(data.get("qty"), 1)
        unit = clean_float(data.get("unit_price"))
        return {
            "name": clean_text(data.get("name"), "Servicio") or "Servicio",
            "description": clean_text(data.get("description")),
            "qty": qty,
            "unit_price": unit,
            "total": qty * unit,
        }

    normalized_items = [normalize_item(item) for item in items]
    normalized_recurring = [normalize_item(item) for item in recurring]
    subtotal = sum(item["total"] for item in normalized_items)
    monthly_total = sum(item["total"] for item in normalized_recurring)
    discount = min(clean_float(quote.get("discount")), subtotal)
    tax = clean_float(quote.get("tax"))
    total = max(0, subtotal - discount) + tax
    terms = htmlish_text(quote.get("terms"))
    match = re.search(r"validez[^0-9]*(\d+)\s*d[ií]as?", terms, re.IGNORECASE) or re.search(
        r"(\d+)\s*d[ií]as?", terms, re.IGNORECASE
    )

    return {
        "quote_number": clean_text(quote.get("number"), "Sin guardar") or "Sin guardar",
        "title": clean_text(quote.get("title"), "Presupuesto") or "Presupuesto",
        "project_type": clean_text(quote.get("project_type"), "Proyecto"),
        "status": clean_text(quote.get("status"), "Borrador"),
        "currency": currency,
        "scope": htmlish_text(quote.get("scope")) or "Según detalle de servicios.",
        "notes": htmlish_text(quote.get("notes")),
        "terms": terms,
        "issuer": {
            "brand": clean_text(issuer.get("brand"), "Presupuestos Web") or "Presupuestos Web",
            "tagline": clean_text(issuer.get("tagline"), "Desarrollo web, apps y automatizaciones"),
            "email": clean_text(issuer.get("email")),
            "phone": clean_text(issuer.get("phone")),
            "website": clean_text(issuer.get("website")),
            "location": clean_text(issuer.get("location")),
        },
        "client": {
            "name": clean_text(client.get("name")),
            "company": clean_text(client.get("company")),
            "email": clean_text(client.get("email")),
            "phone": clean_text(client.get("phone")),
            "notes": clean_text(client.get("notes")),
        },
        "items": normalized_items,
        "recurring": normalized_recurring,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "monthly_total": monthly_total,
        "issue_date": datetime.now().strftime("%d/%m/%Y"),
        "validity": f"{match.group(1)} días" if match else "Ver condiciones",
    }


def html_lines(values: list[object]) -> str:
    lines = [clean_text(value) for value in values if clean_text(value)]
    if not lines:
        return '<p class="muted">Sin datos cargados</p>'
    return "".join(f"<p>{html_escape(line)}</p>" for line in lines)


def nl2br_html(value: object) -> str:
    return "<br>".join(html_escape(line) for line in htmlish_text(value).split("\n"))


def money_html(value: object, currency: str) -> str:
    return html_escape(money(value, currency))


def quote_pdf_html(payload: dict) -> str:
    data = normalize_pdf_context(payload)
    issuer = data["issuer"]
    client = data["client"]
    client_name = client["company"] or client["name"] or "Cliente"
    issuer_lines = html_lines([issuer["email"], issuer["phone"], issuer["website"], issuer["location"]])
    client_lines = html_lines([client["company"], client["name"], client["email"], client["phone"]])

    def table(title: str, rows: list[dict], monthly: bool = False) -> str:
        if not rows:
            return ""
        label = "Mensual" if monthly else "Unitario"
        body = []
        for index, item in enumerate(rows, start=1):
            body.append(
                f"""
                <article class="service-row">
                  <div class="service-index">{index:02d}</div>
                  <div class="service-copy">
                    <h3>{html_escape(item["name"])}</h3>
                    <p>{nl2br_html(item["description"])}</p>
                  </div>
                  <div class="service-price">
                    <span>Cant. {item["qty"]:g}</span>
                    <span>{label}: {money_html(item["unit_price"], data["currency"])}</span>
                    <strong>{money_html(item["total"], data["currency"])}</strong>
                  </div>
                </article>
                """
            )
        return f"""
        <section class="block services-block">
          <h2>{html_escape(title)}</h2>
          <div class="service-list">{''.join(body)}</div>
        </section>
        """

    optional_sections = ""
    if data["notes"]:
        optional_sections += f"""
        <section class="block soft">
          <h2>Notas</h2>
          <p>{nl2br_html(data["notes"])}</p>
        </section>
        """
    if data["terms"]:
        optional_sections += f"""
        <section class="block soft">
          <h2>Condiciones</h2>
          <p>{nl2br_html(data["terms"])}</p>
        </section>
        """

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{html_escape(data["quote_number"])} - {html_escape(data["title"])}</title>
  <style>
    @page {{
      size: A4;
      margin: 14mm;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: #ffffff;
      color: #1e2a32;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 11.5px;
      line-height: 1.45;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    p {{
      margin: 0 0 4px;
    }}

    .document {{
      width: 100%;
    }}

    .top {{
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: flex-start;
      padding-bottom: 16px;
      border-bottom: 1px solid #dce5df;
      margin-bottom: 18px;
    }}

    .brand {{
      display: flex;
      gap: 12px;
      align-items: center;
      min-width: 0;
    }}

    .mark {{
      width: 42px;
      height: 42px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 0 0 auto;
      border-radius: 8px;
      background: #285f50;
      color: #ffffff;
      font-weight: 800;
      font-size: 13px;
    }}

    .brand strong {{
      display: block;
      font-size: 16px;
      color: #17242b;
    }}

    .brand span,
    .meta span,
    .summary span,
    .investment span,
    .muted {{
      color: #687680;
    }}

    .meta {{
      text-align: right;
      display: grid;
      gap: 4px;
      font-size: 10.5px;
      max-width: 180px;
      overflow-wrap: anywhere;
    }}

    .status {{
      display: inline-block;
      border: 1px solid #b9d8c9;
      border-radius: 999px;
      background: #eef8f4;
      color: #285f50;
      padding: 3px 9px;
      font-weight: 800;
      text-transform: uppercase;
    }}

    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 205px;
      gap: 20px;
      align-items: stretch;
      border: 1px solid #dce5df;
      border-left: 8px solid #285f50;
      border-radius: 12px;
      background: #f3f7f5;
      padding: 20px;
      margin-bottom: 14px;
      break-inside: avoid;
    }}

    .hero-label {{
      display: block;
      color: #285f50;
      font-size: 9px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
      margin-bottom: 7px;
    }}

    h1 {{
      margin: 0 0 9px;
      color: #15232a;
      font-size: 25px;
      line-height: 1.12;
    }}

    .hero p {{
      color: #40505a;
      font-size: 12px;
    }}

    .investment {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-end;
      text-align: right;
      border-left: 1px solid #dce5df;
      padding-left: 16px;
      min-width: 0;
    }}

    .investment strong {{
      display: block;
      color: #285f50;
      font-size: 20px;
      line-height: 1.15;
      margin: 4px 0;
    }}

    .investment small {{
      color: #40505a;
    }}

    .summary {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 9px;
      margin: 0 0 16px;
      break-inside: avoid;
    }}

    .summary div {{
      min-height: 54px;
      border: 1px solid #dce5df;
      border-radius: 8px;
      background: #fbfcfb;
      padding: 9px 10px;
    }}

    .summary span {{
      display: block;
      margin-bottom: 4px;
      font-size: 8.5px;
      font-weight: 800;
      text-transform: uppercase;
    }}

    .summary strong {{
      display: block;
      font-size: 11px;
      line-height: 1.25;
    }}

    .parties {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 14px;
      break-inside: avoid;
    }}

    .party,
    .block {{
      border: 1px solid #dce5df;
      border-radius: 8px;
      background: #ffffff;
      padding: 12px 13px;
    }}

    h2 {{
      margin: 0 0 8px;
      color: #285f50;
      font-size: 10px;
      letter-spacing: .05em;
      text-transform: uppercase;
    }}

    .block {{
      margin: 0 0 12px;
    }}

    .scope {{
      border-left: 5px solid #2b6597;
      background: #fbfdff;
      break-inside: avoid;
    }}

    .services-block {{
      break-inside: auto;
    }}

    .service-list {{
      display: grid;
      gap: 8px;
    }}

    .service-row {{
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr) 150px;
      gap: 12px;
      align-items: start;
      border: 1px solid #dce5df;
      border-radius: 8px;
      background: #fbfcfb;
      padding: 10px 11px;
      break-inside: avoid;
      page-break-inside: avoid;
    }}

    .service-index {{
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 7px;
      background: #eef4f1;
      color: #285f50;
      font-size: 9px;
      font-weight: 800;
    }}

    .service-copy {{
      min-width: 0;
    }}

    .service-copy h3 {{
      margin: 0 0 4px;
      color: #15232a;
      font-size: 12px;
      line-height: 1.25;
    }}

    .service-copy p {{
      margin: 0;
      color: #40505a;
      overflow-wrap: anywhere;
    }}

    .service-price {{
      display: grid;
      gap: 3px;
      justify-items: end;
      text-align: right;
      color: #687680;
      font-size: 9.5px;
    }}

    .service-price strong {{
      margin-top: 4px;
      color: #15232a;
      font-size: 12px;
      white-space: nowrap;
    }}

    .economics {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 245px;
      gap: 18px;
      align-items: start;
      background: #f8faf9;
      break-inside: avoid;
    }}

    .totals {{
      border: 1px solid #dce5df;
      border-radius: 8px;
      overflow: hidden;
      background: #ffffff;
    }}

    .totals-row {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 8px 10px;
      border-bottom: 1px solid #dce5df;
    }}

    .totals-row:last-child {{
      border-bottom: 0;
    }}

    .totals-row strong {{
      white-space: nowrap;
    }}

    .grand {{
      background: #285f50;
      color: #ffffff;
      font-size: 13px;
      font-weight: 800;
    }}

    .soft {{
      break-inside: avoid;
    }}

    .footer {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      border-top: 1px solid #dce5df;
      color: #687680;
      font-size: 9px;
      margin-top: 18px;
      padding-top: 8px;
    }}
  </style>
</head>
<body>
  <main class="document">
    <header class="top">
      <div class="brand">
        <div class="mark">{html_escape(initials(issuer["brand"]))}</div>
        <div>
          <strong>{html_escape(issuer["brand"])}</strong>
          <span>{html_escape(issuer["tagline"])}</span>
        </div>
      </div>
      <div class="meta">
        <span>{html_escape(data["quote_number"])}</span>
        <strong class="status">{html_escape(data["status"])}</strong>
        <span>{html_escape(data["issue_date"])}</span>
      </div>
    </header>

    <section class="hero">
      <div>
        <span class="hero-label">Propuesta comercial</span>
        <h1>{html_escape(data["title"])}</h1>
        <p>Preparada para <strong>{html_escape(client_name)}</strong></p>
      </div>
      <div class="investment">
        <span>Inversión estimada</span>
        <strong>{money_html(data["total"], data["currency"])}</strong>
        <small>{("+ " + money(data["monthly_total"], data["currency"]) + " mensuales") if data["monthly_total"] else "Sin abono mensual incluido"}</small>
      </div>
    </section>

    <section class="summary">
      <div><span>Tipo de proyecto</span><strong>{html_escape(data["project_type"])}</strong></div>
      <div><span>Servicios cotizados</span><strong>{len(data["items"]) + len(data["recurring"])}</strong></div>
      <div><span>Moneda</span><strong>{html_escape(data["currency"])}</strong></div>
      <div><span>Validez</span><strong>{html_escape(data["validity"])}</strong></div>
    </section>

    <section class="parties">
      <div class="party">
        <h2>Cliente</h2>
        {client_lines}
      </div>
      <div class="party">
        <h2>Emitido por</h2>
        <p><strong>{html_escape(issuer["brand"])}</strong></p>
        {issuer_lines}
      </div>
    </section>

    <section class="block scope">
      <h2>Alcance</h2>
      <p>{nl2br_html(data["scope"])}</p>
    </section>

    {table("Detalle del proyecto", data["items"])}
    {table("Servicios mensuales", data["recurring"], monthly=True)}

    <section class="block economics">
      <div>
        <h2>Resumen económico</h2>
        <p class="muted">Los valores se calculan según los conceptos detallados en esta propuesta.</p>
      </div>
      <div class="totals">
        <div class="totals-row"><span>Subtotal</span><strong>{money_html(data["subtotal"], data["currency"])}</strong></div>
        <div class="totals-row"><span>Descuento</span><strong>{money_html(data["discount"], data["currency"])}</strong></div>
        <div class="totals-row"><span>Impuestos</span><strong>{money_html(data["tax"], data["currency"])}</strong></div>
        <div class="totals-row grand"><span>Total proyecto</span><strong>{money_html(data["total"], data["currency"])}</strong></div>
        {f'<div class="totals-row"><span>Total mensual</span><strong>{money_html(data["monthly_total"], data["currency"])}</strong></div>' if data["monthly_total"] else ""}
      </div>
    </section>

    {optional_sections}

    <footer class="footer">
      <span>{html_escape(issuer["brand"])}</span>
      <span>{html_escape(data["quote_number"])}</span>
    </footer>
  </main>
</body>
</html>"""


def chrome_executable() -> str | None:
    candidates = [
        shutil.which("chrome"),
        shutil.which("chrome.exe"),
        shutil.which("msedge"),
        shutil.which("msedge.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def quote_pdf_browser(payload: dict) -> bytes:
    chrome = chrome_executable()
    if not chrome:
        raise RuntimeError("No se encontró Chrome o Edge para generar el PDF.")

    with tempfile.TemporaryDirectory(prefix="presupuesto_pdf_") as temp:
        temp_dir = Path(temp)
        html_path = temp_dir / "presupuesto.html"
        pdf_path = temp_dir / "presupuesto.pdf"
        html_path.write_text(quote_pdf_html(payload), encoding="utf-8")
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45, creationflags=creationflags)
        if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
            raise RuntimeError("Chrome no generó un PDF válido.")
        return pdf_path.read_bytes()


def quote_pdf(payload: dict) -> bytes:
    try:
        return quote_pdf_browser(payload)
    except Exception as exc:
        print(f"No se pudo generar PDF con Chrome, usando respaldo interno: {exc}")
        return quote_pdf_native(payload)


def download_name(value: object) -> str:
    name = clean_text(value, "presupuesto") or "presupuesto"
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in name)
    return safe.strip("-") or "presupuesto"


def get_client(conn: sqlite3.Connection, client_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
    return row_to_dict(row) if row else None


def upsert_client(conn: sqlite3.Connection, payload: dict) -> str:
    client = payload or {}
    client_id = clean_text(client.get("id"))
    timestamp = now_iso()
    name = clean_text(client.get("name"), "Cliente sin nombre") or "Cliente sin nombre"
    fields = {
        "name": name,
        "company": clean_text(client.get("company")),
        "email": clean_text(client.get("email")),
        "phone": clean_text(client.get("phone")),
        "notes": clean_text(client.get("notes")),
    }

    if client_id and get_client(conn, client_id):
        conn.execute(
            """
            UPDATE clients
               SET name = ?, company = ?, email = ?, phone = ?, notes = ?, updated_at = ?
             WHERE id = ?
            """,
            (
                fields["name"],
                fields["company"],
                fields["email"],
                fields["phone"],
                fields["notes"],
                timestamp,
                client_id,
            ),
        )
        return client_id

    client_id = new_id()
    conn.execute(
        """
        INSERT INTO clients (id, name, company, email, phone, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            client_id,
            fields["name"],
            fields["company"],
            fields["email"],
            fields["phone"],
            fields["notes"],
            timestamp,
            timestamp,
        ),
    )
    return client_id


def quote_detail(conn: sqlite3.Connection, quote_id: str) -> dict | None:
    row = conn.execute(
        """
        SELECT q.*, c.name AS client_name, c.company AS client_company,
               c.email AS client_email, c.phone AS client_phone, c.notes AS client_notes
          FROM quotes q
          JOIN clients c ON c.id = q.client_id
         WHERE q.id = ?
        """,
        (quote_id,),
    ).fetchone()
    if not row:
        return None
    data = row_to_dict(row)
    data["client"] = {
        "id": data["client_id"],
        "name": data.pop("client_name"),
        "company": data.pop("client_company"),
        "email": data.pop("client_email"),
        "phone": data.pop("client_phone"),
        "notes": data.pop("client_notes"),
    }
    data["items"] = parse_json_list(data.pop("items_json"))
    data["recurring_items"] = parse_json_list(data.pop("recurring_items_json"))
    data["config"] = parse_json_obj(data.pop("config_json"))
    return data


class BudgetHandler(BaseHTTPRequestHandler):
    server_version = "PresupuestosWeb/1.0"

    def log_message(self, format: str, *args: object) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api_get(parsed.path, parse_qs(parsed.query))
            return
        self.serve_static(parsed.path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api_post(parsed.path)
            return
        self.json_response({"error": "Ruta no encontrada"}, HTTPStatus.NOT_FOUND)

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api_delete(parsed.path)
            return
        self.json_response({"error": "Ruta no encontrada"}, HTTPStatus.NOT_FOUND)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self.json_response({"error": "JSON inválido"}, HTTPStatus.BAD_REQUEST)
            raise
        return payload if isinstance(payload, dict) else {}

    def json_response(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def pdf_response(self, payload: dict) -> None:
        body = quote_pdf(payload)
        quote = payload.get("quote", {}) if isinstance(payload.get("quote"), dict) else {}
        filename = f"{download_name(quote.get('number') or quote.get('title'))}.pdf"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, request_path: str) -> None:
        path = "/index.html" if request_path in ("", "/") else unquote(request_path)
        if path.startswith("/"):
            path = path[1:]
        file_path = (BASE_DIR / path).resolve()

        if STATIC_DIR not in file_path.parents and file_path != BASE_DIR / "index.html":
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not file_path.exists() or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_api_get(self, path: str, query: dict[str, list[str]]) -> None:
        with db() as conn:
            if path == "/api/clients":
                rows = conn.execute(
                    """
                    SELECT c.*,
                           COUNT(q.id) AS quote_count,
                           MAX(q.updated_at) AS last_quote_at
                      FROM clients c
                      LEFT JOIN quotes q ON q.client_id = c.id
                     GROUP BY c.id
                     ORDER BY c.updated_at DESC
                    """
                ).fetchall()
                self.json_response([row_to_dict(row) for row in rows])
                return

            if path == "/api/quotes":
                rows = conn.execute(
                    """
                    SELECT q.id, q.client_id, q.number, q.title, q.project_type,
                           q.mode, q.currency, q.status, q.subtotal, q.discount,
                           q.tax, q.total, q.monthly_total, q.created_at, q.updated_at,
                           c.name AS client_name, c.company AS client_company
                      FROM quotes q
                      JOIN clients c ON c.id = q.client_id
                     ORDER BY q.updated_at DESC
                    """
                ).fetchall()
                self.json_response([row_to_dict(row) for row in rows])
                return

            if path.startswith("/api/quotes/"):
                quote_id = path.rsplit("/", 1)[-1]
                detail = quote_detail(conn, quote_id)
                if not detail:
                    self.json_response({"error": "Cotización no encontrada"}, HTTPStatus.NOT_FOUND)
                    return
                self.json_response(detail)
                return

        self.json_response({"error": "Ruta no encontrada"}, HTTPStatus.NOT_FOUND)

    def handle_api_post(self, path: str) -> None:
        payload = self.read_json()
        with db() as conn:
            if path == "/api/pdf":
                self.pdf_response(payload)
                return

            if path == "/api/quotes":
                client_id = upsert_client(conn, payload.get("client", {}))
                quote = payload.get("quote", {}) or {}
                quote_id = clean_text(quote.get("id"))
                timestamp = now_iso()
                items = quote.get("items") if isinstance(quote.get("items"), list) else []
                recurring = (
                    quote.get("recurring_items")
                    if isinstance(quote.get("recurring_items"), list)
                    else []
                )
                config = quote.get("config") if isinstance(quote.get("config"), dict) else {}
                values = {
                    "title": clean_text(quote.get("title"), "Presupuesto web") or "Presupuesto web",
                    "project_type": clean_text(quote.get("project_type"), "Sitio web"),
                    "mode": clean_text(quote.get("mode"), "Manual"),
                    "currency": clean_text(quote.get("currency"), "ARS"),
                    "status": clean_text(quote.get("status"), "Borrador"),
                    "scope": clean_text(quote.get("scope")),
                    "notes": clean_text(quote.get("notes")),
                    "terms": clean_text(quote.get("terms")),
                    "config_json": json.dumps(config, ensure_ascii=False),
                    "items_json": json.dumps(items, ensure_ascii=False),
                    "recurring_items_json": json.dumps(recurring, ensure_ascii=False),
                    "subtotal": clean_float(quote.get("subtotal")),
                    "discount": clean_float(quote.get("discount")),
                    "tax": clean_float(quote.get("tax")),
                    "total": clean_float(quote.get("total")),
                    "monthly_total": clean_float(quote.get("monthly_total")),
                }

                if quote_id and quote_detail(conn, quote_id):
                    conn.execute(
                        """
                        UPDATE quotes
                           SET client_id = ?, title = ?, project_type = ?, mode = ?,
                               currency = ?, status = ?, scope = ?, notes = ?, terms = ?,
                               config_json = ?, items_json = ?, recurring_items_json = ?,
                               subtotal = ?, discount = ?, tax = ?, total = ?,
                               monthly_total = ?, updated_at = ?
                         WHERE id = ?
                        """,
                        (
                            client_id,
                            values["title"],
                            values["project_type"],
                            values["mode"],
                            values["currency"],
                            values["status"],
                            values["scope"],
                            values["notes"],
                            values["terms"],
                            values["config_json"],
                            values["items_json"],
                            values["recurring_items_json"],
                            values["subtotal"],
                            values["discount"],
                            values["tax"],
                            values["total"],
                            values["monthly_total"],
                            timestamp,
                            quote_id,
                        ),
                    )
                else:
                    quote_id = new_id()
                    conn.execute(
                        """
                        INSERT INTO quotes (
                            id, client_id, number, title, project_type, mode, currency,
                            status, scope, notes, terms, config_json, items_json,
                            recurring_items_json, subtotal, discount, tax, total,
                            monthly_total, created_at, updated_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            quote_id,
                            client_id,
                            quote_number(conn),
                            values["title"],
                            values["project_type"],
                            values["mode"],
                            values["currency"],
                            values["status"],
                            values["scope"],
                            values["notes"],
                            values["terms"],
                            values["config_json"],
                            values["items_json"],
                            values["recurring_items_json"],
                            values["subtotal"],
                            values["discount"],
                            values["tax"],
                            values["total"],
                            values["monthly_total"],
                            timestamp,
                            timestamp,
                        ),
                    )

                conn.commit()
                self.json_response(quote_detail(conn, quote_id), HTTPStatus.CREATED)
                return

            if path.startswith("/api/quotes/") and path.endswith("/duplicate"):
                quote_id = path.split("/")[-2]
                source = quote_detail(conn, quote_id)
                if not source:
                    self.json_response({"error": "Cotización no encontrada"}, HTTPStatus.NOT_FOUND)
                    return
                timestamp = now_iso()
                new_quote_id = new_id()
                conn.execute(
                    """
                    INSERT INTO quotes (
                        id, client_id, number, title, project_type, mode, currency,
                        status, scope, notes, terms, config_json, items_json,
                        recurring_items_json, subtotal, discount, tax, total,
                        monthly_total, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        new_quote_id,
                        source["client_id"],
                        quote_number(conn),
                        f"Copia de {source['title']}",
                        source["project_type"],
                        source["mode"],
                        source["currency"],
                        "Borrador",
                        source["scope"],
                        source["notes"],
                        source["terms"],
                        json.dumps(source["config"], ensure_ascii=False),
                        json.dumps(source["items"], ensure_ascii=False),
                        json.dumps(source["recurring_items"], ensure_ascii=False),
                        source["subtotal"],
                        source["discount"],
                        source["tax"],
                        source["total"],
                        source["monthly_total"],
                        timestamp,
                        timestamp,
                    ),
                )
                conn.commit()
                self.json_response(quote_detail(conn, new_quote_id), HTTPStatus.CREATED)
                return

        self.json_response({"error": "Ruta no encontrada"}, HTTPStatus.NOT_FOUND)

    def handle_api_delete(self, path: str) -> None:
        with db() as conn:
            if path.startswith("/api/quotes/"):
                quote_id = path.rsplit("/", 1)[-1]
                cur = conn.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
                conn.commit()
                if cur.rowcount:
                    self.json_response({"ok": True})
                else:
                    self.json_response({"error": "Cotización no encontrada"}, HTTPStatus.NOT_FOUND)
                return

        self.json_response({"error": "Ruta no encontrada"}, HTTPStatus.NOT_FOUND)


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), BudgetHandler)
    print("App de presupuestos lista en http://127.0.0.1:8000")
    print(f"Base de datos: {DB_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    main()
