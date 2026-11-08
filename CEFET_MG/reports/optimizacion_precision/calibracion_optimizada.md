# Calibración optimizada

Se mantiene sigma de entrenamiento por filas originales únicas, ddof=1. La condición inicial
impuesta no aporta residuo a calibración. No hay eliminación de muestras de evaluación.
Las cifras principales son medias de MAE/RMSE/NRMSE por corrida, no RMSE agrupado.
Cuatro inicios seed 20261108 para cada estructura/partición. En perfiles, dos inicios por
punto para limitar coste; cada fold repite la selección de retardo/τ con su entrenamiento.

LS minimiza suma de residuos normalizados al cuadrado. Minimax minimiza un auxiliar z
sujeto a MSE_h1≤z y MSE_h2≤z; SLSQP en parámetros escalados. La variante regularizada
añade 1e-4 media(log(p/p_LS)²) sólo para parámetros con cota inferior positiva.
El ancla LS se calcula en el mismo entrenamiento. Ninguna puntuación usa esa penalización.
Las soluciones minimax pueden empeorar h2 al redistribuir error hacia el tanque menos favorecido.
No se interpreta un coste menor como una mejora garantizada en evaluación.

Se emplea [least_squares de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)
y [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html), con cotas y diagnósticos guardados.

| model | parameters | condition | active_bounds | starts_success | cost_min | cost_max | optimizer_success |
|---|---|---|---|---|---|---|---|
| C_bomba | 6 | 12.215 | [0, 0, 0, 0, 0, 0] | 4 | 47.211 | 47.211 | True |
| D_conservativo | 3 | 5.0621 | [0, 0, 0] | 4 | 146.62 | 146.62 | True |
| E_lineal_raiz | 3 | 6.5181 |  | 4 | 304.28 | 304.28 | True |
| F_exponentes | 5 | 5.2027 | m,n | 4 | 146.62 | 146.62 | True |
| G_resistencia_mixta | 4 | 63.32 | lambda12 | 4 | 146.62 | 146.62 | True |
| H_doble_resistencia | 5 | 66.356 | lambda12,lambda_out | 4 | 146.62 | 146.62 | True |
| I_bomba_monotona | 4 | 83.335 | c | 4 | 143.94 | 143.94 | True |
| J_flexible_restringido | 6 | 108.14 | n | 4 | 51.22 | 51.22 | True |
| K_zona_muerta | 4 | 10.786 |  | 4 | 110.2 | 110.2 | True |
| L_cabeza_efectiva | 4 | 13.452 |  | 4 | 130.29 | 130.29 | True |
| M_cascada | 3 | 6.011 |  | 4 | 345.59 | 345.59 | True |
| O_bomba_saturante | 3 | 5.7421 |  | 4 | 196.32 | 196.32 | True |
| P_D_bomba_monotona | 4 | 41.65 |  | 4 | 51.303 | 51.303 | True |
| P_D_bomba_monotona__minimax | 4 | 15.903 |  | 4 | 51.303 | 51.303 | True |
| P_D_bomba_monotona__regularizado | 4 | 15.963 |  | 4 | 51.303 | 51.303 | True |
| J_flexible_restringido__minimax | 6 | 32.523 | m,n | 4 | 51.22 | 51.22 | True |
| J_flexible_restringido__regularizado | 6 | 32.636 | m,n | 4 | 51.22 | 51.22 | True |
| P_D_bomba_monotona__retardo | 5 | 26.047 |  | 2 | 35.264 | 35.264 | True |
| P_D_bomba_monotona__actuador | 5 | 26.146 |  | 2 | 35.368 | 35.368 | True |
| Q_balance_local | 5 | 24.3 |  | 4 | 50.751 | 50.751 | True |
| R_balance_monotono | 6 | 180.33 |  | 4 | 51.096 | 51.096 | True |
| S_balance_empirico_C | 6 | 26.011 |  | 4 | 47.211 | 47.211 | True |
| T_bomba_carga_local | 6 | 58.643 |  | 4 | 47.211 | 47.211 | True |
| U_bomba_carga_monotona | 7 | 305.05 |  | 4 | 47.002 | 47.002 | True |
| U_bomba_carga_monotona__minimax | 7 | 312.32 |  | 4 | 47.002 | 47.002 | True |
| U_bomba_carga_monotona__regularizado | 7 | 312.1 |  | 4 | 47.002 | 47.002 | True |
| S_balance_empirico_C__minimax | 6 | 26.984 |  | 4 | 47.211 | 47.211 | True |
| S_balance_empirico_C__regularizado | 6 | 26.975 |  | 4 | 47.211 | 47.211 | True |
| U_bomba_carga_monotona__retardo | 8 | 262.64 |  | 2 | 32.057 | 32.057 | True |
| U_bomba_carga_monotona__actuador | 8 | 220.06 |  | 2 | 31.681 | 31.681 | True |

Valores, puntos iniciales, costes, límites activos, mensajes y convergencia en `fit_*.json`
y `all_fits.json`. `parameters.csv` permite comparar coeficientes. C/D se leen congelados
de la primera etapa. Las cotas nuevas son restricciones de familia y regularidad, no
especificaciones medidas: q*∈[0.01,10] cm/s, r∈[0.03,3], exponentes 0.5–1,
γ∈[0.2,2], coeficientes de Bernstein positivos y conductancias positivas; ver config.json.
Si una cota es activa no se presenta su valor como estimación precisa de una propiedad física.
