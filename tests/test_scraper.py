from pathlib import Path

from src.scraper import detectar_variante, exportar_csv, parsear_ofertas, precio_a_entero

FIXTURE = Path(__file__).parent / "fixtures" / "ofertas_s24_demo.html"


def test_extraer_cuatro_registros_de_html_sintetico():
    ofertas = parsear_ofertas(FIXTURE.read_text(encoding="utf-8"), url_base="https://example.org/")
    assert len(ofertas) == 4
    assert ofertas[0]["precio_cop"] == 3499900
    assert ofertas[0]["enlace"] == "https://example.org/catalogo/ejemplo-01"
    assert all("sintéticos" in registro["origen"] for registro in ofertas)


def test_identificar_variante():
    assert detectar_variante("Samsung Galaxy S24 Ultra") == "S24 Ultra"
    assert detectar_variante("Samsung Galaxy S24 Plus") == "S24 Plus"
    assert detectar_variante("Samsung Galaxy S24 FE") == "S24 FE"
    assert detectar_variante("Samsung Galaxy S24 256 GB") == "S24"


def test_precios_cop():
    assert precio_a_entero("$3.499.900") == 3499900
    assert precio_a_entero("sin precio") is None


def test_sin_datos_reales_no_inventa_registros():
    assert parsear_ofertas("<html><body>Sin tarjetas de producto</body></html>") == []


def test_no_acepta_precio_vacio_y_deduplica():
    html = """<li class="poly-card"><a href="/p">S24</a><h2>S24</h2><span class="andes-money-amount__fraction">3500</span></li>
    <li class="poly-card"><a href="/p">S24</a><h2>S24</h2><span class="andes-money-amount__fraction">3500</span></li>
    <li class="poly-card"><a href="/sin">S24</a><h2>S24</h2><span class="andes-money-amount__fraction">-</span></li>"""
    assert len(parsear_ofertas(html)) == 1


def test_exportar_csv_utf8(tmp_path):
    registros = parsear_ofertas(FIXTURE.read_text(encoding="utf-8"))
    ruta = tmp_path / "datos.csv"
    exportar_csv(registros, ruta)
    contenido = ruta.read_text(encoding="utf-8-sig")
    assert "precio_cop" in contenido
    assert "3499900" in contenido
    assert len(contenido.splitlines()) == 5
