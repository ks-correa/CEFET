# Modelos continuos y límites físicos

Hechos documentados: dos tanques cilíndricos acoplados, niveles en cm, bomba 0–100%,
punto operativo (47.4,31.2,50). No se dispone de esquema de válvulas, áreas, alturas de
conexión, sensores ni curva caudal-bomba. La búsqueda por títulos exactos de los dos
artículos citados en README no permitió recuperar su texto. Por tanto, no se certifica
que el montaje sea exactamente la siguiente hipótesis:

```text
u (%) → bomba → Qin → [tanque 1, h1, A1] → Q12 → [tanque 2, h2, A2] → Qout
```

Este es un diagrama conceptual hipotético, sin valor de fotografía o evidencia del montaje.
Se requiere documentación primaria del circuito antes de defender esa topología como real.

Balances bajo la hipótesis: A1 dh1/dt=Qin−Q12; A2 dh2/dt=Q12−Qout.
Definir r=A1/A2, s=C12/A1. Los modelos B,D implementan

q12=s sqrt(max(h1−h2,0)); qin=s sqrt(16.2) (u/50)^gamma;
qout=s sqrt(16.2/31.2) sqrt(max(h2,0));
dh1/dt=qin−q12; dh2/dt=r(q12−qout).

Los q son Q/A1 (cm/s), no litros/s. s tiene unidades sqrt(cm)/s; r y gamma son
adimensionales. B fija gamma=1; D lo estima entre 0.2 y 4. La potencia es una
aproximación parsimoniosa de respuesta de bomba, no una curva medida. Equilibrio impuesto
al punto documentado. Caudales no negativos para u>=0; no modela inversión de flujo.
La singularidad de la raíz en nivel cero limita la extrapolación y el orden numérico efectivo.

Conservación: d(h1+h2/r)/dt=qin−qout. Multiplicar por A1 restituye volumen real, pero A1
no es conocido. La identidad sólo verifica coherencia algebraica del modelo condicional;
no demuestra conservación medida. Escalar conjuntamente áreas y coeficientes de caudal
deja las trayectorias iguales: no son identificables por separado a partir de estos niveles.
La igualdad nominal de capacidad no prueba igualdad de áreas.

Modelos A,C: x=h−h*, dx1/dt=−a x1+b x2+k v; dx2/dt=c x1−d x2.
a=bc/d+e, b,c,d,e,k>0 garantiza traza negativa y determinante ed>0.
A usa v=u−50; C usa v=50[(u/50)^gamma−1]. b,c,d,e en s^-1,
k en cm/(s punto porcentual). Modelo local de acoplamiento y disipación; no permite
atribuir un caudal volumétrico único ni certificar conservación sin estructura adicional.
La segunda ecuación representa transferencia local neta. No se confunde esta representación
con un balance geométrico demostrado del montaje. No garantiza positividad global;
se inspeccionan las trayectorias del dominio observado y se reporta la extrapolación.

Los balances por tanque explican la hipótesis física; el modelo lineal sirve además como
referencia básica. No se elige una estructura física por similitud gráfica solamente.

RK4 calcula simultáneamente ambos estados con cuatro pendientes. Cada intervalo entre
registros se subdivide en ceil(dt/paso) subpasos; todos usan u[i], incluida la última
pendiente. Al pasar a t[i+1] se cambia la entrada. Así ninguna pendiente usa una entrada
futura ni un nivel futuro observado. Se usan los tiempos reales, no se redondean a 4 s.
La condición inicial medida se introduce una sola vez por corrida.

## Actualización de fase 3

El modelo principal de la aplicación es U_bomba_carga_monotona__retardo, código 15 de src/precision_models.py; parámetros exactos en anexo B. La app expone sus ecuaciones completas. q12=max(0,q*+k12[(h1−h2)−16.2]); qout=max(0,q*+kout[h2−31.2]); Qin/A1=max(0,q*F(u(t−2)/100)/F(0.5)−kpump[h1−47.4]); F(z)=z+(b−1)z²+(1−2b+c)z³/3. dh1/dt=qin−q12; dh2/dt=r(q12−qout). El motor reutiliza RK4 verificado, particiona cambios discontinuos y usa u=50% antes del inicio. No corrige estados con mediciones futuras. La representación animada sólo reproduce esos estados y no integra ecuaciones propias.
