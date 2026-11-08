"""Ejecutar: python -m streamlit run app.py."""
from dataclasses import replace
import json
import numpy as np
import pandas as pd
import streamlit as st
from src.data_processing import ROOT
from src.simulation_engine import (U,P,MODELS,calibrated_config,exploratory_config,load_run,
                                   run_simulation,prediction_metrics,REFERENCES)
from src.scenarios import SCENARIOS,compare_scenarios
from src.tank_view import tank_view

st.set_page_config(page_title='CEFET-MG · Simulador de tanques',page_icon=':material/water_drop:',layout='wide')
LABELS={U:'U · mejora conjunta',P:'P · alternativa parsimoniosa','C_bomba':'C · referencia predictiva','D_conservativo':'D · balance efectivo'}
SECTIONS=['Proyecto','Sistema hidráulico','Modelo matemático','Resultados experimentales','Escenarios','Validación y ajuste','Decisión','Fuentes y reproducción']

@st.cache_data(max_entries=64)
def calculate(run,window,name,parameters,mode,initial,step):
    f=load_run(run,window);config=replace(calibrated_config(name),parameters=parameters,mode=mode)
    y=run_simulation(f,config,initial,step)
    comparison=compare_scenarios(f,config,step,initial) if name==U else None
    return f,y,prediction_metrics(f,y,config),comparison

@st.cache_data(max_entries=8)
def scientific_csv(name):return pd.read_csv(ROOT/'reports/optimizacion_precision'/name)

def chart(frame,columns,title,unit,key,reference=None):
    series=[dict(name=c,type='line',showSymbol=False,encode=dict(x='t',y=c),lineStyle=dict(width=2)) for c in columns]
    if reference is not None:
        series[0]['markLine']=dict(symbol='none',data=[dict(yAxis=reference,name='Referencia')],lineStyle=dict(type='dashed',color='#889aa5'))
    st.echarts_chart(dict(title=dict(text=title,textStyle=dict(fontSize=14)),
        tooltip=dict(trigger='axis'),legend=dict(top=30),grid=dict(top=68,bottom=55,left=60,right=20),
        dataset=dict(source=frame[['t']+columns]),xAxis=dict(type='value',name='Tiempo (s)'),
        yAxis=dict(type='value',name=unit,scale=True),dataZoom=[dict(type='inside'),dict(type='slider',height=16,bottom=8)],
        series=series),height=290,key=key,alt=title)

def data_table(f,label):
    st.dataframe(f,hide_index=True,width='stretch',alt=label)

def restore_copy(name,rid,names):
    st.session_state.overrides.pop(name,None);st.session_state.initials.pop((rid,name),None)
    for parameter in names:st.session_state.pop(f'param_{name}_{parameter}',None)
    for j in [1,2]:st.session_state.pop(f'initial{j}_{rid}_{name}',None)

if 'overrides' not in st.session_state:st.session_state.overrides={}
if 'initials' not in st.session_state:st.session_state.initials={}
with st.sidebar:
    st.caption('MODELADO Y SIMULACIÓN')
    st.header('CEFET-MG')
    page=st.radio('Secciones',SECTIONS,index=1,key='section')
    st.divider()
    run=st.selectbox('Corrida experimental',range(1,11),index=7,key='run')
    window=st.selectbox('Horizonte registrado',['excitacion'] if run==10 else ['excitacion','completa'],
                        format_func=lambda v:'Excitación · ≈800 s' if v=='excitacion' else 'Con recuperación · ≈1700 s',key='window')
    model=st.selectbox('Modelo',MODELS,format_func=lambda n:LABELS[n],key='model')
    step=st.selectbox('Paso RK4 máximo (s)',[.5,1.,2.,4.],index=1,key='step')
    explore=st.toggle('Modo exploratorio',key='explore')
    st.caption('La reproducción visual no modifica el tiempo de integración. Datos publicados, sin mediciones en vivo.')

base=calibrated_config(model)
parameters=st.session_state.overrides.get(model,base.parameters) if explore else base.parameters
config=replace(exploratory_config(base,parameters),mode='exploratorio' if explore else 'calibrado')
initial=st.session_state.initials.get((run,model)) if explore else None
st.caption('CEFET-MG / LABORATORIO DE SEÑALES Y SISTEMAS / ANÁLISIS ACADÉMICO')
st.title('Simulador de tanques acoplados')
st.markdown('Dos niveles de agua, una entrada de bomba y un modelo continuo que se contrasta con registros experimentales.')
with st.container(horizontal=True):
    st.badge('Exploración · parámetros o condiciones editables' if explore else 'Configuración calibrada · evaluación interna',icon=':material/science:')
    st.caption(f'{LABELS[model]} · corrida {run} · RK4 ≤ {step:g} s')

