# Esquema definitivo de trece diapositivas para revisión

Títulos y orden comprobados contra la guía original. No se crea el PowerPoint. Todas las fuentes son rutas desde CEFET_MG. Nombres y fecha de sustentación por completar.

## 1. Portada

**Objetivo:** Identificar el trabajo, autores y alcance.

**Contenido resumido:** Título propuesto: Modelado local y simulación de dos tanques CEFET-MG. Asignatura Modelado y Simulación. Integrantes y fecha de sustentación por completar.

**Datos verificables:** Título del proyecto y asignatura documentados. Nombres de integrantes y fecha de sustentación pendientes.

**Gráfica o figura:** Título tipográfico, sin fotografía ficticia ni resultados decorativos.

**Archivo fuente:** `docs/anexos_proyecto.md`; `referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`

**Explicación oral sugerida:** Presentamos un trabajo de modelado con registros publicados de un montaje real. Las mediciones pertenecen a los investigadores y nuestro aporte es su análisis y simulación.

**Limitaciones que no deben omitirse:** Faltan nombres de los dos integrantes y fecha de sustentación. No inventarlos.

## 2. Problema y pregunta de decisión

**Objetivo:** Vincular variabilidad de bombeo, desviaciones locales y decisión nominal.

**Contenido resumido:** ¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal? Se limita a alternativas evaluadas cerca del equilibrio, sin demanda externa documentada.

**Datos verificables:** Referencias nominales 47.4/31.2 cm y 50%. Sin demanda externa documentada.

**Gráfica o figura:** Breve contraste entre entrada de identificación y operación nominal. La revisión se sustenta en el diagnóstico D50.

**Archivo fuente:** `docs/consolidacion_final/definicion_problema.md`; `data/raw/README.md`

**Explicación oral sugerida:** Comparamos la respuesta de los niveles ante distinta variabilidad de mando. La decisión vale para el régimen nominal estudiado y para este conjunto de alternativas.

**Limitaciones que no deben omitirse:** No hay demanda externa ni consigna móvil documentada. Una restricción que excluya D50 sería una hipótesis nueva.

## 3. Esquema del sistema

**Objetivo:** Explicar estados, frontera del modelo y conexión supuesta.

**Contenido resumido:** Dos niveles h1/h2, bomba y flujos efectivos qin/q12/qout. La misma transferencia sale del primer balance y entra al segundo. Áreas absolutas y circuito preciso no identificados.

**Datos verificables:** Dos estados y tres flujos efectivos. El dibujo representa el modelo, no la geometría certificada.

**Gráfica o figura:** Recorte de la escena vigente de los dos tanques, sin presentarla como plano ni fotografía.

**Archivo fuente:** `reports/consolidacion_final/figures/aplicacion_vigente.png`; `src/simulation_engine.py`; `docs/consolidacion_final/modelo_y_variables.md`

**Explicación oral sugerida:** La transferencia aparece con signos opuestos en ambos balances. El esquema explica el modelo; no contiene áreas ni conexiones medidas por nosotros.

**Limitaciones que no deben omitirse:** No presentar alturas de conexiones, áreas o tuberías del dibujo como geometría medida.

## 4. Datos reales

**Objetivo:** Demostrar origen experimental y trazabilidad sin atribuir mediciones a los estudiantes.

**Contenido resumido:** Dataset de Silva, Coelho y Leite, CEFET-MG. 4502 registros en captura completa, niveles cm, bomba %, muestreo ≈4 s. Diez extractos cortos son partes de la captura larga. La señal se repite. Uso externo autorizado según comunicación del usuario.

**Datos verificables:** 4502 filas en captura larga; muestreo ≈4 s; diez repeticiones; unidades cm y %; cuantización aparente ≈0.453 cm.

**Gráfica o figura:** Gráfica exploratoria de captura completa y tabla pequeña de archivos/variables. Cuantización aparente ≈0.453 cm por código.

**Archivo fuente:** `reports/figures/exploracion.png`; `reports/auditoria_dataset.md`; `data/raw/README.md`; `docs/anexos_proyecto.md`

