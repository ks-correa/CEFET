# Evidencias preparadas para las 13 diapositivas

No se produce todavía la presentación definitiva. Las rutas figures/ de esta tabla están en reports/simulador/.

| n | diapositiva | evidencia | nota |
|---|---|---|---|
| 1 | Portada | docs/anexos_proyecto.md | Completar nombres y fecha de sustentación |
| 2 | Problema y pregunta | docs/definicion_problema.md | Decisión local de regulación |
| 3 | Esquema del sistema | assets/tanks.html; figures/aplicacion_sistema.png | Esquema conceptual; topología no certificada |
| 4 | Datos reales | data/raw/README.md; reports/auditoria_dataset.md | Mediciones de investigadores; sin fotos propias |
| 5 | Variables y parámetros | reports/simulador/parametros_U.csv; docs/anexos_proyecto.md | Valores exactos y unidades efectivas |
| 6 | Modelo matemático | src/precision_models.py (código 15); docs/modelo_matematico.md | Balances locales, no volumen absoluto certificado |
| 7 | Implementación | src/simulation_engine.py; reports/simulador/tests.txt | RK4 reutilizado; entrada causal con δ=2 s |
| 8 | Calibración | reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json | No se reajustó para escenarios |
| 9 | Validación | reports/simulador/regresion_U.csv | Medias por corrida; evaluación interna previamente examinada |
| 10 | Escenarios | docs/protocolo_escenarios.md | E0/E1/E2 y reglas fijadas antes de ejecutar |
| 11 | Resultados | reports/simulador/comparacion_escenarios.csv; figures/escenarios_excitacion.png | Indicadores de regulación, distintos de errores predictivos |
| 12 | Decisión y limitaciones | reports/simulador/resultados_y_decision.md | E1 según regla; compensaciones, sin prueba física |
| 13 | Referencias y evidencias | Zenodo DOI 10.5281/zenodo.19856119; reports/simulador/integridad.json | Autoría externa; reproducibilidad y pruebas |

Ambos estudiantes deben ejecutar el análisis, explicar las ecuaciones y distinguir métricas predictivas de regulación. No se certifica un ensayo de sustentación que aún no realizaron.
