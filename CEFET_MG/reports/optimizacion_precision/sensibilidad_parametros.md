# Sensibilidad e identificabilidad

El Jacobiano relativo usa columnas multiplicadas por max(|p|,0.1), con diferencias
unilaterales cerca de cotas. Los números de condición y valores singulares describen
sensibilidad local del ajuste; no son intervalos de confianza bajo ruido autocorrelacionado.
Para C/D originales se conserva la convención de escalado de la etapa 1 (columnas por p);
no comparar directamente sus condiciones con las nuevas como si usaran la misma escala.

| model | parameters | condition | active_bounds |
|---|---|---|---|
| C_bomba | 6 | 12.215 | [0, 0, 0, 0, 0, 0] |
| D_conservativo | 3 | 5.0621 | [0, 0, 0] |
| E_lineal_raiz | 3 | 6.5181 |  |
| F_exponentes | 5 | 5.2027 | m,n |
| G_resistencia_mixta | 4 | 63.32 | lambda12 |
| H_doble_resistencia | 5 | 66.356 | lambda12,lambda_out |
| I_bomba_monotona | 4 | 83.335 | c |
| J_flexible_restringido | 6 | 108.14 | n |
| K_zona_muerta | 4 | 10.786 |  |
| L_cabeza_efectiva | 4 | 13.452 |  |
| M_cascada | 3 | 6.011 |  |
| O_bomba_saturante | 3 | 5.7421 |  |
| P_D_bomba_monotona | 4 | 41.65 |  |
| P_D_bomba_monotona__minimax | 4 | 15.903 |  |
| P_D_bomba_monotona__regularizado | 4 | 15.963 |  |
| J_flexible_restringido__minimax | 6 | 32.523 | m,n |
| J_flexible_restringido__regularizado | 6 | 32.636 | m,n |
| P_D_bomba_monotona__retardo | 5 | 26.047 |  |
| P_D_bomba_monotona__actuador | 5 | 26.146 |  |
| Q_balance_local | 5 | 24.3 |  |
| R_balance_monotono | 6 | 180.33 |  |
| S_balance_empirico_C | 6 | 26.011 |  |
| T_bomba_carga_local | 6 | 58.643 |  |
| U_bomba_carga_monotona | 7 | 305.05 |  |
| U_bomba_carga_monotona__minimax | 7 | 312.32 |  |
| U_bomba_carga_monotona__regularizado | 7 | 312.1 |  |
| S_balance_empirico_C__minimax | 6 | 26.984 |  |
| S_balance_empirico_C__regularizado | 6 | 26.975 |  |
| U_bomba_carga_monotona__retardo | 8 | 262.64 |  |
| U_bomba_carga_monotona__actuador | 8 | 220.06 |  |

Cambios máximos de trayectorias ante perturbaciones iniciales y de parámetros:

| model | test | max_state_change_cm |
|---|---|---|
| C_bomba | inicial | 0.22687 |
| C_bomba | parametro | 0.83951 |
| D_conservativo | inicial | 0.22687 |
| D_conservativo | parametro | 0.19459 |
| E_lineal_raiz | inicial | 0.22687 |
| E_lineal_raiz | parametro | 0.14376 |
| F_exponentes | inicial | 0.22687 |
| F_exponentes | parametro | 0.19459 |
| G_resistencia_mixta | inicial | 0.22687 |
| G_resistencia_mixta | parametro | 0.19459 |
| H_doble_resistencia | inicial | 0.22687 |
| H_doble_resistencia | parametro | 0.19459 |
| I_bomba_monotona | inicial | 0.22687 |
| I_bomba_monotona | parametro | 0.09908 |
| J_flexible_restringido | inicial | 0.22687 |
| J_flexible_restringido | parametro | 0.10441 |
| J_flexible_restringido__minimax | inicial | 0.22687 |
| J_flexible_restringido__minimax | parametro | 0.10095 |
| J_flexible_restringido__regularizado | inicial | 0.22687 |
| J_flexible_restringido__regularizado | parametro | 0.10097 |
| K_zona_muerta | inicial | 0.22687 |
| K_zona_muerta | parametro | 0.25139 |
| L_cabeza_efectiva | inicial | 0.22687 |
| L_cabeza_efectiva | parametro | 0.20147 |
| M_cascada | inicial | 0.22687 |
| M_cascada | parametro | 0.14611 |
| O_bomba_saturante | inicial | 0.22687 |
| O_bomba_saturante | parametro | 0.091267 |
| P_D_bomba_monotona | inicial | 0.22687 |
| P_D_bomba_monotona | parametro | 0.10438 |
| P_D_bomba_monotona__actuador | inicial | 0.22687 |
| P_D_bomba_monotona__actuador | parametro | 0.10186 |
| P_D_bomba_monotona__minimax | inicial | 0.22687 |
| P_D_bomba_monotona__minimax | parametro | 0.10095 |
| P_D_bomba_monotona__regularizado | inicial | 0.22687 |
| P_D_bomba_monotona__regularizado | parametro | 0.10098 |
| P_D_bomba_monotona__retardo | inicial | 0.22687 |
| P_D_bomba_monotona__retardo | parametro | 0.10194 |
| Q_balance_local | inicial | 0.22687 |
| Q_balance_local | parametro | 0.29451 |
| R_balance_monotono | inicial | 0.22687 |
| R_balance_monotono | parametro | 0.29388 |
| S_balance_empirico_C | inicial | 0.22687 |
| S_balance_empirico_C | parametro | 0.34145 |
| S_balance_empirico_C__minimax | inicial | 0.22687 |
| S_balance_empirico_C__minimax | parametro | 0.35465 |
| S_balance_empirico_C__regularizado | inicial | 0.22687 |
| S_balance_empirico_C__regularizado | parametro | 0.35463 |
| T_bomba_carga_local | inicial | 0.22687 |
| T_bomba_carga_local | parametro | 0.65237 |
| U_bomba_carga_monotona | inicial | 0.22687 |
| U_bomba_carga_monotona | parametro | 0.64879 |
| U_bomba_carga_monotona__actuador | inicial | 0.22687 |
| U_bomba_carga_monotona__actuador | parametro | 0.50362 |
| U_bomba_carga_monotona__minimax | inicial | 0.22687 |
| U_bomba_carga_monotona__minimax | parametro | 0.66081 |
| U_bomba_carga_monotona__regularizado | inicial | 0.22687 |
| U_bomba_carga_monotona__regularizado | parametro | 0.66087 |
| U_bomba_carga_monotona__retardo | inicial | 0.22687 |
| U_bomba_carga_monotona__retardo | parametro | 0.58727 |

