# Bondad de ajuste y alcance

La evaluación interna confirma que introducir una respuesta no lineal de bomba mejora
la reproducción frente al modelo lineal y las referencias constantes. No certifica una
curva física de bomba ni validación externa. Protocolo y ecuaciones en `docs/`.

## Evaluación principal

Entrenamiento: corridas 1–7 completas; evaluación: 8–10 libres. Desviaciones estándar
de entrenamiento: 5.98415640 cm para h1 y
3.05827325 cm para h2 (ddof=1), usando filas
de origen únicas. Se excluye del objetivo el estado inicial impuesto de cada corrida.
Los valores siguientes son medias de métricas por corrida; no RMSE agrupado entre filas.
La última corrida es más corta y se informa individualmente en `metrics.csv`.

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| A_lineal | h1 | 1.3801 | 1.9033 | 0.31806 | 1.2241 |
| A_lineal | h2 | 1.2308 | 1.5545 | 0.50829 | 1.2151 |
| B_hidraulico | h1 | 1.9888 | 2.4951 | 0.41695 | 1.967 |
| B_hidraulico | h2 | 1.6054 | 1.8151 | 0.59351 | 1.6024 |
| C_bomba | h1 | 0.76006 | 1.0808 | 0.1806 | -0.28408 |
| C_bomba | h2 | 0.2061 | 0.26865 | 0.087843 | 0.13059 |
| D_conservativo | h1 | 0.92948 | 1.256 | 0.20989 | 0.10485 |
| D_conservativo | h2 | 0.67855 | 0.79464 | 0.25983 | 0.45557 |
| equilibrio | h1 | 5.7491 | 7.3637 | 1.2305 | 2.8376 |
| equilibrio | h2 | 3.3415 | 4.1837 | 1.368 | 2.4282 |
| persistencia | h1 | 5.5532 | 7.2543 | 1.2122 | 2.5365 |
| persistencia | h2 | 3.0496 | 3.9362 | 1.2871 | 1.9727 |

Excitación completa de 800 s, sin diluir el error con la recuperación:

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| A_lineal | h1 | 1.9073 | 2.3517 | 0.39299 | 1.7117 |
| A_lineal | h2 | 1.6357 | 1.8788 | 0.61433 | 1.6277 |
| B_hidraulico | h1 | 2.4204 | 2.9227 | 0.48841 | 2.3848 |
| B_hidraulico | h2 | 1.7757 | 1.9367 | 0.63325 | 1.771 |
| C_bomba | h1 | 1.0681 | 1.352 | 0.22593 | -0.48116 |
| C_bomba | h2 | 0.23475 | 0.30492 | 0.099703 | 0.14251 |
| D_conservativo | h1 | 1.1344 | 1.5075 | 0.25191 | -0.13693 |
| D_conservativo | h2 | 0.67512 | 0.81223 | 0.26558 | 0.32145 |
| equilibrio | h1 | 7.9129 | 9.1178 | 1.5236 | 3.424 |
| equilibrio | h2 | 4.2298 | 5.0067 | 1.6371 | 2.8161 |
| persistencia | h1 | 7.817 | 9.0109 | 1.5058 | 3.1229 |
| persistencia | h2 | 4.025 | 4.7653 | 1.5582 | 2.3605 |

## Validación cruzada por grupos

Cinco particiones contiguas de dos corridas reservadas, ocho para ajuste. Cada partición
usa su propia desviación estándar de entrenamiento; no se recalcula con evaluación.

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| A_lineal | h1 | 1.235 | 1.7904 | 0.29222 | 1.0808 |
| A_lineal | h2 | 1.0771 | 1.4315 | 0.45895 | 1.0434 |
| B_hidraulico | h1 | 1.8534 | 2.3782 | 0.38809 | 1.8321 |
| B_hidraulico | h2 | 1.51 | 1.7487 | 0.56037 | 1.5041 |
| C_bomba | h1 | 0.64959 | 0.99138 | 0.16185 | -0.19588 |
| C_bomba | h2 | 0.19313 | 0.25192 | 0.080755 | 0.085347 |
| D_conservativo | h1 | 0.8579 | 1.1765 | 0.19201 | 0.21215 |
| D_conservativo | h2 | 0.65844 | 0.77117 | 0.24709 | 0.47009 |

Peor NRMSE por tanque entre las diez corridas reservadas:

| model | tank | NRMSE |
|---|---|---|
| A_lineal | h1 | 0.39522 |
| A_lineal | h2 | 0.627 |
| B_hidraulico | h1 | 0.49145 |
| B_hidraulico | h2 | 0.64144 |
| C_bomba | h1 | 0.2263 |
| C_bomba | h2 | 0.10889 |
| D_conservativo | h1 | 0.25231 |
| D_conservativo | h2 | 0.26516 |

## Extrapolación temporal

