# Bondad de ajuste optimizada

Todos los candidatos, incluidos descartados, se evalúan con MAE/RMSE cm, NRMSE adimensional,
sesgo, máximo absoluto, R², error final y diferencia entre máximos. `metrics.csv` conserva
cada corrida, partición y fase. R² puede ser negativo. El error en máximos mide amplitud,
no sincronía temporal. Residuo=simulado−observado. No se corrige con niveles observados futuros.

Comparación principal completa:

| model | RMSE_h1 | RMSE_h2 | NRMSE_h1 | NRMSE_h2 | CV_peor_NRMSE | Conservacion |
|---|---|---|---|---|---|---|
| P_D_bomba_monotona__retardo | 0.84433 | 0.30306 | 0.14109 | 0.099095 | 0.12624 | Balance efectivo; topología hipotética |
| P_D_bomba_monotona__actuador | 0.84541 | 0.30356 | 0.14127 | 0.099257 | 0.12645 | Balance efectivo; topología hipotética |
| U_bomba_carga_monotona__retardo | 0.87253 | 0.24169 | 0.14581 | 0.079027 | 0.1297 | Balance local; conductancias efectivas |
| U_bomba_carga_monotona__actuador | 0.88186 | 0.23484 | 0.14737 | 0.07679 | 0.13005 | Balance local; conductancias efectivas |
| U_bomba_carga_monotona__minimax | 0.97494 | 0.50363 | 0.16292 | 0.16468 | 0.14806 | Balance local; conductancias efectivas |
| U_bomba_carga_monotona__regularizado | 0.97492 | 0.50381 | 0.16292 | 0.16474 | 0.14807 | Balance local; conductancias efectivas |
| P_D_bomba_monotona__minimax | 0.9719 | 0.5028 | 0.16241 | 0.16441 | 0.14824 | Balance efectivo; topología hipotética |
| J_flexible_restringido__minimax | 0.9719 | 0.5028 | 0.16241 | 0.16441 | 0.14824 | Balance efectivo; topología hipotética |
| J_flexible_restringido__regularizado | 0.9719 | 0.50298 | 0.16241 | 0.16446 | 0.14824 | Balance efectivo; topología hipotética |
| P_D_bomba_monotona__regularizado | 0.9719 | 0.50303 | 0.16241 | 0.16448 | 0.14824 | Balance efectivo; topología hipotética |
| S_balance_empirico_C__regularizado | 0.97861 | 0.50265 | 0.16353 | 0.16436 | 0.14866 | Balance local con transferencia empírica |
| S_balance_empirico_C__minimax | 0.97862 | 0.50262 | 0.16354 | 0.16435 | 0.14866 | Balance local con transferencia empírica |
| U_bomba_carga_monotona | 1.0754 | 0.2727 | 0.17971 | 0.089168 | 0.16119 | Balance local; conductancias efectivas |
| S_balance_empirico_C | 1.0808 | 0.26865 | 0.1806 | 0.087843 | 0.16185 | Balance local con transferencia empírica |
| T_bomba_carga_local | 1.0808 | 0.26865 | 0.1806 | 0.087843 | 0.16185 | Balance local; conductancias efectivas |
| C_bomba | 1.0808 | 0.26865 | 0.1806 | 0.087843 | 0.16185 | Sin flujos identificados en original |
| P_D_bomba_monotona | 1.0886 | 0.30912 | 0.18191 | 0.10108 | 0.16357 | Balance efectivo; topología hipotética |
| J_flexible_restringido | 1.0914 | 0.30523 | 0.18239 | 0.099806 | 0.16411 | Balance efectivo; topología hipotética |
| Q_balance_local | 1.1307 | 0.27818 | 0.18894 | 0.09096 | 0.16836 | Balance local; conductancias efectivas |
| R_balance_monotono | 1.1341 | 0.28126 | 0.18952 | 0.091966 | 0.16881 | Balance local; conductancias efectivas |
| L_cabeza_efectiva | 1.143 | 0.77577 | 0.19101 | 0.25366 | 0.23991 | Balance efectivo; topología hipotética |
| D_conservativo | 1.256 | 0.79464 | 0.20989 | 0.25983 | 0.24709 | Balance efectivo; topología hipotética |
| G_resistencia_mixta | 1.256 | 0.79464 | 0.20989 | 0.25983 | 0.24709 | Balance efectivo; topología hipotética |
| F_exponentes | 1.256 | 0.79464 | 0.20989 | 0.25983 | 0.24709 | Balance efectivo; topología hipotética |
| H_doble_resistencia | 1.256 | 0.79464 | 0.20989 | 0.25983 | 0.24709 | Balance efectivo; topología hipotética |
| K_zona_muerta | 1.6839 | 0.39068 | 0.2814 | 0.12775 | 0.25138 | Balance efectivo; topología hipotética |
| I_bomba_monotona | 1.8945 | 0.48155 | 0.31658 | 0.15746 | 0.28219 | Balance efectivo; topología hipotética |
| O_bomba_saturante | 2.1446 | 0.61084 | 0.35838 | 0.19973 | 0.31885 | Balance efectivo; topología hipotética |
| E_lineal_raiz | 2.3645 | 0.92635 | 0.39513 | 0.3029 | 0.35458 | Balance efectivo; topología hipotética |
| M_cascada | 2.6977 | 0.87145 | 0.4508 | 0.28495 | 0.39965 | Balance efectivo; topología hipotética |

