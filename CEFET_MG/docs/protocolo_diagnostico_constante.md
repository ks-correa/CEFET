# Protocolo complementario de decisión

Este diagnóstico se añade después de conocer la decisión E1. No modifica los protocolos,
parámetros, resultados, criterios ni los tres escenarios principales de la aplicación.
Es exploración interna sobre registros previamente examinados, sin nueva validación externa.

D50: mando constante de 50% en cada tiempo registrado, con historia previa también de 50%.
Se usa U_bomba_carga_monotona__retardo, sus parámetros exactos, desfase efectivo de 2 s,
las condiciones iniciales de cada corrida, marcas temporales, RK4 máximo 1 s y referencias
47.4/31.2 cm. Se evalúan las diez excitaciones (~800 s) y las nueve corridas completas
con recuperación (~1700 s). No se añade recuperación a la corrida 10.

Se reutiliza regulation_indicators sin cambios. E0/E1/E2 se leen de los resultados guardados.
La prueba incluye RMSE/MAE de regulación, máximos, variación, bandas ±2 cm, media/variabilidad
del mando, TV y la integral de (u−50)^2. Un valor cero de esa integral representa cero
desviación de mando respecto al 50%, no energía eléctrica nula ni bomba apagada.

Se contrasta D50 con los tres escenarios y, de forma explícitamente complementaria, se
aplica la misma regla de decisión a un conjunto ampliado E0/E1/E2/D50. Se conserva la
decisión histórica del conjunto original y no se reescribe como si hubiera considerado D50.
No se anticipa un ganador. Se explicará que el equilibrio bajo u=50% está incorporado en
la parametrización de U, y que h0 se encuentra cerca del punto operativo.

Para investigar el efecto de la media entre E1 y E2 se admite una ablación separada de mando,
sin ajustar coeficientes del modelo. Para cada horizonte se determina un desplazamiento
constante a partir únicamente de las entradas de corridas 1–7, haciendo coincidir la media
temporal promedio del mando E2 desplazado y nuevamente limitado causalmente con la de E1.
Se resuelve una raíz escalar en el intervalo [-5,+5] puntos porcentuales usando sólo esas
entradas. La transformación es clip(E2+offset,0,100), seguida por el limitador causal
original (historia 50%, 10 pp por primer intervalo, 2.5 pp/s después). Así no se usa una
media futura de la corrida evaluada para decidir su mando, y se preservan rango e historial.
El mismo offset congelado se aplica a todas las corridas de ese horizonte; 8–10 se reportan
por separado como comparación de desarrollo ya examinada. No constituye una política
certificada ni una optimización del error. El pequeño ajuste de la transición inicial al
relimitar impide llamarlo una intervención que sólo cambia un número y nada más.

La ablación de media no entra en la regla de selección de los tres escenarios originales.
Las métricas de validación de predicción de U no se recalculan ni se sustituyen por errores
de regulación. Se comprobarán SHA256 de todos los archivos preexistentes antes y después.
