# Comparación de evaluación interna

Los diez experimentos comparten una entrada y ya se examinaron. Esta fase es desarrollo
adaptativo, aunque cada ajuste respete sus grupos. No se obtiene validación externa nueva.
Principal: 1–7 ajustan, 8–10 puntúan. CV: cinco folds contiguos, ocho corridas ajustan y
dos puntúan. Los perfiles se seleccionan de nuevo dentro del entrenamiento de cada fold.
Se evalúan estados libres desde una condición inicial medida, sin reinicializar en las ventanas.

Todos los candidatos, evaluación principal y peor NRMSE medio CV:

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

CV por tanque del recomendado y referencias:

| model | tank | MAE | RMSE | NRMSE | bias | max_abs | R2 | final_error | peak_error |
|---|---|---|---|---|---|---|---|---|---|
| C_bomba | h1 | 0.64959 | 0.99138 | 0.16185 | -0.19588 | 5.1858 | 0.97463 | 0.075636 | 0.61059 |
| C_bomba | h2 | 0.19313 | 0.25192 | 0.080755 | 0.085347 | 0.95986 | 0.99363 | 0.20701 | 0.21068 |
| D_conservativo | h1 | 0.8579 | 1.1765 | 0.19201 | 0.21215 | 5.7826 | 0.96407 | 0.32205 | 0.11465 |
| D_conservativo | h2 | 0.65844 | 0.77117 | 0.24709 | 0.47009 | 1.6954 | 0.93925 | 0.45905 | -0.68271 |
| P_D_bomba_monotona__retardo | h1 | 0.53708 | 0.77329 | 0.12624 | -0.18633 | 2.9957 | 0.98453 | 0.0072449 | 1.735 |
| P_D_bomba_monotona__retardo | h2 | 0.23845 | 0.28571 | 0.091548 | 0.12924 | 0.75988 | 0.99163 | 0.27815 | -0.40294 |

Prueba temporal: calibrar sólo 320 s iniciales de desarrollo y predecir t>320 s en 8–10:

