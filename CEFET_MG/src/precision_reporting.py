"""Informes avanzados derivados exclusivamente de los CSV/JSON ejecutados."""
import json,hashlib
import numpy as np
import pandas as pd
from .data_processing import ROOT
from .precision_study import OUT,dump
from .precision_models import SPECS
from .reporting import table

def summary_figures(wide,phase,data,profiles,recommended):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figs=OUT/'figures'; figs.mkdir(exist_ok=True)
    ordered=wide.set_index('model').sort_values('CV_peor_NRMSE',ascending=False)
    fig,axes=plt.subplots(1,2,figsize=(17,max(7,len(ordered)*.32)))
    for metric,ax in zip(['RMSE','NRMSE'],axes):
        y=np.arange(len(ordered))
        ax.barh(y-.15,ordered[f'{metric}_h1'],height=.3,label='h1')
        ax.barh(y+.15,ordered[f'{metric}_h2'],height=.3,label='h2')
        ax.set_yticks(y,ordered.index,fontsize=8)
        ax.set_xlabel(metric+(' (cm)' if metric=='RMSE' else ' (adimensional)'))
        ax.set_title('Medias por corrida | evaluación interna 8–10 | corridas completas');ax.legend()
    fig.tight_layout();fig.savefig(figs/'comparacion_todos.png',dpi=120);plt.close(fig)
    relevant=['C_bomba','D_conservativo',recommended]
    q=data[(data.protocol=='cv')&(data.window=='completa')&data.model.isin(relevant)]
    fig,ax=plt.subplots(1,2,figsize=(13,5))
    for c,a in zip(['h1','h2'],ax):
        q[q.tank==c].pivot(index='run',columns='model',values='NRMSE').plot(ax=a,marker='o')
        a.set_title(c+' | evaluación cruzada interna | corridas completas');a.set_xlabel('Corrida reservada');a.set_ylabel('NRMSE')
    fig.tight_layout();fig.savefig(figs/'errores_por_corrida.png',dpi=120);plt.close(fig)
    q=phase[phase.model.isin(relevant)&phase.window.isin(['excitacion','recuperacion'])]
    fig,ax=plt.subplots(1,2,figsize=(14,5))
    for c,a in zip(['h1','h2'],ax):
        q[q.tank==c].pivot(index='model',columns='window',values='RMSE').plot.bar(ax=a,rot=15)
        a.set_ylabel('RMSE (cm)');a.set_title(c+' | medias por corrida | evaluación interna 8–10')
    fig.tight_layout();fig.savefig(figs/'error_por_fase.png',dpi=120);plt.close(fig)
    if len(profiles):
        labels=profiles.model.unique();fig,ax=plt.subplots(len(labels),1,figsize=(10,3*len(labels)),squeeze=False)
        for a,label in zip(ax[:,0],labels):
            q=profiles[(profiles.model==label)&(profiles.stage=='principal')]
            field='delay' if 'retardo' in label else 'tau'
            a.plot(q[field],q.mse_sum,marker='o');a.set_xlabel(field+' (s)');a.set_ylabel('Suma MSE normalizado')
            a.set_title(label+' | perfil con reajuste en desarrollo 1–7')
        fig.tight_layout();fig.savefig(figs/'perfiles_dinamica.png',dpi=120);plt.close(fig)

