# Protocolo fijado antes de calibrar

Fecha 8 de noviembre de 2026. Evaluación interna previamente examinada, sin validación ciega.
Unidad estadística: corrida de la captura larga, sin duplicar extractos h1/h2.
Cada corrida incluye excitación de 800 s y recuperación disponible hasta la siguiente corrida.
Última corrida: recuperación no disponible. Las fronteras pueden compartir un estado inicial,
que no es una observación de error independiente ni se usa para corregir estados posteriores.

Desarrollo principal: corridas 1–7 completas. Evaluación: 8–10. Se informan por separado
excitación (0–800 s), recuperación (>800 s), primeros 320 s y tramo tardío (>320 s).
Validación cruzada: cinco grupos contiguos de dos corridas, ajustando sobre los otros ocho.
Prueba temporal: calibrar sólo t<=320 s de 1–7, simular libres las corridas 8–10 completas;
informar t>320 s. Arranque: simular la captura anterior a la primera excitación sin calibrarlo.

Objetivo: mínimos cuadrados de residuos hsim-hobs divididos por la desviación estándar
muestral (ddof=1) de cada tanque en el entrenamiento correspondiente; pesos iguales por muestra.
Cuatro inicializaciones reproducibles, semilla 20261108, cotas positivas, RK4 máximo 1 s.
Los estados frontera se deduplican por fila original al calcular la desviación estándar.
La condición inicial impuesta no participa del residuo de calibración (es cero por construcción).
NRMSE=RMSE/sigma_entrenamiento, sin recalcular con evaluación. Umbral interno <=0.30
en ambos tanques, corridas completas y excitación; reportar todas las particiones y fallas.
Comparar A lineal estable, B hidráulico de bomba lineal, C local con bomba potencial y
D hidráulico conservativo con bomba potencial. B y D son hipótesis de topología aún no verificada.
Selección: comparar validación cruzada, priorizar menor complejidad entre candidatos que
cumplan el umbral; ninguna mejora estadística certifica la topología. No ajustar con evaluación
principal. Referencias: persistencia inicial constante, equilibrio documentado, A lineal.

Convergencia: pasos máximos 4,2,1,0.5 s y SciPy DOP853 por intervalo de entrada constante.
Residuos: sesgo, ACF 20 retardos, Ljung–Box descriptivo sin inferencia confirmatoria (cuantización,
dependencia temporal, parámetros estimados). Métricas por corrida, tanque e intervalo.
No desarrollar UI ni tomar decisiones contrafactuales si falla el criterio interno.