Al ajustar sólo los primeros 320 s de 1–7 y predecir el resto de 8–10 sin reinicialización:

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| A_lineal | h1 | 3.0775 | 3.672 | 0.5109 | 3.0775 |
| A_lineal | h2 | 2.6628 | 3.0615 | 1.3095 | 2.6628 |
| B_hidraulico | h1 | 2.3731 | 2.8535 | 0.39702 | 2.3687 |
| B_hidraulico | h2 | 2.096 | 2.3495 | 1.005 | 2.0954 |
| C_bomba | h1 | 1.7098 | 2.1081 | 0.2933 | 1.635 |
| C_bomba | h2 | 1.7942 | 2.0377 | 0.87158 | 1.7942 |
| D_conservativo | h1 | 0.94225 | 1.2491 | 0.17379 | 0.77423 |
| D_conservativo | h2 | 0.94815 | 1.0709 | 0.45804 | 0.94591 |

La degradación de h2 indica que los primeros 320 s no identifican suficientemente
su comportamiento tardío. No ocultar este resultado usando únicamente el ajuste completo.

Arranque desde niveles bajos, excluido del ajuste y fuera del alcance local:

| model | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|
| A_lineal | h1 | 3.528 | 5.1907 | 0.8674 | 3.5265 |
| A_lineal | h2 | 2.6393 | 3.7442 | 1.2243 | 2.6302 |
| B_hidraulico | h1 | 4.1855 | 6.8484 | 1.1444 | 4.1822 |
| B_hidraulico | h2 | 3.068 | 4.9734 | 1.6262 | 3.0656 |
| C_bomba | h1 | 2.3266 | 4.3403 | 0.7253 | 2.3232 |
| C_bomba | h2 | 1.5581 | 2.5404 | 0.83067 | 1.5495 |
| D_conservativo | h1 | 2.6621 | 4.9136 | 0.8211 | 2.6582 |
| D_conservativo | h2 | 2.0498 | 3.6673 | 1.1991 | 2.0471 |

Ningún modelo satisface el umbral en el arranque. No recomendar llenado en frío.

## Residuos

Para el candidato predictivo C, seleccionado para diagnóstico por menor NRMSE medio CV:

| run | tank | ACF1 | Q20 | p_descriptivo |
|---|---|---|---|---|
| 8 | h1 | 0.72788 | 436.31 | 5.801e-80 |
| 8 | h2 | 0.47483 | 611.69 | 9.889e-117 |
| 9 | h1 | 0.72345 | 420.67 | 1.0443e-76 |
| 9 | h2 | 0.53567 | 792.64 | 5.1689e-155 |
| 10 | h1 | 0.73367 | 200.72 | 8.12e-32 |
| 10 | h2 | 0.69347 | 682.47 | 1.1268e-131 |

El residuo se define simulado−observado: sesgo positivo significa sobrepredicción.
La dependencia temporal visible y ACF impiden interpretar las muestras como errores
independientes. Ljung–Box Q(20) y su p-valor son descriptivos: parámetros estimados,
cuantización y secuencias compartidas incumplen una interpretación confirmatoria sencilla.
Un p pequeño señala estructura; un p alto tampoco demostraría validez. No se aplican
KS o chi-cuadrado de frecuencias como prueba universal del modelo.

`metrics.csv` incluye MAE/RMSE cm, NRMSE adimensional, sesgo cm, error absoluto máximo cm,
R² (sin unidad), diferencia entre máximos cm y error final cm. El error en máximos compara
amplitudes, no coincidencia temporal. R² puede ser negativo y no mide causalidad.
Las ventanas inicial, tardía, excitación y recuperación se reportan sin reajustar estados.

## Estimación y sensibilidad

| model | cond_Jrel | cost_min | cost_max | converged | bounds |
|---|---|---|---|---|---|
| A_lineal | 9.4135 | 429.08 | 429.08 | 4 | 0 |
| B_hidraulico | 4.3305 | 697.45 | 697.45 | 4 | 0 |
| C_bomba | 12.215 | 47.211 | 47.211 | 4 | 0 |
| D_conservativo | 5.0621 | 146.62 | 146.62 | 4 | 0 |

El número de condición corresponde al Jacobiano de residuos con columnas multiplicadas
por los parámetros: sensibilidad relativa local. Sus valores singulares se conservan en
`calibration.json`; no son intervalos de confianza bajo ruido autocorrelacionado.
Los cuatro puntos iniciales, criterios de terminación, cotas activas y costes se guardan
para cada ajuste principal, temporal y cruzado. Una buena condición local no elimina
la no identificabilidad estructural de áreas/caudales absolutos.

## Verificación numérica

