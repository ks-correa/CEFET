# Dictamen técnico de viabilidad

**VIABLE CON LIMITACIONES para reproducción local de las corridas completas disponibles.**
No equivale a aprobación docente ni autoriza conclusiones sobre otros regímenes.

1. Hay mediciones de ambos tanques atribuidas a un montaje físico por los investigadores.
2. Procedencia y unidades cm/% verificadas en README y [Zenodo](https://zenodo.org/records/19856119).
3. El acoplamiento está documentado, pero el circuito hidráulico preciso no: falta esquema primario.
4. Balances B,D coherentes bajo una hipótesis explícita; A,C son aproximaciones locales.
5. Se estiman parámetros efectivos; no áreas ni caudales absolutos por separado.
6. RK4 se contrastó con solución lineal exacta, convergencia y DOP853.
7. Cumplimiento por cada corrida de evaluación principal y CV, tanto completa como excitación:
   {"A_lineal": false, "B_hidraulico": false, "C_bomba": true, "D_conservativo": true}. La preferencia parsimoniosa según protocolo es **D_conservativo**;
   C es la alternativa predictiva con menor error, no un reemplazo oculto del modelo conservativo.
8. MAE/RMSE/NRMSE principales por tanque y modelo:

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| C_bomba | h1 | 0.76006 | 1.0808 | 0.1806 | -0.28408 |
| C_bomba | h2 | 0.2061 | 0.26865 | 0.087843 | 0.13059 |
| D_conservativo | h1 | 0.92948 | 1.256 | 0.20989 | 0.10485 |
| D_conservativo | h2 | 0.67855 | 0.79464 | 0.25983 | 0.45557 |

9. Hay sesgos y autocorrelación residual; la precisión escalar no demuestra ruido blanco.
10. C y D superan persistencia y equilibrio; también mejoran A. Ver tabla completa en bondad de ajuste.
11. Funcionan en las excitaciones repetidas observadas y recuperación, con calibración completa.
12. Fallan en arranque y en la prueba temporal de h2 al ajustar únicamente primeros 320 s.
13. Evidencia interna previamente examinada; CV reproduce estabilidad entre repeticiones de
la misma señal, no validación ciega ni externa. No se seleccionó ventana favorable para ocultar fallas.
14. Faltan nuevas entradas independientes, plano del circuito, áreas, curva de bomba y
metadatos de sensores. Debe confirmarse con el docente la aceptación de datos de terceros.

La siguiente etapa exige acotar escenarios al régimen observado, mantener explícita la
hipótesis de circuito y distinguir contrafactuales de mediciones. Este entregable se limita
a la primera etapa solicitada: no se construyó Streamlit, AgentPy ni las 13 diapositivas.
La suficiencia temporal no se declara resuelta: si se exige calibrar sólo 320 s, el dictamen
para ese protocolo específico es NO VIABLE con estos candidatos.
