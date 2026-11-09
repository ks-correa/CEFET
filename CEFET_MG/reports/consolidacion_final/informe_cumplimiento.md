# Informe final de cumplimiento — fase 4

La implementación y el esquema están listos para revisión. No se generó PowerPoint. Se conservaron los protocolos y resultados históricos; el conjunto vigente se revisó retrospectivamente tras D50, sin modificar la regla ni recalibrar U.

**Resultado ejecutado:** 46 pruebas aprobadas (40 existentes y 6 nuevas), comprobación de tipos aprobada, API y navegador comprobados. Aplicación vigente: http://127.0.0.1:8501 (`app_final.py`; inicio reproducible con `iniciar_entrega_final.ps1`).

| Comprobación | Evidencia y alcance |
|---|---|
| Integridad de datos y antecedentes | Huellas SHA-256 de 707 archivos coinciden; pruebas históricas intactas. |
| Conservación de parámetros U | Configuración exacta conservada; sin ejecutar calibración ni seleccionar nuevos parámetros. |
| Reproducción de validación | Trayectorias de corridas 8–10 con diferencia máxima 0 cm frente a las predicciones archivadas. |
| Balances efectivos | Pruebas existentes de intercambio compartido y balance total aprobadas; no certifican volumen físico absoluto. |
| Causalidad | Retención causal, desfase y transformaciones comprobados; alterar entradas futuras no altera el prefijo. |
| Tres escenarios vigentes | E0 observado, E1 atenuación, E2 constante; 19 comparaciones, mismos horizontes y condiciones. S_HIST separado. |
| Correspondencia aplicación/resultados | AppTest nueve páginas; API HTTP; navegador: E2 coincide con RK4 y regla calculada. Servidor activo comprobado. |
| Consistencia documental | Documentos vigentes recomiendan E2 nominal y declaran revisión retrospectiva. Índice marca informes E1 como históricos preservados. |
| Reproducibilidad | Comparación reejecutada contra trayectorias e indicadores guardados; 46 pruebas aprobadas y tipos sin errores. |
| Guía docente | Guía contrastada; exactamente 13 diapositivas con ocho campos y fuentes. Esquema preparado; PPT y sustentación pendientes. |

## Decisión y límites

E2 constante al 50% fue elegida en 19 comparaciones nominales y 90 exploraciones pequeñas. Esta repetición no constituye validación externa ni demuestra optimalidad global. El equilibrio nominal está incorporado en U; sin demanda externa documentada, mantener el mando es una alternativa legítima. La señal original sirve para identificar la dinámica y no es una obligación operativa documentada.

La comparación histórica de medias E1/suavizado y su corrección permanecen en `reports/diagnostico_control_constante/`. No se atribuye toda la diferencia histórica a la suavidad: sus medias difieren. Suavizado y atenuación siguen siendo contrafactuales. Una demanda variable, consigna móvil o restricción de servicio podría exigir mando variable, pero no está documentada aquí.

El sesgo sostenido de −2 pp desplaza el equilibrio calculado a (44.056, 28.624) cm: no hay rechazo perfecto. Las exploraciones iniciales son ±1 cm y los pulsos ±2 pp durante 40 s, aplicados por igual. Se informan excursiones de E0/E1 fuera del rectángulo medido. No se acredita robustez física, ahorro eléctrico ni exactitud fuera del dominio examinado.

## Entregables y alcance documental

Esquema: `docs/consolidacion_final/esquema_definitivo_13.md`. Documentación vigente e historial: `docs/consolidacion_final/indice_versiones.md`. Anexos A, B y C: `docs/consolidacion_final/anexos_A_B_C.md`. Evidencia: `tests.txt`, `typecheck.txt`, `agent_checks.json`, `browser_checks.json`, `server_active.json`, `integridad.json` y figuras de este directorio.

Integrantes registrados en el Anexo A: Kevin Santiago Correa Acosta (67001271) y Santiago Cárdenas Rubio (67001160), asignatura Modelado y Simulación, Universidad Católica de Colombia, fecha 8 de noviembre de 2026. La autorización docente para el uso del dataset externo se registra según la comunicación de los estudiantes; no se inventa un acta firmada. No hay fotografías propias del montaje físico ni plano geométrico certificado.