def main():
    d=pd.read_csv(OUT/'metrics.csv');fits=json.loads((OUT/'all_fits.json').read_text())
    reg=json.loads((OUT/'registry.json').read_text());base=json.loads((OUT/'baseline_diagnosis.json').read_text())
    numeric=pd.read_csv(OUT/'numerical_verification.csv');sens=pd.read_csv(OUT/'sensitivity.csv')
    diag=pd.DataFrame(json.loads((OUT/'residual_diagnostics.json').read_text()))
    write=lambda name,text:(OUT/name).write_text(text,encoding='utf-8')
    p=d[(d.protocol=='principal')&(d.role=='evaluacion')&(d.window=='completa')]
    cv=d[(d.protocol=='cv')&(d.window=='completa')]
    def aggregate(frame):
        return frame.groupby(['model','tank'])[['MAE','RMSE','NRMSE','bias','max_abs','R2','final_error','peak_error']].mean().reset_index()
    primary=aggregate(p); cross=aggregate(cv)
    wide=primary.pivot(index='model',columns='tank',values=['MAE','RMSE','NRMSE','bias'])
    wide.columns=['_'.join(x) for x in wide.columns];wide=wide.reset_index()
    cvworst=cross.groupby('model').NRMSE.max();wide['CV_peor_NRMSE']=wide.model.map(cvworst)
    for ref in ['C_bomba','D_conservativo']:
        refrow=wide[wide.model==ref].iloc[0]
        for tank in ['h1','h2']:
            wide[f'mejora_RMSE_pct_vs_{ref}_{tank}']=100*(1-wide[f'RMSE_{tank}']/refrow[f'RMSE_{tank}'])
            wide[f'reduccion_RMSE_cm_vs_{ref}_{tank}']=refrow[f'RMSE_{tank}']-wide[f'RMSE_{tank}']
    def family(label):return reg[label]['base'] if label in reg else label
    def conservation(label):
        if label=='C_bomba':return 'Sin flujos identificados en original'
        if label=='D_conservativo':return 'Balance efectivo; topología hipotética'
        if family(label)=='S_balance_empirico_C':return 'Balance local con transferencia empírica'
        if family(label)[0] in ['Q','R','T','U']:return 'Balance local; conductancias efectivas'
        return 'Balance efectivo; topología hipotética'
    wide['Conservacion']=wide.model.map(conservation)
    wide['Limitaciones']='Desarrollo sobre entrada repetida; sin áreas ni topología confirmadas'
    wide=wide.sort_values('CV_peor_NRMSE');wide.to_csv(OUT/'resultados_comparativos.csv',index=False)
    primary.to_csv(OUT/'principal_por_tanque.csv',index=False);cross.to_csv(OUT/'cv_por_tanque.csv',index=False)
    # Tabla completa permanece disponible; clasificación por CV con desempate por complejidad.
    def complexity(label):
        return len(fits[label]['principal']['parameters'])+(1 if label.endswith(('__retardo','__actuador')) else 0)
    predictive=wide.iloc[0].model
    candidates=[x for x in wide.model if x!='C_bomba' and family(x)!='S_balance_empirico_C']
    best_value=min(cvworst[x] for x in candidates)
    near=[x for x in candidates if cvworst[x]<=best_value*1.01]
    recommended=min(near,key=lambda x:(complexity(x),cvworst[x]))
    chosen=wide[wide.model==recommended].iloc[0];cref=wide[wide.model=='C_bomba'].iloc[0]
    pareto=[]
    for _,row in wide.iterrows():
        others=wide[(wide.NRMSE_h1<=row.NRMSE_h1)&(wide.NRMSE_h2<=row.NRMSE_h2)&
                    ((wide.NRMSE_h1<row.NRMSE_h1)|(wide.NRMSE_h2<row.NRMSE_h2))]
        if len(others)==0:pareto.append(row.model)
    minima={tank:dict(model=wide.loc[wide[f'NRMSE_{tank}'].idxmin(),'model'],
                    NRMSE=float(wide[f'NRMSE_{tank}'].min())) for tank in ['h1','h2']}
    simultaneous=bool(chosen.NRMSE_h1<cref.NRMSE_h1 and chosen.NRMSE_h2<cref.NRMSE_h2)
    cvrec=cross[cross.model==recommended].set_index('tank');cvc=cross[cross.model=='C_bomba'].set_index('tank')
    simultaneous_cv=bool((cvrec.NRMSE<cvc.NRMSE).all())
    joint_candidates=[]
    for label in candidates:
        row=wide[wide.model==label].iloc[0];cvrow=cross[cross.model==label].set_index('tank')
        if row.NRMSE_h1<cref.NRMSE_h1 and row.NRMSE_h2<cref.NRMSE_h2 and (cvrow.NRMSE<cvc.NRMSE).all():
            joint_candidates.append(label)
    joint_best=min(joint_candidates,key=lambda x:cvworst[x]) if joint_candidates else None
    joint_table=wide[wide.model.isin(joint_candidates)]
    dump(OUT/'selection.json',dict(predictive_lowest_worst_cv=predictive,recommended=recommended,
        parameters=fits[recommended]['principal']['parameters'],delay=fits[recommended]['principal'].get('delay',0),
        tau=fits[recommended]['principal'].get('tau',0),
        scale_cm=fits[recommended]['principal']['scale_cm'],minima_primary=minima,
        simultaneous_improvement_primary=simultaneous,simultaneous_improvement_cv=simultaneous_cv,
        simultaneous_candidates=joint_candidates,best_simultaneous=joint_best,
        pareto_primary=pareto,criterion='Peor NRMSE medio CV, preferir menos parámetros dentro de 1% relativo; balance condicional'))
    def meanwindows(protocol='principal',role='evaluacion'):
        return d[(d.protocol==protocol)&(d.role==role)].groupby(['model','window','tank'])[['MAE','RMSE','NRMSE','bias']].mean().reset_index()
    phase=meanwindows();phase.to_csv(OUT/'metricas_por_fase.csv',index=False)
    comparable=['model','RMSE_h1','RMSE_h2','NRMSE_h1','NRMSE_h2','CV_peor_NRMSE','Conservacion']
    fitrows=[]; paramrows=[]; profiles=[]
    for label,log in fits.items():
        l=log['principal'];costs=[s['cost'] for s in l['starts']]
        fitrows.append(dict(model=label,parameters=complexity(label),condition=l['condition'],
            active_bounds=','.join(l.get('active_bounds',[])) if isinstance(l.get('active_bounds'),list) and all(isinstance(x,str) for x in l.get('active_bounds',[])) else str(l.get('active_bounds')),
            starts_success=sum(s['success'] for s in l['starts']),cost_min=min(costs),cost_max=max(costs),
            optimizer_success=l.get('optimizer',{}).get('success') if l.get('optimizer') else True))
        for key,value in l['parameters'].items():paramrows.append(dict(model=label,parameter=key,value=value))
        for stage,adj in [('principal',l)]+[(f'cv_{k}',z) for k,z in log.get('cv',{}).items()]:
            for row in adj.get('profile_costs',[]):
                profiles.append(dict(model=label,stage=stage,delay=row['delay'],tau=row['tau'],
                                      mse_sum=sum(row['mse']),mse_h1=row['mse'][0],mse_h2=row['mse'][1],
                                      selected=adj['delay']==row['delay'] and adj['tau']==row['tau']))
    fitframe=pd.DataFrame(fitrows);fitframe.to_csv(OUT/'optimizer_diagnostics.csv',index=False)
    pd.DataFrame(paramrows).to_csv(OUT/'parameters.csv',index=False)
    pf=pd.DataFrame(profiles);pf.to_csv(OUT/'delay_actuator_profiles.csv',index=False)
    # Escalas individuales de identificación de parámetros entre particiones.
    parameter_variation=[]
    for label,log in fits.items():
        for key in log['principal']['parameters']:
            vals=[v['parameters'][key] for v in log['cv'].values()]
            parameter_variation.append(dict(model=label,parameter=key,min=min(vals),max=max(vals),mean=np.mean(vals),
                                            relative_sd=np.std(vals,ddof=1)/max(abs(np.mean(vals)),1e-12)))
    pd.DataFrame(parameter_variation).to_csv(OUT/'parameter_variation_cv.csv',index=False)
    l=fits[recommended]['principal']; sigma=l['scale_cm']
    write('diagnostico_modelos.md',f'''# Diagnóstico de C y D

Se conservaron parámetros y ecuaciones originales, sin recalibrarlos. Las nuevas tablas
reproducen exactamente sus puntuaciones compartidas con la primera etapa (prueba automática).
La evaluación sigue siendo desarrollo con series previamente examinadas.

Jacobianos en el equilibrio y relaciones de sensibilidad:

```json
{json.dumps(base,indent=2,ensure_ascii=False)}
```

D impone q12=s sqrt(h1−h2) y qout=s sqrt(16.2/31.2) sqrt(h2): las derivadas de transferencia
frente a h1 y h2 tienen magnitudes iguales, y la relación amortiguamiento/acoplamiento de h2
es 1+16.2/31.2=1.51923. C estima esas sensibilidades por separado. Ésta es una diferencia
estructural comprobada, no una prueba de que una válvula o un sensor concretos sean la causa.
Los exponentes y resistencias alternativos constituyen ablaciones para comprobar esa hipótesis.

Sesgos y errores de ambas referencias por fase:

{table(phase[phase.model.isin(['C_bomba','D_conservativo'])])}

Los signos son simulado−real. Un sesgo de h2 no se elimina automáticamente cambiando sólo
la potencia de bomba. `baseline_lag_correlations.csv` informa correlaciones residuo–entrada
pasada, pero la entrada escalonada y la memoria hidráulica impiden identificarlas con retardo
físico. Los perfiles con entradas causalmente desplazadas son la comprobación de modelo.

La sensibilidad inicial se estudia ±medio código y se conserva la trayectoria libre.
Cuantización aproximada 0.45289/0.45374 cm; precisión certificada del sensor desconocida.
La falta de geometría, caudal y señales distintas impide resolver de manera única si el sesgo
procede de ley de descarga, bomba, datum de nivel, ajuste de equilibrio o dinámica omitida.
''')
    hypotheses=pd.DataFrame([dict(model=n,parameters=len(s.names),hypothesis=s.hypothesis) for n,s in SPECS.items()])
    write('hipotesis_investigadas.md','''# Hipótesis investigadas

'''+table(hypotheses)+'''

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
''')
    write('modelos_candidatos.md','''# Formulación de candidatos

Para todos los modelos nuevos: dh1/dt=qin−q12; dh2/dt=r(q12−qout), r=A1/A2.
Los caudales q=Q/A1 están en cm/s y r es adimensional. Por ello
d(h1+h2/r)/dt=qin−qout. No se suman alturas como volumen físico ni se inventan áreas.

Se parametriza por q*=qin(50,h*) y se normalizan cabezas con H12=16.2 cm y H2=31.2 cm.
E: q12=q*Δh/H12, qout=q*sqrt(h2/H2). F: q12=q*(Δh/H12)^m,
qout=q*(h2/H2)^n, m,n∈[0.5,1]. G/H: v=λz+(1−λ)z², z=q/q*,
λ∈[0,1]; se invierte esa relación para q12 y/o qout. D fija m=n=0.5.
L reemplaza H12 por H12−offset y Δh por Δh−offset. M usa sqrt(h1/47.4) en q12.

Bomba potencial: q*=q(50), q(u)=q*(u/50)^γ. Zona muerta K sustituye u por
max(u−d,0)/(50−d). O: q(u)=q*[1−exp(−βu/50)]/[1−exp(−β)].
Curva cúbica I/J/P/R/U: z=u/100, F(z)=z+(b−1)z²+(1−2b+c)z³/3;
q(u)=q*F(z)/F(0.5). F'(z)=(1−z)²+2bz(1−z)+cz²>0 para b,c>0 y 0≤u≤100.
Es una curva empírica suave de sólo dos parámetros, sin tabla de cada escalón experimental.

Q/R: q12=max(0,q*+k12[(h1−h2)−16.2]); qout=max(0,q*+kout(h2−31.2)).
k12,kout en s^-1. T/U: mismos caudales y qin=max(0,q(u)−kpump(h1−47.4)),
kpump en s^-1. Son aproximaciones locales: el recorte no garantiza leyes correctas de
vaciado ni comportamiento real con bomba apagada fuera del régimen observado.

S: q12=max(0,q*+a(h1−47.4)−b(h2−31.2)); qout lineal local.
Su transferencia a≠b no depende únicamente del desnivel. S y T pueden realizar algebraicamente
C dentro del dominio sin recorte, mediante relaciones dadas en el protocolo; eso no
valida caudales reales ni áreas. T atribuye una diferencia de pendientes a la bomba,
mientras S la atribuye a la conexión: ambos pueden ser observacionalmente equivalentes.

Actuador opcional: dq_a/dt=[q_command(u,h1)−q_a]/τ, qin=q_a. Es un estado de actuador,
no un tanque. q_a inicial=q* supone régimen previo a 50%; en arranque esta historia no
está documentada. Retardo: aplicar u(t−δ) causal, usando 50% antes del inicio local.
RK4 particiona también los eventos desplazados y limita subpaso a τ/4 si τ>0.
''')
    write('calibracion_optimizada.md',f'''# Calibración optimizada

Se mantiene sigma de entrenamiento por filas originales únicas, ddof=1. La condición inicial
impuesta no aporta residuo a calibración. No hay eliminación de muestras de evaluación.
Las cifras principales son medias de MAE/RMSE/NRMSE por corrida, no RMSE agrupado.
Cuatro inicios seed 20261108 para cada estructura/partición. En perfiles, dos inicios por
punto para limitar coste; cada fold repite la selección de retardo/τ con su entrenamiento.

LS minimiza suma de residuos normalizados al cuadrado. Minimax minimiza un auxiliar z
sujeto a MSE_h1≤z y MSE_h2≤z; SLSQP en parámetros escalados. La variante regularizada
añade 1e-4 media(log(p/p_LS)²) sólo para parámetros con cota inferior positiva.
El ancla LS se calcula en el mismo entrenamiento. Ninguna puntuación usa esa penalización.
Las soluciones minimax pueden empeorar h2 al redistribuir error hacia el tanque menos favorecido.
No se interpreta un coste menor como una mejora garantizada en evaluación.

Se emplea [least_squares de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)
y [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html), con cotas y diagnósticos guardados.

{table(fitframe)}

Valores, puntos iniciales, costes, límites activos, mensajes y convergencia en `fit_*.json`
y `all_fits.json`. `parameters.csv` permite comparar coeficientes. C/D se leen congelados
de la primera etapa. Las cotas nuevas son restricciones de familia y regularidad, no
especificaciones medidas: q*∈[0.01,10] cm/s, r∈[0.03,3], exponentes 0.5–1,
γ∈[0.2,2], coeficientes de Bernstein positivos y conductancias positivas; ver config.json.
Si una cota es activa no se presenta su valor como estimación precisa de una propiedad física.
''')
    relevant=[recommended,'C_bomba','D_conservativo']
    quant={'h1':.45288822016,'h2':.45373915776}
    comparison_quant=primary[primary.model.isin(relevant)].copy()
    comparison_quant['RMSE_codigos']=comparison_quant.apply(lambda r:r.RMSE/quant[r.tank],axis=1)
    comparison_quant.to_csv(OUT/'sensor_resolution_comparison.csv',index=False)
    write('bondad_ajuste_optimizada.md',f'''# Bondad de ajuste optimizada

Todos los candidatos, incluidos descartados, se evalúan con MAE/RMSE cm, NRMSE adimensional,
sesgo, máximo absoluto, R², error final y diferencia entre máximos. `metrics.csv` conserva
cada corrida, partición y fase. R² puede ser negativo. El error en máximos mide amplitud,
no sincronía temporal. Residuo=simulado−observado. No se corrige con niveles observados futuros.

Comparación principal completa:

{table(wide[comparable])}

Residuos del recomendado y referencias, corrida completa:

{table(diag[(diag.model.isin(relevant))&(diag.phase=='completa')].drop(columns='acf'))}

Los resultados completos de ACF20, Q20 y p descriptivo se guardan por corrida y fase.
Los p-valores no prueban ni refutan universalmente el modelo; estimación de parámetros,
cuantización y dependencia temporal limitan su interpretación. No se aplica KS ni una
prueba de frecuencias para certificar un sistema dinámico. Inspeccionar sesgo y ACF aun
cuando las métricas sean pequeñas. Un p=0 representa subdesbordamiento numérico, no probabilidad exacta nula.

Relación con resolución aparente de sensores:

{table(comparison_quant[['model','tank','MAE','RMSE','NRMSE','RMSE_codigos']])}

La cuantización es ≈0.453 cm por código; no es exactitud certificada. Bajo un error ideal
uniforme de cuantización se obtendría Δ/sqrt(12)≈0.131 cm, pero esto no es un límite
inferior demostrado para la predicción de estos registros ni una incertidumbre certificada.
Hay dispersión entre corridas, deriva, sincronización y dinámica omitida que también contribuyen.

`figures/trajectories_*.png` y `residuals_*.png` incluyen todos los candidatos y ambos tanques:
observado/simulado, bomba, residuo-tiempo, residuo-nivel, histograma, distribución empírica y ACF.
Se muestran todas las corridas reservadas 8–10, incluidos tramos tardíos y recuperación disponible.
''')
    temporal=d[(d.protocol=='temporal')&(d.window=='tardia_320')].groupby(['model','tank'])[['RMSE','NRMSE','bias']].mean().reset_index()
    cold=d[(d.protocol=='arranque')&(d.window=='completa')].groupby(['model','tank'])[['RMSE','NRMSE','bias']].mean().reset_index()
    write('validacion_comparativa.md',f'''# Comparación de evaluación interna

Los diez experimentos comparten una entrada y ya se examinaron. Esta fase es desarrollo
adaptativo, aunque cada ajuste respete sus grupos. No se obtiene validación externa nueva.
Principal: 1–7 ajustan, 8–10 puntúan. CV: cinco folds contiguos, ocho corridas ajustan y
dos puntúan. Los perfiles se seleccionan de nuevo dentro del entrenamiento de cada fold.
Se evalúan estados libres desde una condición inicial medida, sin reinicializar en las ventanas.

Todos los candidatos, evaluación principal y peor NRMSE medio CV:

{table(wide[comparable])}

CV por tanque del recomendado y referencias:

{table(cross[cross.model.isin(relevant)])}

Prueba temporal: calibrar sólo 320 s iniciales de desarrollo y predecir t>320 s en 8–10:

{table(temporal)}

Arranque frío separado (no se ajustó con él):

{table(cold)}

Los modelos locales no se consideran válidos para arranque aunque mejoren en operación.
Fases de excitación y recuperación completas en `metricas_por_fase.csv`; la corrida 10
no contiene recuperación y no se rellena. Tampoco se elimina para mejorar el agregado.
La variación por corrida puede verse en `metrics.csv` y las figuras comparativas.

Verificación numérica: máximo |RK4(1 s)−DOP853| entre todos los modelos/corridas
={numeric[numeric.method=='DOP853'].max_vs_half_cm.max():.6g} cm.
Balance algebraico máximo efectivo={numeric[numeric.method=='balance_cm_s'].max_vs_half_cm.max():.6g} cm/s.
Pasos 4,2,1,0.5 s y resultados individuales en `numerical_verification.csv`.
El error numérico se separa del error frente a las mediciones; no se elige paso por ajuste empírico.
''')
    write('sensibilidad_parametros.md',f'''# Sensibilidad e identificabilidad

El Jacobiano relativo usa columnas multiplicadas por max(|p|,0.1), con diferencias
unilaterales cerca de cotas. Los números de condición y valores singulares describen
sensibilidad local del ajuste; no son intervalos de confianza bajo ruido autocorrelacionado.
Para C/D originales se conserva la convención de escalado de la etapa 1 (columnas por p);
no comparar directamente sus condiciones con las nuevas como si usaran la misma escala.

{table(fitframe[['model','parameters','condition','active_bounds']])}

Cambios máximos de trayectorias ante perturbaciones iniciales y de parámetros:

{table(sens.groupby(['model','test']).max_state_change_cm.max().reset_index())}

Iniciales: ±medio código de h1 y h2 por separado. Parámetros: ±1% hacia el interior de
la cota, mínimo 0.001 en unidades del parámetro para evitar perturbación nula; delta real
en `sensitivity.csv`. No son un experimento de incertidumbre probabilística conjunta.
`parameter_variation_cv.csv` registra estabilidad de cada coeficiente entre folds.
Áreas y caudales absolutos siguen siendo estructuralmente no identificables: escala común
de área y caudal no cambia niveles. S/T muestran además ambigüedad de interpretación física.

Perfiles de retardo y actuador, selección en cada entrenamiento:

{table(pf[pf.selected][['model','stage','delay','tau','mse_sum']])}

El perfil completo se conserva en `delay_actuator_profiles.csv`, incluyendo puntos desfavorables.
Un mínimo en cero o cerca de él, o cambios del mínimo entre folds, no respalda una constante
física identificada. Los intervalos no se presentan como tiempos medidos: el muestreo es ≈4 s,
las transiciones tienen jitter y sólo hay una secuencia repetida. La selección por coste
no prueba un mecanismo de actuador. Un τ adicional es un estado interno de bomba, no un tanque.
''')
    gaincols=['model']+[f'mejora_RMSE_pct_vs_{ref}_{tank}' for ref in ['C_bomba','D_conservativo'] for tank in ['h1','h2']]
    detail=wide[wide.model==recommended]
    write('modelo_recomendado.md',f'''# Modelo recomendado y decisión

**Recomendación local provisional: {recommended}.** Menor peor NRMSE medio CV bruto:
{predictive}. Se prefiere menor complejidad entre candidatos con balance condicional dentro
de 1% relativo del mejor peor NRMSE CV. Las cifras no demuestran óptimo global ni validación externa.
La topología, los caudales absolutos y el mecanismo de bomba siguen sin estar confirmados.

{table(detail[comparable])}

Mejora porcentual del RMSE (positivo=mejora; negativo=empeora):

{table(detail[gaincols])}

Parámetros y configuración en `selection.json` y `parameters.csv`. Las escalas principales
se mantienen en {sigma[0]:.8f} cm y {sigma[1]:.8f} cm. La familia no se recomienda para
desbordamiento, vaciado ni arranque; es una representación local con caudales efectivos.

## Respuestas finales

1. Menor NRMSE principal h1: {minima['h1']['NRMSE']:.8f}, modelo {minima['h1']['model']}.
2. Menor NRMSE principal h2: {minima['h2']['NRMSE']:.8f}, modelo {minima['h2']['model']}.
   Son mínimos descriptivos de una búsqueda y pueden pertenecer a candidatos distintos.
3. ¿Se consiguió mejorar simultáneamente a C? Candidatos que mejoran ambos tanques tanto
   en principal como en CV: {', '.join(joint_candidates) if joint_candidates else 'ninguno'}.
   Mejor peor NRMSE CV entre ellos: {joint_best}.
   El recomendado por menor peor error global mejora simultáneamente: principal {simultaneous}; CV {simultaneous_cv}.
4. Reducción RMSE frente a C: h1={cref.RMSE_h1-chosen.RMSE_h1:+.6f} cm;
   h2={cref.RMSE_h2-chosen.RMSE_h2:+.6f} cm. Frente a D, ver tabla y CSV comparativo.
5. Menor error según peor NRMSE medio CV: {predictive}; no equivale al mínimo separado de cada tanque.
6. Ningún candidato tiene topología real verificada. D tiene una hipótesis global más restrictiva;
   Q/R/T/U tienen balances locales explícitos; S es una realización empírica. Conservar balance
   algebraico no da por sí solo mayor respaldo experimental.
7. Es posible escribir balances locales con precisión comparable a C (T es algebraicamente
   equivalente en el dominio sin recorte), pero esa equivalencia no demuestra una nueva ley
   física. La mejora adicional se cuantifica arriba, sin confundirla con identificación del circuito.
8. La estabilidad entre corridas está documentada por CV y por métricas individuales.
   Compartir la señal limita la generalización; comparar también excitación y recuperación.
9. Revisar ACF y sesgos en el informe de bondad: una reducción de RMSE no vuelve independientes
   los residuos. Los p-valores se reportan sólo como diagnóstico descriptivo.
10. Limitan la reducción: cuantización y dispersión experimental, curva de bomba desconocida,
    pérdidas no medidas, sincronización, posible deriva y ambigüedad de parámetros físicos.
    No se atribuye una causa única ni se declara alcanzado un límite teórico de error.
11. Sí, se necesita otra secuencia experimental y documentación del montaje para sustentar
    generalización y distinguir hipótesis de bomba/conexión que producen niveles similares.
12. Para escenarios académicos locales usar provisionalmente {recommended}, con la misma
    saturación de señal y alcance observado, contrastándolo con C/D. Sus resultados serán
    contrafactuales simulados. No declarar funcionamiento real de una política no ensayada.

Frontera de Pareto principal (dos NRMSE): {', '.join(pareto)}.
Todos los candidatos descartados y variantes se conservan en los CSV y figuras.
No se desarrolló AgentPy, Streamlit ni presentación.
''')
    with (OUT/'modelo_recomendado.md').open('a',encoding='utf-8') as f:
        f.write('''

## Alternativa que mejora simultáneamente ambos tanques

'''+table(joint_table[comparable])+'''

'''+table(joint_table[gaincols])+f'''

La elección tiene un compromiso explícito: {recommended} minimiza el peor error con
menos parámetros; {joint_best} es la opción si se exige que ninguno de los dos tanques
empeore frente a C. Para escenarios que prioricen esa mejora conjunta, usar {joint_best}
como alternativa local y contrastarla con la recomendación parsimoniosa. No ocultar
la mayor complejidad ni confundir el desfase efectivo con un retardo físico medido.
''')
    ablations=['P_D_bomba_monotona','P_D_bomba_monotona__retardo','P_D_bomba_monotona__actuador',
               'U_bomba_carga_monotona','U_bomba_carga_monotona__retardo','U_bomba_carga_monotona__actuador']
    with (OUT/'diagnostico_modelos.md').open('a',encoding='utf-8') as f:
        f.write('''

## Ablación de dinámica de entrada

'''+table(wide[wide.model.isin(ablations)][['model','RMSE_h1','RMSE_h2','NRMSE_h1','NRMSE_h2','CV_peor_NRMSE']])+'''

La comparación mantiene la familia y vuelve a estimar sus parámetros con desarrollo.
La mejora al admitir desfase se sostiene entre grupos, lo que respalda una corrección
temporal efectiva de reproducción. No demuestra si su origen es bomba, adquisición o
transporte hidráulico. El mecanismo no se puede separar con estas señales solamente.
Una curva estática más flexible por sí sola no produjo la mayor parte de la reducción.
''')
    with (OUT/'sensibilidad_parametros.md').open('a',encoding='utf-8') as f:
        f.write('''

## Interpretación del perfil obtenido

P elige δ=2 s en todos los folds; también τ=2 s con el modelo alternativo de actuador.
Ambos obtienen errores muy próximos y la diferencia de peor NRMSE CV es menor que 1%.
U también elige δ=2 s en todos los folds; su τ preferido cambia entre 2 y 4 s.
Esto respalda un desfase efectivo respecto a las marcas temporales registradas, sin
identificar de forma única un retardo de transporte o una constante de bomba.
El perfil es discreto y no prueba que 2.000 s sea un óptimo continuo exacto. No se exploró
un adelanto no causal. Con Ts≈4 s no se puede certificar la precisión de ese tiempo físico.
''')
    write('README.md','''# Reproducción de la optimización de precisión

Desde la raíz CEFET_MG y con los paquetes fijados de requirements.txt:

```powershell
$env:PYTHONIOENCODING='utf-8'
../.venv/Scripts/python.exe -m src.precision_study
../.venv/Scripts/python.exe -m src.precision_extend
../.venv/Scripts/python.exe -m src.precision_diagnostics
../.venv/Scripts/python.exe -m src.precision_reporting
../.venv/Scripts/python.exe -m pytest -q tests | Out-File -Encoding utf8 reports/optimizacion_precision/tests.txt
../.venv/Scripts/python.exe -m src.precision_reporting
```

Si el entorno está dentro de CEFET_MG, sustituir ../.venv por .venv. No ejecutar los
comandos de primera etapa: este flujo sólo escribe optimizacion_precision y sus propios logs.
El primer comando reproduce las once familias iniciales y sus variantes; el segundo añade
las cinco familias locales y variantes adaptativas declaradas. No usar métricas de esta
búsqueda como validación externa. config.json, environment.json y code_manifest.json
registran configuración, versiones y huellas. Cada ajuste principal se repite en diagnostics;
reproducibility.json compara parámetros exactos. No se repitió toda la búsqueda CV una
segunda vez: la comprobación repetida se limita a ajustes principales y al perfil elegido.

Leer modelo_recomendado.md, diagnostico_modelos.md y validacion_comparativa.md.
No se sustituyen los informes, parámetros ni figuras de la primera etapa.
''')
    sources=list((ROOT/'src').glob('*.py'))+[ROOT/'docs/protocolo_optimizacion.md']+list((ROOT/'tests').glob('*.py'))
    dump(OUT/'code_manifest.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    repeated=json.loads((OUT/'reproducibility.json').read_text())
    dump(OUT/'campaign_summary.json',dict(total_models=len(fits),base_families=len(SPECS),
        principal_refits=len(repeated),principal_exact=all(x['exact'] for x in repeated),
        evaluation='Desarrollo interno adaptativo; no validación externa',
        existing_results_preserved=json.loads((OUT/'integrity.json').read_text())['originals_unchanged']))
    summary_figures(wide,phase,d,pf,recommended)
    print('Recomendado:',recommended,'; predictivo:',predictive,'; mejora simultánea:',simultaneous,simultaneous_cv)

if __name__=='__main__':main()
