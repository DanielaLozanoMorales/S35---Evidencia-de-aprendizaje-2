"""Extrae datos de una copia HTML de demostración o de origen autorizado.

No hace peticiones web ni evade bloqueos. El HTML debe obtenerse por medios
permitidos. Los datos incluidos en tests/fixtures son sintéticos.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

FIELDS = ["producto", "variante", "precio_cop", "enlace", "origen"]
SELECTOR_CARDS = "li.poly-card, li.ui-search-layout__item, div.ui-search-result__wrapper"
SELECTOR_TITLES = "h2.ui-search-item__title, a.poly-component__title, h2"
SELECTOR_PRICE = "span.andes-money-amount__fraction"


def detectar_variante(nombre: str) -> str:
    n = nombre.casefold()
    if "s24 ultra" in n:
        return "S24 Ultra"
    if "s24 plus" in n or "s24+" in n:
        return "S24 Plus"
    if "s24 fe" in n:
        return "S24 FE"
    return "S24" if "s24" in n else "Otro"


def precio_a_entero(texto: str) -> int | None:
    """Convierte COP con separadores de miles, ej. '3.499.900' a 3499900."""
    limpio = re.sub(r"[^0-9]", "", texto)
    return int(limpio) if limpio else None


def parsear_ofertas(html: str, *, url_base: str = "https://example.org/", origen: str = "Demostración (datos sintéticos)") -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    ofertas = []
    enlaces_vistos = set()

    for tarjeta in soup.select(SELECTOR_CARDS):
        titulo = tarjeta.select_one(SELECTOR_TITLES)
        precio = tarjeta.select_one(SELECTOR_PRICE)
        enlace = tarjeta.select_one("a.poly-component__title[href], a[href]")
        if not (titulo and precio and enlace):
            continue
        nombre = titulo.get_text(" ", strip=True)
        valor = precio_a_entero(precio.get_text(" ", strip=True))
        href = urljoin(url_base, enlace.get("href", "").strip())
        if not nombre or valor is None or valor <= 0 or urlsplit(href).scheme not in ("http", "https"):
            continue
        if href in enlaces_vistos:
            continue
        enlaces_vistos.add(href)
        ofertas.append({
            "producto": nombre,
            "variante": detectar_variante(nombre),
            "precio_cop": valor,
            "enlace": href,
            "origen": origen,
        })
    return ofertas


def leer_html(ruta: Path) -> str:
    return Path(ruta).read_text(encoding="utf-8")


def exportar_csv(ofertas: list[dict], ruta: Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=FIELDS)
        escritor.writeheader()
        escritor.writerows(ofertas)