**Explicación oral sugerida:** Los datos tienen trazabilidad y unidades documentadas. Las diez corridas cortas son partes de la captura larga y repiten una señal, por lo que no duplicamos observaciones.

**Limitaciones que no deben omitirse:** Instrumento específico, fecha exacta de adquisición y fotografías verificadas no disponibles. Autorización comunicada, sin acta adjunta. No equiparar cuantización con exactitud certificada.

## 5. Variables, parámetros y unidades

**Objetivo:** Fijar unidades y distinguir coeficientes efectivos de geometría real.

**Contenido resumido:** h1/h2 cm, t s, u %, referencias 47.4/31.2 cm y 50%. Siete parámetros globales de U y desfase efectivo 2 s. q=Q/A1 en cm/s, r=A1/A2. Condición inicial del primer registro, una sola vez.

**Datos verificables:** Siete parámetros de U, sin ajuste nuevo; desfase efectivo 2 s; tabla con valores completos.

**Gráfica o figura:** Tabla de parametros_U.csv con valores exactos; redondeo sólo visual indicando que se ejecutan los valores completos.

**Archivo fuente:** `reports/consolidacion_final/parametros_U_vigentes.csv`; `docs/consolidacion_final/anexos_A_B_C.md`

**Explicación oral sugerida:** Estos valores efectivos se cargan completos del archivo calibrado. No conocemos áreas para convertirlos a litros por segundo.

**Limitaciones que no deben omitirse:** No convertir a litros/s ni deducir áreas a partir de capacidad nominal. Los 2 s no son retardo físico certificado.

## 6. Modelo matemático

**Objetivo:** Mostrar una EDO por tanque y sus hipótesis locales.

**Contenido resumido:** dh1/dt=qin−q12; dh2/dt=r(q12−qout). q12 y qout son conductancias locales con caudales no negativos. qin usa curva cúbica monótona y corrección por h1. Señal causal u(t−2). Identidad efectiva d(h1+h2/r)/dt=qin−qout.

**Datos verificables:** Dos EDO y las expresiones exactas de qin, q12, qout y F(z), código 15.

**Gráfica o figura:** Ecuaciones exactas de U código 15, con definición F(z)=z+(b−1)z²+(1−2b+c)z³/3, sin sustituirlas por una raíz de Torricelli global.

**Archivo fuente:** `src/precision_models.py`; `docs/consolidacion_final/modelo_y_variables.md`

**Explicación oral sugerida:** U describe balances locales. La bomba tiene curva monótona y dependencia efectiva de la altura; no estamos afirmando una curva física certificada del equipo.

**Limitaciones que no deben omitirse:** Balance matemático local, sin conservación volumétrica global certificada ni interpretación física única del circuito.

## 7. Implementación

**Objetivo:** Explicar que el motor y la animación usan una sola trayectoria.

**Contenido resumido:** Python y RK4 simultáneo, paso máximo 1 s, eventos de entrada particionados y mando previo 50%. La animación reproduce estados calculados. Comprobaciones de finitud, no negatividad, causalidad y comparación DOP853.

**Datos verificables:** RK4 máximo 1 s, eventos causales; tanques comparados con estados calculados; pruebas en navegador.

**Gráfica o figura:** Captura del simulador y tabla numérica de verificación. D50 difiere de DOP853 ≈10⁻⁶ cm en las corridas comprobadas.

**Archivo fuente:** `src/simulation_engine.py`; `reports/consolidacion_final/browser_checks.json`; `docs/consolidacion_final/rk4_calibracion_validacion.md`

**Explicación oral sugerida:** RK4 integra ambos estados juntos y cambia la entrada sólo cuando corresponde. La animación reproduce esa trayectoria y su velocidad no cambia las ecuaciones.

**Limitaciones que no deben omitirse:** La velocidad de reproducción visual no cambia la integración. No hay mediciones en vivo ni un segundo motor de animación.

## 8. Calibración

