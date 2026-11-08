# Esquema revisado de las 13 diapositivas

Documento para revisión previa al PowerPoint. Conserva exactamente los títulos y el orden
de la sección 3 de la guía docente, comprobados por código. No se genera un PPTX.
Cada bloque especifica objetivo, contenido verificable, gráfica/evidencia, fuente y límite.
Las rutas se expresan desde la raíz CEFET_MG. Nombres y fecha de sustentación siguen pendientes.

Clave de lectura: «observado» son registros físicos de los investigadores; «predicción»
son estados calculados comparados internamente con esos registros; «contrafactual» son
escenarios sin una medición correspondiente. El resultado pequeño de D50 es regulación
frente a un objetivo, sin implicar nueva precisión predictiva.

## 1. Portada

**Objetivo:** Identificar el trabajo, autores y alcance.

**Contenido:** Título propuesto: Modelado local y simulación de dos tanques CEFET-MG. Asignatura Modelado y Simulación. Integrantes y fecha de sustentación por completar.

**Gráfica o evidencia:** Título tipográfico, sin fotografía ficticia ni resultados decorativos.

**Fuentes:** `docs/anexos_proyecto.md`; `referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`

**Límite o afirmación pendiente:** Faltan nombres de los dos integrantes y fecha de sustentación. No inventarlos.

## 2. Problema y pregunta de decisión

**Objetivo:** Separar identificación experimental de regulación nominal y formular una decisión que incluya la constante.

**Contenido:** Reproducir niveles reales con un modelo local. Pregunta revisada: ¿conviene mantener 50% o transformar la excitación experimental para regular ambos niveles, sin demandas externas documentadas? No partir de que una señal variable sea necesaria.

**Gráfica o evidencia:** Breve contraste entre entrada de identificación y operación nominal. La revisión se sustenta en el diagnóstico D50.

**Fuentes:** `docs/definicion_problema.md`; `data/raw/README.md`; `reports/diagnostico_control_constante/informe_diagnostico.md`

**Límite o afirmación pendiente:** No hay demanda externa ni consigna móvil documentada. Una restricción que excluya D50 sería una hipótesis nueva.

## 3. Esquema del sistema

**Objetivo:** Explicar estados, frontera del modelo y conexión supuesta.

**Contenido:** Dos niveles h1/h2, bomba y flujos efectivos qin/q12/qout. La misma transferencia sale del primer balance y entra al segundo. Áreas absolutas y circuito preciso no identificados.

**Gráfica o evidencia:** Recorte de la escena del simulador, rotulado como esquema conceptual del modelo, no plano real ni fotografía.

**Fuentes:** `reports/simulador/figures/aplicacion_sistema.png`; `src/simulation_engine.py`; `docs/modelo_matematico.md`

**Límite o afirmación pendiente:** No presentar alturas de conexiones, áreas o tuberías del dibujo como geometría medida.

## 4. Datos reales

**Objetivo:** Demostrar origen experimental y trazabilidad sin atribuir mediciones a los estudiantes.

**Contenido:** Dataset de Silva, Coelho y Leite, CEFET-MG. 4502 registros en captura completa, niveles cm, bomba %, muestreo ≈4 s. Diez extractos cortos son partes de la captura larga. La señal se repite. Uso externo autorizado según comunicación del usuario.

**Gráfica o evidencia:** Gráfica exploratoria de captura completa y tabla pequeña de archivos/variables. Cuantización aparente ≈0.453 cm por código.

**Fuentes:** `reports/figures/exploracion.png`; `reports/auditoria_dataset.md`; `data/raw/README.md`; `docs/anexos_proyecto.md`

**Límite o afirmación pendiente:** Instrumento específico, fecha exacta de adquisición y fotografías verificadas no disponibles. Autorización comunicada, sin acta adjunta. No equiparar cuantización con exactitud certificada.

## 5. Variables, parámetros y unidades

**Objetivo:** Fijar unidades y distinguir coeficientes efectivos de geometría real.

**Contenido:** h1/h2 cm, t s, u %, referencias 47.4/31.2 cm y 50%. Siete parámetros globales de U y desfase efectivo 2 s. q=Q/A1 en cm/s, r=A1/A2. Condición inicial del primer registro, una sola vez.

**Gráfica o evidencia:** Tabla de parametros_U.csv con valores exactos; redondeo sólo visual indicando que se ejecutan los valores completos.

**Fuentes:** `reports/simulador/parametros_U.csv`; `docs/anexos_proyecto.md`; `reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json`

**Límite o afirmación pendiente:** No convertir a litros/s ni deducir áreas a partir de capacidad nominal. Los 2 s no son retardo físico certificado.

## 6. Modelo matemático

**Objetivo:** Mostrar una EDO por tanque y sus hipótesis locales.

