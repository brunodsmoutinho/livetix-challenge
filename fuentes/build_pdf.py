#!/usr/bin/env python3
"""Convierte los Markdown de docs/ a un PDF profesional unico."""

from pathlib import Path
from datetime import datetime
import markdown
from weasyprint import HTML, CSS

ROOT = Path.home() / "livetix-diagram"
DOCS = ROOT / "docs"

DOCUMENTS = [
    DOCS / "01-decisiones.md",
    DOCS / "02-iac.md",
]

DIAGRAMS = [
    ROOT / "LiveTix-Arquitectura.png",
]

CSS_STYLE = """
@page {
    size: A4;
    margin: 2cm 1.8cm;
    @bottom-center {
        content: "LiveTix — Página " counter(page) " de " counter(pages);
        font-size: 9px;
        color: #666;
    }
}
body {
    font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a1a;
}
h1 {
    font-size: 22pt;
    color: #0b3d91;
    border-bottom: 3px solid #0b3d91;
    padding-bottom: 6px;
    margin-top: 30px;
    page-break-before: always;
}
h1:first-of-type { page-break-before: avoid; }
h2 {
    font-size: 15pt;
    color: #0b3d91;
    margin-top: 22px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 3px;
}
h3 { font-size: 12pt; color: #333; margin-top: 16px; }
code {
    background: #f4f4f4;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "SF Mono", Menlo, monospace;
    font-size: 9.5pt;
}
pre {
    background: #f6f8fa;
    border-left: 4px solid #0b3d91;
    padding: 10px 14px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.4;
}
pre code { background: none; padding: 0; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 9.5pt;
}
th, td { border: 1px solid #ddd; padding: 7px 10px; text-align: left; }
th { background: #0b3d91; color: white; }
tr:nth-child(even) { background: #f8f9fa; }
blockquote {
    border-left: 4px solid #f0ad4e;
    background: #fff8e6;
    padding: 8px 14px;
    margin: 12px 0;
    color: #5a4a1a;
}
img {
    max-width: 100%;
    display: block;
    margin: 14px auto;
    border: 1px solid #ddd;
}
hr { border: none; border-top: 1px solid #ddd; margin: 22px 0; }
.cover {
    text-align: center;
    padding-top: 80px;
    page-break-after: always;
}
.cover h1 {
    font-size: 36pt;
    border: none;
    color: #0b3d91;
    margin-bottom: 10px;
}
.cover .subtitle { font-size: 16pt; color: #555; margin-bottom: 40px; }
.cover .meta { font-size: 11pt; color: #777; line-height: 2; }
"""

COVER = f"""
<div class="cover">
    <h1>LiveTix</h1>
    <div class="subtitle">Plataforma Global de Venta de Boletos</div>
    <div class="subtitle" style="font-size:13pt;">System Design Challenge</div>
    <div class="meta">
        <p><strong>Autor:</strong> Bruno Moutinho</p>
        <p><strong>Rol:</strong> Cloud Engineer Senior</p>
        <p><strong>Fecha:</strong> {datetime.now().strftime('%d de %B de %Y')}</p>
        <p><strong>Nube:</strong> AWS (3 regiones, 3 continentes)</p>
    </div>
</div>
"""


def md_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "attr_list"],
    )


def build():
    parts = [COVER]

    for doc in DOCUMENTS:
        if not doc.exists():
            print(f"AVISO: no existe {doc} (saltando)")
            continue
        print(f"Procesando: {doc.name}")
        parts.append(md_to_html(doc.read_text(encoding="utf-8")))

    if DIAGRAMS:
        parts.append("<h1>Diagrama de Arquitectura</h1>")
        for img in DIAGRAMS:
            if img.exists():
                parts.append(f'<img src="file://{img}" alt="{img.stem}"/>')
                print(f"Diagrama incluido: {img.name}")

    full_html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/></head>
<body>{''.join(parts)}</body></html>"""

    html_file = DOCS / "LiveTix-Entrega.html"
    html_file.write_text(full_html, encoding="utf-8")

    pdf_file = DOCS / "LiveTix-Entrega.pdf"
    HTML(string=full_html, base_url=str(ROOT)).write_pdf(
        pdf_file, stylesheets=[CSS(string=CSS_STYLE)]
    )
    print(f"\nOK: PDF generado en {pdf_file}")


if __name__ == "__main__":
    build()
