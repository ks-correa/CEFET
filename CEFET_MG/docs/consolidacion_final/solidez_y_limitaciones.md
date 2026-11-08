# Solidez local y límites de la recomendación

Las pruebas nuevas son simulaciones exploratorias declaradas, sin mediciones nuevas,
sin ajuste de parámetros y sin búsqueda de políticas. Seis desplazamientos iniciales de
1 cm y tres perturbaciones de mando ±2 pp se compararon para cada una de diez excitaciones.
La misma intervención se aplicó a E0/E1/E2. Resultado de la regla:

| case | recommended | comparaciones |
|---|---|---|
| inicial_+0_+1 | E2 | 10 |
| inicial_+0_-1 | E2 | 10 |
| inicial_+1_+0 | E2 | 10 |
| inicial_+1_+1 | E2 | 10 |
| inicial_-1_+0 | E2 | 10 |
| inicial_-1_-1 | E2 | 10 |
| pulso_mas2 | E2 | 10 |
| pulso_menos2 | E2 | 10 |
| sesgo_menos2 | E2 | 10 |

Peor resultado de E2 por familia exploratoria, entre las diez corridas:

| case | RMSE_ref_h1_cm | RMSE_ref_h2_cm | max_deviation_h1_cm | max_deviation_h2_cm |
|---|---|---|---|---|
| inicial_+0_+1 | 0.26139 | 0.31204 | 0.51533 | 0.99818 |
| inicial_+0_-1 | 0.50188 | 0.54658 | 0.99664 | 1.4556 |
| inicial_+1_+0 | 0.1089 | 0.115 | 1.0008 | 0.45556 |
| inicial_+1_+1 | 0.37381 | 0.39463 | 1.0008 | 0.99818 |
| inicial_-1_+0 | 0.33978 | 0.28176 | 1.4521 | 0.56764 |
| inicial_-1_-1 | 0.63068 | 0.63013 | 1.4521 | 1.4556 |
| pulso_mas2 | 0.26846 | 0.21695 | 0.81297 | 0.45556 |
| pulso_menos2 | 0.34336 | 0.27282 | 0.997 | 0.45556 |
| sesgo_menos2 | 1.3904 | 0.89935 | 2.6414 | 1.8742 |

La preferencia se mantiene en 90/90 comparaciones exploratorias. Esto no acredita un
control robusto del montaje. No se añadieron demandas hidráulicas ni se fingieron
perturbaciones experimentales. El sesgo persistente −2 pp hace que el mando aplicado a
E2 pase a 48% tras el evento y desplaza los niveles: no permanece una regulación perfecta.

El equilibrio local a u=50% es (47.4,31.2) cm por construcción. El Jacobiano nominal tiene
autovalores -0.05420481 y -0.00331368 s⁻¹.
Ambos son negativos en el modelo, dentro de la rama activa; esto indica estabilidad
asintótica local matemática, sin certificar estabilidad global o experimental.
A u=48% el equilibrio predicho es (44.056022,
28.624084) cm. Un sesgo sostenido no se rechaza sin error
por el mero uso de un mando constante. No se ensayó realimentación física.

Rangos: E2 presenta 0 muestras fuera
del rectángulo de niveles observado en estas pruebas. En el conjunto E0/E1/E2 hay
1968 valores de nivel fuera de ese rectángulo; se conservan en robustez/rangos.csv.
Esos desvíos, principalmente de E0/E1 al excitar el sistema, impiden afirmar que todas
las trayectorias permanezcan estrictamente dentro del soporte experimental. Estar dentro
de un rectángulo tampoco garantiza cobertura de estados conjuntos. No se ocultan las excursiones.
Muestras de saturación de mando registradas: 0.

Una señal variable sería necesaria para una consigna móvil, demanda de caudal, restricción
de disponibilidad o perturbación documentada que exigiera corregir desviaciones. No se
atribuyen esas condiciones al montaje sin datos. La excitación variable sí tuvo finalidad
de identificación experimental, distinta de la regulación nominal aquí comparada.

Sin mediciones adicionales se puede defender: origen publicado, reproducción interna
de U, consistencia numérica, mejores indicadores de E2 entre estos escenarios y límites
de la sensibilidad simulada. No se puede afirmar optimalidad global, ahorro eléctrico,
seguridad, rechazo de perturbaciones reales o generalización a entradas nuevas.
