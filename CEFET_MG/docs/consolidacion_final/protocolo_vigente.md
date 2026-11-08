# Protocolo vigente de la entrega final

Esta revisión se realiza después de examinar los resultados del diagnóstico constante.
No es un protocolo previo a la búsqueda original ni una validación externa nueva.
La decisión histórica E1 se conserva para el conjunto de escenarios de fase 3.

La comparación principal vigente contiene exactamente tres escenarios:

- E0: mando experimental de referencia, retenido causalmente.
- E1: atenuación 50+0.8(u0−50).
- E2: operación constante al 50%, equivalente al diagnóstico anterior D50.

El antiguo E2 de fase 3, suavizado a 10 pp/4 s, se denomina ahora S_HIST en los análisis
complementarios. Sus archivos y su protocolo originales no se renombran ni se sobrescriben.
El mapa explícito evita confundir números de versiones: E2 vigente = D50 diagnóstico;
S_HIST vigente = E2 histórico. E0 y E1 conservan exactamente sus entradas y resultados.

U, sus siete coeficientes, desfase efectivo de 2 s, condición inicial registrada, marcas
temporales y RK4 máximo 1 s son los mismos. Se conservan 10 excitaciones y 9 registros
completos con recuperación. No se inventa recuperación en corrida 10.

Se reutilizan sin cambios regulation_indicators y decide de src/scenarios.py. La regla
comprueba ambos RMSE de regulación, mejora ≥5% en uno, TV del mando no mayor que E0 y
cambio de media ≤5 pp frente a E0. Entre elegibles minimiza el peor RMSE/banda de 2 cm.
La preferencia de escenarios actualizada es retrospectiva, aunque la función de puntuación
y la regla de decisión no cambian. No se rediseñan para que E2 gane.

La pregunta propuesta es: ¿Cómo influye la variabilidad de la señal de bombeo en la
estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición
de operación permite minimizar sus desviaciones respecto al equilibrio nominal?
Aquí «estabilidad» se operacionaliza como desviaciones y variación de niveles en el
régimen local evaluado. «Minimizar» se limita a las alternativas nominales comparadas,
sin prometer mínimo global ni estabilidad robusta de un montaje no identificado plenamente.

## Pruebas exploratorias fijadas antes de ejecutarlas

Sin nuevas políticas ni ajuste de parámetros:

1. Seis desplazamientos iniciales de 1 cm: (+1,0), (−1,0), (0,+1), (0,−1), (+1,+1),
   (−1,−1), en cada una de las 10 excitaciones. Son pequeñas desviaciones de estado
   inicial próximas al equilibrio, no mediciones nuevas ni impulsos ocultos de volumen.
2. Tres perturbaciones aditivas del mando, comunes a E0/E1/E2: pulso +2 pp entre 400 y
   440 s, pulso −2 pp en el mismo intervalo y sesgo persistente −2 pp desde 400 s.
   Se conocen sólo al llegar su instante y se retienen causalmente. El mando se restringe
   a 0–100%; se informará cualquier saturación. No se modela una demanda hidráulica
   externa inventada ni se presenta una perturbación de mando como prueba de rechazo
   de perturbaciones de carga del montaje.
3. Se examinan equilibrio y Jacobiano locales de U, manteniendo el término de entrada
   dependiente de h1 y el circuito efectivo original. El equilibrio bajo mando 48% es
   una predicción matemática, no una medición. Sirve para advertir que un sesgo sostenido
   puede desplazar el nivel: ausencia de nueva desviación no se presume.

Las perturbaciones de mando son pequeñas frente al rango experimental; las iniciales
equivalen aproximadamente a dos códigos de sensor. Esto justifica una sensibilidad local,
sin atribuir exactitud certificada a los sensores ni robustez universal al modelo.
Se registran rangos y excursiones respecto al rectángulo de niveles medidos, sin ocultarlas.

La validación predictiva de U se reproduce separadamente con su configuración original,
sin perturbaciones: RMSE≈0.87253/0.24169 cm, NRMSE≈0.14581/0.07903.
Los pequeños RMSE de E2 son de regulación respecto al objetivo, no esa validación.
