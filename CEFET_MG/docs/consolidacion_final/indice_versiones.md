# Índice de entrega y antecedentes históricos

## 1. Versión vigente de entrega final

- **Simulador interactivo:** [`app_final.py`](../../app_final.py) e [`iniciar_entrega_final.ps1`](../../iniciar_entrega_final.ps1).
- **Motor y escenarios vigentes:** [`src/simulation_engine.py`](../../src/simulation_engine.py) y [`src/final_scenarios.py`](../../src/final_scenarios.py).
- **Documentación vigente:** [`docs/consolidacion_final/`](.) (`definicion_problema.md`, `modelo_y_variables.md`, `rk4_calibracion_validacion.md`, `protocolo_vigente.md`, `escenarios_resultados_decision.md`, `solidez_y_limitaciones.md`, `anexos_A_B_C.md`, `registro_metodologico.md`, `indice_versiones.md`, `matriz_cumplimiento.md`, `esquema_definitivo_13.md`).
- **Resultados y evidencias vigentes:** [`reports/consolidacion_final/`](../../reports/consolidacion_final/) (`informe_final.md`, `informe_cumplimiento.md`, `comparacion_principal.csv`, `resumen_excitaciones.csv`, `parametros_U_vigentes.csv`, `validacion_U_sin_cambios.csv`, `decisiones_vigentes.json`, `suavizado_historico.csv`, `robustez/` y `figures/`).
- **Definición vigente de escenarios:**
  - **E0:** señal de bombeo experimental registrada.
  - **E1:** señal atenuada $50 + 0.80(u_0 - 50)$.
  - **E2:** bombeo constante al $50\%$ (equivalente al diagnóstico `D50`).
  - **S_HIST:** escenario histórico complementario (antiguo suavizado causal de $10\text{ pp}/4\text{ s}$).

---

## 2. Antecedentes históricos preservados por reproducibilidad y pruebas automatizadas

Los siguientes directorios y documentos corresponden a etapas previas de investigación y desarrollo. Se conservan **íntegros byte a byte** porque sustentan la trazabilidad metodológica y sus huellas SHA-256 son verificadas automáticamente por la batería de pruebas (`tests/test_project.py`, `tests/test_precision.py`, `tests/test_simulator.py`, `tests/test_constant_diagnostic.py` y `tests/test_final_consolidation.py`):

1. **Etapa 1 — Auditoría del dataset y línea base (`A_lineal`, `B_hidraulico`, `C_bomba`, `D_conservativo`):**
   - **Archivos:** `reports/auditoria_dataset.md`, `reports/bondad_ajuste.md`, `reports/viabilidad.md`, `reports/calibration.json`, `reports/metrics.csv`, `reports/robustness.csv`, `reports/figures/` y `docs/protocolo_previo.md`, `docs/definicion_problema.md`, `docs/modelo_matematico.md`, `docs/registro_decisiones.md`.
   - **Reproducción histórica:** `python -m src.experiments`, `python -m src.robustness`, `python -m src.reproduce`, `python -m src.reporting`.

2. **Etapa 2 — Campaña de optimización de precisión (30 variantes y selección del modelo `U`):**
   - **Archivos:** `reports/optimizacion_precision/` (`all_fits.json`, `fit_U_bomba_carga_monotona__retardo.json`, `metrics.csv`, `sensitivity.csv`, `residual_diagnostics.json`, `modelo_recomendado.md`, `validacion_comparativa.md`, `figures/`, `predictions/`) y `docs/protocolo_optimizacion.md`.
   - **Reproducción histórica:** documentada en [`reports/optimizacion_precision/README.md`](../../reports/optimizacion_precision/README.md) (`src.precision_study`, `src.precision_extend`, `src.precision_diagnostics`, `src.precision_reporting`).

3. **Etapa 3 — Simulador preliminar con conjunto restringido de escenarios:**
   - **Archivos:** `app.py`, `src/scenarios.py`, `reports/simulador/` y `docs/protocolo_escenarios.md`, `docs/anexos_proyecto.md`, `docs/evidencias_13_diapositivas.md`, `docs/guia_simulador.md`, `docs/matriz_cumplimiento_guia.md`.
   - **Contexto metodológico:** en aquella fase preliminar, `E2` designaba el suavizado causal de $10\text{ pp}/4\text{ s}$ (hoy `S_HIST`) y `E1` obtuvo la recomendación dentro de ese conjunto restringido. Dichos documentos no representan la recomendación nominal vigente.

4. **Etapa 3.5 — Diagnóstico de control constante (`D50`) y ablación de media:**
   - **Archivos:** `reports/diagnostico_control_constante/` (`informe_diagnostico.md`, `comparacion_complementaria.csv`, `ablacion_media.csv`, `interpretacion_media.csv`, `figures/`) y `docs/protocolo_diagnostico_constante.md`, `docs/esquema_13_diapositivas_revisado.md`.
   - **Contexto metodológico y reproducción:** demostró que la operación constante al $50\%$ (`D50`, hoy `E2` vigente) evita excitar desviaciones respecto al equilibrio nominal incorporado en `U` y motivó la revisión retrospectiva documentada en [`registro_metodologico.md`](registro_metodologico.md). Comandos de reproducción aislada: `python -m src.constant_control_diagnostic` y `python -m src.constant_control_reporting`.