**Objetivo:** Documentar cómo se obtuvieron los parámetros sin reajustar para escenarios.

**Contenido resumido:** Mínimos cuadrados normalizados conjuntos, multinicio reproducible, escalas de entrenamiento por filas únicas. Ajuste principal corridas 1–7 completas. U conserva siete coeficientes; el perfil de desfase usa 2 s. La exploración de 30 variantes usó datos ya examinados.

**Datos verificables:** Entrenamiento principal 1–7; evaluación interna 8–10; cuatro inicializaciones; 30 variantes exploradas.

**Gráfica o figura:** Tabla reducida de parámetros finales y esquema de particiones 1–7 / 8–10. No mostrar una nueva calibración para D50 ni para la ablación de media.

**Archivo fuente:** `src/precision_study.py`; `docs/protocolo_optimizacion.md`; `reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json`; `reports/optimizacion_precision/campaign_summary.json`

**Explicación oral sugerida:** Los coeficientes se estimaron con desarrollo y se conservaron. La exploración previa de variantes obliga a llamar interna a la evaluación.

**Limitaciones que no deben omitirse:** Elegir entre 30 variantes reduce independencia de la evaluación. El offset de mando de la ablación no es un nuevo parámetro calibrado de U.

## 9. Validación

**Objetivo:** Cuantificar reproducción de datos y declarar su calidad de evidencia.

**Contenido resumido:** Evaluación interna previamente examinada. U: RMSE h1≈0.87253 cm, h2≈0.24169 cm; NRMSE≈0.14581/0.07903; MAE según tabla reproducida. NRMSE divide por sigma de entrenamiento. Promedios por corrida 8–10 en horizontes disponibles, no RMSE agrupado. CV por grupos y residuos autocorrelacionados.

**Datos verificables:** RMSE predictivo U: 0.87253/0.24169 cm; NRMSE: 0.14581/0.07903; MAE: 0.62896/0.18748 cm, medias por corrida.

**Gráfica o figura:** Trayectorias observadas frente a U en corridas 8–10 y tabla breve de métricas; ACF como apoyo o evidencia enlazada.

**Archivo fuente:** `reports/consolidacion_final/validacion_U_sin_cambios.csv`; `reports/optimizacion_precision/figures/trajectories_U_bomba_carga_monotona__retardo.png`; `reports/optimizacion_precision/residual_diagnostics.json`

**Explicación oral sugerida:** Aquí medimos error contra observaciones reales. Estos RMSE son distintos de las desviaciones respecto al objetivo que aparecerán al comparar escenarios.

**Limitaciones que no deben omitirse:** No es validación externa. NRMSE no es porcentaje del nivel. La corrida 10 no tiene recuperación; no afirmar precisión en arranque o señales nuevas.

## 10. Escenarios

**Objetivo:** Explicar exactamente los tres escenarios vigentes y sus condiciones comunes.

**Contenido resumido:** E0 mando experimental; E1=50+0.8(u0−50); E2=50% constante. Mismos U, h0, tiempos, parámetros, paso y referencias. El antiguo suavizado queda como S_HIST complementario. Revisión posterior al diagnóstico.

**Datos verificables:** Tres escenarios principales, 10 excitaciones (~800 s) y 9 corridas con recuperación (~1700 s).

**Gráfica o figura:** Señales escalonadas de la comparación vigente y mapa de versiones.

**Archivo fuente:** `docs/consolidacion_final/protocolo_vigente.md`; `src/final_scenarios.py`; `reports/consolidacion_final/figures/escenarios_vigentes.png`

**Explicación oral sugerida:** La revisión incorpora el mando constante como E2. La antigua señal suavizada sigue disponible como complemento; declaramos que cambiamos el conjunto después del diagnóstico.

**Limitaciones que no deben omitirse:** No fue la selección previa original. E1/E2 no tienen mediciones contrafactuales y la entrada de identificación tiene otra finalidad.

## 11. Resultados y comparación

**Objetivo:** Comparar tres escenarios con números calculados y dos tipos de error separados.

