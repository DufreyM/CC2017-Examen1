"""Convierte un archivo Markdown a PDF usando python-markdown + xhtml2pdf."""
import sys
import markdown
from xhtml2pdf import pisa

CSS = """
<style>
@page { size: letter; margin: 2cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #1a1a1a; }
h1 { font-size: 18pt; margin-top: 0; }
h2 { font-size: 14pt; margin-top: 18pt; border-bottom: 1pt solid #888; padding-bottom: 3pt; }
h3 { font-size: 12pt; margin-top: 14pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; }
th, td { border: 0.5pt solid #999; padding: 4pt 6pt; font-size: 9.5pt; }
th { background-color: #e8e8e8; }
code { font-family: Courier, monospace; background-color: #f2f2f2; padding: 1pt 3pt; font-size: 9pt; }
pre { font-family: Courier, monospace; background-color: #f2f2f2; padding: 6pt; font-size: 8.5pt;
      white-space: pre-wrap; border: 0.5pt solid #ccc; }
blockquote { border-left: 2pt solid #999; margin: 6pt 0; padding-left: 10pt; color: #333; }
ol, ul { margin-top: 4pt; margin-bottom: 4pt; }
</style>
"""


def convertir(ruta_md, ruta_pdf):
    with open(ruta_md, "r", encoding="utf-8") as f:
        texto_md = f.read()

    cuerpo_html = markdown.markdown(
        texto_md, extensions=["tables", "fenced_code", "sane_lists"]
    )
    html_completo = f"<html><head>{CSS}</head><body>{cuerpo_html}</body></html>"

    with open(ruta_pdf, "wb") as f:
        resultado = pisa.CreatePDF(html_completo, dest=f, encoding="utf-8")

    if resultado.err:
        print(f"Hubo {resultado.err} error(es) al generar {ruta_pdf}")
    else:
        print(f"PDF generado: {ruta_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python convertir_a_pdf.py entrada.md salida.pdf")
        sys.exit(1)
    convertir(sys.argv[1], sys.argv[2])
