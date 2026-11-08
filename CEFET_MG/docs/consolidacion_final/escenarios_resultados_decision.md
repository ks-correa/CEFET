# Escenarios, resultados y decisión vigentes

E0: mando experimental. E1: 50+0.8(u0−50). E2: mando constante 50%.
S_HIST: antiguo suavizado, sólo complementario. Revisión posterior al examen de resultados,
sin cambiar los coeficientes U, el motor, las métricas ni la función de decisión.
Ver protocolo_vigente.md y registro_metodologico.md para no confundir versiones de E2.

Regla: no empeorar ambos RMSE frente a E0, mejorar al menos uno ≥5%, TV del mando no
mayor que E0 y cambio de media ≤5 pp; entre elegibles, menor peor RMSE/banda de 2 cm.
Los tres casos comparten h0, parámetros, tiempos, paso y referencias. Las bandas no son
límites físicos certificados. La corrida 10 no tiene recuperación inventada.

Corrida 8 en excitación (~800 s), indicadores de regulación:

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|
| E0 | 9.1026 | 5.0073 | 48.748 | 1454.9 | 6.353e+05 |
| E1 | 7.0168 | 3.7754 | 48.998 | 1163.9 | 4.0659e+05 |
| E2 | 0.19707 | 0.19702 | 50 | 0 | 0 |

Promedio de indicadores por corrida en las diez excitaciones:

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|
| E0 | 9.1006 | 5.0052 | 48.748 | 1454.9 | 6.353e+05 |
| E1 | 7.0157 | 3.7742 | 48.998 | 1163.9 | 4.0659e+05 |
| E2 | 0.16169 | 0.1662 | 50 | 0 | 0 |

Decisiones nominales:

| window | recommended | comparaciones |
|---|---|---|
| completa | E2 | 9 |
| excitacion | E2 | 10 |

**E2 es la mejor alternativa nominal evaluada bajo estas condiciones simuladas.** La
bomba al 50% está en el equilibrio de U y las iniciales se encuentran cerca. No hay una
demanda externa documentada que obligue a variar el mando. La salida pasiva del modelo
sigue presente y se compensa nominalmente con entrada de bomba.

El resultado no demuestra óptimo global, energía ahorrada, seguridad ni ensayo físico de
E2. TV y ∫(u−50)² son cero en nominal, pero la bomba sigue funcionando al 50%: ese índice
de esfuerzo relativo no mide energía eléctrica. El control constante es lazo abierto.

La recomendación histórica E1 era válida para el conjunto restringido de fase 3; se
preserva íntegra en sus archivos y se contextualiza aquí. El suavizado S_HIST y la
ablación de media no cambian esta decisión nominal. No se igualaron retrospectivamente
medias para modificar los resultados principales. Su diferencia está documentada en el
diagnóstico: la media original del suavizado era mayor que la de E1.
