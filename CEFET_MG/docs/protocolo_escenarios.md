# Reglas fijadas antes de ejecutar los escenarios

Modelo principal U_bomba_carga_monotona__retardo, parámetros exactos de all_fits.json,
sin recalibración. Misma condición inicial observada, tiempos, duración, paso RK4=1 s,
historia de entrada previa u=50%, desfase efectivo de 2 s y referencias (47.4,31.2 cm).
Principal: 201 estados / 200 intervalos observados, aproximadamente 800 s, sin redondear
sus marcas temporales. Complementario: corrida completa sólo cuando existe recuperación.

E0 u0(t) registrada, retenida causalmente por intervalos. E1=50+0.8(u0−50).
E2: en t=0, u2(0)=clip(u0(0),50−10,50+10); posteriormente
u2[i]=u2[i−1]+clip(u0[i]−u2[i−1],−2.5Δt_i,+2.5Δt_i).
La primera transición usa un intervalo nominal de 4 s, con historia previa a 50%; las
siguientes usan el tiempo real transcurrido. No interpola ni anticipa entradas futuras.
El mando se retiene hasta el siguiente registro, y después se aplica el mismo desfase de U.
10 puntos porcentuales / 4 s es un criterio de simulación, no especificación del actuador.

Indicadores respecto a referencia: RMSE temporal, desviación absoluta media temporal,
máximo absoluto, desviación estándar temporal, variación total y tiempos dentro/fuera
de bandas ±2 cm para cada tanque. Bandas analíticas, no límites certificados de seguridad.
El promedio temporal de estados usa cuadratura trapezoidal en las marcas de salida; se
declara esta aproximación distinta de la puntuación muestral de validación científica.
Señal de mando: media y desviación ponderadas por duración mediante retención constante,
variación total incluyendo el salto inicial desde 50%, y esfuerzo integral (u−50)^2dt.
Se informa también media del mando aplicado tras el desfase.

Regla de decisión por corrida: una alternativa es elegible si no empeora ninguno de
los dos RMSE de regulación, reduce al menos uno ≥5%, no aumenta la variación total
del mando y cambia su media menos de 5 puntos porcentuales respecto a E0.
Entre elegibles se minimiza max(RMSE_ref_h1/2,RMSE_ref_h2/2), desempate por menor TV_u.
Si no hay elegibles, no se recomienda sustitución. Si otro escenario tiene ventaja en
otro indicador se declara la compensación, sin llamarlo dominancia total.
Estas preferencias analíticas se fijan antes de ver resultados y no certifican seguridad.

E0 se compara además con observaciones: MAE/RMSE/NRMSE/sesgo de predicción, usando las
escalas originales. E1/E2 no tienen observaciones contrafactuales: nunca se les atribuye
un error de predicción frente a la corrida real. Se evalúan las diez excitaciones y las
nueve recuperaciones disponibles; la última corrida no se extiende a 1700 s.
