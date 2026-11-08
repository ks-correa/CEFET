"""Tres escenarios, métricas y regla de decisión congelada en docs/protocolo_escenarios.md."""
import numpy as np
import pandas as pd
from .simulation_engine import calibrated_config,run_simulation,REFERENCES,U

SCENARIOS={'E0':'Base experimental','E1':'Modulación atenuada','E2':'Modulación suavizada'}

def transform_input(t,u,scenario):
    t,u=np.asarray(t,dtype=float),np.asarray(u,dtype=float)
    if scenario=='E0':return u.copy()
    if scenario=='E1':return 50+.8*(u-50)
    if scenario!='E2':raise ValueError('Escenario no disponible')
    result=np.empty_like(u);last=50.
    for i in range(len(u)):
        limit=10. if i==0 else 2.5*(t[i]-t[i-1])
        last+=np.clip(u[i]-last,-limit,limit);result[i]=last
    return result

def time_average(t,y):return float(np.trapezoid(y,t)/(t[-1]-t[0]))

def regulation_indicators(f,band=2.):
    t=f.t.values;duration=t[-1]-t[0];row={'duration_s':float(duration)}
    for c,ref in zip(['h1','h2'],REFERENCES):
        y=f[c].values;e=y-ref;mean=time_average(t,y)
        row.update({f'RMSE_ref_{c}_cm':np.sqrt(time_average(t,e**2)),
                    f'MAE_ref_{c}_cm':time_average(t,abs(e)),f'max_deviation_{c}_cm':float(np.max(abs(e))),
                    f'max_{c}_cm':float(y.max()),f'std_{c}_cm':np.sqrt(time_average(t,(y-mean)**2)),
                    f'TV_{c}_cm':float(abs(np.diff(y)).sum())})
        # Tiempo por segmentos lineales entre estados, con cruces exactos de la banda.
        inside=0.
        for a,b,dt in zip(e[:-1],e[1:],np.diff(t)):
            cuts=[0.,1.]
            if b!=a:
                cuts += [x for level in [-band,band] if 0<(x:=(level-a)/(b-a))<1]
            cuts=sorted(cuts)
            inside+=sum((r-l)*dt for l,r in zip(cuts[:-1],cuts[1:]) if abs(a+(b-a)*(l+r)/2)<=band)
        row[f'inside_{c}_s']=inside;row[f'outside_{c}_s']=duration-inside
    dt=np.diff(t);u=f.u_command.values;mean=float(np.sum(u[:-1]*dt)/duration)
    row.update(u_mean_pct=mean,u_std_pp=float(np.sqrt(np.sum((u[:-1]-mean)**2*dt)/duration)),
               TV_u_pp=float(abs(u[0]-50)+abs(np.diff(u[:-1])).sum()),
               effort_pp2_s=float(np.sum((u[:-1]-50)**2*dt)),
               applied_u_mean_pct=float(f.attrs.get('applied_u_mean_pct',np.sum(f.u_applied.values[:-1]*dt)/duration)))
    return row

def compare_scenarios(observed,config=None,step=1.,initial=None):
    config=calibrated_config() if config is None else config
    if config.name!=U:raise ValueError('Los escenarios principales comparten el modelo U')
    trajectories={};rows=[]
    for code in SCENARIOS:
        frame=observed.copy();frame['u']=transform_input(frame.t,frame.u,code)
        result=run_simulation(frame,config,initial,step);trajectories[code]=result
        rows.append(dict(scenario=code,**regulation_indicators(result)))
    table=pd.DataFrame(rows)
    for col in ['RMSE_ref_h1_cm','RMSE_ref_h2_cm','TV_u_pp','u_mean_pct']:
        base=table.loc[0,col];table[col+'_change_pct']=100*(table[col]/base-1) if abs(base)>1e-12 else np.nan
    table['u_mean_difference_pp']=table.u_mean_pct-table.u_mean_pct.iloc[0]
    return trajectories,table,decide(table)

def decide(table):
    base=table.set_index('scenario').loc['E0'];eligible=[]
    for _,row in table.iterrows():
        if row.scenario=='E0':continue
        ratios=[row[f'RMSE_ref_{c}_cm']/base[f'RMSE_ref_{c}_cm'] for c in ['h1','h2']]
        if max(ratios)<=1+1e-9 and min(ratios)<=.95 and row.TV_u_pp<=base.TV_u_pp+1e-9 and abs(row.u_mean_pct-base.u_mean_pct)<=5:
            eligible.append(row)
    if not eligible:return dict(recommended=None,text='Ninguna alternativa cumple la regla: conservar E0 como referencia y explicar las compensaciones.')
    best=min(eligible,key=lambda row:(max(row.RMSE_ref_h1_cm/2,row.RMSE_ref_h2_cm/2),row.TV_u_pp))
    return dict(recommended=best.scenario,text=f'{best.scenario} cumple la regla local: no empeora los RMSE de regulación, mejora al menos uno ≥5%, no aumenta TV del mando y cambia su media ≤5 pp. No equivale a dominancia en todos los indicadores ni a prueba física.')
