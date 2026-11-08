# Protocolo de desarrollo avanzado

Se conserva íntegra la primera etapa. Esta fase es búsqueda de desarrollo adaptativa sobre
datos ya examinados; no constituye validación externa ni ciega. Fecha: 8 de noviembre de 2026.

Antes de ejecutar la búsqueda se fijan estas familias: E transferencia lineal y salida raíz;
F exponentes de transferencia/salida entre 0.5 y 1; G resistencia mixta lineal/cuadrática
en transferencia; H resistencias mixtas en transferencia y salida; I transferencia lineal
y bomba cúbica monótona; J exponentes acotados y bomba cúbica monótona;
K transferencia lineal con zona muerta de bomba; L raíz con desfase de cabeza efectivo;
M cascada gravitacional sin contrapresión; O transferencia lineal con bomba exponencial
saturante; P estructura D con bomba cúbica monótona. C y D permanecen como referencias congeladas.
Cada hipótesis es condicional: no se conoce plano, Reynolds ni curva certificada.

No se usan funciones del tiempo ni coeficientes por escalón ni por corrida. Como máximo
seis parámetros globales por estructura. Todos mantienen dos balances compartiendo exactamente
la transferencia; caudales efectivos no negativos para el dominio evaluado.
La resistencia mixta interpola pérdidas lineales y cuadráticas de carga. La potencia 0.5–1
es una aproximación efectiva acotada, no identificación de un régimen de Reynolds.

Ajuste principal con 1–7, evaluación 8–10; mismo sigma de entrenamiento deduplicado y misma
puntuación por corrida/ventana que etapa 1. Cuatro inicializaciones, seed 20261108.
RK4 máximo 1 s. Comparación de cinco grupos contiguos de dos corridas para cada familia.
Prueba temporal: t<=320 s en 1–7; predicción libre posterior en 8–10. Arranque separado.

Objetivo inicial de cribado: mínimos cuadrados normalizados. Para los dos mejores candidatos
conservativos según peor NRMSE medio CV de ambos tanques, comparar además minimax de
MSE normalizado y minimax con penalización 1e-4 media(log(p/p_LS)^2) en los parámetros
estrictamente positivos. El regularizador ancla la solución LS del mismo entrenamiento;
no usa parámetros de las corridas reservadas. No comparar costes LS como si fueran minimax.
Se registran las variantes aunque empeoren. La puntuación sigue siendo MAE/RMSE/NRMSE originales.

En el mejor candidato físico de desarrollo, perfilar retardos causales 0,0.5,1,2,4,8 s
y constante de actuador 0,1,2,4,8 s. Cada perfil reajusta únicamente 1–7. El perfil se diagnostica
antes de admitir un parámetro adicional; la mejora de coste no basta para certificar tiempo
físico. Comparar el mejor perfil con retardo/actuador nulos por grupos para valorar estabilidad.
No admitir adelantos de entrada (retardo negativo). Antes de t=0 de cada corrida local,
usar u=50%; en arranque, historia previa desconocida se declara como supuesto.

Selección descriptiva multiobjetivo: priorizar el peor NRMSE de ambos tanques en CV,
revisar también excitación/recuperación, estabilidad por corrida, sesgos, condicionamiento,
cotas y sensibilidad. Una diferencia menor que 1% relativo se considera marginal y se
prefiere menor número de parámetros; no equivale a significación estadística. Reportar frontera
de Pareto y mínimos por tanque, que pueden pertenecer a candidatos distintos.
No prometer mínimo global de todas las formulaciones posibles.

## Extensión adaptativa declarada

Durante el cribado inicial, E–H no mejoraron D y J se aproximó a C sin superarlo.
Esto justifica examinar si el problema es la restricción entre caudal de equilibrio y
conductancia impuesta por leyes globales. Se añaden Q y R: balances locales con caudales
q12=q*+k12[(h1−h2)−16.2], qout=q*+kout(h2−31.2), coeficientes positivos, con bomba
potencial (Q, cinco parámetros) o cúbica monótona (R, seis). Son aproximaciones de Taylor
locales; los caudales se restringen a no negativos y deben inspeccionarse en el dominio.
No prueban una ley global de vaciado. La extrapolación en frío se conserva aunque falle.

Se añade S como control conceptual, seis parámetros: q12=q*+a(h1−47.4)−b(h2−31.2),
qout=q*+kout(h2−31.2), Qin=q*(u/50)^gamma. S puede reproducir algebraicamente C en el
dominio sin recorte: q*=50k_C, a=a_C, b=b_C, r=c_C/a_C, kout=d_C/r−b_C.
La transferencia con a≠b no es una función pura del desnivel. Este control NO convierte
a C en una hidráulica verificada ni constituye evidencia nueva de conservación real.
El balance matemático no cambia: d(h1+h2/r)/dt=qin−qout. S se clasifica como híbrido
empírico y una equivalencia con C no se contabiliza como mejora científica.

Se conservan todos los candidatos y se repiten las mismas particiones, criterios y
diagnósticos para Q/R/S. Los mejores candidatos se comparan con minimax y regularización;
la fase es explícitamente adaptativa, sin modificar la puntuación ni borrar ensayos previos.

Una segunda realización T mantiene q12 dependiente sólo del desnivel e incorpora
Qin=q*f(u)−kpump(h1−47.4), con kpump>=0: corrección local de caudal por carga de bomba.
Es coherente con una pendiente caudal-carga negativa de ciertas bombas, pero no se conoce
el tipo de bomba ni su curva en CEFET. T tiene seis parámetros y puede representar C
si kpump=a_C−b_C>=0, r=c_C/b_C y kout=d_C/r−b_C>0. Esta equivalencia debe declararse,
no se vende como una mejora independiente. La hipótesis causal no queda identificada.

U sustituye la potencia de T por una curva cúbica monótona de dos parámetros. Se amplía
explícitamente el límite inicial a siete parámetros globales sólo para esta ablación anidada:
permite separar una corrección de carga (apoyada por a_C>b_C) de la forma de bomba, sin
coeficientes dependientes del tiempo o corrida. Se penaliza su complejidad en la selección.
Esta extensión es exploratoria y debe demostrar mejora relevante por grupos antes de
recomendarse; la comparación no es confirmatoria ni descubre el mecanismo real de bomba.
El recorte de caudales evita flujos negativos pero no extiende la validez de Taylor al arranque.

Verificación: pasos 4,2,1,0.5 s, DOP853 segmentado en eventos, sensibilidad inicial ±medio
código y parámetros +1%, Jacobiano relativo y perfiles de coste. Residuos por corrida,
no concatenados sin discontinuidades; ACF/Ljung–Box descriptivos. Repetir ajustes principales
y comparar artefactos deterministas. Guardar hashes antes/después de originales y primera etapa.