| run | step | max_vs_step1_cm |
|---|---|---|
| 8 | 4.0 | 4.7241e-05 |
| 8 | 2.0 | 2.7041e-06 |
| 8 | 1.0 | 0 |
| 8 | 0.5 | 1.7542e-07 |
| 8 | SciPy_DOP853 | 1.8779e-07 |
| 9 | 4.0 | 4.8207e-05 |
| 9 | 2.0 | 2.7817e-06 |
| 9 | 1.0 | 0 |
| 9 | 0.5 | 1.8268e-07 |
| 9 | SciPy_DOP853 | 1.9571e-07 |
| 10 | 4.0 | 6.2881e-05 |
| 10 | 2.0 | 3.4551e-06 |
| 10 | 1.0 | 0 |
| 10 | 0.5 | 2.1264e-07 |
| 10 | SciPy_DOP853 | 2.2688e-07 |

Los errores de RK4 frente a DOP853 (~10^-7 cm con paso máximo 1 s) son mucho menores
que el error experimental. Reducir paso no resuelve sesgo estructural. La comparación
usa exactamente las mismas discontinuidades causales de bomba. La identidad de conservación
de B,D está en las predicciones como `balance_effective_cm_s`; no se suman alturas como volumen.

Figuras: `figures/exploracion.png`, `trajectory_8.png` a `trajectory_10.png`,
`residuals_8.png` a `residuals_10.png`, `model_comparison.png`, `errors_by_run.png`.
Todas distinguen mediciones y simulación. No se declara que una estrategia operativa
nueva haya sido medida. Para generalización se requieren señales nuevas y circuito documentado.


## Robustez y modelo conservativo recomendado

`modelo_recomendado.json` contiene D, elegido por parsimonia según el protocolo.
`selected_model.json` identifica C exclusivamente como candidato de menor error medio
para las figuras y diagnósticos predictivos. No son el mismo criterio de elección.
`figures/conservative_8.png` muestra D, con su hipótesis física expresamente indicada.

Sensibilidad: perturbación +1% de cada parámetro sin reajuste, y condición inicial ±media
unidad de cuantización en cada tanque. `robustness.csv` conserva todos los resultados,
incluidas métricas por tanque para perturbaciones iniciales. No son intervalos probabilísticos
ni incorporan incertidumbre estructural. Resumen de cambios máximos de estado:

| model | test | max_state_change_cm |
|---|---|---|
| A_lineal | SciPy_DOP853 | 3.6526e-07 |
| A_lineal | convergencia | 0.0001083 |
| A_lineal | inicial_h1 | 0.22644 |
| A_lineal | inicial_h2 | 0.22687 |
| A_lineal | parametro_1pct | 0.17856 |
| B_hidraulico | SciPy_DOP853 | 5.8677e-07 |
| B_hidraulico | balance_algebraico_cm_s | 1.1102e-16 |
| B_hidraulico | convergencia | 0.0001603 |
| B_hidraulico | inicial_h1 | 0.22644 |
| B_hidraulico | inicial_h2 | 0.22687 |
| B_hidraulico | parametro_1pct | 0.13335 |
| C_bomba | SciPy_DOP853 | 2.2688e-07 |
| C_bomba | convergencia | 6.3071e-05 |
| C_bomba | inicial_h1 | 0.22644 |
| C_bomba | inicial_h2 | 0.22687 |
| C_bomba | parametro_1pct | 0.2132 |
| D_conservativo | SciPy_DOP853 | 2.353e-06 |
| D_conservativo | balance_algebraico_cm_s | 2.2204e-16 |
| D_conservativo | convergencia | 0.00071409 |
| D_conservativo | inicial_h1 | 0.22644 |
| D_conservativo | inicial_h2 | 0.22687 |
| D_conservativo | parametro_1pct | 0.19459 |

Diagnóstico de residuos D (corridas completas reservadas):

| run | tank | ACF1 | Q20 | p_descriptivo |
|---|---|---|---|---|
| 8 | h1 | 0.81332 | 776.07 | 1.6931e-151 |
| 8 | h2 | 0.93117 | 6307.5 | 0 |
| 9 | h1 | 0.80988 | 733.39 | 1.888e-142 |
| 9 | h2 | 0.94267 | 6365.7 | 0 |
| 10 | h1 | 0.80852 | 239.56 | 1.4429e-39 |
| 10 | h2 | 0.94927 | 2831.5 | 0 |

También D presenta dependencia temporal; no debe defenderse como reproducción exacta
del circuito. Se contrastó DOP853 y pasos 4,2,1,0.5 s para los cuatro candidatos. El balance
algebraico de B,D está limitado por redondeo de punto flotante, y no es evidencia empírica
de conservación volumétrica. El test lineal exacto aporta una comprobación independiente de RK4.


## Reproducción completa

Se ejecutó de nuevo la auditoría, los cuatro candidatos, los ajustes principales,
cinco particiones cruzadas y el ajuste temporal con semilla/configuración idénticas.
Coincidencia SHA256 exacta de 59 artefactos: True.
Detalle en `reproducibility.json`; pruebas automatizadas en `tests.txt`.