| model | tank | RMSE | NRMSE | bias |
|---|---|---|---|---|
| C_bomba | h1 | 2.1081 | 0.2933 | 1.635 |
| C_bomba | h2 | 2.0377 | 0.87158 | 1.7942 |
| D_conservativo | h1 | 1.2491 | 0.17379 | 0.77423 |
| D_conservativo | h2 | 1.0709 | 0.45804 | 0.94591 |
| E_lineal_raiz | h1 | 2.3323 | 0.32451 | 1.5001 |
| E_lineal_raiz | h2 | 1.3234 | 0.56605 | 1.1551 |
| F_exponentes | h1 | 1.3438 | 0.18696 | 0.89371 |
| F_exponentes | h2 | 1.2003 | 0.51342 | 1.0612 |
| G_resistencia_mixta | h1 | 1.2491 | 0.17379 | 0.77423 |
| G_resistencia_mixta | h2 | 1.0709 | 0.45804 | 0.94591 |
| H_doble_resistencia | h1 | 1.347 | 0.18742 | 0.89752 |
| H_doble_resistencia | h2 | 1.2053 | 0.51556 | 1.0654 |
| I_bomba_monotona | h1 | 1.6843 | 0.23434 | 0.50905 |
| I_bomba_monotona | h2 | 0.56394 | 0.24121 | 0.42355 |
| J_flexible_restringido | h1 | 1.0881 | 0.15139 | 0.53464 |
| J_flexible_restringido | h2 | 0.88872 | 0.38014 | 0.78675 |
| J_flexible_restringido__minimax | h1 | 1.4955 | 0.20807 | 1.0992 |
| J_flexible_restringido__minimax | h2 | 1.458 | 0.62363 | 1.3134 |
| J_flexible_restringido__regularizado | h1 | 1.496 | 0.20815 | 1.0997 |
| J_flexible_restringido__regularizado | h2 | 1.4581 | 0.62367 | 1.3134 |
| K_zona_muerta | h1 | 1.8028 | 0.25083 | 0.79848 |
| K_zona_muerta | h2 | 0.80099 | 0.34261 | 0.64914 |
| L_cabeza_efectiva | h1 | 1.1425 | 0.15896 | 0.59156 |
| L_cabeza_efectiva | h2 | 1.0325 | 0.44163 | 0.90859 |
| M_cascada | h1 | 2.2678 | 0.31553 | -0.030844 |
| M_cascada | h2 | 1.0357 | 0.443 | 0.49517 |
| O_bomba_saturante | h1 | 2.062 | 0.28689 | 1.1782 |
| O_bomba_saturante | h2 | 1.057 | 0.45212 | 0.91244 |
| P_D_bomba_monotona | h1 | 1.0881 | 0.15139 | 0.53464 |
| P_D_bomba_monotona | h2 | 0.88872 | 0.38014 | 0.78675 |
| P_D_bomba_monotona__actuador | h1 | 0.89076 | 0.12393 | 0.51887 |
| P_D_bomba_monotona__actuador | h2 | 0.8511 | 0.36405 | 0.75788 |
| P_D_bomba_monotona__minimax | h1 | 1.1649 | 0.16207 | 0.70249 |
| P_D_bomba_monotona__minimax | h2 | 1.0322 | 0.4415 | 0.92602 |
| P_D_bomba_monotona__regularizado | h1 | 1.1662 | 0.16226 | 0.70419 |
| P_D_bomba_monotona__regularizado | h2 | 1.0334 | 0.44201 | 0.92709 |
| P_D_bomba_monotona__retardo | h1 | 0.9023 | 0.12554 | 0.53357 |
| P_D_bomba_monotona__retardo | h2 | 0.85623 | 0.36624 | 0.76273 |
| Q_balance_local | h1 | 1.5512 | 0.21583 | 1.0204 |
| Q_balance_local | h2 | 1.6909 | 0.72324 | 1.499 |
| R_balance_monotono | h1 | 1.5141 | 0.21066 | 0.98465 |
| R_balance_monotono | h2 | 1.6588 | 0.70954 | 1.4751 |
| S_balance_empirico_C | h1 | 2.1081 | 0.29331 | 1.635 |
| S_balance_empirico_C | h2 | 2.0377 | 0.87158 | 1.7942 |
| S_balance_empirico_C__minimax | h1 | 2.8188 | 0.39219 | 2.3348 |
| S_balance_empirico_C__minimax | h2 | 2.5514 | 1.0913 | 2.2527 |
| S_balance_empirico_C__regularizado | h1 | 2.8182 | 0.39211 | 2.3342 |
| S_balance_empirico_C__regularizado | h2 | 2.551 | 1.0912 | 2.2524 |
| T_bomba_carga_local | h1 | 2.1081 | 0.2933 | 1.635 |
| T_bomba_carga_local | h2 | 2.0377 | 0.87158 | 1.7942 |
| U_bomba_carga_monotona | h1 | 2.1589 | 0.30037 | 1.6942 |
| U_bomba_carga_monotona | h2 | 2.0786 | 0.8891 | 1.8308 |
| U_bomba_carga_monotona__actuador | h1 | 1.3493 | 0.18774 | 1.0061 |
| U_bomba_carga_monotona__actuador | h2 | 1.4427 | 0.61711 | 1.298 |
| U_bomba_carga_monotona__minimax | h1 | 2.8921 | 0.40239 | 2.405 |
| U_bomba_carga_monotona__minimax | h2 | 2.6096 | 1.1162 | 2.2993 |
| U_bomba_carga_monotona__regularizado | h1 | 2.8881 | 0.40183 | 2.4015 |
| U_bomba_carga_monotona__regularizado | h2 | 2.607 | 1.1151 | 2.2972 |
| U_bomba_carga_monotona__retardo | h1 | 1.3811 | 0.19216 | 1.0274 |
| U_bomba_carga_monotona__retardo | h2 | 1.5842 | 0.67762 | 1.4178 |

Arranque frío separado (no se ajustó con él):

