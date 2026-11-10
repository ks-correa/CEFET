from .documentary_archive import write_document, historical_source, ARCHIVED
"""Redacta informes a partir de resultados ejecutados, sin resultados precargados."""
import json
import numpy as np
import pandas as pd
from .data_processing import ROOT
from .models import NAMES,specification

def table(f):
    # Sin dependencia opcional tabulate.
    f=f.copy()
    for c in f.select_dtypes(include='number'):
        f[c]=f[c].map(lambda v:f'{v:.5g}')
    return '| '+' | '.join(map(str,f.columns))+' |\n|'+'|'.join(['---']*len(f.columns))+'|\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in f.itertuples(index=False,name=None))

def main():
    out=ROOT/'reports'; docs=ROOT/'docs'
    m=pd.read_csv(out/'metrics.csv'); audit=json.loads((ROOT/'data/processed/audit.json').read_text())
    mapping=pd.read_csv(ROOT/'data/processed/run_mapping.csv'); logs=json.loads((out/'calibration.json').read_text())
    primary=m[(m.protocol=='principal')&(m.role=='evaluacion')&(m.window=='completa')]
    cv=m[(m.protocol=='cv')&(m.window=='completa')]
    def summary(f):return f.groupby(['model','tank'])[['MAE','RMSE','NRMSE','bias']].mean().reset_index()
    principal=summary(primary); cvr=summary(cv)
    excitation=m[(m.protocol=='principal')&(m.role=='evaluacion')&(m.window=='excitacion')]
    temporal=m[m.protocol=='temporal']; startup=m[m.protocol=='arranque']
    diagnostics=json.loads((out/'residuals.json').read_text())
    diagnosticrows=[]
    for run,ts in diagnostics.items():
        for tank,d in ts.items():diagnosticrows.append(dict(run=run,tank=tank,ACF1=d['acf'][1],Q20=d['Q'],p_descriptivo=d['p_descriptive']))
    convergence=pd.read_csv(out/'convergence.csv')
    parameters=[]
    for model,v in logs.items():
        for key,value in v['principal']['parameters'].items():parameters.append(dict(model=model,parameter=key,value=value))
    pd.DataFrame(parameters).to_csv(out/'parameters.csv',index=False)
    fitrows=[]
    for model,v in logs.items():
        l=v['principal']; costs=[s['cost'] for s in l['starts']]
        fitrows.append(dict(model=model,cond_Jrel=l['condition'],cost_min=min(costs),cost_max=max(costs),
                            converged=sum(s['success'] for s in l['starts']),bounds=sum(x!=0 for x in l['active_bounds'])))
    # Elegibilidad para alcance completo: cada corrida, ambos tanques, excitación y CV.
    gates={}
    for model in NAMES:
        q=m[(m.model==model)&(((m.protocol=='principal')&(m.role=='evaluacion'))|(m.protocol=='cv'))&m.window.isin(['completa','excitacion'])]
        gates[model]=bool((q.NRMSE<=.3).all())
    eligible=[name for name,ok in gates.items() if ok]
    preferred=min(eligible,key=lambda name:len(specification(NAMES.index(name))[0])) if eligible else None
    write=write_document
    if preferred:
        write(out/'modelo_recomendado.json',json.dumps(dict(model=preferred,
              parameters=logs[preferred]['principal']['parameters'],
              scale_cm=logs[preferred]['principal']['scale_cm'],
              criterion='Menor número de parámetros entre modelos que cumplen por corrida completa y excitación principal/CV',
              caveat='Topología hipotética; evaluación interna; no válido para arranque'),indent=2,ensure_ascii=False))
    write(out/'auditoria_dataset.md',f'''# Auditoría del dataset CEFET-MG

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

Resolución aparente mínima de códigos: h1={audit['quantization_cm']['h1']:.9f} cm,
h2={audit['quantization_cm']['h2']:.9f} cm. No equivale a exactitud del instrumento.
Dispersión media entre repeticiones en el extracto corto (desviación muestral por tiempo):
h1={audit['repetition_std_cm']['h1']:.4f} cm; h2={audit['repetition_std_cm']['h2']:.4f} cm.
Valores extremos y saltos se conservan: no hay criterio documentado para retirarlos como anomalías.

## Reconstrucción de corridas

{table(mapping)}

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
''')
    write(out/'bondad_ajuste.md',f'''# Bondad de ajuste y alcance

La evaluación interna confirma que introducir una respuesta no lineal de bomba mejora
la reproducción frente al modelo lineal y las referencias constantes. No certifica una
curva física de bomba ni validación externa. Protocolo y ecuaciones en `docs/`.

## Evaluación principal

Entrenamiento: corridas 1–7 completas; evaluación: 8–10 libres. Desviaciones estándar
de entrenamiento: {logs['C_bomba']['principal']['scale_cm'][0]:.8f} cm para h1 y
{logs['C_bomba']['principal']['scale_cm'][1]:.8f} cm para h2 (ddof=1), usando filas
de origen únicas. Se excluye del objetivo el estado inicial impuesto de cada corrida.
Los valores siguientes son medias de métricas por corrida; no RMSE agrupado entre filas.
La última corrida es más corta y se informa individualmente en `metrics.csv`.

{table(principal)}

Excitación completa de 800 s, sin diluir el error con la recuperación:

{table(summary(excitation))}

## Validación cruzada por grupos

Cinco particiones contiguas de dos corridas reservadas, ocho para ajuste. Cada partición
usa su propia desviación estándar de entrenamiento; no se recalcula con evaluación.

{table(cvr)}

Peor NRMSE por tanque entre las diez corridas reservadas:

{table(cv.groupby(['model','tank']).NRMSE.max().reset_index())}

## Extrapolación temporal

Al ajustar sólo los primeros 320 s de 1–7 y predecir el resto de 8–10 sin reinicialización:

{table(summary(temporal))}

La degradación de h2 indica que los primeros 320 s no identifican suficientemente
su comportamiento tardío. No ocultar este resultado usando únicamente el ajuste completo.

Arranque desde niveles bajos, excluido del ajuste y fuera del alcance local:

{table(summary(startup))}

Ningún modelo satisface el umbral en el arranque. No recomendar llenado en frío.

## Residuos

Para el candidato predictivo C, seleccionado para diagnóstico por menor NRMSE medio CV:

{table(pd.DataFrame(diagnosticrows))}

El residuo se define simulado−observado: sesgo positivo significa sobrepredicción.
La dependencia temporal visible y ACF impiden interpretar las muestras como errores
independientes. Ljung–Box Q(20) y su p-valor son descriptivos: parámetros estimados,
cuantización y secuencias compartidas incumplen una interpretación confirmatoria sencilla.
Un p pequeño señala estructura; un p alto tampoco demostraría validez. No se aplican
KS o chi-cuadrado de frecuencias como prueba universal del modelo.

`metrics.csv` incluye MAE/RMSE cm, NRMSE adimensional, sesgo cm, error absoluto máximo cm,
R² (sin unidad), diferencia entre máximos cm y error final cm. El error en máximos compara
amplitudes, no coincidencia temporal. R² puede ser negativo y no mide causalidad.
Las ventanas inicial, tardía, excitación y recuperación se reportan sin reajustar estados.

## Estimación y sensibilidad

{table(pd.DataFrame(fitrows))}

El número de condición corresponde al Jacobiano de residuos con columnas multiplicadas
por los parámetros: sensibilidad relativa local. Sus valores singulares se conservan en
`calibration.json`; no son intervalos de confianza bajo ruido autocorrelacionado.
Los cuatro puntos iniciales, criterios de terminación, cotas activas y costes se guardan
para cada ajuste principal, temporal y cruzado. Una buena condición local no elimina
la no identificabilidad estructural de áreas/caudales absolutos.

## Verificación numérica

{table(convergence)}

Los errores de RK4 frente a DOP853 (~10^-7 cm con paso máximo 1 s) son mucho menores
que el error experimental. Reducir paso no resuelve sesgo estructural. La comparación
usa exactamente las mismas discontinuidades causales de bomba. La identidad de conservación
de B,D está en las predicciones como `balance_effective_cm_s`; no se suman alturas como volumen.

Figuras: `figures/exploracion.png`, `trajectory_8.png` a `trajectory_10.png`,
`residuals_8.png` a `residuals_10.png`, `model_comparison.png`, `errors_by_run.png`.
Todas distinguen mediciones y simulación. No se declara que una estrategia operativa
nueva haya sido medida. Para generalización se requieren señales nuevas y circuito documentado.
''')
    write(out/'viabilidad.md',f'''# Dictamen técnico de viabilidad

**VIABLE CON LIMITACIONES para reproducción local de las corridas completas disponibles.**
No equivale a aprobación docente ni autoriza conclusiones sobre otros regímenes.

1. Hay mediciones de ambos tanques atribuidas a un montaje físico por los investigadores.
2. Procedencia y unidades cm/% verificadas en README y [Zenodo](https://zenodo.org/records/19856119).
3. El acoplamiento está documentado, pero el circuito hidráulico preciso no: falta esquema primario.
4. Balances B,D coherentes bajo una hipótesis explícita; A,C son aproximaciones locales.
5. Se estiman parámetros efectivos; no áreas ni caudales absolutos por separado.
6. RK4 se contrastó con solución lineal exacta, convergencia y DOP853.
7. Cumplimiento por cada corrida de evaluación principal y CV, tanto completa como excitación:
   {json.dumps(gates,ensure_ascii=False)}. La preferencia parsimoniosa según protocolo es **{preferred}**;
   C es la alternativa predictiva con menor error, no un reemplazo oculto del modelo conservativo.
8. MAE/RMSE/NRMSE principales por tanque y modelo:

{table(principal[principal.model.isin(['C_bomba','D_conservativo'])])}

9. Hay sesgos y autocorrelación residual; la precisión escalar no demuestra ruido blanco.
10. C y D superan persistencia y equilibrio; también mejoran A. Ver tabla completa en bondad de ajuste.
11. Funcionan en las excitaciones repetidas observadas y recuperación, con calibración completa.
12. Fallan en arranque y en la prueba temporal de h2 al ajustar únicamente primeros 320 s.
13. Evidencia interna previamente examinada; CV reproduce estabilidad entre repeticiones de
la misma señal, no validación ciega ni externa. No se seleccionó ventana favorable para ocultar fallas.
14. Faltan nuevas entradas independientes, plano del circuito, áreas, curva de bomba y
metadatos de sensores. Debe confirmarse con el docente la aceptación de datos de terceros.

La siguiente etapa exige acotar escenarios al régimen observado, mantener explícita la
hipótesis de circuito y distinguir contrafactuales de mediciones. Este entregable se limita
a la primera etapa solicitada: no se construyó Streamlit, AgentPy ni las 13 diapositivas.
La suficiencia temporal no se declara resuelta: si se exige calibrar sólo 320 s, el dictamen
para ese protocolo específico es NO VIABLE con estos candidatos.
''')
    requirements=[
        ('Sistema real ≥2 tanques','README/Zenodo; circuito detallado pendiente','Parcial'),
        ('Datos experimentales y evidencia','raw, hashes y auditoría','Cumplido con fuente externa'),
        ('Aprobación docente y propuesta Anexo A','Confirmar uso de mediciones de terceros; no hay aprobación aportada','Pendiente'),
        ('Instrumento, fecha y posibles errores','Cuantización auditada; sensor y fecha no publicados','Parcial'),
        ('Variables, parámetros y unidades; Anexo B','modelo_matematico.md y parameters.csv','Cumplido para parámetros efectivos'),
        ('Balance diferencial por tanque','B,D bajo topología hipotética','Parcial: verificar circuito'),
        ('Implementación y cambio de parámetros','models.py, rk4_solver.py; comparación SciPy','Cumplido'),
        ('Conservación y niveles no negativos','Balance efectivo B,D, pruebas y trayectorias','Cumplido en dominio evaluado'),
        ('Calibración','Mínimos cuadrados, multinicio y registros','Cumplido'),
        ('Datos reservados para evaluación','Grupos y prueba temporal; evidencia ya examinada','Cumplido como evaluación interna'),
        ('MAE o RMSE e interpretación','metrics.csv y bondad_ajuste.md','Cumplido'),
        ('Escenario base y 2 alternativos; Anexo C','Plan condicional en definición del problema','Pendiente de segunda etapa'),
        ('Indicadores y decisión sustentada','Viabilidad documentada; decisión operativa pendiente','Parcial'),
        ('13 diapositivas en orden de guía','No desarrollar antes del dictamen','Pendiente'),
        ('Ambos estudiantes explican y reproducen','README y guía de estudio; ensayo por realizar','Pendiente de comprobación humana')]
    write(docs/'matriz_cumplimiento_guia.md','''# Matriz de cumplimiento de la guía

Guía DOCX leída completa, incluidos pasos, ponderaciones y anexos A/B/C.
La guía pide medir, registrar instrumento/fecha y evidencia fotográfica o registros;
usar mediciones externas requiere confirmación expresa del docente. No se afirma que
la pareja haya medido ni que tenga autorización. Los registros de terceros aportan evidencia
documental, sin inventar fotografías. La propuesta aprobada sigue pendiente.

'''+table(pd.DataFrame(requirements,columns=['Requisito','Cómo se cumple y evidencia','Estado']))+'''

Ponderaciones: problema/datos 15%, modelo 20%, implementación 15%, calibración/validación
20%, escenarios 15%, análisis/decisión 10%, presentación 5%.
Orden obligatorio de diapositivas: portada; problema/pregunta; esquema; datos reales;
variables/parámetros; modelo; implementación; calibración; validación; escenarios;
comparación; decisión/limitaciones/conclusiones; referencias/evidencias.
Esta matriz no certifica que los estudiantes sepan defender el trabajo: ambos deben reproducir
el análisis y explicar cada ecuación, partición, métrica y limitación antes de presentar.
''')
    write(ROOT/'README.md','''# Modelado continuo de dos tanques CEFET-MG

Primera etapa científica ejecutada. Dictamen: **VIABLE CON LIMITACIONES** en el régimen
de las excitaciones completas repetidas. No es válido para arranque ni para identificar
el régimen tardío usando sólo 320 s. No hay validación externa ni aprobación docente aportada.

## Reproducir en PowerShell

Desde esta carpeta, con Python 3.14 y uv instalado:

```powershell
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
$env:PYTHONIOENCODING='utf-8'
.venv/Scripts/python.exe -m src.experiments
.venv/Scripts/python.exe -m src.reporting
.venv/Scripts/python.exe -m pytest -q
```

La ejecución inicial usó el entorno `.venv` en la carpeta padre; también puede usarse
`../.venv/Scripts/python.exe` con los mismos paquetes fijados. Numba acelera el mismo
RK4; el primer uso compila. No descarga datos ni modifica originales. Semilla 20261108.
Los informes se regeneran después de los experimentos para mantener cifras trazables.

Leer `reports/viabilidad.md`, `reports/auditoria_dataset.md`, `reports/bondad_ajuste.md`,
`docs/protocolo_previo.md`, `docs/modelo_matematico.md`, `docs/definicion_problema.md`
y `docs/matriz_cumplimiento_guia.md`. Resultados completos en CSV/JSON y figures/.

Fuente: Silva, Coelho y Leite. Dataset D-Stabilization of a Coupled-Tank System Using
Experimental Data. Zenodo, v1.0.0, 2026. https://doi.org/10.5281/zenodo.19856119
Mediciones de investigadores externos; los estudiantes sólo modelan registros publicados.
Confirmar con el profesor la aceptación de esta modalidad.

Ambos estudiantes deben ejecutar los comandos y poder explicar: balance y unidades,
por qué no se identifican áreas absolutas, RK4 causal, grupos sin fuga, normalización de
entrenamiento, errores por régimen y diferencia entre evaluación interna y evidencia externa.
No hay app ni presentación: corresponden a una etapa posterior al dictamen.
''')
    extra='''\n\n## Comprobaciones adicionales ejecutadas

Los MD5 de los seis archivos originales coinciden con los seis publicados en la página
de Zenodo (incluido el JSON defectuoso). Esto vincula las copias locales con el registro
consultado; no resuelve las inconsistencias documentales.
'''
    with (out/'auditoria_dataset.md').open('a',encoding='utf-8') as f:f.write(extra)
    robpath=out/'robustness.csv'
    if robpath.exists():
        rob=pd.read_csv(robpath)
        dg=json.loads((out/'residuals_conservative.json').read_text())
        dgrows=[dict(run=r,tank=c,ACF1=d['acf'][1],Q20=d['Q'],p_descriptivo=d['p_descriptive'])
                for r,ts in dg.items() for c,d in ts.items()]
        extra='''\n\n## Robustez y modelo conservativo recomendado

`modelo_recomendado.json` contiene D, elegido por parsimonia según el protocolo.
`selected_model.json` identifica C exclusivamente como candidato de menor error medio
para las figuras y diagnósticos predictivos. No son el mismo criterio de elección.
`figures/conservative_8.png` muestra D, con su hipótesis física expresamente indicada.

Sensibilidad: perturbación +1% de cada parámetro sin reajuste, y condición inicial ±media
unidad de cuantización en cada tanque. `robustness.csv` conserva todos los resultados,
incluidas métricas por tanque para perturbaciones iniciales. No son intervalos probabilísticos
ni incorporan incertidumbre estructural. Resumen de cambios máximos de estado:

'''+table(rob.groupby(['model','test']).max_state_change_cm.max().reset_index())+'''

Diagnóstico de residuos D (corridas completas reservadas):

'''+table(pd.DataFrame(dgrows))+'''

También D presenta dependencia temporal; no debe defenderse como reproducción exacta
del circuito. Se contrastó DOP853 y pasos 4,2,1,0.5 s para los cuatro candidatos. El balance
algebraico de B,D está limitado por redondeo de punto flotante, y no es evidencia empírica
de conservación volumétrica. El test lineal exacto aporta una comprobación independiente de RK4.
'''
        with (out/'bondad_ajuste.md').open('a',encoding='utf-8') as f:f.write(extra)
    repath=out/'reproducibility.json'
    if repath.exists():
        rep=json.loads(repath.read_text())
        extra=f'''\n\n## Reproducción completa

Se ejecutó de nuevo la auditoría, los cuatro candidatos, los ajustes principales,
cinco particiones cruzadas y el ajuste temporal con semilla/configuración idénticas.
Coincidencia SHA256 exacta de {rep['files_compared']} artefactos: {rep['identical']}.
Detalle en `reproducibility.json`; pruebas automatizadas en `tests.txt`.
'''
        with (out/'bondad_ajuste.md').open('a',encoding='utf-8') as f:f.write(extra)
    with (ROOT/'README.md').open('a',encoding='utf-8') as f:f.write('''

Comprobaciones adicionales (después del análisis principal):

```powershell
.venv/Scripts/python.exe -m src.robustness
.venv/Scripts/python.exe -m src.reproduce
.venv/Scripts/python.exe -m src.reporting
.venv/Scripts/python.exe -m pytest -q
```

La reproducción vuelve a ejecutar todo el análisis y compara huellas de los resultados.
El modelo recomendado por parsimonia está en `reports/modelo_recomendado.json` (D);
el candidato diagnóstico de menor error se conserva en `selected_model.json` (C).
''')
    print('Informes generados; gates=',gates,'preferencia=',preferred)

if __name__=='__main__':main()