**Contenido:** dh1/dt=qin−q12; dh2/dt=r(q12−qout). q12 y qout son conductancias locales con caudales no negativos. qin usa curva cúbica monótona y corrección por h1. Señal causal u(t−2). Identidad efectiva d(h1+h2/r)/dt=qin−qout.

**Gráfica o evidencia:** Ecuaciones exactas de U código 15, con definición F(z)=z+(b−1)z²+(1−2b+c)z³/3, sin sustituirlas por una raíz de Torricelli global.

**Fuentes:** `src/precision_models.py`; `docs/modelo_matematico.md`; `reports/optimizacion_precision/modelos_candidatos.md`

**Límite o afirmación pendiente:** Balance matemático local, sin conservación volumétrica global certificada ni interpretación física única del circuito.

## 7. Implementación

**Objetivo:** Explicar que el motor y la animación usan una sola trayectoria.

**Contenido:** Python y RK4 simultáneo, paso máximo 1 s, eventos de entrada particionados y mando previo 50%. La animación reproduce estados calculados. Comprobaciones de finitud, no negatividad, causalidad y comparación DOP853.

**Gráfica o evidencia:** Captura del simulador y tabla numérica de verificación. D50 difiere de DOP853 ≈10⁻⁶ cm en las corridas comprobadas.

**Fuentes:** `src/simulation_engine.py`; `src/precision_models.py`; `reports/simulador/browser_checks.json`; `reports/diagnostico_control_constante/integridad_y_verificacion.json`

**Límite o afirmación pendiente:** La velocidad de reproducción visual no cambia la integración. No hay mediciones en vivo ni un segundo motor de animación.

## 8. Calibración

**Objetivo:** Documentar cómo se obtuvieron los parámetros sin reajustar para escenarios.

**Contenido:** Mínimos cuadrados normalizados conjuntos, multinicio reproducible, escalas de entrenamiento por filas únicas. Ajuste principal corridas 1–7 completas. U conserva siete coeficientes; el perfil de desfase usa 2 s. La exploración de 30 variantes usó datos ya examinados.

**Gráfica o evidencia:** Tabla reducida de parámetros finales y esquema de particiones 1–7 / 8–10. No mostrar una nueva calibración para D50 ni para la ablación de media.

**Fuentes:** `src/precision_study.py`; `docs/protocolo_optimizacion.md`; `reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json`; `reports/optimizacion_precision/campaign_summary.json`

**Límite o afirmación pendiente:** Elegir entre 30 variantes reduce independencia de la evaluación. El offset de mando de la ablación no es un nuevo parámetro calibrado de U.

## 9. Validación

**Objetivo:** Cuantificar reproducción de datos y declarar su calidad de evidencia.

**Contenido:** Evaluación interna previamente examinada. U: RMSE h1≈0.87253 cm, h2≈0.24169 cm; NRMSE≈0.14581/0.07903; MAE según tabla reproducida. NRMSE divide por sigma de entrenamiento. Promedios por corrida 8–10 en horizontes disponibles, no RMSE agrupado. CV por grupos y residuos autocorrelacionados.

**Gráfica o evidencia:** Trayectorias observadas frente a U en corridas 8–10 y tabla breve de métricas; ACF como apoyo o evidencia enlazada.

**Fuentes:** `reports/optimizacion_precision/figures/trajectories_U_bomba_carga_monotona__retardo.png`; `reports/simulador/regresion_U.csv`; `reports/optimizacion_precision/cv_por_tanque.csv`; `reports/optimizacion_precision/residual_diagnostics.json`

**Límite o afirmación pendiente:** No es validación externa. NRMSE no es porcentaje del nivel. La corrida 10 no tiene recuperación; no afirmar precisión en arranque o señales nuevas.

## 10. Escenarios

**Objetivo:** Definir exactamente los tres casos originales y situar el diagnóstico fuera de ese conjunto.

**Contenido:** E0 entrada registrada; E1=50+0.8(u0−50); E2 limitador causal de 10 pp/4 s usando dt real. Mismos U/h0/horizonte/RK4/parámetros/referencias. D50=50% es una comprobación complementaria, no E3 ni un cambio retroactivo del protocolo.

**Gráfica o evidencia:** Gráficas de mandos E0/E1/E2 y sus medias. Corrida 8: E1≈48.998%, E2≈50.065%, diferencia≈1.067 pp. Nota del diagnóstico constante.

**Fuentes:** `docs/protocolo_escenarios.md`; `reports/simulador/figures/escenarios_excitacion.png`; `docs/protocolo_diagnostico_constante.md`; `reports/diagnostico_control_constante/interpretacion_media.csv`