try:
    observed,simulation,errors,comparison=calculate(run,window,model,parameters,config.mode,initial,step)
except ValueError as exc:
    st.error(str(exc),title='Configuración fuera del dominio permitido');st.stop()

if page=='Proyecto':
    st.header('Reproducir antes de decidir')
    st.markdown('**Pregunta:** ¿cómo afectan las variaciones de bomba a ambos niveles y qué modificación reduce sus desviaciones respecto a 47,4 y 31,2 cm?')
    st.markdown('El sistema físico pertenece a CEFET-MG, Divinópolis, Brasil. Sus investigadores publicaron niveles y entrada de bomba. La pareja desarrolla el modelo y reutiliza esas mediciones; no construyó ni midió el montaje.')
    st.info('El docente aceptó usar los datos externos, según la autorización comunicada por los estudiantes en esta fase. La topología hidráulica detallada y las áreas siguen sin estar identificadas.')
    st.subheader('Alcance de la evidencia')
    st.markdown('Diez repeticiones comparten una señal de entrada. Las 30 variantes se investigaron sobre registros ya examinados. La evaluación es interna; no acredita generalización a señales nuevas ni arranque desde niveles bajos.')
    st.link_button('Consultar el dataset oficial','https://zenodo.org/records/19856119')

elif page=='Sistema hidráulico':
    scenario=st.segmented_control('Trayectoria',list(SCENARIOS),default='E0',format_func=lambda x:f'{x} · {SCENARIOS[x]}',key='scenario') or 'E0'
    if scenario!='E0' and comparison is None:
        st.info('E1 y E2 se comparan con el modelo U. Selecciona U en la barra lateral.');scenario='E0'
    trajectory=comparison[0][scenario] if comparison else simulation
    st.caption('E0: entrada observada y respuesta simulada.' if scenario=='E0' else f'{scenario}: entrada hipotética y respuesta contrafactual simulada; no ensayada físicamente.')
    tank_view(trajectory,f'{scenario} · corrida {run} · '+('exploratorio' if explore else 'parámetros calibrados'),key='tank_scene')
    with st.container(horizontal=True):
        st.metric('h1 final',f'{trajectory.h1.iloc[-1]:.3f} cm')
        st.metric('h2 final',f'{trajectory.h2.iloc[-1]:.3f} cm')
        st.metric('Duración registrada',f'{trajectory.t.iloc[-1]:.2f} s')
    st.caption('Los controles reproducen exclusivamente estados calculados. Las curvas pequeñas y el cursor comparten esos mismos tiempos. La bomba muestra la entrada aplicada tras el desfase; su historia inicial es 50%.')
    st.download_button('Descargar trayectoria calculada',trajectory.to_csv(index=False),'trayectoria.csv','text/csv',key='download_trajectory')

