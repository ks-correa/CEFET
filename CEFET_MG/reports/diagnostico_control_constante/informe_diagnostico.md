# Comprobación complementaria de la decisión E1

**D50, mando constante al 50%, supera a E1 bajo las condiciones nominales simuladas.**
E1 conserva su recomendación histórica dentro del conjunto E0/E1/E2. Al añadir D50,
la misma regla elige D50 en las 19 comparaciones. Este resultado acota la recomendación
original y evita presentarla como una política óptima general.

## Qué se conserva y qué se añade

Se preservan los archivos anteriores, incluidos protocolos, código de E0/E1/E2, parámetros
de U y resultados de validación. SHA256: 707 archivos comprobados,
sin modificaciones. El registro está en manifest_previo.json e integridad_y_verificacion.json.
No se recalibra ningún coeficiente. No se añaden escenarios principales a la aplicación.
La app sigue mostrando la decisión del conjunto original; esta revisión se consulta por separado.

Nuevo diagnóstico: u(t)=50%, misma condición inicial de cada corrida, tiempos reales,
modelo U exacto, historia previa al 50%, desfase efectivo 2 s, RK4 máximo 1 s y referencias
47.4/31.2 cm. Diez excitaciones y nueve registros completos con recuperación. La corrida
10 termina en ~800 s y no se extiende. D50 no es una cuarta medición ni un ensayo físico.

## Resultados de la corrida 8 en excitación

| scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | u_mean_pct | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|
| E0 | 9.1026 | 5.0073 | 48.748 | 1454.9 | 6.353e+05 |
| E1 | 7.0168 | 3.7754 | 48.998 | 1163.9 | 4.0659e+05 |
| E2 | 8.3483 | 4.3203 | 50.065 | 1196.9 | 3.9093e+05 |
| D50 | 0.19707 | 0.19702 | 50 | 0 | 0 |

Son RMSE de **regulación** frente al objetivo, no RMSE de predicción frente a mediciones.
D50 reduce esos RMSE frente a E1 un 97.19% en h1 y un 94.78% en h2.
Mantiene ambos niveles dentro de ±2 cm durante los 800.000099 s disponibles.
La desviación máxima es 0.452088 cm en h1 y 0.455560 cm en h2.
Las bandas son criterios analíticos propios, sin valor de límite físico certificado.

La variación total del mando y la integral de (u−50)² son cero porque el mando permanece
en su referencia. **Esto no significa consumo energético cero, bomba apagada ni ausencia
de circulación de agua.** El caudal nominal del modelo es positivo. No hay mediciones
eléctricas para concluir ahorro de energía.

## Resumen por horizonte

| window | scenario | RMSE_ref_h1_cm | RMSE_ref_h2_cm | MAE_ref_h1_cm | MAE_ref_h2_cm | u_mean_pct | TV_u_pp | effort_pp2_s |
|---|---|---|---|---|---|---|---|---|
| completa | D50 | 0.11283 | 0.11482 | 0.066807 | 0.067858 | 50 | 0 | 0 |
| completa | E0 | 6.4656 | 3.7493 | 4.527 | 2.851 | 49.411 | 1460.6 | 6.353e+05 |
| completa | E1 | 4.959 | 2.7971 | 3.4285 | 2.1054 | 49.529 | 1168.5 | 4.066e+05 |
| completa | E2 | 5.7431 | 2.9972 | 3.6814 | 1.9996 | 50.031 | 1202.6 | 3.9093e+05 |
| excitacion | D50 | 0.16169 | 0.1662 | 0.13071 | 0.13377 | 50 | 0 | 0 |
| excitacion | E0 | 9.1006 | 5.0052 | 7.681 | 4.2291 | 48.748 | 1454.9 | 6.353e+05 |
| excitacion | E1 | 7.0157 | 3.7742 | 5.9141 | 3.1871 | 48.998 | 1163.9 | 4.0659e+05 |
| excitacion | E2 | 8.3513 | 4.3243 | 7.3289 | 3.7361 | 50.065 | 1196.9 | 3.9093e+05 |

Medias de indicadores por corrida, no un RMSE global sobre todas las muestras ni réplicas
de señales de excitación independientes. Las condiciones iniciales difieren ligeramente.
Resultado de aplicar la regla sin modificar sus criterios, en un conjunto ampliado:

| window | original_choice | supplementary_choice | casos |
|---|---|---|---|
| completa | E1 | D50 | 9 |
| excitacion | E1 | D50 | 10 |

## Por qué la constante resulta favorecida

U tiene por construcción un equilibrio en (h1,h2,u)=(47.4,31.2,50). Las condiciones iniciales
experimentales están próximas a ese punto. Los escenarios no incluyen demanda externa,
consignas móviles ni perturbaciones temporales medidas que obliguen a variar la bomba.
El modelo sí incluye una salida pasiva dependiente del nivel: mantener 50% compensa esa
salida nominal, no equivale a cerrar el sistema.

Desde ese estado cercano al equilibrio, una entrada constante evita la excitación que
producía desviaciones. Por tanto, D50 es una alternativa nominal legítima dentro del
problema modelado y una referencia obligatoria para interpretar E1. No se demuestra que
sea un óptimo global para otras condiciones iniciales o perturbaciones desconocidas.
Tampoco que el montaje real responda exactamente como el modelo bajo esta política nueva.
Los tramos medidos de recuperación a 50% aportan contexto, pero no son un nuevo ensayo
independiente de D50 desde cada condición inicial ni certifican rechazo de perturbaciones.

El resultado de D50 es particularmente favorable porque el objetivo coincide con el
equilibrio incorporado al modelo. No se debe presentar su pequeño error de regulación
como una nueva precisión predictiva superior a la validación original de U.