**Límite o afirmación pendiente:** E0 tiene mando observado y respuesta predicha. E1/E2/D50 tienen mandos hipotéticos. No comparar E1/E2 como si sus medias fueran idénticas.

## 11. Resultados y comparación

**Objetivo:** Mostrar la comparación original y el control nominal que cambia su interpretación.

**Contenido:** Tabla de RMSE de regulación h1/h2, media y TV del mando de E0/E1/E2, con fila D50 separada como diagnóstico. Corrida 8: D50≈0.19707/0.19702 cm, frente a E1≈7.01683/3.77536 cm. Corroborar con resumen de 10 excitaciones y 9 registros completos. E2 con media igualada no supera E1 en la ablación.

**Gráfica o evidencia:** figures/constante_excitacion.png y tabla de cuatro filas con D50 visualmente separado. Las tablas completas y media_*.png quedan como evidencia de respaldo.

**Fuentes:** `reports/diagnostico_control_constante/figures/constante_excitacion.png`; `reports/diagnostico_control_constante/comparacion_complementaria.csv`; `reports/diagnostico_control_constante/resumen_por_horizonte.csv`; `reports/diagnostico_control_constante/ablacion_media.csv`

**Límite o afirmación pendiente:** Son desviaciones respecto al objetivo, no errores frente a mediciones contrafactuales. Cero índice ∫(u−50)² no significa energía cero.

## 12. Decisión, limitaciones y conclusiones

**Objetivo:** Presentar una conclusión condicionada que no fuerce el éxito de E1.

**Contenido:** E1 gana sólo entre los tres casos originales según la regla previa. Al ampliar el diagnóstico, D50 gana en 19/19 comparaciones. En nominal sin demanda externa documentada, mantener 50% es la referencia preferible del modelo. Para exigir variación haría falta una demanda, consigna o restricción documentada. La excitación de identificación cumple otro objetivo.

**Gráfica o evidencia:** Conteo de decisiones originales/complementarias y conclusión del informe. Explicación del equilibrio incorporado a U y de h0 cerca de él.

**Fuentes:** `reports/diagnostico_control_constante/decisiones_complementarias.json`; `reports/diagnostico_control_constante/informe_diagnostico.md`; `data/raw/README.md`

**Límite o afirmación pendiente:** Sin demostración de óptimo global, rechazo de perturbaciones, ahorro de energía, seguridad ni eficacia física de nuevas estrategias. Áreas/topología, arranque y generalización pendientes.

## 13. Referencias y evidencias

**Objetivo:** Permitir comprobar origen, cálculos y límites sin inventar anexos.

**Contenido:** Zenodo DOI 10.5281/zenodo.19856119; Silva, Coelho y Leite. README experimental y guía docente. Código, parámetros, huellas, informes y pruebas. Diferenciar autorización comunicada de un acta adjunta inexistente.

**Gráfica o evidencia:** Bibliografía breve y rutas reproducibles del proyecto. Referencias enlazadas a los datos y comandos de reproducción.

**Fuentes:** `https://doi.org/10.5281/zenodo.19856119`; `data/raw/README.md`; `referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`; `reports/diagnostico_control_constante/manifest_previo.json`; `reports/diagnostico_control_constante/tests.txt`

**Límite o afirmación pendiente:** No hay fotos propias, repositorio remoto informado ni texto completo verificado de los artículos asociados. No atribuir esas evidencias a la pareja.

## Afirmaciones que no deben pasar al PowerPoint como hechos

- «E1 es la mejor política nominal»: sólo ganó en el conjunto original; D50 cambia esa conclusión.
- «Se requiere una señal variable para operar»: falta una demanda o restricción documentada que la imponga.
- «D50 valida mejor el modelo»: su pequeño RMSE de regulación no es una nueva comparación con mediciones.
- «Se ahorra energía eléctrica»: no hay potencia ni consumo medidos; el índice de esfuerzo es relativo a 50%.
- «Los estudiantes realizaron el experimento»: lo realizaron investigadores de CEFET-MG.
- «El plano, áreas y caudales absolutos están identificados»: sólo se conocen estados y coeficientes efectivos.
- «El retardo físico es exactamente 2 s»: se identificó un desfase efectivo de reproducción, con mecanismo ambiguo.
- «La validación es externa o ciega»: los registros y las repeticiones ya se examinaron al elegir modelos.
- «El modelo sirve para arranque, desbordamiento o entradas nuevas»: la evidencia actual no lo respalda.
- «Hay fotos propias, instrumento/fecha exactos, acta docente y nombres de autores estudiantiles completos»: esos materiales no se aportaron.

La autorización de uso de datos externos sí se registra como comunicación explícita del
usuario en fase 3. Su existencia comunicada no autoriza inventar un documento firmado.
Las referencias a E1 de los informes históricos se mantienen y se contextualizan; no se borran.
