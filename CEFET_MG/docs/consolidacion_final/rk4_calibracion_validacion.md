# Integración, calibración y evaluación conservadas

Motor: src/simulation_engine.py reutiliza el RK4 simultáneo ya contrastado de
src/precision_models.py. Cada intervalo se subdivide en ceil(dt/paso) subpasos y se
particiona en cambios de entrada, incluidos los eventos desplazados 2 s. Paso por defecto
1 s; opciones verificadas 0.5/1/2/4 s. La animación sólo reproduce estados calculados.

Calibración histórica: mínimos cuadrados conjuntos normalizados, cuatro inicios reproducibles,
semilla 20261108, cotas de familia, entrenamiento principal corridas 1–7 completas. Las escalas
de entrenamiento usan filas originales únicas y ddof=1. No se recalibró en esta fase.
Treinta variantes previamente examinadas limitan la independencia de la evaluación.

Evaluación interna de U, media de métricas por corrida 8–10 en sus horizontes disponibles:

| tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|
| h1 | 0.62896 | 0.87253 | 0.14581 | -0.28446 |
| h2 | 0.18748 | 0.24169 | 0.079027 | 0.12545 |

La trayectoria coincide con la versión científica anterior; máxima diferencia:
0 cm. Esto es regresión numérica, no validación
externa nueva. NRMSE=RMSE/sigma de entrenamiento, no porcentaje del nivel de agua.
MAE/RMSE están en cm. El criterio NRMSE≤0.30 es interno, no norma universal del profesor.

Se conservan CV por grupos, sensibilidad, ACF y diagnósticos Ljung–Box descriptivos en
reports/optimizacion_precision/. Persisten sesgos y autocorrelación. El arranque desde niveles
bajos y la predicción tardía de h2 ajustando sólo 320 s siguen limitados. Las repeticiones
comparten señal y no prueban generalización a demandas nuevas.

Los RMSE de regulación de E2 frente a referencias son distintos de esta tabla predictiva.
Su pequeño valor no mejora ni reemplaza la validación. Las pruebas existentes siguen
ejecutándose sin cambiar sus archivos ni expectativas históricas.