| model | tank | RMSE | NRMSE | bias |
|---|---|---|---|---|
| C_bomba | h1 | 4.3403 | 0.7253 | 2.3232 |
| C_bomba | h2 | 2.5404 | 0.83067 | 1.5495 |
| D_conservativo | h1 | 4.9136 | 0.8211 | 2.6582 |
| D_conservativo | h2 | 3.6673 | 1.1991 | 2.0471 |
| E_lineal_raiz | h1 | 4.2413 | 0.70875 | 2.1872 |
| E_lineal_raiz | h2 | 3.7692 | 1.2325 | 2.0518 |
| F_exponentes | h1 | 4.9136 | 0.8211 | 2.6582 |
| F_exponentes | h2 | 3.6673 | 1.1991 | 2.0471 |
| G_resistencia_mixta | h1 | 4.9136 | 0.8211 | 2.6582 |
| G_resistencia_mixta | h2 | 3.6673 | 1.1991 | 2.0471 |
| H_doble_resistencia | h1 | 4.9136 | 0.8211 | 2.6582 |
| H_doble_resistencia | h2 | 3.6673 | 1.1991 | 2.0471 |
| I_bomba_monotona | h1 | 5.1879 | 0.86695 | 3.065 |
| I_bomba_monotona | h2 | 4.4837 | 1.4661 | 2.6847 |
| J_flexible_restringido | h1 | 6.3188 | 1.0559 | 3.7385 |
| J_flexible_restringido | h2 | 4.291 | 1.4031 | 2.6374 |
| J_flexible_restringido__minimax | h1 | 5.6877 | 0.95046 | 3.2971 |
| J_flexible_restringido__minimax | h2 | 3.7326 | 1.2205 | 2.2771 |
| J_flexible_restringido__regularizado | h1 | 5.6898 | 0.95081 | 3.2988 |
| J_flexible_restringido__regularizado | h2 | 3.7325 | 1.2205 | 2.2776 |
| K_zona_muerta | h1 | 4.4964 | 0.75138 | 2.5956 |
| K_zona_muerta | h2 | 3.6803 | 1.2034 | 2.2296 |
| L_cabeza_efectiva | h1 | 5.127 | 0.85677 | 2.8127 |
| L_cabeza_efectiva | h2 | 3.6189 | 1.1833 | 2.0399 |
| M_cascada | h1 | 6.3933 | 1.0684 | 3.5695 |
| M_cascada | h2 | 4.5211 | 1.4783 | 2.6264 |
| O_bomba_saturante | h1 | 4.1801 | 0.69853 | 2.1939 |
| O_bomba_saturante | h2 | 3.6036 | 1.1783 | 2.0096 |
| P_D_bomba_monotona | h1 | 6.3305 | 1.0579 | 3.7408 |
| P_D_bomba_monotona | h2 | 4.2637 | 1.3942 | 2.6201 |
| P_D_bomba_monotona__actuador | h1 | 6.3381 | 1.0591 | 3.6621 |
| P_D_bomba_monotona__actuador | h2 | 4.1181 | 1.3466 | 2.5103 |
| P_D_bomba_monotona__minimax | h1 | 5.6877 | 0.95046 | 3.2971 |
| P_D_bomba_monotona__minimax | h2 | 3.7326 | 1.2205 | 2.2771 |
| P_D_bomba_monotona__regularizado | h1 | 5.6905 | 0.95093 | 3.2994 |
| P_D_bomba_monotona__regularizado | h2 | 3.7325 | 1.2204 | 2.2778 |
| P_D_bomba_monotona__retardo | h1 | 6.3117 | 1.0547 | 3.6499 |
| P_D_bomba_monotona__retardo | h2 | 4.1109 | 1.3442 | 2.5059 |
| Q_balance_local | h1 | 3.9434 | 0.65898 | 2.2104 |
| Q_balance_local | h2 | 2.6299 | 0.85994 | 1.5949 |
| R_balance_monotono | h1 | 3.9497 | 0.66003 | 2.2096 |
| R_balance_monotono | h2 | 2.6431 | 0.86425 | 1.598 |
| S_balance_empirico_C | h1 | 4.3403 | 0.7253 | 2.3232 |
| S_balance_empirico_C | h2 | 2.5404 | 0.83067 | 1.5495 |
| S_balance_empirico_C__minimax | h1 | 4.4507 | 0.74374 | 2.4465 |
| S_balance_empirico_C__minimax | h2 | 2.3749 | 0.77653 | 1.5309 |
| S_balance_empirico_C__regularizado | h1 | 4.4495 | 0.74354 | 2.4457 |
| S_balance_empirico_C__regularizado | h2 | 2.3741 | 0.77628 | 1.5303 |
| T_bomba_carga_local | h1 | 4.3403 | 0.7253 | 2.3232 |
| T_bomba_carga_local | h2 | 2.5404 | 0.83067 | 1.5495 |
| U_bomba_carga_monotona | h1 | 4.5929 | 0.76752 | 2.4922 |
| U_bomba_carga_monotona | h2 | 2.7495 | 0.89905 | 1.6805 |
| U_bomba_carga_monotona__actuador | h1 | 4.4424 | 0.74236 | 2.3771 |
| U_bomba_carga_monotona__actuador | h2 | 2.828 | 0.92471 | 1.6996 |
| U_bomba_carga_monotona__minimax | h1 | 4.7385 | 0.79184 | 2.6432 |
| U_bomba_carga_monotona__minimax | h2 | 2.6057 | 0.85202 | 1.6806 |
| U_bomba_carga_monotona__regularizado | h1 | 4.7305 | 0.7905 | 2.6382 |
| U_bomba_carga_monotona__regularizado | h2 | 2.6 | 0.85016 | 1.6766 |
| U_bomba_carga_monotona__retardo | h1 | 4.5238 | 0.75596 | 2.432 |
| U_bomba_carga_monotona__retardo | h2 | 2.7784 | 0.9085 | 1.6835 |

Los modelos locales no se consideran válidos para arranque aunque mejoren en operación.
Fases de excitación y recuperación completas en `metricas_por_fase.csv`; la corrida 10
no contiene recuperación y no se rellena. Tampoco se elimina para mejorar el agregado.
La variación por corrida puede verse en `metrics.csv` y las figuras comparativas.

Verificación numérica: máximo |RK4(1 s)−DOP853| entre todos los modelos/corridas
=0.000165585 cm.
Balance algebraico máximo efectivo=2.22045e-16 cm/s.
Pasos 4,2,1,0.5 s y resultados individuales en `numerical_verification.csv`.
El error numérico se separa del error frente a las mediciones; no se elige paso por ajuste empírico.