**Contenido resumido:** RMSE de regulación y mando medio/TV: E0≈9.10264/5.00727 cm; E1≈7.01683/3.77536; E2≈0.19707/0.19702 en corrida 8, ≈800 s. La tabla predictiva de U permanece aparte. Resumen sobre diez excitaciones y nueve recuperaciones.

**Datos verificables:** Corrida 8: E2 mando medio 50%, TV=0, RMSE de regulación ≈0.19707/0.19702 cm; revisar tabla fuente exacta.

**Gráfica o figura:** Tabla breve de tres filas y gráfica vigente. Señalar que el índice relativo de esfuerzo de E2 es cero, sin inferir energía eléctrica.

**Archivo fuente:** `reports/consolidacion_final/comparacion_principal.csv`; `reports/consolidacion_final/resumen_excitaciones.csv`; `reports/consolidacion_final/figures/escenarios_vigentes.png`

**Explicación oral sugerida:** La constante reduce las desviaciones nominales porque evita excitar el equilibrio. Que su índice relativo de esfuerzo sea cero no significa que la bomba no consuma.

**Limitaciones que no deben omitirse:** No comparar estos RMSE contra el objetivo con RMSE de predicción contra mediciones. No inferir ahorro eléctrico ni seguridad.

## 12. Decisión, limitaciones y conclusiones

**Objetivo:** Defender E2 nominalmente y acotar la sensibilidad simulada.

**Contenido resumido:** E2 es la mejor alternativa nominal evaluada: 19/19 comparaciones. Se mantiene en 90 sensibilidades exploratorias. El equilibrio está incorporado a U y h0 es próximo. Sesgo sostenido desplaza el equilibrio; no hay prueba de rechazo de perturbaciones reales.

**Datos verificables:** 19 decisiones nominales E2; 90 exploratorias E2; equilibrio calculado a 48%≈(44.056,28.624) cm.

**Gráfica o figura:** Conteo de decisiones, figura de sensibilidad y predicción del equilibrio a 48%.

**Archivo fuente:** `reports/consolidacion_final/decisiones_vigentes.json`; `reports/consolidacion_final/robustez/decisiones.json`; `reports/consolidacion_final/figures/sensibilidad_E2.png`; `docs/consolidacion_final/solidez_y_limitaciones.md`

**Explicación oral sugerida:** La recomendación es E2 bajo estas condiciones. Las pruebas pequeñas no prueban rechazo de perturbaciones, y un sesgo sostenido desplaza los niveles calculados.

**Limitaciones que no deben omitirse:** Sin óptimo global, política física ensayada, generalización externa, ahorro de energía ni robustez experimental. Informar excursiones de E0/E1 fuera del rectángulo medido.

## 13. Referencias y evidencias

**Objetivo:** Permitir comprobar origen, cálculos y límites sin inventar anexos.

**Contenido resumido:** Zenodo DOI 10.5281/zenodo.19856119; Silva, Coelho y Leite. README experimental y guía docente. Código, parámetros, huellas, informes y pruebas. Diferenciar autorización comunicada de un acta adjunta inexistente.

**Datos verificables:** DOI 10.5281/zenodo.19856119, autores Silva/Coelho/Leite; huellas de archivos y rutas de reproducción.

**Gráfica o figura:** Bibliografía breve y rutas reproducibles del proyecto. Referencias enlazadas a los datos y comandos de reproducción.

**Archivo fuente:** `https://doi.org/10.5281/zenodo.19856119`; `data/raw/README.md`; `referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`; `reports/consolidacion_final/integridad.json`; `docs/consolidacion_final/registro_metodologico.md`

**Explicación oral sugerida:** Las fuentes permiten revisar cada cifra. Conservamos originales, resultados históricos, código y pruebas sin inventar fotografías ni mediciones propias.

**Limitaciones que no deben omitirse:** No hay fotos propias, repositorio remoto informado ni texto completo verificado de los artículos asociados. No atribuir esas evidencias a la pareja.

