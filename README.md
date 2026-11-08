# S35 - Evidencia de aprendizaje 2. Optimizando la productividad en el mundo del software

**Estudiante:** Daniela Lozano Morales.  **Asignatura:** Programación para Análisis de Datos.  **Año:** 2026.

## Objetivo
Continuar la Evidencia 1 (Mercado Libre / Samsung Galaxy S24) y practicar Git, GitHub, pruebas automatizadas y CI/CD con GitHub Actions. El proyecto **no consulta automáticamente Mercado Libre**. Usa un HTML de demostración sintético para que la evaluación sea reproducible y respete las restricciones de acceso de terceros.

## Estructura
- `src/scraper.py`: identifica tarjetas HTML, títulos, precios y enlaces, y exporta CSV.
- `src/dashboard.py`: construye un sitio estático con la tabla.
- `tests/fixtures/ofertas_s24_demo.html`: HTML **ficticio**, no extraído de Mercado Libre.
- `tests/test_*.py`: siete pruebas automáticas.
- `main.py`: ejecutable principal.
- `.github/workflows/ci-cd.yml`: flujo de integración y despliegue continuos.
- `docs/`: archivos de salida publicados por GitHub Pages.

