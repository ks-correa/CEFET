# Anexos de la guía académica

## Anexo A Propuesta y datos del sistema

Título: modelado continuo de dos tanques CEFET-MG y comparación de señales de bomba.
Integrantes: completar los nombres de los dos estudiantes antes de entregar.
Sistema real: dos tanques cilíndricos acoplados de CEFET-MG, Divinópolis, Brasil; capacidad
nominal documentada de 200 L por tanque. No se deducen áreas a partir de esa capacidad.
Pregunta: ¿qué modificación causal del mando reduce desviaciones locales de ambos niveles?
Variables: h1/h2 cm, t s, u %. Herramienta: Python, RK4 y Streamlit.

**Uso de mediciones externas autorizado por el docente**, según la comunicación explícita
del usuario en las instrucciones de fase 3. No se recibió un acta ni fecha de autorización:
no se inventan firma o documento. No equivale a afirmar aprobación formal de cada detalle
de la propuesta. Los investigadores realizaron las mediciones, no los estudiantes.
Instrumento específico y fecha de adquisición no publicados en el material disponible.
La pareja verifica, modela y compara registros secundarios con trazabilidad SHA256.

## Anexo B Variables y parámetros

h1,h2: estados en cm; t: s; u: %; h*=(47.4,31.2) cm; u*=50%.
q=Q/A1: flujos efectivos cm/s, sin conversión a litros/s. Condiciones iniciales: primer
estado observado de la corrida seleccionada, aplicado una sola vez. Desfase δ=2 s,
efectivo; historia de mando previa a t=0: 50%. Parámetros exactos:

| símbolo | valor | unidad | fuente |
|---|---|---|---|
| qstar | 1.1901768213433377 | cm/s (Q/A1) | all_fits.json → U → principal |
| r | 0.28068693475733053 | adimensional (A1/A2) | all_fits.json → U → principal |
| k12 | 0.039766247050466483 | s⁻¹ | all_fits.json → U → principal |
| kout | 0.011857107887654482 | s⁻¹ | all_fits.json → U → principal |
| kpump | 0.0032622340261774787 | s⁻¹ | all_fits.json → U → principal |
| b | 0.71741375825579845 | adimensional | all_fits.json → U → principal |
| c | 0.58172099393448107 | adimensional | all_fits.json → U → principal |

Fuente: `reports/optimizacion_precision/all_fits.json`, modelo U_bomba_carga_monotona__retardo, sección principal.
Los archivos originales no se editan al modificar parámetros en la aplicación.
El balance d(h1+h2/r)/dt=qin−qout es una identidad efectiva del modelo, sin volumen absoluto certificado.

## Anexo C Escenarios e indicadores

E0: señal experimental, condiciones iniciales de la misma corrida.
E1: 50+0.8(u0−50), hipótesis de atenuación del 20%.
E2: límite causal 10 pp/4 s; primera actualización desde 50%, posteriores según dt real.
Cada mando permanece constante hasta el siguiente registro; después se aplica δ=2 s.
Mismos parámetros, h0, tiempos, paso y referencias para los tres escenarios.
Principal: 800 s registrados; recuperación sólo en corridas 1–9, nunca se inventa en 10.

Indicadores y regla fijados en `docs/protocolo_escenarios.md`. Tablas completas ejecutadas
en `reports/simulador/comparacion_escenarios.csv`; decisión en resultados_y_decision.md.
No confundir reproducción de observaciones con desviación del objetivo de regulación.
