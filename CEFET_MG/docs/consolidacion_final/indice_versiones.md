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
   - **Archivos:** `reports/auditoria_dataset.md`, `reports/bondad_ajuste.md`, `reports/viabilidad.md`, `reports/calibration.json`, `reports/metrics.csv`, `reports/robustness.csv`, `reports/figures/` y `docs/protocolo_previo.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/definicion_problema.md`, `docs/modelo_matematico.md`, `docs/registro_decisiones.md`.
   - **Reproducción histórica:** `python -m src.experiments`, `python -m src.robustness`, `python -m src.reproduce`, `python -m src.reporting`.

2. **Etapa 2 — Campaña de optimización de precisión (30 variantes y selección del modelo `U`):**
   - **Archivos:** `reports/optimizacion_precision/` (`all_fits.json`, `fit_U_bomba_carga_monotona__retardo.json`, `metrics.csv`, `sensitivity.csv`, `residual_diagnostics.json`, `modelo_recomendado.md`, `validacion_comparativa.md`, `figures/`, `predictions/`) y `docs/protocolo_optimizacion.md`.
   - **Reproducción histórica:** documentada en [`reports/optimizacion_precision/README.md`](../../reports/optimizacion_precision/README.md) (`src.precision_study`, `src.precision_extend`, `src.precision_diagnostics`, `src.precision_reporting`).

3. **Etapa 3 — Simulador preliminar con conjunto restringido de escenarios:**
   - **Archivos:** `app.py`, `src/scenarios.py`, `reports/simulador/` y `docs/protocolo_escenarios.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/anexos_proyecto.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/evidencias_13_diapositivas.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/guia_simulador.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/matriz_cumplimiento_guia.md`.
   - **Contexto metodológico:** en aquella fase preliminar, `E2` designaba el suavizado causal de $10\text{ pp}/4\text{ s}$ (hoy `S_HIST`) y `E1` obtuvo la recomendación dentro de ese conjunto restringido. Dichos documentos no representan la recomendación nominal vigente.

4. **Etapa 3.5 — Diagnóstico de control constante (`D50`) y ablación de media:**
   - **Archivos:** `reports/diagnostico_control_constante/` (`informe_diagnostico.md`, `comparacion_complementaria.csv`, `ablacion_media.csv`, `interpretacion_media.csv`, `figures/`) y `docs/protocolo_diagnostico_constante.md`, `https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/esquema_13_diapositivas_revisado.md`.
   - **Contexto metodológico y reproducción:** demostró que la operación constante al $50\%$ (`D50`, hoy `E2` vigente) evita excitar desviaciones respecto al equilibrio nominal incorporado en `U` y motivó la revisión retrospectiva documentada en [`registro_metodologico.md`](registro_metodologico.md). Comandos de reproducción aislada: `python -m src.constant_control_diagnostic` y `python -m src.constant_control_reporting`.


## Depuraci?n documental e integridad vigente

Se retiraron siete documentos redundantes: LEEME_PRIMERO.md, anexos_proyecto.md,
definicion_problema.md, evidencias_13_diapositivas.md,
esquema_13_diapositivas_revisado.md, guia_simulador.md y matriz_cumplimiento_guia.md.
La gu?a r?pida est? en README; los anexos, problema, esquema y cumplimiento vigentes
est?n en este directorio. El registro de hashes de LEEME est? duplicado en
`data/processed/sha256.json`; las pruebas conservan tambi?n la comprobaci?n de su
contenido archivado. Se conservan los protocolos, modelos hist?ricos e informes de
optimizaci?n porque explican estructuras, variantes y resultados espec?ficos.

La etiqueta anotada publicada `cefet-archivo-cientifico-completo` apunta a
`444042936475cd204576d6488f7599993ee98636`, con los 44 Markdown y manifiestos originales.
Para recuperar y comprobar la versi?n completa, usar un checkout separado:

```powershell
git fetch origin tag cefet-archivo-cientifico-completo
git worktree add ../CEFET-historico cefet-archivo-cientifico-completo
```

Los cinco manifiestos hist?ricos no se editan. Las cinco pruebas de integridad
ahora verifican en Git los bytes documentales retirados o actualizados de forma
expl?cita en `reports/consolidacion_final/integridad_vigente.json`; para el resto
siguen comprobando los archivos locales. Git aplica sus filtros de checkout porque
los manifiestos originales se calcularon sobre CRLF en Windows. Es necesario disponer
de Git y de la etiqueta local; no se omiten archivos ausentes ni hashes discordantes.
La nueva prueba de integridad vigente comprueba todos los archivos conservados
registrados, incluidas las pruebas y los generadores adaptados. Su cobertura es
complementaria a los manifiestos originales. Los valores cient?ficos esperados
no cambian. Los generadores hist?ricos omiten los siete documentos retirados y
sus metadatos enlazan la versi?n hist?rica recuperable cuando corresponde.
