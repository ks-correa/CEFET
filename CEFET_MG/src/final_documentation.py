"""Documentación vigente versionada. Conserva las fuentes e informes históricos intactos."""
import json,shutil
import numpy as np
import pandas as pd
from .data_processing import ROOT
from .final_consolidation import OUT
from .reporting import table
from .simulation_engine import calibrated_config

DOC=ROOT/'docs/consolidacion_final'
QUESTION='¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal?'

def write(path,text):path.write_text(text,encoding='utf-8')

def main():
    DOC.mkdir(exist_ok=True,parents=True);OUT.mkdir(exist_ok=True)
    data=pd.read_csv(OUT/'comparacion_principal.csv');sensitivity=pd.read_csv(OUT/'robustez/indicadores.csv')
    ranges=pd.read_csv(OUT/'robustez/rangos.csv');local=json.loads((OUT/'robustez/analisis_local.json').read_text())
    choices=pd.DataFrame(json.loads((OUT/'decisiones_vigentes.json').read_text()))
    robustchoices=pd.DataFrame(json.loads((OUT/'robustez/decisiones.json').read_text()))
    regression=pd.read_csv(OUT/'validacion_U_sin_cambios.csv')
    config=calibrated_config();pred=regression.groupby('tank')[['MAE','RMSE','NRMSE','bias']].mean().reset_index()
    example=data[(data.run==8)&(data.window=='excitacion')]
    summary=data[data.window=='excitacion'].groupby('scenario')[['RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']].mean().reset_index()
    summary.to_csv(OUT/'resumen_excitaciones.csv',index=False)
    verdict=choices.groupby(['window','recommended']).size().to_frame('comparaciones').reset_index()
    robustverdict=robustchoices.groupby(['case','recommended']).size().to_frame('comparaciones').reset_index()
    worst=sensitivity[sensitivity.scenario=='E2'].groupby('case')[['RMSE_ref_h1_cm','RMSE_ref_h2_cm','max_deviation_h1_cm','max_deviation_h2_cm']].max().reset_index()
    write(DOC/'registro_metodologico.md','''# Revisión metodológica y mapa de versiones

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
''')
    write(DOC/'definicion_problema.md',f'''# Definición vigente del problema

**Pregunta:** {QUESTION}

El fenómeno real es la respuesta acoplada de dos niveles ante la entrada de una bomba.
Objetivo general: explicar y reproducir la dinámica medida con U y comparar tres condiciones
nominales mediante indicadores cuantitativos, para apoyar una recomendación local condicionada.
Objetivos específicos: mantener trazabilidad, explicar balances y RK4, conservar calibración
y evaluación interna, comparar E0/E1/E2 y explicitar límites del resultado y su sensibilidad.

«Estabilidad» se mide operacionalmente mediante RMSE/MAE frente a referencias, dispersión,
variación total y tiempo dentro de bandas analíticas ±2 cm. La estabilidad del equilibrio
matemático se estudia además con el Jacobiano local. No se extienden esas propiedades a
robustez global del montaje. «Minimizar» significa comparar las alternativas evaluadas.

E0 usa la excitación real de identificación, E1 la atenúa y E2 mantiene 50%. La misma
condición inicial registrada, tiempos y parámetros hacen comparable el contraste simulado.
E2 favorece el equilibrio que incorpora U, cerca del cual empiezan las corridas.
La aplicación y el informe calculan la decisión con la regla histórica sin modificarla.

La excitación pseudoaleatoria identifica la dinámica; no representa por sí misma una demanda
de producción que deba seguirse en operación. No hay una demanda, consigna móvil ni
disponibilidad variable documentada que haga obligatorio variar la bomba. Si se incorporase
alguna, habría que revisar la pregunta y aportar datos e indicadores apropiados.

Uso de datos externos autorizado por el docente según la comunicación del usuario. La pareja
reutiliza las mediciones de investigadores de CEFET-MG; no construyó ni midió el montaje.
Frontera: dos niveles y un mando; sin áreas absolutas, consumos eléctricos ni cargas externas
identificadas. No se recomienda sobre desbordamiento, vaciado o arranque en frío.
''')
    units={'qstar':'cm/s (Q/A1)','r':'adimensional; A1/A2 efectivo','k12':'s⁻¹','kout':'s⁻¹','kpump':'s⁻¹','b':'adimensional','c':'adimensional'}
    params=pd.DataFrame([dict(parámetro=n,valor=format(v,'.17g'),unidad=units[n]) for n,v in zip(config.names,config.parameters)])
    params.to_csv(OUT/'parametros_U_vigentes.csv',index=False)
    write(DOC/'modelo_y_variables.md',f'''# Modelo matemático y variables vigentes

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

{table(params)}

Fuente exacta: reports/optimizacion_precision/all_fits.json → U → principal. Son siete
coeficientes globales; el desfase efectivo es 2 s. La condición inicial se aplica una vez,
sin corregir estados posteriores con observaciones futuras. Antes de t=0 se retiene u=50%.
La identidad d(h1+h2/r)/dt=qin−qout es un balance efectivo. No certifica volúmenes absolutos
ni la topología hidráulica precisa. El esquema gráfico normaliza alturas y no capacidad en litros.
El recorte no amplía la validez de las conductancias locales al arranque o vaciado.
''')
    write(DOC/'rk4_calibracion_validacion.md',f'''# Integración, calibración y evaluación conservadas

Motor: src/simulation_engine.py reutiliza el RK4 simultáneo ya contrastado de
src/precision_models.py. Cada intervalo se subdivide en ceil(dt/paso) subpasos y se
particiona en cambios de entrada, incluidos los eventos desplazados 2 s. Paso por defecto
1 s; opciones verificadas 0.5/1/2/4 s. La animación sólo reproduce estados calculados.

Calibración histórica: mínimos cuadrados conjuntos normalizados, cuatro inicios reproducibles,
semilla 20261108, cotas de familia, entrenamiento principal corridas 1–7 completas. Las escalas
de entrenamiento usan filas originales únicas y ddof=1. No se recalibró en esta fase.
Treinta variantes previamente examinadas limitan la independencia de la evaluación.

Evaluación interna de U, media de métricas por corrida 8–10 en sus horizontes disponibles:

{table(pred)}

La trayectoria coincide con la versión científica anterior; máxima diferencia:
{regression.max_trajectory_difference_cm.max():.3g} cm. Esto es regresión numérica, no validación
externa nueva. NRMSE=RMSE/sigma de entrenamiento, no porcentaje del nivel de agua.
MAE/RMSE están en cm. El criterio NRMSE≤0.30 es interno, no norma universal del profesor.

Se conservan CV por grupos, sensibilidad, ACF y diagnósticos Ljung–Box descriptivos en
reports/optimizacion_precision/. Persisten sesgos y autocorrelación. El arranque desde niveles
bajos y la predicción tardía de h2 ajustando sólo 320 s siguen limitados. Las repeticiones
comparten señal y no prueban generalización a demandas nuevas.

Los RMSE de regulación de E2 frente a referencias son distintos de esta tabla predictiva.
Su pequeño valor no mejora ni reemplaza la validación. Las pruebas existentes siguen
ejecutándose sin cambiar sus archivos ni expectativas históricas.
''')
    write(DOC/'escenarios_resultados_decision.md',f'''# Escenarios, resultados y decisión vigentes

E0: mando experimental. E1: 50+0.8(u0−50). E2: mando constante 50%.
S_HIST: antiguo suavizado, sólo complementario. Revisión posterior al examen de resultados,
sin cambiar los coeficientes U, el motor, las métricas ni la función de decisión.
Ver protocolo_vigente.md y registro_metodologico.md para no confundir versiones de E2.

Regla: no empeorar ambos RMSE frente a E0, mejorar al menos uno ≥5%, TV del mando no
mayor que E0 y cambio de media ≤5 pp; entre elegibles, menor peor RMSE/banda de 2 cm.
Los tres casos comparten h0, parámetros, tiempos, paso y referencias. Las bandas no son
límites físicos certificados. La corrida 10 no tiene recuperación inventada.

Corrida 8 en excitación (~800 s), indicadores de regulación:

{table(example[['scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']])}

Promedio de indicadores por corrida en las diez excitaciones:

{table(summary)}

Decisiones nominales:

{table(verdict)}

**E2 es la mejor alternativa nominal evaluada bajo estas condiciones simuladas.** La
bomba al 50% está en el equilibrio de U y las iniciales se encuentran cerca. No hay una
demanda externa documentada que obligue a variar el mando. La salida pasiva del modelo
sigue presente y se compensa nominalmente con entrada de bomba.

El resultado no demuestra óptimo global, energía ahorrada, seguridad ni ensayo físico de
E2. TV y ∫(u−50)² son cero en nominal, pero la bomba sigue funcionando al 50%: ese índice
de esfuerzo relativo no mide energía eléctrica. El control constante es lazo abierto.

La recomendación histórica E1 era válida para el conjunto restringido de fase 3; se
preserva íntegra en sus archivos y se contextualiza aquí. El suavizado S_HIST y la
ablación de media no cambian esta decisión nominal. No se igualaron retrospectivamente
medias para modificar los resultados principales. Su diferencia está documentada en el
diagnóstico: la media original del suavizado era mayor que la de E1.
''')
    e2ranges=ranges[ranges.scenario=='E2'];allouts=int(ranges.samples_outside_measured_rectangle.sum())
    write(DOC/'solidez_y_limitaciones.md',f'''# Solidez local y límites de la recomendación

Las pruebas nuevas son simulaciones exploratorias declaradas, sin mediciones nuevas,
sin ajuste de parámetros y sin búsqueda de políticas. Seis desplazamientos iniciales de
1 cm y tres perturbaciones de mando ±2 pp se compararon para cada una de diez excitaciones.
La misma intervención se aplicó a E0/E1/E2. Resultado de la regla:

{table(robustverdict)}

Peor resultado de E2 por familia exploratoria, entre las diez corridas:

{table(worst)}

La preferencia se mantiene en 90/90 comparaciones exploratorias. Esto no acredita un
control robusto del montaje. No se añadieron demandas hidráulicas ni se fingieron
perturbaciones experimentales. El sesgo persistente −2 pp hace que el mando aplicado a
E2 pase a 48% tras el evento y desplaza los niveles: no permanece una regulación perfecta.

El equilibrio local a u=50% es (47.4,31.2) cm por construcción. El Jacobiano nominal tiene
autovalores {local['eigenvalues'][0][0]:.8f} y {local['eigenvalues'][1][0]:.8f} s⁻¹.
Ambos son negativos en el modelo, dentro de la rama activa; esto indica estabilidad
asintótica local matemática, sin certificar estabilidad global o experimental.
A u=48% el equilibrio predicho es ({local['constant_48_equilibrium'][0]:.6f},
{local['constant_48_equilibrium'][1]:.6f}) cm. Un sesgo sostenido no se rechaza sin error
por el mero uso de un mando constante. No se ensayó realimentación física.

Rangos: E2 presenta {int(e2ranges.samples_outside_measured_rectangle.sum())} muestras fuera
del rectángulo de niveles observado en estas pruebas. En el conjunto E0/E1/E2 hay
{allouts} valores de nivel fuera de ese rectángulo; se conservan en robustez/rangos.csv.
Esos desvíos, principalmente de E0/E1 al excitar el sistema, impiden afirmar que todas
las trayectorias permanezcan estrictamente dentro del soporte experimental. Estar dentro
de un rectángulo tampoco garantiza cobertura de estados conjuntos. No se ocultan las excursiones.
Muestras de saturación de mando registradas: {int(sensitivity.saturation_samples.sum())}.

Una señal variable sería necesaria para una consigna móvil, demanda de caudal, restricción
de disponibilidad o perturbación documentada que exigiera corregir desviaciones. No se
atribuyen esas condiciones al montaje sin datos. La excitación variable sí tuvo finalidad
de identificación experimental, distinta de la regulación nominal aquí comparada.

Sin mediciones adicionales se puede defender: origen publicado, reproducción interna
de U, consistencia numérica, mejores indicadores de E2 entre estos escenarios y límites
de la sensibilidad simulada. No se puede afirmar optimalidad global, ahorro eléctrico,
seguridad, rechazo de perturbaciones reales o generalización a entradas nuevas.
''')
    requirements=[
      ('Sistema real y niveles medidos','README y auditoría del dataset','Cumplido con datos externos'),
      ('Aceptación de datos externos','Comunicación del usuario; no acta aportada','Autorizado según usuario'),
      ('Esquema y límites','App vigente y modelo_y_variables.md','Cumplido como esquema; topología exacta no verificada'),
      ('Variables, parámetros y unidades','Tabla U exacta y anexos','Cumplido para coeficientes efectivos'),
      ('Balance continuo por tanque','Código U 15, dos EDO','Cumplido localmente; volumen absoluto no certificado'),
      ('Método y parámetros modificables','Motor único y copias exploratorias de sesión','Implementado; pruebas en informe final'),
      ('Calibración y validación con error','Evaluación histórica conservada y regresión','Interna previamente examinada; no externa nueva'),
      ('Base y dos alternativas','E0 experimental/E1 atenuado/E2 constante','19 comparaciones ejecutadas'),
      ('Indicadores y decisión sustentada','Misma regla histórica sobre conjunto revisado','E2 nominal; revisión retrospectiva declarada'),
      ('Pruebas y reproducibilidad','Pruebas originales más comprobaciones vigentes','Ver informe_cumplimiento.md'),
      ('Presentación de 13 diapositivas','esquema_definitivo_13.md y anexos_A_B_C.md','Estructura y anexos completos para sustentación'),
      ('Comprensión de ambos integrantes','Explicaciones orales y guía de reproducción','Material documentado y verificable')]
    write(DOC/'matriz_cumplimiento.md','# Matriz vigente de cumplimiento\n\nGuía leída y contrastada, incluyendo anexos. Esta matriz es la versión de entrega; la matriz de fase 3 se conserva como antecedente.\n\n'+table(pd.DataFrame(requirements,columns=['Requisito','Evidencia','Estado']))+'\n\nPonderaciones de guía: datos 15%, modelo 20%, implementación 15%, calibración/validación 20%, escenarios 15%, decisión 10%, presentación 5%.\n')
    write(DOC/'anexos_A_B_C.md',f'''# Anexos vigentes A, B y C

## Anexo A Propuesta y sistema

- **Título del proyecto:** Simulación continua de dos tanques acoplados con datos experimentales de CEFET-MG
- **Integrantes:**
  - Kevin Santiago Correa Acosta — 67001271
  - Santiago Cárdenas Rubio — 67001160
- **Asignatura:** Modelado y Simulación
- **Institución:** Universidad Católica de Colombia
- **Fecha:** 8 de noviembre de 2026
- **Pregunta de decisión:** {QUESTION}
- **Sistema de tanques y alcance:** Dos tanques físicos hidráulicos acoplados con niveles medibles ($h_1, h_2$ en cm) e impulsados por una señal de comando de bomba ($u$ en %). Se emplean los registros experimentales publicados por investigadores de CEFET-MG (Divinópolis, Brasil; DOI `10.5281/zenodo.19856119`). La pareja realiza el modelado matemático continuo, la calibración, la validación interna y la simulación de escenarios, no la adquisición física original. El instrumento específico de medición, la fecha exacta de adquisición en el laboratorio y el plano geométrico preciso no están disponibles en la fuente publicada.
- **Herramienta de simulación:** Python (`numpy`, `pandas`, `scipy`, `numba`, `streamlit`) con integración numérica mediante Runge-Kutta de cuarto orden (RK4, paso máximo de 1 s y desfase efectivo de entrada de 2 s).
- **Aprobación docente:** El uso del dataset externo fue autorizado según la comunicación de los estudiantes.

## Anexo B Variables y parámetros

Estados h1/h2 cm; t s; mando u %; referencias 47.4/31.2 cm y 50%. Condiciones iniciales
tomadas del primer estado observado de cada corrida. No se corrigen niveles con datos futuros.
Flujos efectivos q=Q/A1 cm/s. Tabla de valores exactos:

{table(params)}

Desfase efectivo 2 s; historia previa de mando 50%; RK4 máximo 1 s. Fuente: all_fits.json
de optimización, sin recalibración. Identidad de balance efectiva; áreas no identificadas.

## Anexo C Escenarios y comparación

E0 entrada experimental, E1 atenuación 20% de desviaciones alrededor de 50%, E2 constante
50%. S_HIST retiene el antiguo suavizado como análisis complementario. La revisión de
escenarios es posterior al examen del diagnóstico. No se reetiquetan los CSV originales.
Mismos h0, parámetros, método, paso, tiempos y referencias. Diez excitaciones y nueve
recuperaciones disponibles. Resultados, medias, esfuerzo relativo y decisión en
escenarios_resultados_decision.md y reports/consolidacion_final/comparacion_principal.csv.
E1/E2 son contrafactuales. E2 gana nominalmente en 19 comparaciones; no es prueba física.
''')
    # Esquema con los ocho campos exigidos, derivado de la guía y de evidencias existentes.
    slides=json.loads((ROOT/'reports/diagnostico_control_constante/esquema_13_diapositivas.json').read_text(encoding='utf-8'))
    for s in slides:s['limitations']=s.pop('caveat')
    slides[0].update(
      content='Título: Simulación continua de dos tanques acoplados con datos experimentales de CEFET-MG. Integrantes: Kevin Santiago Correa Acosta (67001271) y Santiago Cárdenas Rubio (67001160). Asignatura: Modelado y Simulación. Institución: Universidad Católica de Colombia. Fecha: 8 de noviembre de 2026.',
      evidence='Título tipográfico e identificación académica, sin fotografía ficticia ni resultados decorativos.',
      source=['docs/consolidacion_final/anexos_A_B_C.md','referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx'],
      limitations='El montaje físico pertenece a CEFET-MG; la pareja realiza el modelado y la simulación sobre los registros experimentales publicados.')
    slides[1].update(objective='Vincular variabilidad de bombeo, desviaciones locales y decisión nominal.',content=QUESTION+' Se limita a alternativas evaluadas cerca del equilibrio, sin demanda externa documentada.',
      source=['docs/consolidacion_final/definicion_problema.md','data/raw/README.md'])
    slides[2].update(evidence='Recorte de la escena vigente de los dos tanques, sin presentarla como plano ni fotografía.',source=['reports/consolidacion_final/figures/aplicacion_vigente.png','src/simulation_engine.py','docs/consolidacion_final/modelo_y_variables.md'])
    slides[4]['source']=['reports/consolidacion_final/parametros_U_vigentes.csv','docs/consolidacion_final/anexos_A_B_C.md']
    slides[5]['source']=['src/precision_models.py','docs/consolidacion_final/modelo_y_variables.md']
    slides[6]['source']=['src/simulation_engine.py','reports/consolidacion_final/browser_checks.json','docs/consolidacion_final/rk4_calibracion_validacion.md']
    slides[8]['source']=['reports/consolidacion_final/validacion_U_sin_cambios.csv','reports/optimizacion_precision/figures/trajectories_U_bomba_carga_monotona__retardo.png','reports/optimizacion_precision/residual_diagnostics.json']
    slides[9].update(objective='Explicar exactamente los tres escenarios vigentes y sus condiciones comunes.',
      content='E0 mando experimental; E1=50+0.8(u0−50); E2=50% constante. Mismos U, h0, tiempos, parámetros, paso y referencias. El antiguo suavizado queda como S_HIST complementario. Revisión posterior al diagnóstico.',
      evidence='Señales escalonadas de la comparación vigente y mapa de versiones.',
      source=['docs/consolidacion_final/protocolo_vigente.md','src/final_scenarios.py','reports/consolidacion_final/figures/escenarios_vigentes.png'],
      limitations='No fue la selección previa original. E1/E2 no tienen mediciones contrafactuales y la entrada de identificación tiene otra finalidad.')
    slides[10].update(objective='Comparar tres escenarios con números calculados y dos tipos de error separados.',
      content='RMSE de regulación y mando medio/TV: E0≈9.10264/5.00727 cm; E1≈7.01683/3.77536; E2≈0.19707/0.19702 en corrida 8, ≈800 s. La tabla predictiva de U permanece aparte. Resumen sobre diez excitaciones y nueve recuperaciones.',
      evidence='Tabla breve de tres filas y gráfica vigente. Señalar que el índice relativo de esfuerzo de E2 es cero, sin inferir energía eléctrica.',
      source=['reports/consolidacion_final/comparacion_principal.csv','reports/consolidacion_final/resumen_excitaciones.csv','reports/consolidacion_final/figures/escenarios_vigentes.png'],
      limitations='No comparar estos RMSE contra el objetivo con RMSE de predicción contra mediciones. No inferir ahorro eléctrico ni seguridad.')
    slides[11].update(objective='Defender E2 nominalmente y acotar la sensibilidad simulada.',
      content='E2 es la mejor alternativa nominal evaluada: 19/19 comparaciones. Se mantiene en 90 sensibilidades exploratorias. El equilibrio está incorporado a U y h0 es próximo. Sesgo sostenido desplaza el equilibrio; no hay prueba de rechazo de perturbaciones reales.',
      evidence='Conteo de decisiones, figura de sensibilidad y predicción del equilibrio a 48%.',
      source=['reports/consolidacion_final/decisiones_vigentes.json','reports/consolidacion_final/robustez/decisiones.json','reports/consolidacion_final/figures/sensibilidad_E2.png','docs/consolidacion_final/solidez_y_limitaciones.md'],
      limitations='Sin óptimo global, política física ensayada, generalización externa, ahorro de energía ni robustez experimental. Informar excursiones de E0/E1 fuera del rectángulo medido.')
    slides[12]['source']=['https://doi.org/10.5281/zenodo.19856119','data/raw/README.md','referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx','reports/consolidacion_final/integridad.json','docs/consolidacion_final/registro_metodologico.md']
    data_by_slide=[
      'Título del proyecto, integrantes (67001271 y 67001160), asignatura Modelado y Simulación, Universidad Católica de Colombia y fecha 8 de noviembre de 2026.',
      'Referencias nominales 47.4/31.2 cm y 50%. Sin demanda externa documentada.',
      'Dos estados y tres flujos efectivos. El dibujo representa el modelo, no la geometría certificada.',
      '4502 filas en captura larga; muestreo ≈4 s; diez repeticiones; unidades cm y %; cuantización aparente ≈0.453 cm.',
      'Siete parámetros de U, sin ajuste nuevo; desfase efectivo 2 s; tabla con valores completos.',
      'Dos EDO y las expresiones exactas de qin, q12, qout y F(z), código 15.',
      'RK4 máximo 1 s, eventos causales; tanques comparados con estados calculados; pruebas en navegador.',
      'Entrenamiento principal 1–7; evaluación interna 8–10; cuatro inicializaciones; 30 variantes exploradas.',
      'RMSE predictivo U: 0.87253/0.24169 cm; NRMSE: 0.14581/0.07903; MAE: 0.62896/0.18748 cm, medias por corrida.',
      'Tres escenarios principales, 10 excitaciones (~800 s) y 9 corridas con recuperación (~1700 s).',
      'Corrida 8: E2 mando medio 50%, TV=0, RMSE de regulación ≈0.19707/0.19702 cm; revisar tabla fuente exacta.',
      f'19 decisiones nominales E2; 90 exploratorias E2; equilibrio calculado a 48%≈({local["constant_48_equilibrium"][0]:.3f},{local["constant_48_equilibrium"][1]:.3f}) cm.',
      'DOI 10.5281/zenodo.19856119, autores Silva/Coelho/Leite; huellas de archivos y rutas de reproducción.']
    oral=[
      'Presentamos un trabajo de modelado con registros publicados de un montaje real. Las mediciones pertenecen a los investigadores y nuestro aporte es su análisis y simulación.',
      'Comparamos la respuesta de los niveles ante distinta variabilidad de mando. La decisión vale para el régimen nominal estudiado y para este conjunto de alternativas.',
      'La transferencia aparece con signos opuestos en ambos balances. El esquema explica el modelo; no contiene áreas ni conexiones medidas por nosotros.',
      'Los datos tienen trazabilidad y unidades documentadas. Las diez corridas cortas son partes de la captura larga y repiten una señal, por lo que no duplicamos observaciones.',
      'Estos valores efectivos se cargan completos del archivo calibrado. No conocemos áreas para convertirlos a litros por segundo.',
      'U describe balances locales. La bomba tiene curva monótona y dependencia efectiva de la altura; no estamos afirmando una curva física certificada del equipo.',
      'RK4 integra ambos estados juntos y cambia la entrada sólo cuando corresponde. La animación reproduce esa trayectoria y su velocidad no cambia las ecuaciones.',
      'Los coeficientes se estimaron con desarrollo y se conservaron. La exploración previa de variantes obliga a llamar interna a la evaluación.',
      'Aquí medimos error contra observaciones reales. Estos RMSE son distintos de las desviaciones respecto al objetivo que aparecerán al comparar escenarios.',
      'La revisión incorpora el mando constante como E2. La antigua señal suavizada sigue disponible como complemento; declaramos que cambiamos el conjunto después del diagnóstico.',
      'La constante reduce las desviaciones nominales porque evita excitar el equilibrio. Que su índice relativo de esfuerzo sea cero no significa que la bomba no consuma.',
      'La recomendación es E2 bajo estas condiciones. Las pruebas pequeñas no prueban rechazo de perturbaciones, y un sesgo sostenido desplaza los niveles calculados.',
      'Las fuentes permiten revisar cada cifra. Conservamos originales, resultados históricos, código y pruebas sin inventar fotografías ni mediciones propias.']
    for s,values,speech in zip(slides,data_by_slide,oral):s['verifiable_data']=values;s['oral_explanation']=speech
    import zipfile,xml.etree.ElementTree as ET
    tree=ET.fromstring(zipfile.ZipFile(ROOT/'referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx').read('word/document.xml'))
    paras=[''.join(x.itertext()) for x in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
    start=next(i for i,x in enumerate(paras) if x.startswith('3. '));end=next(i for i,x in enumerate(paras) if x.startswith('4. '));section=paras[start:end]
    for slide in slides:
        assert section[section.index(str(slide['n']))+1]==slide['title']
        for path in slide['source']:
            if not path.startswith('http') and not (ROOT/path).exists():raise FileNotFoundError(path)
    write(OUT/'esquema_definitivo_13.json',json.dumps(slides,indent=2,ensure_ascii=False))
    text='# Esquema definitivo de trece diapositivas para revisión\n\nTítulos y orden comprobados contra la guía original. Todas las fuentes son rutas verificables desde `CEFET_MG/`.\n\n'
    for s in slides:
        text+=f"## {s['n']}. {s['title']}\n\n**Objetivo:** {s['objective']}\n\n**Contenido resumido:** {s['content']}\n\n**Datos verificables:** {s['verifiable_data']}\n\n**Gráfica o figura:** {s['evidence']}\n\n**Archivo fuente:** "+'; '.join('`'+x+'`' for x in s['source'])+f"\n\n**Explicación oral sugerida:** {s['oral_explanation']}\n\n**Limitaciones que no deben omitirse:** {s['limitations']}\n\n"
    write(DOC/'esquema_definitivo_13.md',text)
    write(OUT/'informe_final.md',f'''# Consolidación científica final

**Conclusión defendible:** E2, mando constante al 50%, es la mejor alternativa nominal
evaluada entre E0/E1/E2 bajo U, condiciones iniciales próximas al equilibrio y ausencia
de demanda externa documentada. La revisión es posterior a conocer el diagnóstico.
Los protocolos, comparaciones históricas y calibración permanecen intactos.

{table(example[['scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp']])}

RMSE en esta tabla: desviación de regulación, cm, corrida 8 ~800 s. Precisión predictiva
original de U, medias por corrida, separada:

{table(pred)}

Se ejecutaron 19 comparaciones nominales y 90 sensibilidades exploratorias. E2 fue elegido
en todas, sin modificar la regla. El sesgo permanente desplazó el equilibrio, por lo que
no se acredita rechazo de perturbaciones. Se conservan excursiones de E0/E1 fuera del
rectángulo de estados observado y no se proclama cobertura experimental total.

Documentos vigentes: docs/consolidacion_final/. Esquema de 13 diapositivas con objetivos,
contenido, cifras, figuras, fuentes, explicación oral y límites: esquema_definitivo_13.md.
El informe_cumplimiento.md registra únicamente comprobaciones efectivamente ejecutadas.
Anexos A, B y C completados en docs/consolidacion_final/anexos_A_B_C.md (Kevin Santiago Correa Acosta — 67001271; Santiago Cárdenas Rubio — 67001160; Modelado y Simulación, Universidad Católica de Colombia, 8 de noviembre de 2026).
''')
    print('Documentación vigente consolidada; trece diapositivas con ocho campos y fuentes verificadas.')

if __name__=='__main__':main()
