# Paquete de inicio — Proyecto de simulación continua CEFET-MG

## Fuente principal
Datos experimentales originales del conjunto «D-Stabilization of a Coupled-Tank System Using Experimental Data», CEFET-MG. Consultar el README y la publicación original para atribución y condiciones de uso.

- data/raw/h1.csv y data/raw/h2.csv: 81 filas por tanque, t_ref y Experimento1..10.
- data/raw/U.csv: 80 señales de bomba por intervalo; debe comprobarse la alineación temporal.
- data/raw/complete_data.csv: 4502 observaciones de una captura más extensa; NO asumir sin análisis que son datos independientes ni que son duplicados de las otras tablas.
- data/raw/README.md: fuente principal para unidades: niveles en cm, señal de bomba en %.
- data/raw/operational_parameters.json: TRUNCADO, contiene etiquetas h3_op/h4_op y unidades conflictivas; solo usar como evidencia de inconsistencia, NO como configuración válida.
- referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx: guía docente original; exige sistema real y mediciones y 13 diapositivas.

## Secuencia científica
1. Auditar fuente, archivos, unidades, entradas y corridas.
2. Establecer criterios y protocolo de evaluación antes de seleccionar modelo.
3. Implementar una línea base e integrar EDO con RK4.
4. Calibrar y comparar modelos interpretables; incluir conservación y unidades.
5. Evaluar errores y bondad de ajuste con los datos disponibles sin usar mediciones futuras.
6. Concluir alcances reales y límites. Solo después considerar escenarios/UI/presentación.

## Nota de honestidad metodológica
Este dataset ya se usó en una exploración adaptativa anterior y se conocieron métricas sobre repeticiones. Rehacer los experimentos mejora reproducibilidad pero NO crea por sí solo una nueva validación independiente. Las mismas señales de bomba se repiten en las corridas cortas. Solicitar autorización al docente para usar mediciones experimentales de terceros.

## Huellas SHA256
- data/raw/h1.csv: 8bcc8e870c19c9f54de122e65963fc52fe1fd23a95f6335a297a51d3d4daf81e
- data/raw/h2.csv: dff73ca67048dc031bc9f6834115ae759e7f73b217ff09aea04f0411e24a3925
- data/raw/U.csv: 2a6da4ae0f990ad94003444ca7ac8e2a7a5c14dfab1951be1fa741260be54cf3
- data/raw/complete_data.csv: 6b2470f4a0ed64d3cfeb82ee7ec5e6803c6297e48d2a6cfe5af0a7787cebbd78
- data/raw/README.md: 671553956771bf1c249fcc8e655e72e1f6b752c56914c29a2cb55312e0744219
- data/raw/operational_parameters.json: 565aed05d19e19d6eddbf82234cb3076c98308645c5a3d4ce8f4fc8dd2adb810
- referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx: 21cb59dd2597a4473ace1dd9551ae7d4f9f13cab259c8035478d3bc109871fa9