Iniciales: ±medio código de h1 y h2 por separado. Parámetros: ±1% hacia el interior de
la cota, mínimo 0.001 en unidades del parámetro para evitar perturbación nula; delta real
en `sensitivity.csv`. No son un experimento de incertidumbre probabilística conjunta.
`parameter_variation_cv.csv` registra estabilidad de cada coeficiente entre folds.
Áreas y caudales absolutos siguen siendo estructuralmente no identificables: escala común
de área y caudal no cambia niveles. S/T muestran además ambigüedad de interpretación física.

Perfiles de retardo y actuador, selección en cada entrenamiento:

| model | stage | delay | tau | mse_sum |
|---|---|---|---|---|
| P_D_bomba_monotona__retardo | principal | 2 | 0 | 0.023707 |
| P_D_bomba_monotona__retardo | cv_0 | 2 | 0 | 0.024197 |
| P_D_bomba_monotona__retardo | cv_1 | 2 | 0 | 0.023793 |
| P_D_bomba_monotona__retardo | cv_2 | 2 | 0 | 0.023498 |
| P_D_bomba_monotona__retardo | cv_3 | 2 | 0 | 0.023353 |
| P_D_bomba_monotona__retardo | cv_4 | 2 | 0 | 0.024015 |
| P_D_bomba_monotona__actuador | principal | 0 | 2 | 0.023777 |
| P_D_bomba_monotona__actuador | cv_0 | 0 | 2 | 0.024253 |
| P_D_bomba_monotona__actuador | cv_1 | 0 | 2 | 0.023863 |
| P_D_bomba_monotona__actuador | cv_2 | 0 | 2 | 0.023566 |
| P_D_bomba_monotona__actuador | cv_3 | 0 | 2 | 0.023423 |
| P_D_bomba_monotona__actuador | cv_4 | 0 | 2 | 0.024085 |
| U_bomba_carga_monotona__retardo | principal | 2 | 0 | 0.021551 |
| U_bomba_carga_monotona__retardo | cv_0 | 2 | 0 | 0.02142 |
| U_bomba_carga_monotona__retardo | cv_1 | 2 | 0 | 0.021548 |
| U_bomba_carga_monotona__retardo | cv_2 | 2 | 0 | 0.021498 |
| U_bomba_carga_monotona__retardo | cv_3 | 2 | 0 | 0.021492 |
| U_bomba_carga_monotona__retardo | cv_4 | 2 | 0 | 0.021587 |
| U_bomba_carga_monotona__actuador | principal | 0 | 4 | 0.021298 |
| U_bomba_carga_monotona__actuador | cv_0 | 0 | 2 | 0.021356 |
| U_bomba_carga_monotona__actuador | cv_1 | 0 | 4 | 0.021385 |
| U_bomba_carga_monotona__actuador | cv_2 | 0 | 4 | 0.021388 |
| U_bomba_carga_monotona__actuador | cv_3 | 0 | 4 | 0.021289 |
| U_bomba_carga_monotona__actuador | cv_4 | 0 | 4 | 0.021377 |

El perfil completo se conserva en `delay_actuator_profiles.csv`, incluyendo puntos desfavorables.
Un mínimo en cero o cerca de él, o cambios del mínimo entre folds, no respalda una constante
física identificada. Los intervalos no se presentan como tiempos medidos: el muestreo es ≈4 s,
las transiciones tienen jitter y sólo hay una secuencia repetida. La selección por coste
no prueba un mecanismo de actuador. Un τ adicional es un estado interno de bomba, no un tanque.


## Interpretación del perfil obtenido

P elige δ=2 s en todos los folds; también τ=2 s con el modelo alternativo de actuador.
Ambos obtienen errores muy próximos y la diferencia de peor NRMSE CV es menor que 1%.
U también elige δ=2 s en todos los folds; su τ preferido cambia entre 2 y 4 s.
Esto respalda un desfase efectivo respecto a las marcas temporales registradas, sin
identificar de forma única un retardo de transporte o una constante de bomba.
El perfil es discreto y no prueba que 2.000 s sea un óptimo continuo exacto. No se exploró
un adelanto no causal. Con Ts≈4 s no se puede certificar la precisión de ese tiempo físico.
