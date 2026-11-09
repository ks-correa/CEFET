# CEFET-MG — Guía de ejecución y reproducción

> Para la presentación completa del proyecto, ecuaciones, parámetros calibrados y tablas de resultados, consultar el [`README.md` principal del repositorio](../README.md).

## 1. Ejecutar el simulador vigente

Desde este directorio (`CEFET_MG/`) en **PowerShell**:

```powershell
.\iniciar_entrega_final.ps1
```

O ejecutando directamente con el intérprete del entorno virtual:

```powershell
..\.venv\Scripts\python.exe -m streamlit run app_final.py --server.address=127.0.0.1 --server.port=8501
```

- **Punto de entrada vigente:** [`app_final.py`](app_final.py) (implementa los escenarios vigentes `E0` experimental, `E1` señal atenuada, `E2` bombeo constante al 50 % y `S_HIST` como complemento histórico).
- **Archivo histórico para pruebas:** `app.py` y `src/scenarios.py` se conservan únicamente porque son verificados por las pruebas de regresión histórica (`tests/test_simulator.py` y manifiestos SHA-256); no constituyen el punto de entrada de la entrega final.

## 2. Ubicación de los datos y resultados vigentes

- **Datos experimentales originales:** [`data/raw/`](data/raw/) (`complete_data.csv`, `h1.csv`, `h2.csv`, `U.csv`, [`README.md`](data/raw/README.md)).
- **Corridas procesadas y auditoría:** [`data/processed/`](data/processed/) (`run_01.csv` a `run_10.csv`, `run_mapping.csv`, `audit.json`, `sha256.json`).
- **Documentación final vigente:** [`docs/consolidacion_final/`](docs/consolidacion_final/) (incluye [`anexos_A_B_C.md`](docs/consolidacion_final/anexos_A_B_C.md), [`modelo_y_variables.md`](docs/consolidacion_final/modelo_y_variables.md), [`protocolo_vigente.md`](docs/consolidacion_final/protocolo_vigente.md), [`escenarios_resultados_decision.md`](docs/consolidacion_final/escenarios_resultados_decision.md), [`solidez_y_limitaciones.md`](docs/consolidacion_final/solidez_y_limitaciones.md) e [`indice_versiones.md`](docs/consolidacion_final/indice_versiones.md)).
- **Resultados y evidencias vigentes:** [`reports/consolidacion_final/`](reports/consolidacion_final/) ([`informe_final.md`](reports/consolidacion_final/informe_final.md), [`informe_cumplimiento.md`](reports/consolidacion_final/informe_cumplimiento.md), `comparacion_principal.csv`, `parametros_U_vigentes.csv`, `validacion_U_sin_cambios.csv`, `robustez/` y `figures/`).
- **Calibración y selección del modelo `U` (30 variantes):** [`reports/optimizacion_precision/`](reports/optimizacion_precision/) (`all_fits.json`, `fit_U_bomba_carga_monotona__retardo.json`, `metrics.csv`, `figures/`).

## 3. Ejecutar pruebas y reproducir resultados vigentes (sin recalibrar `U`)

```powershell
# Ejecutar las 46 pruebas automatizadas
..\.venv\Scripts\python.exe -m pytest -q tests

# Reproducir las 19 comparaciones nominales, las 90 exploraciones de sensibilidad y la documentación vigente
..\.venv\Scripts\python.exe -m src.final_consolidation
..\.venv\Scripts\python.exe -m src.final_documentation
```

*(Si el entorno `.venv` está dentro de `CEFET_MG/`, sustituir `..\.venv` por `.\.venv`).*
