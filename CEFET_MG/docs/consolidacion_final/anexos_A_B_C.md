# Anexos vigentes A B y C

## Anexo A Propuesta y sistema

Título: Modelado local y simulación de dos tanques CEFET-MG. Integrantes y fecha de
sustentación por completar, sin inventar identidades. Pregunta: ¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal?
Dos tanques físicos acoplados; registros de CEFET-MG. Uso de datos externos autorizado
por el docente según comunicación del usuario. No se recibió acta firmada ni aprobación
formal de cada detalle. La pareja realiza modelado, no la adquisición original.
Instrumento específico, fecha exacta del experimento y plano preciso no disponibles.

## Anexo B Variables y parámetros

Estados h1/h2 cm; t s; mando u %; referencias 47.4/31.2 cm y 50%. Condiciones iniciales
tomadas del primer estado observado de cada corrida. No se corrigen niveles con datos futuros.
Flujos efectivos q=Q/A1 cm/s. Tabla de valores exactos:

| parámetro | valor | unidad |
|---|---|---|
| qstar | 1.1901768213433377 | cm/s (Q/A1) |
| r | 0.28068693475733053 | adimensional; A1/A2 efectivo |
| k12 | 0.039766247050466483 | s⁻¹ |
| kout | 0.011857107887654482 | s⁻¹ |
| kpump | 0.0032622340261774787 | s⁻¹ |
| b | 0.71741375825579845 | adimensional |
| c | 0.58172099393448107 | adimensional |

Desfase efectivo 2 s; historia previa de mando 50%; RK4 máximo 1 s. Fuente: all_fits.json
de optimización, sin recalibración. Identidad de balance efectiva; áreas no identificadas.

## Anexo C Escenarios y comparación

E0 entrada experimental, E1 atenuación 20% de desviaciones alrededor de 50%, E2 constante
50%. S_HIST retiene el antiguo suavizado como análisis complementario. La revisión de
escenarios es posterior al examen del diagnóstico. No se reetiquetan los CSV originales.
Mismos h0, parámetros, método, paso, tiempos y referencias. Diez excitaciones y nueve
recuperaciones disponibles. Resultados, medias, esfuerzo relativo y decisión en
escenarios_resultados_decision.md y reports/consolidacion_final/comparacion_principal.csv.
E1/E2 son contrafactuales. E2 gana nominalmente en 19 comparaciones; no es prueba física.
