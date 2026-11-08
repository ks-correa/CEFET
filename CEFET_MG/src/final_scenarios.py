"""Escenarios vigentes. El módulo histórico src.scenarios permanece intacto."""
import numpy as np
import pandas as pd
from .scenarios import transform_input as historical_input,regulation_indicators,decide
from .simulation_engine import U,calibrated_config,run_simulation

SCENARIOS={'E0':'Referencia experimental','E1':'Atenuación alrededor de 50%','E2':'Operación constante al 50%'}
MAPPING={'E0':'E0 histórico','E1':'E1 histórico','E2':'D50 diagnóstico','S_HIST':'E2 histórico (suavizado)'}

def transform_input(t,u,scenario):
    if scenario=='E2':return np.full(len(u),50.,dtype=float)
    if scenario=='S_HIST':return historical_input(t,u,'E2')
    if scenario in ('E0','E1'):return historical_input(t,u,scenario)
    raise ValueError('Escenario vigente no disponible')

def compare_scenarios(observed,config=None,step=1.,initial=None,disturbance=None):
    config=calibrated_config() if config is None else config
    if config.name!=U:raise ValueError('La comparación principal vigente usa U')
    trajectories={};rows=[]
    d=np.zeros(len(observed)) if disturbance is None else np.asarray(disturbance,dtype=float)
    if d.shape!=(len(observed),) or not np.isfinite(d).all():raise ValueError('Perturbación inválida')
    for code in SCENARIOS:
        f=observed.copy();command=transform_input(f.t,f.u,code);f['u']=np.clip(command+d,0,100)
        trajectory=run_simulation(f,config,initial,step);trajectories[code]=trajectory
        rows.append(dict(scenario=code,**regulation_indicators(trajectory),
                         saturation_samples=int(np.sum(command+d!=f.u.values))))
    table=pd.DataFrame(rows)
    for col in ['RMSE_ref_h1_cm','RMSE_ref_h2_cm','TV_u_pp','u_mean_pct']:
        base=table.loc[0,col];table[col+'_change_pct']=100*(table[col]/base-1) if abs(base)>1e-12 else np.nan
    table['u_mean_difference_pp']=table.u_mean_pct-table.u_mean_pct.iloc[0]
    verdict=decide(table)
    verdict['text']+=' Revisión de escenarios posterior al diagnóstico; la regla no se modificó.'
    if verdict['recommended']=='E2':
        verdict['text']+=' Es la mejor alternativa nominal evaluada cerca del equilibrio, sin demandas externas documentadas; no implica óptimo global, ahorro eléctrico ni ensayo físico.'
    return trajectories,table,verdict

def smoothing_complement(observed,config=None,step=1.,initial=None):
    config=calibrated_config() if config is None else config
    f=observed.copy();f['u']=transform_input(f.t,f.u,'S_HIST')
    y=run_simulation(f,config,initial,step)
    return y,pd.DataFrame([dict(scenario='S_HIST',**regulation_indicators(y))])
