from src.dashboard import construir_dashboard


def test_dashboard_genera_html(tmp_path):
    destino = tmp_path / "index.html"
    ofertas = [{"producto":"Samsung S24 <demo>", "variante":"S24", "precio_cop":3499900,
                "enlace":"https://example.org/1", "origen":"Demostración (datos sintéticos)"}]
    construir_dashboard(ofertas, destino)
    texto = destino.read_text(encoding="utf-8")
    assert "<!doctype html>" in texto
    assert "3.499.900" in texto
    assert "Samsung S24 &lt;demo&gt;" in texto
    assert "Datos sintéticos" in texto
