"""Compila la tabla CSV y un sitio estático desde un HTML de ejemplo."""
from __future__ import annotations

import argparse
from pathlib import Path

from src.dashboard import construir_dashboard
from src.scraper import exportar_csv, leer_html, parsear_ofertas


def main() -> None:
    p = argparse.ArgumentParser(description="Procesamiento HTML académico del Samsung Galaxy S24")
    p.add_argument("--input", type=Path, default=Path("tests/fixtures/ofertas_s24_demo.html"), help="HTML disponible de forma autorizada")
    p.add_argument("--csv", type=Path, default=Path("docs/datos_s24_demo.csv"))
    p.add_argument("--site", type=Path, default=Path("docs/index.html"))
    p.add_argument("--origen", default="Demostración (datos sintéticos)", help="Descripción verificable del origen de los datos")
    args = p.parse_args()
    ofertas = parsear_ofertas(leer_html(args.input), origen=args.origen)
    if not ofertas:
        raise SystemExit("No se encontraron ofertas válidas: no se publican datos inventados como si fueran extraídos.")
    exportar_csv(ofertas, args.csv)
    construir_dashboard(ofertas, args.site)
    print(f"OK: {len(ofertas)} registros de prueba -> {args.csv} y {args.site}")


if __name__ == "__main__":
    main()
