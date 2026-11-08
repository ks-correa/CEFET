# Revisión metodológica y mapa de versiones

La fase 3 definió E0 experimental, E1 atenuado y E2 suavizado. E1 ganó bajo la regla
prefijada en ese conjunto. El diagnóstico posterior añadió D50 y encontró una alternativa
nominal mejor en las 19 comparaciones. Esta fase reorganiza la entrega después de haber
examinado esos resultados: es una revisión retrospectiva, no una selección previa original.

Mapa vigente: E0=E0 histórico; E1=E1 histórico; E2=D50 diagnóstico; S_HIST=E2 histórico.
El escenario de suavizado sigue en análisis complementarios. No se alteraron sus CSV,
protocolos ni las 19 decisiones históricas. La regla y los indicadores no cambian.
El cambio es el conjunto de alternativas y la interpretación de la decisión.

La aplicación vigente se ejecuta con app_final.py y el lanzador iniciar_entrega_final.ps1.
app.py y src/scenarios.py conservan la versión histórica para poder ejecutar sus pruebas
y reproducir resultados antiguos. No se usan como punto de entrada de la entrega actual.
La documentación vigente está en docs/consolidacion_final/ y los resultados en
reports/consolidacion_final/. Los documentos de etapas previas son antecedentes fechados
por la secuencia del proyecto; sus recomendaciones se interpretan en su conjunto original.

La política preferida actual es E2, sólo como mejor alternativa nominal evaluada cerca
del equilibrio y sin demanda externa documentada. No se afirma óptimo global, energía
eléctrica ahorrada, seguridad, rechazo de perturbaciones ni eficacia física de políticas
no ensayadas. La validación original de U conserva sus métricas y limitaciones.