elif page=='Modelo matemático':
    st.header('Balances locales de U')
    st.caption('Ecuaciones exactas: src/precision_models.py, código 15. Coeficientes efectivos; sin áreas ni caudales absolutos inventados.')
    st.latex(r'\dot h_1=q_{in}-q_{12},\qquad \dot h_2=r(q_{12}-q_{out})')
    st.latex(r'q_{12}=\max(0,q_*+k_{12}[(h_1-h_2)-16.2]),\quad q_{out}=\max(0,q_*+k_{out}(h_2-31.2))')
    st.latex(r'z=u(t-\delta)/100,\quad F(z)=z+(b-1)z^2+\frac{1-2b+c}{3}z^3')
    st.latex(r'q_{in}=\max\left(0,q_*\frac{F(z)}{F(0.5)}-k_{pump}(h_1-47.4)\right),\quad\delta=2\;s')
    st.markdown('h en cm, t en s; q=Q/A₁ en cm/s, r=A₁/A₂; conductancias k en s⁻¹; b y c adimensionales. Antes del inicio, u=50%. El desfase es efectivo y no un retardo físico certificado.')
    data_table(pd.DataFrame(dict(parámetro=base.names,calibrado=base.parameters,activo=parameters)),'Parámetros calibrados y activos del modelo seleccionado')
    if model!=U:st.info('La tabla corresponde al modelo seleccionado; las ecuaciones expuestas arriba son las de U. Las formulaciones C/D/P están documentadas en los informes científicos.')
    if explore:
        from src.precision_models import SPECS
        from src.models import specification
        if model in (U,P):lo,hi=SPECS[model.split('__')[0]].lo,SPECS[model.split('__')[0]].hi
        else:_,lo,hi,_=specification(2 if model=='C_bomba' else 3)
        with st.form('parameter_form'):
            st.subheader('Modificar una copia de parámetros')
            new=[]
            for name,value,lower,upper in zip(base.names,parameters,lo,hi):
                new.append(st.number_input(name,min_value=float(lower),max_value=float(upper),value=float(value),format='%.8f',key=f'param_{model}_{name}'))
            cols=st.columns(2)
            h1=cols[0].number_input('h1 inicial (cm)',min_value=0.,value=float((initial or tuple(observed[['h1','h2']].iloc[0]))[0]),key=f'initial1_{run}_{model}')
            h2=cols[1].number_input('h2 inicial (cm)',min_value=0.,value=float((initial or tuple(observed[['h1','h2']].iloc[0]))[1]),key=f'initial2_{run}_{model}')
            if st.form_submit_button('Aplicar exploración',key='apply_parameters'):
                st.session_state.overrides[model]=tuple(new);st.session_state.initials[(run,model)]=(h1,h2);st.rerun()
        st.button('Restaurar copia calibrada',key='restore_parameters',on_click=restore_copy,args=(model,run,base.names))
    else:st.caption('Activa «Modo exploratorio» para editar una copia. Los archivos calibrados permanecen intactos.')
    st.warning('El balance d(h1+h2/r)/dt=qin−qout es efectivo. No demuestra conservación volumétrica global certificada ni validez de la linealización fuera del régimen evaluado.')

elif page=='Resultados experimentales':
    st.header('Observado frente a calculado')
    st.caption(f'Métricas calculadas para esta corrida y ventana. Escalas de entrenamiento: {base.scale[0]:.6f} y {base.scale[1]:.6f} cm. '+('Resultados exploratorios, sin distintivo de validación original.' if explore else 'No son precisión universal ni evaluación externa nueva.'))
    data_table(errors,'Errores de predicción de la corrida y ventana seleccionadas; MAE y RMSE en cm')
    for c,ref in zip(['h1','h2'],REFERENCES):
        frame=pd.DataFrame(dict(t=observed.t,Observado=observed[c],Simulado=simulation[c]))
        chart(frame,['Observado','Simulado'],f'{c} · corrida {run} · {window}','Nivel (cm)',f'observed_{c}',ref)
    chart(pd.DataFrame(dict(t=simulation.t,Registrada=simulation.u_command,Aplicada=simulation.u_applied)),['Registrada','Aplicada'],'Mando y entrada tras el desfase','Bomba (%)','input_chart')
    residual=pd.DataFrame(dict(t=simulation.t,h1=simulation.h1-observed.h1,h2=simulation.h2-observed.h2))
    chart(residual,['h1','h2'],'Residuos · simulado menos observado','Residuo (cm)','residual_chart',0.)

elif page in ('Escenarios','Decisión'):
    st.header('Tres entradas, condiciones comparables' if page=='Escenarios' else 'Decisión calculada con indicadores')
    if comparison is None:st.info('Selecciona U para ejecutar la comparación principal.');st.stop()
    trajectories,table,decision=comparison
    st.markdown('**E0:** mando registrado. **E1:** 50 + 0,80(u₀−50). **E2:** limitación causal de cambios a 10 puntos porcentuales por 4 s, usando los intervalos reales. E1 y E2 son contrafactuales.')
    st.caption('Mismas condiciones iniciales, parámetros, marcas temporales, duración, método, paso y desfase. Bandas de análisis ±2 cm; no son límites físicos certificados.')
    columns=['scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','MAE_ref_h1_cm','MAE_ref_h2_cm','max_h1_cm','max_h2_cm','u_mean_pct','u_mean_difference_pp','TV_u_pp']
    data_table(table[columns],'Indicadores de regulación de los tres escenarios, niveles en cm y mando en porcentaje')
    st.info(decision['text'],title='Resultado de la regla de decisión')
    st.caption('Regla previa: ambos RMSE de regulación no empeoran, al menos uno mejora ≥5%, TV del mando no aumenta y diferencia de mando medio ≤5 pp. Entre elegibles: menor peor RMSE/banda. No implica dominancia total ni prueba física.')
    for c,unit,ref in [('h1','Nivel (cm)',47.4),('h2','Nivel (cm)',31.2),('u_command','Bomba (%)',None)]:
        chart(pd.DataFrame({'t':simulation.t,**{key:value[c] for key,value in trajectories.items()}}),list(SCENARIOS),f'{c} · E0 / E1 / E2',unit,f'scenarios_{c}',ref)
    data_table(table,'Todos los indicadores y diferencias porcentuales respecto a E0')
    st.download_button('Descargar comparación numérica',table.to_csv(index=False),'comparacion_escenarios.csv','text/csv',key='download_comparison')
    st.caption('Estos RMSE miden desviación del objetivo, no error predictivo frente a observaciones. Una modificación puede cambiar la media del mando y producir compensaciones entre niveles y esfuerzo.')

