# Diagnóstico de C y D

Se conservaron parámetros y ecuaciones originales, sin recalibrarlos. Las nuevas tablas
reproducen exactamente sus puntuaciones compartidas con la primera etapa (prueba automática).
La evaluación sigue siendo desarrollo con series previamente examinadas.

Jacobianos en el equilibrio y relaciones de sensibilidad:

```json
{
  "C_bomba": {
    "jacobian": [
      [
        -0.03477568994083348,
        0.031273152836894254
      ],
      [
        0.010643101000163356,
        -0.01382815829046582
      ]
    ],
    "eigenvalues_real_imag": [
      [
        -0.045338632384706375,
        0.0
      ],
      [
        -0.0032652158465929296,
        0.0
      ]
    ],
    "damping_to_coupling_h2": 1.2992602710670111,
    "h1_head_derivative_ratio": 1.1119982088856464
  },
  "D_conservativo": {
    "jacobian": [
      [
        -0.036464723340845495,
        0.03646483588637395
      ],
      [
        0.010522149299303927,
        -0.01598560950341989
      ]
    ],
    "eigenvalues_real_imag": [
      [
        -0.04832803893370009,
        0.0
      ],
      [
        -0.004122293910565299,
        0.0
      ]
    ],
    "damping_to_coupling_h2": 1.5192342409052673,
    "h1_head_derivative_ratio": 0.9999969135874133
  }
}
```

D impone q12=s sqrt(h1−h2) y qout=s sqrt(16.2/31.2) sqrt(h2): las derivadas de transferencia
frente a h1 y h2 tienen magnitudes iguales, y la relación amortiguamiento/acoplamiento de h2
es 1+16.2/31.2=1.51923. C estima esas sensibilidades por separado. Ésta es una diferencia
estructural comprobada, no una prueba de que una válvula o un sensor concretos sean la causa.
Los exponentes y resistencias alternativos constituyen ablaciones para comprobar esa hipótesis.

Sesgos y errores de ambas referencias por fase:

| model | window | tank | MAE | RMSE | NRMSE | bias |
|---|---|---|---|---|---|---|
| C_bomba | completa | h1 | 0.76006 | 1.0808 | 0.1806 | -0.28408 |
| C_bomba | completa | h2 | 0.2061 | 0.26865 | 0.087843 | 0.13059 |
| C_bomba | excitacion | h1 | 1.0681 | 1.352 | 0.22593 | -0.48116 |
| C_bomba | excitacion | h2 | 0.23475 | 0.30492 | 0.099703 | 0.14251 |
| C_bomba | inicial_320 | h1 | 1.1459 | 1.4943 | 0.2497 | -0.77196 |
| C_bomba | inicial_320 | h2 | 0.2968 | 0.38128 | 0.12467 | 0.26169 |
| C_bomba | recuperacion | h1 | 0.18586 | 0.23718 | 0.039634 | 0.069539 |
| C_bomba | recuperacion | h2 | 0.14289 | 0.1751 | 0.057255 | 0.092432 |
| C_bomba | tardia_320 | h1 | 0.65623 | 0.92314 | 0.15426 | -0.13058 |
| C_bomba | tardia_320 | h2 | 0.17241 | 0.2142 | 0.070038 | 0.078224 |
| D_conservativo | completa | h1 | 0.92948 | 1.256 | 0.20989 | 0.10485 |
| D_conservativo | completa | h2 | 0.67855 | 0.79464 | 0.25983 | 0.45557 |
| D_conservativo | excitacion | h1 | 1.1344 | 1.5075 | 0.25191 | -0.13693 |
| D_conservativo | excitacion | h2 | 0.67512 | 0.81223 | 0.26558 | 0.32145 |
| D_conservativo | inicial_320 | h1 | 1.271 | 1.6773 | 0.28029 | -0.87618 |
| D_conservativo | inicial_320 | h2 | 0.35414 | 0.44576 | 0.14575 | -0.3182 |
| D_conservativo | recuperacion | h1 | 0.55023 | 0.6217 | 0.10389 | 0.54265 |
| D_conservativo | recuperacion | h2 | 0.69005 | 0.76295 | 0.24947 | 0.68907 |
| D_conservativo | tardia_320 | h1 | 0.82909 | 1.0992 | 0.18368 | 0.43981 |
| D_conservativo | tardia_320 | h2 | 0.80632 | 0.89485 | 0.2926 | 0.72708 |

Los signos son simulado−real. Un sesgo de h2 no se elimina automáticamente cambiando sólo
la potencia de bomba. `baseline_lag_correlations.csv` informa correlaciones residuo–entrada
pasada, pero la entrada escalonada y la memoria hidráulica impiden identificarlas con retardo
físico. Los perfiles con entradas causalmente desplazadas son la comprobación de modelo.

La sensibilidad inicial se estudia ±medio código y se conserva la trayectoria libre.
Cuantización aproximada 0.45289/0.45374 cm; precisión certificada del sensor desconocida.
La falta de geometría, caudal y señales distintas impide resolver de manera única si el sesgo
procede de ley de descarga, bomba, datum de nivel, ajuste de equilibrio o dinámica omitida.


## Ablación de dinámica de entrada

| model | RMSE_h1 | RMSE_h2 | NRMSE_h1 | NRMSE_h2 | CV_peor_NRMSE |
|---|---|---|---|---|---|
| P_D_bomba_monotona__retardo | 0.84433 | 0.30306 | 0.14109 | 0.099095 | 0.12624 |
| P_D_bomba_monotona__actuador | 0.84541 | 0.30356 | 0.14127 | 0.099257 | 0.12645 |
| U_bomba_carga_monotona__retardo | 0.87253 | 0.24169 | 0.14581 | 0.079027 | 0.1297 |
| U_bomba_carga_monotona__actuador | 0.88186 | 0.23484 | 0.14737 | 0.07679 | 0.13005 |
| U_bomba_carga_monotona | 1.0754 | 0.2727 | 0.17971 | 0.089168 | 0.16119 |
| P_D_bomba_monotona | 1.0886 | 0.30912 | 0.18191 | 0.10108 | 0.16357 |

La comparación mantiene la familia y vuelve a estimar sus parámetros con desarrollo.
La mejora al admitir desfase se sostiene entre grupos, lo que respalda una corrección
temporal efectiva de reproducción. No demuestra si su origen es bomba, adquisición o
transporte hidráulico. El mecanismo no se puede separar con estas señales solamente.
Una curva estática más flexible por sí sola no produjo la mayor parte de la reducción.