Residuos del recomendado y referencias, corrida completa:

| model | run | tank | phase | acf1 | Q20 | p_descriptive |
|---|---|---|---|---|---|---|
| C_bomba | 8 | h1 | completa | 0.72788 | 436.31 | 5.801e-80 |
| C_bomba | 8 | h2 | completa | 0.47483 | 611.69 | 9.889e-117 |
| C_bomba | 9 | h1 | completa | 0.72345 | 420.67 | 1.0443e-76 |
| C_bomba | 9 | h2 | completa | 0.53567 | 792.64 | 5.1689e-155 |
| C_bomba | 10 | h1 | completa | 0.73367 | 200.72 | 8.12e-32 |
| C_bomba | 10 | h2 | completa | 0.69347 | 682.47 | 1.1268e-131 |
| D_conservativo | 8 | h1 | completa | 0.81332 | 776.07 | 1.6931e-151 |
| D_conservativo | 8 | h2 | completa | 0.93117 | 6307.5 | 0 |
| D_conservativo | 9 | h1 | completa | 0.80988 | 733.39 | 1.888e-142 |
| D_conservativo | 9 | h2 | completa | 0.94267 | 6365.7 | 0 |
| D_conservativo | 10 | h1 | completa | 0.80852 | 239.56 | 1.4429e-39 |
| D_conservativo | 10 | h2 | completa | 0.94927 | 2831.5 | 0 |
| P_D_bomba_monotona__retardo | 8 | h1 | completa | 0.79576 | 647.73 | 2.4735e-124 |
| P_D_bomba_monotona__retardo | 8 | h2 | completa | 0.64731 | 2378.2 | 0 |
| P_D_bomba_monotona__retardo | 9 | h1 | completa | 0.77208 | 566.29 | 3.5775e-107 |
| P_D_bomba_monotona__retardo | 9 | h2 | completa | 0.68005 | 2412.6 | 0 |
| P_D_bomba_monotona__retardo | 10 | h1 | completa | 0.79644 | 208.43 | 2.3999e-33 |
| P_D_bomba_monotona__retardo | 10 | h2 | completa | 0.71467 | 1282.9 | 1.3383e-259 |

Los resultados completos de ACF20, Q20 y p descriptivo se guardan por corrida y fase.
Los p-valores no prueban ni refutan universalmente el modelo; estimación de parámetros,
cuantización y dependencia temporal limitan su interpretación. No se aplica KS ni una
prueba de frecuencias para certificar un sistema dinámico. Inspeccionar sesgo y ACF aun
cuando las métricas sean pequeñas. Un p=0 representa subdesbordamiento numérico, no probabilidad exacta nula.

Relación con resolución aparente de sensores:

| model | tank | MAE | RMSE | NRMSE | RMSE_codigos |
|---|---|---|---|---|---|
| C_bomba | h1 | 0.76006 | 1.0808 | 0.1806 | 2.3864 |
| C_bomba | h2 | 0.2061 | 0.26865 | 0.087843 | 0.59207 |
| D_conservativo | h1 | 0.92948 | 1.256 | 0.20989 | 2.7733 |
| D_conservativo | h2 | 0.67855 | 0.79464 | 0.25983 | 1.7513 |
| P_D_bomba_monotona__retardo | h1 | 0.61397 | 0.84433 | 0.14109 | 1.8643 |
| P_D_bomba_monotona__retardo | h2 | 0.25548 | 0.30306 | 0.099095 | 0.66791 |

La cuantización es ≈0.453 cm por código; no es exactitud certificada. Bajo un error ideal
uniforme de cuantización se obtendría Δ/sqrt(12)≈0.131 cm, pero esto no es un límite
inferior demostrado para la predicción de estos registros ni una incertidumbre certificada.
Hay dispersión entre corridas, deriva, sincronización y dinámica omitida que también contribuyen.

`figures/trajectories_*.png` y `residuals_*.png` incluyen todos los candidatos y ambos tanques:
observado/simulado, bomba, residuo-tiempo, residuo-nivel, histograma, distribución empírica y ACF.
Se muestran todas las corridas reservadas 8–10, incluidos tramos tardíos y recuperación disponible.