## Interpretación de la señal media E1 y E2

En la corrida 8 de ~800 s, E1 tiene mando medio 48.998037% y E2
50.065282%, una diferencia de 1.067246 puntos porcentuales.
La regla original permitía diferencias ≤5 pp frente a E0, pero eso no hacía iguales las
medias entre E1 y E2. Su comparación combinaba forma, desfase, amplitud y componente media.

Se ejecutó una ablación adicional de media, sin modificar E2 original. El offset de mando
se determinó sólo con entradas de corridas 1–7 y después se congeló:

```json
{
  "excitacion": {
    "offset_pp": -1.0721835494258452,
    "development_runs": [
      1,
      2,
      3,
      4,
      5,
      6,
      7
    ],
    "target_mean_pct": 48.99824308719293,
    "training_mean_mismatch_pp": 0.0
  },
  "completa": {
    "offset_pp": -0.5032182290330212,
    "development_runs": [
      1,
      2,
      3,
      4,
      5,
      6,
      7
    ],
    "target_mean_pct": 49.52858492676888,
    "training_mean_mismatch_pp": -7.105427357601002e-15
  }
}
```

Se desplaza E2, se restringe al rango 0–100% y se vuelve a aplicar el limitador causal
desde historia 50%. La corrección no usa la media futura de la corrida evaluada ni niveles
observados futuros. El ajuste inicial por el limitador se declara: no es una intervención
que mantenga idéntica toda la señal excepto un término ideal aislado.

Comparación de desarrollo previamente examinada, corridas 8–10 en excitación:

| run | window | mean_E1 | mean_E2 | mean_corrected | mean_gap_E2_E1_pp | mean_gap_corrected_E1_pp | RMSE_h1_E1 | RMSE_h1_E2 | RMSE_h1_corrected | RMSE_h2_E1 | RMSE_h2_E2 | RMSE_h2_corrected |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | excitacion | 48.998 | 50.065 | 48.998 | 1.0672 | 0.00042294 | 7.0168 | 8.3483 | 8.9323 | 3.7754 | 4.3203 | 4.892 |
| 9 | excitacion | 48.998 | 50.065 | 48.998 | 1.0669 | 6.9012e-05 | 7.0167 | 8.3485 | 8.9324 | 3.7752 | 4.3205 | 4.8921 |
| 10 | excitacion | 48.998 | 50.065 | 48.998 | 1.067 | 0.00013326 | 7.0147 | 8.3514 | 8.9313 | 3.7736 | 4.3254 | 4.8924 |

En la corrida 8, el mando medio corregido es 48.998459%, prácticamente
igual al de E1 (diferencia 0.000423 pp). E2 pasa de RMSE
8.348292/4.320328 cm a
8.932261/4.891961 cm.
En este diagnóstico, bajar la media de E2 empeora ambos indicadores. Su media original
más próxima a 50% le aportaba una ventaja parcial, insuficiente para superar E1.
E1 sigue siendo mejor que esta variante de E2 con media aproximadamente igualada.

No se atribuye toda la diferencia a la media: la bomba es no lineal, depende de h1 y
los estados tienen memoria. Igual promedio de u no implica igual promedio de caudal
ni igual respuesta. No se estima aquí un efecto causal universal de suavizar o de atenuar.

## Revisión de la pregunta de decisión

Pregunta nominal revisada: **¿qué muestran las simulaciones locales sobre mantener el
punto operativo con una bomba constante al 50% frente a transformar la excitación
experimental, cuando no se documenta una demanda externa que obligue a variar el mando?**

Respuesta con la evidencia disponible: preferir D50 como referencia nominal de regulación
en estas simulaciones. E1 sólo es la mejor alternativa del conjunto restringido de
transformaciones originales bajo la regla elegida. No hay una restricción operacional
documentada que descarte el mando constante.

Una señal variable tendría justificación operacional si se documentara, por ejemplo,
una demanda de caudal variable que deba satisfacerse, una consigna temporal obligatoria,
una limitación de disponibilidad de bombeo o perturbaciones que requieran realimentación.
Esas condiciones no se inventan ni se añaden retroactivamente al montaje. Exigirlas daría
lugar a otra pregunta y requeriría datos, ecuaciones e indicadores adicionales.

Sí existe una justificación experimental distinta: variar la entrada ayuda a identificar
la dinámica. El README describe una excitación pseudoaleatoria repetida. Mantener 50%
no sustituye esa excitación para identificar parámetros; por ello una señal de identificación
no debe tratarse automáticamente como una política nominal de operación que necesite
optimizarse sólo por mantener niveles constantes. No se ha evaluado si E1 o E2 preservan
suficiente información de identificación.

## Verificación y límites

Tres ejecuciones D50 repetidas produjeron matrices idénticas. Diferencia máxima frente
a SciPy DOP853 en corridas 8–10: 1.012085e-06 cm.
Pruebas en tests.txt. Configuración, parámetros y versiones en configuracion.json.
La evidencia sigue siendo exploración interna. No hay validación externa nueva, ni
mediciones de E1/E2/D50, ni respaldo para afirmar seguridad, energía o operación global.
Los límites de arranque y de extrapolación temporal de U siguen vigentes.

## Archivos

comparacion_complementaria.csv conserva E0/E1/E2 y agrega D50 en una copia independiente.
ablacion_media.csv e interpretacion_media.csv documentan el análisis de media.
figures/constante_excitacion.png y constante_completa.png muestran los cuatro mandos y
niveles simulados de corrida 8. figures/media_*.png muestra la ablación de media.
