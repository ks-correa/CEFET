# Auditoría del dataset CEFET-MG

Fuente primaria consultada el 8 de noviembre de 2026: [Zenodo](https://zenodo.org/records/19856119),
DOI 10.5281/zenodo.19856119, Silva, Coelho y Leite, versión 1.0.0 publicada el 28 de abril de 2026.
El registro confirma adquisición física en CEFET-MG y niveles cm, u %, Ts=4 s.
Es un dataset, no el texto completo de un artículo. README nombra dos artículos asociados,
pero no contiene DOI ni plano. No se recuperó un artículo primario que resolviera la topología.
La fecha exacta de medición, instrumento, precisión certificada y áreas no están disponibles.
Los autores externos realizaron las mediciones; la pareja realiza modelado secundario.
La página tiene un apartado de licencia sin texto visible: no inferir una licencia específica.

## Integridad y estructura

Los seis originales permanecen intactos. SHA256 en `data/processed/sha256.json`, comprobado
contra las huellas del paquete inicial mediante pruebas. Tipos, columnas, faltantes, duplicados,
monotonía y saltos por archivo se guardan en `audit.json`; estadísticos en `*_statistics.csv`.
No hay faltantes, filas idénticas completas, tiempos repetidos ni inversiones temporales.
Los niveles repetidos son esperables por cuantización, no se eliminan como duplicados.
Captura: 4502 filas, 0–18003.85177 s, dt mínimo 3.851924 s (primer intervalo), máximo
4.001683 s; ningún salto >6 s. Niveles positivos y u dentro de 0–100%.
Rangos completos: h1=3.01775–60.08167 cm; h2=2.15887–36.18931 cm;
u=1.19021–99.61347%. No se declara ausencia de fallas del sensor sólo por estar en rango.

Resolución aparente mínima de códigos: h1=0.452888220 cm,
h2=0.453739158 cm. No equivale a exactitud del instrumento.
Dispersión media entre repeticiones en el extracto corto (desviación muestral por tiempo):
h1=0.2127 cm; h2=0.1376 cm.
Valores extremos y saltos se conservan: no hay criterio documentado para retirarlos como anomalías.

## Reconstrucción de corridas

| run | start_row | end_row | duration_s | h1_initial | h2_initial | short_exact_match | excitation_intervals | recovery_complete |
|---|---|---|---|---|---|---|---|---|
| 1 | 476 | 901 | 1700 | 46.948 | 31.198 | True | 200 | True |
| 2 | 901 | 1326 | 1700 | 47.401 | 30.744 | True | 200 | True |
| 3 | 1326 | 1751 | 1700 | 46.948 | 30.744 | True | 200 | True |
| 4 | 1751 | 2176 | 1700 | 47.401 | 30.744 | True | 200 | True |
| 5 | 2176 | 2601 | 1700 | 47.401 | 30.744 | True | 200 | True |
| 6 | 2601 | 3026 | 1700 | 46.948 | 30.744 | True | 200 | True |
| 7 | 3026 | 3451 | 1700 | 46.948 | 30.744 | True | 200 | True |
| 8 | 3451 | 3876 | 1700 | 46.948 | 30.744 | True | 200 | True |
| 9 | 3876 | 4301 | 1700 | 46.948 | 30.744 | True | 200 | True |
| 10 | 4301 | 4501 | 800 | 47.401 | 30.744 | True | 200 | False |

Índices de origen basados en cero. Cada extracto corto coincide exactamente con los primeros
81 estados de su corrida larga en ambos tanques; U coincide con los primeros 80 intervalos.
Se verificaron estas igualdades por código. Las diez excitaciones completas comparten 200
intervalos y 40 escalones de 5 muestras (~20 s por escalón), no sólo diez niveles.
La señal completa se conserva en los CSV procesados. Las primeras 476 filas preceden la
excitación: incluyen arranque y aproximación al equilibrio; `startup.csv` incluye también
el estado frontera en t≈1903.85 s. No es una nueva corrida independiente.
Nueve corridas tienen excitación y recuperación; diez tienen excitación completa. La última
carece de recuperación. Cada frontera compartida sólo aporta condición inicial, nunca se
usa para reajustar el interior de una trayectoria.

## Inconsistencias

U.csv tiene 80 filas, no las 81 anunciadas; son suficientes para 80 intervalos/81 estados,
sin inventar una entrada final. README habla de diez niveles; se observan 16 en U corto
y 40 en las excitaciones largas. El registro Zenodo también describe diez niveles.
`operational_parameters.json` está truncado y no se puede parsear; contiene h3_op/h4_op
y mm, incompatibles con los niveles h1/h2 en cm. Se excluye del modelo sin editarlo.
Se usa el equilibrio redondeado documentado 47.4/31.2 cm; no se atribuye precisión de cuatro
decimales al archivo defectuoso. Los CSV no incluyen identificador de sensor ni fecha absoluta.

La división aleatoria de filas produciría fuga temporal. Se usan corridas agrupadas y nunca
se agrega `h1.csv` o `h2.csv` como observaciones adicionales a la captura larga.


## Comprobaciones adicionales ejecutadas

Los MD5 de los seis archivos originales coinciden con los seis publicados en la página
de Zenodo (incluido el JSON defectuoso). Esto vincula las copias locales con el registro
consultado; no resuelve las inconsistencias documentales.
