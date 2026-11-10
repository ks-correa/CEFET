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

Los siguientes directorios y documentos corresponden a etapas previas de investigación y desarrollo. Los archivos científicos conservados permanecen **íntegros byte a byte**; los documentos retirados o actualizados se recuperan de la etiqueta histórica. Estos antecedentes sustentan la trazabilidad metodológica y sus huellas SHA-256 son verificadas automáticamente por la batería de pruebas (`tests/test_project.py`, `tests/test_precision.py`, `tests/test_simulator.py`, `tests/test_constant_diagnostic.py` y `tests/test_final_consolidation.py`):

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


## Depuración documental e integridad vigente (9 de noviembre de 2026)

Se revisaron los 37 Markdown restantes y se conservan por su contenido experimental,
metodológico, de calibración, validación o evidencia de decisiones. No se impuso otra
cuota de eliminaciones. Resultado: **44 → 37 Markdown** (siete retirados).

| Documento retirado (relativo a CEFET_MG/) | Motivo y consulta vigente |
|---|---|
| LEEME_PRIMERO.md | Guía inicial sustituida por los README. Sus hashes originales siguen en data/processed/sha256.json; la prueba también comprueba el texto archivado. |
| docs/anexos_proyecto.md | Anexos preliminares sustituidos por anexos_A_B_C.md. Se conserva el contexto original en la etiqueta. |
| docs/definicion_problema.md | La definición vigente declara el alcance y la revisión retrospectiva. |
| docs/esquema_13_diapositivas_revisado.md | Esquema preliminar sustituido por esquema_definitivo_13.md. |
| docs/evidencias_13_diapositivas.md | Las fuentes verificables están en el esquema vigente y sus metadatos JSON. |
| docs/guia_simulador.md | La ejecución y reproducción están en los README vigentes. |
| docs/matriz_cumplimiento_guia.md | La matriz vigente y los anexos recogen los requisitos actuales. |

La etiqueta anotada y publicada
[cefet-archivo-cientifico-completo](https://github.com/ks-correa/CEFET/tree/cefet-archivo-cientifico-completo)
apunta a `444042936475cd204576d6488f7599993ee98636`. Conserva los 44 Markdown,
los manifiestos originales y las pruebas anteriores. Para recuperar la versión completa:

```powershell
git fetch origin tag cefet-archivo-cientifico-completo
git worktree add ../CEFET-historico cefet-archivo-cientifico-completo
Set-Location ../CEFET-historico/CEFET_MG
# Usar el Python del entorno científico instalado, sin recalibrar:
python -m pytest -q tests
```

Los manifiestos `manifest_historico.json`, `original_manifest.json`, `manifest_previo.json`,
`reports/simulador/integridad.json` y `data/processed/sha256.json` no se editan.
Las pruebas de final_consolidation, constant_diagnostic, precision y simulator siguen
recorriendo **todas** sus entradas: los archivos científicos se leen del checkout actual;
solamente las rutas documentales enumeradas en `integridad_vigente.json` se leen de la
etiqueta. La prueba de project comprueba los datos locales y los hashes citados en
LEEME_PRIMERO archivado. No se omiten ausentes ni discrepancias. Esto cambia el alcance:
la comprobación de esos antecedentes documentales es histórica, no del checkout vigente.

`test_current_integrity.py` complementa las pruebas originales: comprueba las huellas de
los archivos vigentes registrados, los siete documentos recuperables y el commit exacto
de la etiqueta. También exige cobertura de todos los archivos versionados (salvo el propio
manifiesto) y comprueba con datos temporales que un dataset ausente o alterado causa error.
Git es necesario y la etiqueta debe existir localmente. Los filtros de
checkout indicados por ruta permiten recuperar los bytes CRLF de los manifiestos de
Windows; para las rutas registradas sin filtros se recupera el blob original.
No se cambian expectativas científicas ni se recalibran modelos. El script de cierre
`record_final_delivery.py` utiliza la misma separación de integridad; sus evidencias de
46 pruebas siguen siendo históricas y no se presentan como la ejecución actual.

Los generadores omiten los siete documentos eliminados, redirigen sus referencias a
fuentes vigentes o a la etiqueta y conservan el comportamiento científico. La comprobación
actual y las razones de conservación por archivo están en
[auditoria_depuracion.json](../../reports/consolidacion_final/auditoria_depuracion.json).
Los registros históricos de pruebas y navegador se conservan sin sobrescribirlos.

Los ocho destinos de referencias se verifican desde las primeras ocho entradas de
Referencias del README principal: cinco rutas públicas de GitHub, Zenodo, SciPy y el
repositorio. **No hay un PowerPoint versionado en este repositorio**: se contrasta este
listado público y el campo source de la diapositiva 13 contra la etiqueta, sin afirmar
una inspección de hipervínculos de un PPTX externo. No se modifica la diapositiva 13.
