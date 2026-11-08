# Hipótesis investigadas

| model | parameters | hypothesis |
|---|---|---|
| E_lineal_raiz | 3 | Transferencia proporcional al desnivel; salida gravitacional |
| F_exponentes | 5 | Leyes efectivas de cabeza con exponente entre laminar y raíz |
| G_resistencia_mixta | 4 | Pérdida de carga lineal más cuadrática en conexión |
| H_doble_resistencia | 5 | Resistencias mixtas en conexión y salida |
| I_bomba_monotona | 4 | Transferencia lineal, salida raíz, curva cúbica monótona |
| J_flexible_restringido | 6 | Exponentes acotados y curva cúbica monótona |
| K_zona_muerta | 4 | Zona muerta efectiva, no certificada; transferencia lineal |
| L_cabeza_efectiva | 4 | Desfase efectivo de cotas entre tanques; no geometría identificada |
| M_cascada | 3 | Descarga de T1 independiente de T2; cascada sin contrapresión |
| O_bomba_saturante | 3 | Bomba exponencial saturante, conexión lineal |
| P_D_bomba_monotona | 4 | Transferencia/salida raíz como D, curva cúbica monótona |
| Q_balance_local | 5 | Conductancias locales positivas, transferencia por desnivel y salida linealizadas |
| R_balance_monotono | 6 | Balances con conductancias locales y bomba cúbica monótona |
| S_balance_empirico_C | 6 | Realización local conservativa de C con transferencia empírica no sólo función del desnivel |
| T_bomba_carga_local | 6 | Balance local: bomba decreciente con carga h1 y transferencia por desnivel |
| U_bomba_carga_monotona | 7 | Balance local: bomba cúbica monótona con corrección de carga h1 |

Todos son balances efectivos bajo circuito hipotético. No se ha confirmado si la conexión
es comunicante, en cascada o con válvulas. M cambia expresamente esa hipótesis y se conserva
aunque empeore. L no identifica una altura de conexión física: es una cabeza efectiva
confundible con referencias de sensor y pérdida no modelada. K no certifica una zona muerta.

La ley de pérdidas lineal/cuadrática se apoya en el marco de conductancias y pérdidas de
carga descrito por [EPA EPANET](https://github.com/USEPA/EPANET2.2/blob/master/User_Manual/docs/3_network_model.rst).
No se calcula Reynolds ni se aplica EPANET como modelo del montaje. La dependencia de bomba
con carga es una hipótesis local compatible con curvas caudal–carga descritas por
[Hydraulic Institute](https://datatool.pumps.org/pump-fundamentals/pump-curves).
No se conoce el tipo ni la curva del equipo concreto; ninguna fuente certifica los coeficientes estimados.

Q/R son linealizaciones de caudales alrededor del equilibrio; T/U añaden efecto local de
carga en la entrada. S es un control algebraico empírico, no descubrimiento de una nueva física.
No se usan coeficientes por tiempo, escalón o corrida ni correcciones con niveles futuros.
La ampliación adaptativa y el séptimo parámetro de U se declaran en el protocolo.
