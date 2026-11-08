# Modelo matemático y variables vigentes

U_bomba_carga_monotona__retardo, exactamente src/precision_models.py, código 15.
h1,h2 en cm; t en s; u en porcentaje; referencias h*=(47.4,31.2) cm, u*=50%.
q=Q/A1 en cm/s, r=A1/A2 efectivo. No se conoce A1 ni se convierte a litros/s.

```text
dh1/dt = qin - q12
dh2/dt = r (q12 - qout)
q12 = max(0, qstar + k12 [(h1-h2)-16.2])
qout = max(0, qstar + kout [h2-31.2])
z = u(t-2)/100
F(z) = z + (b-1)z² + (1-2b+c)z³/3
qin = max(0, qstar F(z)/F(0.5) - kpump [h1-47.4])
```

| parámetro | valor | unidad |
|---|---|---|
| qstar | 1.1901768213433377 | cm/s (Q/A1) |
| r | 0.28068693475733053 | adimensional; A1/A2 efectivo |
| k12 | 0.039766247050466483 | s⁻¹ |
| kout | 0.011857107887654482 | s⁻¹ |
| kpump | 0.0032622340261774787 | s⁻¹ |
| b | 0.71741375825579845 | adimensional |
| c | 0.58172099393448107 | adimensional |

Fuente exacta: reports/optimizacion_precision/all_fits.json → U → principal. Son siete
coeficientes globales; el desfase efectivo es 2 s. La condición inicial se aplica una vez,
sin corregir estados posteriores con observaciones futuras. Antes de t=0 se retiene u=50%.
La identidad d(h1+h2/r)/dt=qin−qout es un balance efectivo. No certifica volúmenes absolutos
ni la topología hidráulica precisa. El esquema gráfico normaliza alturas y no capacidad en litros.
El recorte no amplía la validez de las conductancias locales al arranque o vaciado.
