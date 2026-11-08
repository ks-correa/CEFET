# Registro de decisiones e incidencias

8 de noviembre de 2026. Se inspeccionó el paquete completo, se leyó la guía DOCX
incluidos anexos y se contrastó README con el registro primario de Zenodo. Los originales
no se modificaron. No se recuperó un plano del montaje ni texto completo de artículos
asociados que permitiera confirmar la conexión específica entre tanques.

Se reconstruyeron diez excitaciones completas desde complete_data.csv, verificando
coincidencia exacta de cada extracto h1/h2 y entrada corta. Se usan tiempos reales y
se conservan cuantización y extremos, sin suavizar niveles para favorecer el ajuste.

Se fijaron modelos A–D, particiones y umbral antes de calibrar. El objetivo conjunto
se normaliza con desviación estándar muestral de entrenamiento. Las cotas amplias positivas
limitan inestabilidad numérica y la potencia de bomba; no se atribuyen a especificaciones
medidas. Los valores iniciales y cotas están en `models.specification`.

La selección prevista prioriza parsimonia entre candidatos que cumplen el umbral por
cada corrida completa y excitación, tanto en evaluación principal como cruzada. D cumple
con tres parámetros y se recomienda provisionalmente; C tiene seis y menor error predictivo.
El archivo `selected_model.json` es el selector diagnóstico de menor error para las figuras
predictivas; `modelo_recomendado.json` es el resultado de selección según el protocolo.

Corrección de implementación durante revisión: inicialmente se concatenaron las corridas
para calcular sigma, lo que repetía unas pocas filas frontera compartidas. Se corrigió
deduplicando por `source_row` y retirando el residuo cero de la condición inicial impuesta
del objetivo. No cambió la definición NRMSE, el umbral, las particiones ni el catálogo de
modelos. Se volvió a ejecutar todo y se repitió la comprobación de reproducibilidad.
Se explicita esta corrección para no confundir una reparación de trazabilidad con un
cambio oportunista del criterio después de ver resultados.

La comparación SciPy reinicia el integrador en cada cambio de entrada conservando el
último estado calculado. Nunca reinicializa con niveles futuros medidos. La prueba temporal
calibra sólo las ventanas iniciales de desarrollo y recorre libremente toda la evaluación.

La simulación no identifica consumos de energía ni caudales absolutos. La igualdad de
balance efectivo es una identidad del candidato conservativo, no una validación experimental
de geometría. Los residuos mantienen estructura y la prueba temporal falla en h2.
Por ello el dictamen se limita al régimen de corridas completas con calibración completa.
La interfaz, AgentPy, escenarios contrafactuales y presentación quedan fuera de esta primera etapa.
