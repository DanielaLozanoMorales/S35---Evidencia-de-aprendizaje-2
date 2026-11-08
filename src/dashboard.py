"""Genera una página HTML estática sin bibliotecas JavaScript externas."""
from __future__ import annotations

from html import escape
from pathlib import Path
from urllib.parse import urlsplit


def _cop(n: int) -> str:
    return "$" + format(n, ",").replace(",", ".")


def construir_dashboard(ofertas: list[dict], salida: Path) -> None:
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    filas = []
    for fila in ofertas:
        titulo = escape(str(fila["producto"]))
        variante = escape(str(fila["variante"]))
        precio = _cop(int(fila["precio_cop"]))
        href = str(fila["enlace"])
        link = f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">Ver ejemplo</a>' if urlsplit(href).scheme in ("http", "https") else 'Sin enlace'
        filas.append(f"<tr><td>{titulo}</td><td>{variante}</td><td>{precio}</td><td>{link}</td></tr>")
    tabla = "\n".join(filas) if filas else '<tr><td colspan="4">No hay datos para mostrar.</td></tr>'
    html = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Observatorio S24 | Evidencia 2</title>
<style>
:root{font-family:Arial,Helvetica,sans-serif;color:#15334a;background:#edf3f8}
body{margin:0}header{background:linear-gradient(115deg,#012a40,#543b8c);color:#fff;padding:42px 8%}
h1{font-size:2.2rem;margin:5px 0}header p{opacity:.9;max-width:800px;line-height:1.6}
main{max-width:1100px;margin:30px auto;padding:0 20px}section{background:white;padding:24px;border-radius:14px;box-shadow:0 5px 22px #17364d12}
.tag{display:inline-block;background:#f9e92f;color:#293b45;font-weight:700;padding:7px 12px;border-radius:30px;font-size:.8rem}
.info{background:#fff4d4;border-left:4px solid #c68f1b;padding:14px;margin:20px 0;line-height:1.5}
.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:650px}th{text-align:left;background:#dbe8f3}
th,td{padding:15px;border-bottom:1px solid #e2eaf1}a{color:#543b8c}footer{text-align:center;color:#576d7f;padding:28px}
</style></head><body>
<header><span class="tag">PROTOTIPO ACADÉMICO · DEVOPS</span><h1>Observatorio de ofertas Samsung Galaxy S24</h1>
<p>Continuación de la Evidencia de aprendizaje 1. Procesamiento HTML con Python y BeautifulSoup, control de versiones con Git y CI/CD en GitHub Actions.</p></header>
<main><div class="info"><strong>Datos sintéticos de demostración.</strong> Los precios, nombres y vínculos de esta página son ejemplos preparados para verificar el flujo técnico; no representan publicaciones ni precios vigentes en Mercado Libre. No se realiza scraping en vivo.</div>
<section><h2>Tabla de ofertas de prueba</h2><p>Registros procesados: <strong>__TOTAL__</strong>. Las variantes S24, Plus, Ultra y FE no son productos idénticos; no deben compararse como si lo fueran.</p>
<div class="table-scroll"><table><thead><tr><th>Producto</th><th>Variante</th><th>Precio ilustrativo (COP)</th><th>Enlace ficticio</th></tr></thead><tbody>__FILAS__</tbody></table></div></section>
</main><footer>Proyecto académico de programación, pruebas y despliegue. No afiliado a Mercado Libre ni Samsung.</footer></body></html>"""
    salida.write_text(html.replace("__TOTAL__", str(len(ofertas))).replace("__FILAS__", tabla), encoding="utf-8")
