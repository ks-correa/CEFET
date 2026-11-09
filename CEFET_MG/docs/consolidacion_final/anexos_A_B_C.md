# Anexos vigentes A, B y C

## Anexo A Propuesta y sistema

- **Título del proyecto:** Simulación continua de dos tanques acoplados con datos experimentales de CEFET-MG
- **Integrantes:**
  - Kevin Santiago Correa Acosta — 67001271
  - Santiago Cárdenas Rubio — 67001160
- **Asignatura:** Modelado y Simulación
- **Institución:** Universidad Católica de Colombia
- **Fecha:** 8 de noviembre de 2026
- **Pregunta de decisión:** ¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal?
- **Sistema de tanques y alcance:** Dos tanques físicos hidráulicos acoplados con niveles medibles ($h_1, h_2$ en cm) e impulsados por una señal de comando de bomba ($u$ en %). Se emplean los registros experimentales publicados por investigadores de CEFET-MG (Divinópolis, Brasil; DOI `10.5281/zenodo.19856119`). La pareja realiza el modelado matemático continuo, la calibración, la validación interna y la simulación de escenarios, no la adquisición física original. El instrumento específico de medición, la fecha exacta de adquisición en el laboratorio y el plano geométrico preciso no están disponibles en la fuente publicada.
- **Herramienta de simulación:** Python (`numpy`, `pandas`, `scipy`, `numba`, `streamlit`) con integración numérica mediante Runge-Kutta de cuarto orden (RK4, paso máximo de 1 s y desfase efectivo de entrada de 2 s).
- **Aprobación docente:** El uso del dataset externo fue autorizado según la comunicación de los estudiantes.

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