elif page=='Validación y ajuste':
    st.header('Qué respalda el modelo y qué queda abierto')
    st.caption('Resultados científicos históricos congelados. Independientes de los controles exploratorios de esta sesión.')
    names=[U,P,'C_bomba','D_conservativo']
    scores=scientific_csv('principal_por_tanque.csv')
    data_table(scores[scores.model.isin(names)],'Evaluación interna histórica: medias de métricas por corrida 8 a 10')
    st.markdown('NRMSE = RMSE / desviación estándar de entrenamiento. **0,14581 no es 14,58% del nivel de agua.** El umbral ≤0,30 es un criterio interno del proyecto.')
    data_table(scientific_csv('cv_por_tanque.csv').query('model in @names'),'Evaluación cruzada histórica por grupos de corridas')
    phases=scientific_csv('metricas_por_fase.csv')
    data_table(phases[phases.model.isin(names)&phases.window.isin(['excitacion','recuperacion'])],'Evaluación histórica por excitación y recuperación')
    from src.goodness_of_fit import residual_diagnostics
    acf=pd.DataFrame({'t':np.arange(21),**{c:residual_diagnostics((simulation[c]-observed[c]).values)['acf'] for c in ['h1','h2']}})
    st.caption('ACF de los residuos de la corrida seleccionada'+(' en exploración.' if explore else ' con configuración calibrada.'))
    st.echarts_chart(dict(tooltip=dict(trigger='axis'),legend={},dataset=dict(source=acf.rename(columns={'t':'Retardo'})),
        xAxis=dict(type='value',name='Retardo (muestras ≈4 s)'),yAxis=dict(type='value',name='ACF'),
        series=[dict(type='line',name=c,encode=dict(x='Retardo',y=c)) for c in ['h1','h2']]),height=280,key='acf',alt='Autocorrelación de residuos de ambos tanques')
    st.warning('Persisten sesgos y autocorrelación. El arranque en frío y la predicción tardía de h2 al calibrar sólo 320 s siguen limitados. Una señal repetida no valida nuevas entradas.')

elif page=='Fuentes y reproducción':
    st.header('Evidencia trazable')
    st.markdown('Silva, Guilherme; Coelho, Marcela; Leite, Valter. **D-Stabilization of a Coupled-Tank System Using Experimental Data**, Zenodo, v1.0.0, 2026. [DOI 10.5281/zenodo.19856119](https://doi.org/10.5281/zenodo.19856119).')
    st.markdown('Mediciones: investigadores de CEFET-MG. Modelado y escenarios: trabajo académico de la pareja. No se dispone de fotografías propias, áreas, planos precisos ni exactitud certificada de los sensores.')
    st.code('python -m src.simulator_delivery\npython -m pytest -q tests\npython -m streamlit run app.py',language='powershell')
    st.markdown('Documentación: docs/protocolo_escenarios.md; docs/anexos_proyecto.md; docs/evidencias_13_diapositivas.md. Informes y resultados de esta etapa: reports/simulador/.')
    st.caption('No se ha aportado una URL de repositorio remoto. El proyecto y sus versiones de dependencias se entregan en esta carpeta.')
    st.download_button('Descargar configuración activa',json.dumps(dict(model=model,parameters=dict(zip(base.names,parameters)),step=step,delay=config.delay,mode=config.mode,run=run,window=window),indent=2),
                       'configuracion.json','application/json',key='download_config')
