from .documentary_archive import write_document, historical_source, ARCHIVED
"""Informe complementario y esquema verificable de trece diapositivas, sin crear PPTX."""
import json,hashlib
import numpy as np
import pandas as pd
from .data_processing import ROOT
from .constant_control_diagnostic import OUT
from .reporting import table
from .simulation_engine import calibrated_config

def main():
    data=pd.read_csv(OUT/'comparacion_complementaria.csv');means=pd.read_csv(OUT/'interpretacion_media.csv')
    summary=pd.read_csv(OUT/'resumen_por_horizonte.csv');abl=pd.read_csv(OUT/'ablacion_media.csv')
    decisions=pd.DataFrame(json.loads((OUT/'decisiones_complementarias.json').read_text()))
    integrity=json.loads((OUT/'integridad_y_verificacion.json').read_text())
    cfg=json.loads((OUT/'configuracion.json').read_text());model=calibrated_config()
    example=data[(data.run==8)&(data.window=='excitacion')].set_index('scenario')
    row=example.loc['D50'];e1=example.loc['E1']
    gains={c:100*(1-row[f'RMSE_ref_{c}_cm']/e1[f'RMSE_ref_{c}_cm']) for c in ['h1','h2']}
    counts=decisions.groupby(['window','original_choice','supplementary_choice']).size().to_frame('casos').reset_index()
    columns=['scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']
    chosen=data[(data.run==8)&(data.window=='excitacion')][columns]
    mean8=means[(means.run==8)&(means.window=='excitacion')].iloc[0]
    original_reference=pd.read_csv(ROOT/'reports/simulador/regresion_U.csv')
    reference=original_reference.groupby('tank')[['MAE','RMSE','NRMSE','bias']].mean().reset_index()
    def write(path,text):write_document(path,text)
    write(OUT/'informe_diagnostico.md',f'''# Comprobación complementaria de la decisión E1

**D50, mando constante al 50%, supera a E1 bajo las condiciones nominales simuladas.**
E1 conserva su recomendación histórica dentro del conjunto E0/E1/E2. Al añadir D50,
la misma regla elige D50 en las 19 comparaciones. Este resultado acota la recomendación
original y evita presentarla como una política óptima general.

## Qué se conserva y qué se añade

Se preservan los archivos anteriores, incluidos protocolos, código de E0/E1/E2, parámetros
de U y resultados de validación. SHA256: {integrity['files_compared']} archivos comprobados,
sin modificaciones. El registro está en manifest_previo.json e integridad_y_verificacion.json.
No se recalibra ningún coeficiente. No se añaden escenarios principales a la aplicación.
La app sigue mostrando la decisión del conjunto original; esta revisión se consulta por separado.

Nuevo diagnóstico: u(t)=50%, misma condición inicial de cada corrida, tiempos reales,
modelo U exacto, historia previa al 50%, desfase efectivo 2 s, RK4 máximo 1 s y referencias
47.4/31.2 cm. Diez excitaciones y nueve registros completos con recuperación. La corrida
10 termina en ~800 s y no se extiende. D50 no es una cuarta medición ni un ensayo físico.

## Resultados de la corrida 8 en excitación

{table(chosen)}

Son RMSE de **regulación** frente al objetivo, no RMSE de predicción frente a mediciones.
D50 reduce esos RMSE frente a E1 un {gains['h1']:.2f}% en h1 y un {gains['h2']:.2f}% en h2.
Mantiene ambos niveles dentro de ±2 cm durante los {row.duration_s:.6f} s disponibles.
La desviación máxima es {row.max_deviation_h1_cm:.6f} cm en h1 y {row.max_deviation_h2_cm:.6f} cm en h2.
Las bandas son criterios analíticos propios, sin valor de límite físico certificado.

La variación total del mando y la integral de (u−50)² son cero porque el mando permanece
en su referencia. **Esto no significa consumo energético cero, bomba apagada ni ausencia
de circulación de agua.** El caudal nominal del modelo es positivo. No hay mediciones
eléctricas para concluir ahorro de energía.

## Resumen por horizonte

{table(summary)}

Medias de indicadores por corrida, no un RMSE global sobre todas las muestras ni réplicas
de señales de excitación independientes. Las condiciones iniciales difieren ligeramente.
Resultado de aplicar la regla sin modificar sus criterios, en un conjunto ampliado:

{table(counts)}

## Por qué la constante resulta favorecida

U tiene por construcción un equilibrio en (h1,h2,u)=(47.4,31.2,50). Las condiciones iniciales
experimentales están próximas a ese punto. Los escenarios no incluyen demanda externa,
consignas móviles ni perturbaciones temporales medidas que obliguen a variar la bomba.
El modelo sí incluye una salida pasiva dependiente del nivel: mantener 50% compensa esa
salida nominal, no equivale a cerrar el sistema.

Desde ese estado cercano al equilibrio, una entrada constante evita la excitación que
producía desviaciones. Por tanto, D50 es una alternativa nominal legítima dentro del
problema modelado y una referencia obligatoria para interpretar E1. No se demuestra que
sea un óptimo global para otras condiciones iniciales o perturbaciones desconocidas.
Tampoco que el montaje real responda exactamente como el modelo bajo esta política nueva.
Los tramos medidos de recuperación a 50% aportan contexto, pero no son un nuevo ensayo
independiente de D50 desde cada condición inicial ni certifican rechazo de perturbaciones.

El resultado de D50 es particularmente favorable porque el objetivo coincide con el
equilibrio incorporado al modelo. No se debe presentar su pequeño error de regulación
como una nueva precisión predictiva superior a la validación original de U.

## Interpretación de la señal media E1 y E2

En la corrida 8 de ~800 s, E1 tiene mando medio {mean8.mean_E1:.6f}% y E2
{mean8.mean_E2:.6f}%, una diferencia de {mean8.mean_gap_E2_E1_pp:.6f} puntos porcentuales.
La regla original permitía diferencias ≤5 pp frente a E0, pero eso no hacía iguales las
medias entre E1 y E2. Su comparación combinaba forma, desfase, amplitud y componente media.

Se ejecutó una ablación adicional de media, sin modificar E2 original. El offset de mando
se determinó sólo con entradas de corridas 1–7 y después se congeló:

```json
{json.dumps(cfg['offsets'],indent=2,ensure_ascii=False)}
```

Se desplaza E2, se restringe al rango 0–100% y se vuelve a aplicar el limitador causal
desde historia 50%. La corrección no usa la media futura de la corrida evaluada ni niveles
observados futuros. El ajuste inicial por el limitador se declara: no es una intervención
que mantenga idéntica toda la señal excepto un término ideal aislado.

Comparación de desarrollo previamente examinada, corridas 8–10 en excitación:

{table(means[(means.run>=8)&(means.window=='excitacion')])}

En la corrida 8, el mando medio corregido es {mean8.mean_corrected:.6f}%, prácticamente
igual al de E1 (diferencia {mean8.mean_gap_corrected_E1_pp:.6f} pp). E2 pasa de RMSE
{mean8.RMSE_h1_E2:.6f}/{mean8.RMSE_h2_E2:.6f} cm a
{mean8.RMSE_h1_corrected:.6f}/{mean8.RMSE_h2_corrected:.6f} cm.
En este diagnóstico, bajar la media de E2 empeora ambos indicadores. Su media original
más próxima a 50% le aportaba una ventaja parcial, insuficiente para superar E1.
E1 sigue siendo mejor que esta variante de E2 con media aproximadamente igualada.

No se atribuye toda la diferencia a la media: la bomba es no lineal, depende de h1 y
los estados tienen memoria. Igual promedio de u no implica igual promedio de caudal
ni igual respuesta. No se estima aquí un efecto causal universal de suavizar o de atenuar.

## Revisión de la pregunta de decisión

Pregunta nominal revisada: **¿qué muestran las simulaciones locales sobre mantener el
punto operativo con una bomba constante al 50% frente a transformar la excitación
experimental, cuando no se documenta una demanda externa que obligue a variar el mando?**

Respuesta con la evidencia disponible: preferir D50 como referencia nominal de regulación
en estas simulaciones. E1 sólo es la mejor alternativa del conjunto restringido de
transformaciones originales bajo la regla elegida. No hay una restricción operacional
documentada que descarte el mando constante.

Una señal variable tendría justificación operacional si se documentara, por ejemplo,
una demanda de caudal variable que deba satisfacerse, una consigna temporal obligatoria,
una limitación de disponibilidad de bombeo o perturbaciones que requieran realimentación.
Esas condiciones no se inventan ni se añaden retroactivamente al montaje. Exigirlas daría
lugar a otra pregunta y requeriría datos, ecuaciones e indicadores adicionales.

Sí existe una justificación experimental distinta: variar la entrada ayuda a identificar
la dinámica. El README describe una excitación pseudoaleatoria repetida. Mantener 50%
no sustituye esa excitación para identificar parámetros; por ello una señal de identificación
no debe tratarse automáticamente como una política nominal de operación que necesite
optimizarse sólo por mantener niveles constantes. No se ha evaluado si E1 o E2 preservan
suficiente información de identificación.

## Verificación y límites

Tres ejecuciones D50 repetidas produjeron matrices idénticas. Diferencia máxima frente
a SciPy DOP853 en corridas 8–10: {max(x['max_difference_cm'] for x in integrity['DOP853']):.7g} cm.
Pruebas en tests.txt. Configuración, parámetros y versiones en configuracion.json.
La evidencia sigue siendo exploración interna. No hay validación externa nueva, ni
mediciones de E1/E2/D50, ni respaldo para afirmar seguridad, energía o operación global.
Los límites de arranque y de extrapolación temporal de U siguen vigentes.

## Archivos

comparacion_complementaria.csv conserva E0/E1/E2 y agrega D50 en una copia independiente.
ablacion_media.csv e interpretacion_media.csv documentan el análisis de media.
figures/constante_excitacion.png y constante_completa.png muestran los cuatro mandos y
niveles simulados de corrida 8. figures/media_*.png muestra la ablación de media.
''')
    slides=[
      dict(n=1,title='Portada',objective='Identificar el trabajo, autores y alcance.',
           content='Título propuesto: Modelado local y simulación de dos tanques CEFET-MG. Asignatura Modelado y Simulación. Integrantes y fecha de sustentación por completar.',
           evidence='Título tipográfico, sin fotografía ficticia ni resultados decorativos.',
           source=['docs/anexos_proyecto.md','referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx'],
           caveat='Faltan nombres de los dos integrantes y fecha de sustentación. No inventarlos.'),
      dict(n=2,title='Problema y pregunta de decisión',objective='Separar identificación experimental de regulación nominal y formular una decisión que incluya la constante.',
           content='Reproducir niveles reales con un modelo local. Pregunta revisada: ¿conviene mantener 50% o transformar la excitación experimental para regular ambos niveles, sin demandas externas documentadas? No partir de que una señal variable sea necesaria.',
           evidence='Breve contraste entre entrada de identificación y operación nominal. La revisión se sustenta en el diagnóstico D50.',
           source=['docs/definicion_problema.md','data/raw/README.md','reports/diagnostico_control_constante/informe_diagnostico.md'],
           caveat='No hay demanda externa ni consigna móvil documentada. Una restricción que excluya D50 sería una hipótesis nueva.'),
      dict(n=3,title='Esquema del sistema',objective='Explicar estados, frontera del modelo y conexión supuesta.',
           content='Dos niveles h1/h2, bomba y flujos efectivos qin/q12/qout. La misma transferencia sale del primer balance y entra al segundo. Áreas absolutas y circuito preciso no identificados.',
           evidence='Recorte de la escena del simulador, rotulado como esquema conceptual del modelo, no plano real ni fotografía.',
           source=['reports/simulador/figures/aplicacion_sistema.png','src/simulation_engine.py','docs/modelo_matematico.md'],
           caveat='No presentar alturas de conexiones, áreas o tuberías del dibujo como geometría medida.'),
      dict(n=4,title='Datos reales',objective='Demostrar origen experimental y trazabilidad sin atribuir mediciones a los estudiantes.',
           content='Dataset de Silva, Coelho y Leite, CEFET-MG. 4502 registros en captura completa, niveles cm, bomba %, muestreo ≈4 s. Diez extractos cortos son partes de la captura larga. La señal se repite. Uso externo autorizado según comunicación del usuario.',
           evidence='Gráfica exploratoria de captura completa y tabla pequeña de archivos/variables. Cuantización aparente ≈0.453 cm por código.',
           source=['reports/figures/exploracion.png','reports/auditoria_dataset.md','data/raw/README.md','docs/anexos_proyecto.md'],
           caveat='Instrumento específico, fecha exacta de adquisición y fotografías verificadas no disponibles. Autorización comunicada, sin acta adjunta. No equiparar cuantización con exactitud certificada.'),
      dict(n=5,title='Variables, parámetros y unidades',objective='Fijar unidades y distinguir coeficientes efectivos de geometría real.',
           content='h1/h2 cm, t s, u %, referencias 47.4/31.2 cm y 50%. Siete parámetros globales de U y desfase efectivo 2 s. q=Q/A1 en cm/s, r=A1/A2. Condición inicial del primer registro, una sola vez.',
           evidence='Tabla de parametros_U.csv con valores exactos; redondeo sólo visual indicando que se ejecutan los valores completos.',
           source=['reports/simulador/parametros_U.csv','docs/anexos_proyecto.md','reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json'],
           caveat='No convertir a litros/s ni deducir áreas a partir de capacidad nominal. Los 2 s no son retardo físico certificado.'),
      dict(n=6,title='Modelo matemático',objective='Mostrar una EDO por tanque y sus hipótesis locales.',
           content='dh1/dt=qin−q12; dh2/dt=r(q12−qout). q12 y qout son conductancias locales con caudales no negativos. qin usa curva cúbica monótona y corrección por h1. Señal causal u(t−2). Identidad efectiva d(h1+h2/r)/dt=qin−qout.',
           evidence='Ecuaciones exactas de U código 15, con definición F(z)=z+(b−1)z²+(1−2b+c)z³/3, sin sustituirlas por una raíz de Torricelli global.',
           source=['src/precision_models.py','docs/modelo_matematico.md','reports/optimizacion_precision/modelos_candidatos.md'],
           caveat='Balance matemático local, sin conservación volumétrica global certificada ni interpretación física única del circuito.'),
      dict(n=7,title='Implementación',objective='Explicar que el motor y la animación usan una sola trayectoria.',
           content='Python y RK4 simultáneo, paso máximo 1 s, eventos de entrada particionados y mando previo 50%. La animación reproduce estados calculados. Comprobaciones de finitud, no negatividad, causalidad y comparación DOP853.',
           evidence='Captura del simulador y tabla numérica de verificación. D50 difiere de DOP853 ≈10⁻⁶ cm en las corridas comprobadas.',
           source=['src/simulation_engine.py','src/precision_models.py','reports/simulador/browser_checks.json','reports/diagnostico_control_constante/integridad_y_verificacion.json'],
           caveat='La velocidad de reproducción visual no cambia la integración. No hay mediciones en vivo ni un segundo motor de animación.'),
      dict(n=8,title='Calibración',objective='Documentar cómo se obtuvieron los parámetros sin reajustar para escenarios.',
           content='Mínimos cuadrados normalizados conjuntos, multinicio reproducible, escalas de entrenamiento por filas únicas. Ajuste principal corridas 1–7 completas. U conserva siete coeficientes; el perfil de desfase usa 2 s. La exploración de 30 variantes usó datos ya examinados.',
           evidence='Tabla reducida de parámetros finales y esquema de particiones 1–7 / 8–10. No mostrar una nueva calibración para D50 ni para la ablación de media.',
           source=['src/precision_study.py','docs/protocolo_optimizacion.md','reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json','reports/optimizacion_precision/campaign_summary.json'],
           caveat='Elegir entre 30 variantes reduce independencia de la evaluación. El offset de mando de la ablación no es un nuevo parámetro calibrado de U.'),
      dict(n=9,title='Validación',objective='Cuantificar reproducción de datos y declarar su calidad de evidencia.',
           content='Evaluación interna previamente examinada. U: RMSE h1≈0.87253 cm, h2≈0.24169 cm; NRMSE≈0.14581/0.07903; MAE según tabla reproducida. NRMSE divide por sigma de entrenamiento. Promedios por corrida 8–10 en horizontes disponibles, no RMSE agrupado. CV por grupos y residuos autocorrelacionados.',
           evidence='Trayectorias observadas frente a U en corridas 8–10 y tabla breve de métricas; ACF como apoyo o evidencia enlazada.',
           source=['reports/optimizacion_precision/figures/trajectories_U_bomba_carga_monotona__retardo.png','reports/simulador/regresion_U.csv','reports/optimizacion_precision/cv_por_tanque.csv','reports/optimizacion_precision/residual_diagnostics.json'],
           caveat='No es validación externa. NRMSE no es porcentaje del nivel. La corrida 10 no tiene recuperación; no afirmar precisión en arranque o señales nuevas.'),
      dict(n=10,title='Escenarios',objective='Definir exactamente los tres casos originales y situar el diagnóstico fuera de ese conjunto.',
           content='E0 entrada registrada; E1=50+0.8(u0−50); E2 limitador causal de 10 pp/4 s usando dt real. Mismos U/h0/horizonte/RK4/parámetros/referencias. D50=50% es una comprobación complementaria, no E3 ni un cambio retroactivo del protocolo.',
           evidence='Gráficas de mandos E0/E1/E2 y sus medias. Corrida 8: E1≈48.998%, E2≈50.065%, diferencia≈1.067 pp. Nota del diagnóstico constante.',
           source=['docs/protocolo_escenarios.md','reports/simulador/figures/escenarios_excitacion.png','docs/protocolo_diagnostico_constante.md','reports/diagnostico_control_constante/interpretacion_media.csv'],
           caveat='E0 tiene mando observado y respuesta predicha. E1/E2/D50 tienen mandos hipotéticos. No comparar E1/E2 como si sus medias fueran idénticas.'),
      dict(n=11,title='Resultados y comparación',objective='Mostrar la comparación original y el control nominal que cambia su interpretación.',
           content='Tabla de RMSE de regulación h1/h2, media y TV del mando de E0/E1/E2, con fila D50 separada como diagnóstico. Corrida 8: D50≈0.19707/0.19702 cm, frente a E1≈7.01683/3.77536 cm. Corroborar con resumen de 10 excitaciones y 9 registros completos. E2 con media igualada no supera E1 en la ablación.',
           evidence='figures/constante_excitacion.png y tabla de cuatro filas con D50 visualmente separado. Las tablas completas y media_*.png quedan como evidencia de respaldo.',
           source=['reports/diagnostico_control_constante/figures/constante_excitacion.png','reports/diagnostico_control_constante/comparacion_complementaria.csv','reports/diagnostico_control_constante/resumen_por_horizonte.csv','reports/diagnostico_control_constante/ablacion_media.csv'],
           caveat='Son desviaciones respecto al objetivo, no errores frente a mediciones contrafactuales. Cero índice ∫(u−50)² no significa energía cero.'),
      dict(n=12,title='Decisión, limitaciones y conclusiones',objective='Presentar una conclusión condicionada que no fuerce el éxito de E1.',
           content='E1 gana sólo entre los tres casos originales según la regla previa. Al ampliar el diagnóstico, D50 gana en 19/19 comparaciones. En nominal sin demanda externa documentada, mantener 50% es la referencia preferible del modelo. Para exigir variación haría falta una demanda, consigna o restricción documentada. La excitación de identificación cumple otro objetivo.',
           evidence='Conteo de decisiones originales/complementarias y conclusión del informe. Explicación del equilibrio incorporado a U y de h0 cerca de él.',
           source=['reports/diagnostico_control_constante/decisiones_complementarias.json','reports/diagnostico_control_constante/informe_diagnostico.md','data/raw/README.md'],
           caveat='Sin demostración de óptimo global, rechazo de perturbaciones, ahorro de energía, seguridad ni eficacia física de nuevas estrategias. Áreas/topología, arranque y generalización pendientes.'),
      dict(n=13,title='Referencias y evidencias',objective='Permitir comprobar origen, cálculos y límites sin inventar anexos.',
           content='Zenodo DOI 10.5281/zenodo.19856119; Silva, Coelho y Leite. README experimental y guía docente. Código, parámetros, huellas, informes y pruebas. Diferenciar autorización comunicada de un acta adjunta inexistente.',
           evidence='Bibliografía breve y rutas reproducibles del proyecto. Referencias enlazadas a los datos y comandos de reproducción.',
           source=['https://doi.org/10.5281/zenodo.19856119','data/raw/README.md','referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx','reports/diagnostico_control_constante/manifest_previo.json','reports/diagnostico_control_constante/tests.txt'],
           caveat='No hay fotos propias, repositorio remoto informado ni texto completo verificado de los artículos asociados. No atribuir esas evidencias a la pareja.')
    ]
    # Verificar exactamente títulos y orden del documento docente.
    import zipfile,xml.etree.ElementTree as E
    tree=E.fromstring(zipfile.ZipFile(ROOT/'referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx').read('word/document.xml'))
    paragraphs=[''.join(p.itertext()) for p in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
    begin=next(i for i,t in enumerate(paragraphs) if t.startswith('3. '));end=next(i for i,t in enumerate(paragraphs) if t.startswith('4. '))
    section=paragraphs[begin:end]
    for slide in slides:
        slide['source'] = [historical_source(source) for source in slide['source']]
        i=section.index(str(slide['n']))
        if section[i+1]!=slide['title']:raise RuntimeError('Título distinto de la guía')
        for source in slide['source']:
            if not source.startswith('http') and not (ROOT/source).exists():raise FileNotFoundError(source)
    (OUT/'esquema_13_diapositivas.json').write_text(json.dumps(slides,indent=2,ensure_ascii=False),encoding='utf-8')
    outline='''# Esquema revisado de las 13 diapositivas

Documento para revisión previa al PowerPoint. Conserva exactamente los títulos y el orden
de la sección 3 de la guía docente, comprobados por código. No se genera un PPTX.
Cada bloque especifica objetivo, contenido verificable, gráfica/evidencia, fuente y límite.
Las rutas se expresan desde la raíz CEFET_MG. Nombres y fecha de sustentación siguen pendientes.

Clave de lectura: «observado» son registros físicos de los investigadores; «predicción»
son estados calculados comparados internamente con esos registros; «contrafactual» son
escenarios sin una medición correspondiente. El resultado pequeño de D50 es regulación
frente a un objetivo, sin implicar nueva precisión predictiva.

'''
    for s in slides:
        outline+=f"## {s['n']}. {s['title']}\n\n**Objetivo:** {s['objective']}\n\n**Contenido:** {s['content']}\n\n**Gráfica o evidencia:** {s['evidence']}\n\n**Fuentes:** "+'; '.join(f'`{p}`' for p in s['source'])+f"\n\n**Límite o afirmación pendiente:** {s['caveat']}\n\n"
    outline+='''## Afirmaciones que no deben pasar al PowerPoint como hechos

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
'''
    write(ROOT/'docs/esquema_13_diapositivas_revisado.md',outline)
    write(OUT/'README.md','''# Diagnóstico complementario separado

Leer informe_diagnostico.md y docs/consolidacion_final/esquema_definitivo_13.md; el esquema previo está en la etiqueta cefet-archivo-cientifico-completo.
No se modificó el simulador ni los tres escenarios principales. No se creó PowerPoint.

Desde CEFET_MG y usando el entorno Python existente:

```powershell
$env:PYTHONIOENCODING='utf-8'
../.venv/Scripts/python.exe -m src.constant_control_diagnostic
../.venv/Scripts/python.exe -m pytest -q tests
../.venv/Scripts/python.exe -m src.constant_control_reporting
```

Si .venv es local, quitar ../. El primer comando guarda todos sus resultados en esta carpeta
y compara huellas de los archivos preexistentes. No vuelve a calibrar U. La repetición
sobrescribe sólo los resultados de este diagnóstico, nunca resultados previos de E0/E1/E2.
Las figuras son estáticas para la evidencia científica y están generadas a partir de CSV reales
del proyecto o de escenarios calculados, con etiquetas de contrafactual.
''')
    (OUT/'manifest_codigo_nuevo.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [ROOT/'src/constant_control_diagnostic.py',ROOT/'src/constant_control_reporting.py',ROOT/'docs/protocolo_diagnostico_constante.md',ROOT/'tests/test_constant_diagnostic.py']},indent=2),encoding='utf-8')
    print('Informe y esquema de exactamente 13 diapositivas generados; fuentes locales verificadas.')

if __name__=='__main__':main()
