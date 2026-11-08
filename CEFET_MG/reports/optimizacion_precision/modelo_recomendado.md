# Modelo recomendado y decisión

**Recomendación local provisional: P_D_bomba_monotona__retardo.** Menor peor NRMSE medio CV bruto:
P_D_bomba_monotona__retardo. Se prefiere menor complejidad entre candidatos con balance condicional dentro
de 1% relativo del mejor peor NRMSE CV. Las cifras no demuestran óptimo global ni validación externa.
La topología, los caudales absolutos y el mecanismo de bomba siguen sin estar confirmados.

| model | RMSE_h1 | RMSE_h2 | NRMSE_h1 | NRMSE_h2 | CV_peor_NRMSE | Conservacion |
|---|---|---|---|---|---|---|
| P_D_bomba_monotona__retardo | 0.84433 | 0.30306 | 0.14109 | 0.099095 | 0.12624 | Balance efectivo; topología hipotética |

Mejora porcentual del RMSE (positivo=mejora; negativo=empeora):

| model | mejora_RMSE_pct_vs_C_bomba_h1 | mejora_RMSE_pct_vs_C_bomba_h2 | mejora_RMSE_pct_vs_D_conservativo_h1 | mejora_RMSE_pct_vs_D_conservativo_h2 |
|---|---|---|---|---|
| P_D_bomba_monotona__retardo | 21.876 | -12.809 | 32.776 | 61.862 |

Parámetros y configuración en `selection.json` y `parameters.csv`. Las escalas principales
se mantienen en 5.98415640 cm y 3.05827325 cm. La familia no se recomienda para
desbordamiento, vaciado ni arranque; es una representación local con caudales efectivos.

## Respuestas finales

1. Menor NRMSE principal h1: 0.14109481, modelo P_D_bomba_monotona__retardo.
2. Menor NRMSE principal h2: 0.07678983, modelo U_bomba_carga_monotona__actuador.
   Son mínimos descriptivos de una búsqueda y pueden pertenecer a candidatos distintos.
3. ¿Se consiguió mejorar simultáneamente a C? Candidatos que mejoran ambos tanques tanto
   en principal como en CV: U_bomba_carga_monotona__retardo, U_bomba_carga_monotona__actuador.
   Mejor peor NRMSE CV entre ellos: U_bomba_carga_monotona__retardo.
   El recomendado por menor peor error global mejora simultáneamente: principal False; CV False.
4. Reducción RMSE frente a C: h1=+0.236430 cm;
   h2=-0.034412 cm. Frente a D, ver tabla y CSV comparativo.
5. Menor error según peor NRMSE medio CV: P_D_bomba_monotona__retardo; no equivale al mínimo separado de cada tanque.
6. Ningún candidato tiene topología real verificada. D tiene una hipótesis global más restrictiva;
   Q/R/T/U tienen balances locales explícitos; S es una realización empírica. Conservar balance
   algebraico no da por sí solo mayor respaldo experimental.
7. Es posible escribir balances locales con precisión comparable a C (T es algebraicamente
   equivalente en el dominio sin recorte), pero esa equivalencia no demuestra una nueva ley
   física. La mejora adicional se cuantifica arriba, sin confundirla con identificación del circuito.
8. La estabilidad entre corridas está documentada por CV y por métricas individuales.
   Compartir la señal limita la generalización; comparar también excitación y recuperación.
9. Revisar ACF y sesgos en el informe de bondad: una reducción de RMSE no vuelve independientes
   los residuos. Los p-valores se reportan sólo como diagnóstico descriptivo.
10. Limitan la reducción: cuantización y dispersión experimental, curva de bomba desconocida,
    pérdidas no medidas, sincronización, posible deriva y ambigüedad de parámetros físicos.
    No se atribuye una causa única ni se declara alcanzado un límite teórico de error.
11. Sí, se necesita otra secuencia experimental y documentación del montaje para sustentar
    generalización y distinguir hipótesis de bomba/conexión que producen niveles similares.
12. Para escenarios académicos locales usar provisionalmente P_D_bomba_monotona__retardo, con la misma
    saturación de señal y alcance observado, contrastándolo con C/D. Sus resultados serán
    contrafactuales simulados. No declarar funcionamiento real de una política no ensayada.

Frontera de Pareto principal (dos NRMSE): P_D_bomba_monotona__retardo, U_bomba_carga_monotona__retardo, U_bomba_carga_monotona__actuador.
Todos los candidatos descartados y variantes se conservan en los CSV y figuras.
No se desarrolló AgentPy, Streamlit ni presentación.


## Alternativa que mejora simultáneamente ambos tanques

| model | RMSE_h1 | RMSE_h2 | NRMSE_h1 | NRMSE_h2 | CV_peor_NRMSE | Conservacion |
|---|---|---|---|---|---|---|
| U_bomba_carga_monotona__retardo | 0.87253 | 0.24169 | 0.14581 | 0.079027 | 0.1297 | Balance local; conductancias efectivas |
| U_bomba_carga_monotona__actuador | 0.88186 | 0.23484 | 0.14737 | 0.07679 | 0.13005 | Balance local; conductancias efectivas |

| model | mejora_RMSE_pct_vs_C_bomba_h1 | mejora_RMSE_pct_vs_C_bomba_h2 | mejora_RMSE_pct_vs_D_conservativo_h1 | mejora_RMSE_pct_vs_D_conservativo_h2 |
|---|---|---|---|---|
| U_bomba_carga_monotona__retardo | 19.267 | 10.035 | 30.531 | 69.585 |
| U_bomba_carga_monotona__actuador | 18.404 | 12.582 | 29.788 | 70.447 |

La elección tiene un compromiso explícito: P_D_bomba_monotona__retardo minimiza el peor error con
menos parámetros; U_bomba_carga_monotona__retardo es la opción si se exige que ninguno de los dos tanques
empeore frente a C. Para escenarios que prioricen esa mejora conjunta, usar U_bomba_carga_monotona__retardo
como alternativa local y contrastarla con la recomendación parsimoniosa. No ocultar
la mayor complejidad ni confundir el desfase efectivo con un retardo físico medido.
