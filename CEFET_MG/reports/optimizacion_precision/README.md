# Reproducción de la optimización de precisión

Desde la raíz CEFET_MG y con los paquetes fijados de requirements.txt:

```powershell
$env:PYTHONIOENCODING='utf-8'
../.venv/Scripts/python.exe -m src.precision_study
../.venv/Scripts/python.exe -m src.precision_extend
../.venv/Scripts/python.exe -m src.precision_diagnostics
../.venv/Scripts/python.exe -m src.precision_reporting
../.venv/Scripts/python.exe -m pytest -q tests | Out-File -Encoding utf8 reports/optimizacion_precision/tests.txt
../.venv/Scripts/python.exe -m src.precision_reporting
```

Si el entorno está dentro de CEFET_MG, sustituir ../.venv por .venv. No ejecutar los
comandos de primera etapa: este flujo sólo escribe optimizacion_precision y sus propios logs.
El primer comando reproduce las once familias iniciales y sus variantes; el segundo añade
las cinco familias locales y variantes adaptativas declaradas. No usar métricas de esta
búsqueda como validación externa. config.json, environment.json y code_manifest.json
registran configuración, versiones y huellas. Cada ajuste principal se repite en diagnostics;
reproducibility.json compara parámetros exactos. No se repitió toda la búsqueda CV una
segunda vez: la comprobación repetida se limita a ajustes principales y al perfil elegido.

Leer modelo_recomendado.md, diagnostico_modelos.md y validacion_comparativa.md.
No se sustituyen los informes, parámetros ni figuras de la primera etapa.
