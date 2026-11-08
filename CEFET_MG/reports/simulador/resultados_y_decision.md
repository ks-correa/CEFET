# Resultados ejecutados y decisión de escenarios

Modelo U exacto, sin reajuste. Primero se fijaron `docs/protocolo_escenarios.md` y la regla
de comparación. Se simularon las diez excitaciones completas y nueve corridas con recuperación.
Los 57 CSV de trayectorias contienen niveles, mando registrado/modificado, entrada tras el
desfase, caudales efectivos, derivadas y residuos de balance. E1/E2 son contrafactuales, no mediciones.

## Regresión científica

| tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|
| h1 | 0.62896 | 0.87253 | 0.14581 | -0.28446 |
| h2 | 0.18748 | 0.24169 | 0.079027 | 0.12545 |

Estas cifras son medias por corrida de evaluación 8–10 completas. Diferencia máxima frente
a las trayectorias U originales: 0 cm.
Tolerancia exigida: 1e-9 cm de trayectoria y 1e-10 en métricas; el resultado observado es exacto.
No se recalibró ni se cambió la escala de entrenamiento.

## Excitación de la corrida 8

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | u_mean_difference_pp | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|---|
| E0 | 9.1026 | 5.0073 | 48.748 | 0 | 1454.9 | 6.353e+05 |
| E1 | 7.0168 | 3.7754 | 48.998 | 0.25049 | 1163.9 | 4.0659e+05 |
| E2 | 8.3483 | 4.3203 | 50.065 | 1.3177 | 1196.9 | 3.9093e+05 |

Estos RMSE son de regulación respecto a 47.4/31.2 cm, distintos de RMSE de predicción.
Frente a E0, E1 reduce RMSE de regulación en h1 22.91%
y en h2 24.60%, con diferencia de mando medio
0.2505 puntos porcentuales y reducción de TV del mando 20%.
No se explica la mejora simplemente por una gran disminución de mando medio.

## Diez excitaciones, media de indicadores por corrida

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|
| E0 | 9.1006 | 5.0052 | 48.748 | 1454.9 | 6.353e+05 |
| E1 | 7.0157 | 3.7742 | 48.998 | 1163.9 | 4.0659e+05 |
| E2 | 8.3513 | 4.3243 | 50.065 | 1196.9 | 3.9093e+05 |

Resultado de la regla por ventana:

| window | recommended | comparaciones |
|---|---|---|
| completa | E1 | 9 |
| excitacion | E1 | 10 |

La regla predefinida selecciona E1 en las 19 comparaciones ejecutadas. Eso no demuestra que
E1 sea óptimo entre todas las políticas posibles ni que funcione físicamente en el laboratorio.
E1 es la recomendación académica local bajo estas preferencias y este modelo.

Hay compensaciones: E2 reduce más la variación total de h1 y el índice integral de esfuerzo
en la corrida 8 que E1, pero regula peor ambos niveles. Su máximo h1 es
60.7431 cm frente a 59.9107 cm de E0;
su máximo h2 también aumenta. El suavizado causal no garantiza menores picos.
El índice integral de (u−50)² no mide energía eléctrica ni caudal en litros.
Las bandas ±2 cm son criterios de análisis, no seguridad certificada.

Limitaciones: circuito y áreas sin verificar, conductancias locales, desfase efectivo sin
certificación física, residuos autocorrelacionados, mala extrapolación de arranque y dependencia
de una única entrada repetida. E1/E2 modifican esa señal: su evaluación es contrafactual,
no una nueva validación experimental. Los cambios de parámetros en la app son exploratorios.
