"""Fachada científica única. Reutiliza integradores contrastados, sin recalibrar."""
from dataclasses import dataclass,replace
import json
import numpy as np
import pandas as pd
from .data_processing import ROOT
from .precision_models import SPECS,event_grid,integrate_grid,hydraulic,pump,rhs
from .models import specification,fluxes as old_fluxes,rhs as old_rhs
from .rk4_solver import solve as old_solve
from .goodness_of_fit import metrics

U='U_bomba_carga_monotona__retardo'
P='P_D_bomba_monotona__retardo'
MODELS=(U,'C_bomba','D_conservativo',P)
REFERENCES=(47.4,31.2)
ALLOWED_STEPS=(.5,1.,2.,4.)

@dataclass(frozen=True)
class ModelConfig:
    name:str
    parameters:tuple
    names:tuple
    scale:tuple
    delay:float=0.
    tau:float=0.
    mode:str='calibrado'

def calibrated_config(name=U):
    if name not in MODELS:raise ValueError('Modelo no disponible')
    path=ROOT/'reports/optimizacion_precision/all_fits.json'
    l=json.loads(path.read_text(encoding='utf-8'))[name]['principal']
    return ModelConfig(name,tuple(l['parameters'].values()),tuple(l['parameters']),tuple(l['scale_cm']),
                       float(l.get('delay',0.)),float(l.get('tau',0.)))

def exploratory_config(config,parameters):
    p=tuple(float(x) for x in parameters)
    result=replace(config,parameters=p,mode='exploratorio' if p!=calibrated_config(config.name).parameters else 'calibrado')
    validate_config(result)
    return result

def validate_config(config):
    if config.name not in MODELS:raise ValueError('Modelo no disponible')
    if config.name in (U,P):
        spec=SPECS[config.name.split('__')[0]];lo,hi=spec.lo,spec.hi
    else:_,lo,hi,_=specification(2 if config.name=='C_bomba' else 3)
    p=np.asarray(config.parameters)
    if len(p)!=len(lo) or not np.isfinite(p).all() or np.any(p<lo) or np.any(p>hi):
        raise ValueError('Parámetros fuera de las cotas de identificación')
    if config.delay<0 or config.tau<0:raise ValueError('Dinámica no causal')

def load_run(run=8,window='excitacion'):
    if run not in range(1,11):raise ValueError('Corrida entre 1 y 10')
    f=pd.read_csv(ROOT/f'data/processed/run_{run:02}.csv')
    if window=='excitacion':return f.iloc[:201].copy()
    if window!='completa':raise ValueError('Ventana no reconocida')
    if run==10:raise ValueError('La corrida 10 no tiene recuperación registrada')
    return f.copy()

def run_simulation(frame,config=None,initial=None,step=1.,duration=None):
    config=calibrated_config() if config is None else config;validate_config(config)
    f=frame.copy()
    if duration is not None:
        if duration<=0 or duration>f.t.iloc[-1]+1e-9:raise ValueError('Duración fuera del registro disponible')
        f=f.loc[f.t<=duration].copy()
        if f.t.iloc[-1]<duration:
            row=f.iloc[-1].copy();row['t']=duration
            # Sólo extiende la entrada retenida; nunca inventa observaciones de niveles.
            row[['h1','h2']]=np.nan;f=pd.concat([f,row.to_frame().T],ignore_index=True)
    t=f.t.to_numpy(dtype=float);u=f.u.to_numpy(dtype=float)
    if step not in ALLOWED_STEPS:raise ValueError('Paso no verificado')
    if len(t)<2 or not np.isfinite(t).all() or np.any(np.diff(t)<=0):raise ValueError('Tiempo inválido')
    if not np.isfinite(u).all() or np.any((u<0)|(u>100)):raise ValueError('Bomba fuera de 0–100 %')
    y0=f[['h1','h2']].iloc[0].to_numpy(dtype=float) if initial is None else np.asarray(initial,dtype=float)
    if y0.shape!=(2,) or not np.isfinite(y0).all() or np.any(y0<0):raise ValueError('Condición inicial inválida')
    p=np.asarray(config.parameters)
    out=pd.DataFrame(dict(t=t,u_command=u))
    if config.name in (U,P):
        code=SPECS[config.name.split('__')[0]].code
        grid,controls,idx=event_grid(t,u,config.delay,pre=50.)
        applied_mean=float(np.sum(controls[:-1]*np.diff(grid))/(t[-1]-t[0]))
        full=integrate_grid(grid,controls,y0,p,code,float(step),config.tau)
        y=full[idx,:2];applied=controls[idx]
        fl=np.array([hydraulic(v,p,code) for v in full[idx]])
        qin=np.array([pump(float(v),p,code) for v in applied])
        if config.name==U:qin=np.maximum(0.,qin-p[4]*(y[:,0]-47.4))
        if config.tau>0:qin=full[idx,2]
        deriv=np.array([rhs(v,float(c),p,code,config.tau)[:2] for v,c in zip(full[idx],applied)])
        out[['qin','q12','qout']]=np.column_stack([qin,fl])
        out['balance_h1']=deriv[:,0]-(qin-fl[:,0])
        out['balance_h2']=deriv[:,1]/p[1]-(fl[:,0]-fl[:,1])
        out['balance_total']=deriv[:,0]+deriv[:,1]/p[1]-(qin-fl[:,1])
    else:
        mid=2 if config.name=='C_bomba' else 3
        applied_mean=float(np.sum(u[:-1]*np.diff(t))/(t[-1]-t[0]))
        y=old_solve(t,u,y0,p,mid,step);applied=u
        deriv=np.array([old_rhs(v,float(c),p,mid) for v,c in zip(y,u)])
        fl=old_fluxes(y,u,p,mid);out[['qin','q12','qout']]=fl
        if mid==3:
            out['balance_h1']=deriv[:,0]-(fl[:,0]-fl[:,1])
            out['balance_h2']=deriv[:,1]/p[1]-(fl[:,1]-fl[:,2])
            out['balance_total']=out.balance_h1+out.balance_h2
        else:out[['balance_h1','balance_h2','balance_total']]=np.nan
    if not np.isfinite(y).all() or np.any(y<0):raise ValueError('Trayectoria no finita o negativa: reducir cambios exploratorios')
    out[['h1','h2']]=y;out[['dh1_dt','dh2_dt']]=deriv;out['u_applied']=applied
    original=calibrated_config(config.name)
    mode='calibrado' if (config.mode=='calibrado' and config.parameters==original.parameters and config.delay==original.delay
                        and config.tau==original.tau and np.array_equal(y0,f[['h1','h2']].iloc[0].to_numpy(dtype=float))) else 'exploratorio'
    out.attrs.update(model=config.name,mode=mode,step=step,delay=config.delay,parameters=config.parameters,applied_u_mean_pct=applied_mean,
                     initial=tuple(y0),flow_units='cm/s = Q/A1, no litros/s')
    return out

def prediction_metrics(observed,prediction,config):
    if len(observed)!=len(prediction) or not np.allclose(observed.t,prediction.t,atol=1e-9):
        raise ValueError('Observaciones y predicciones no alineadas')
    return pd.DataFrame([dict(tank=c,**metrics(observed[c].values,prediction[c].values,config.scale[j]))
                         for j,c in enumerate(['h1','h2'])])
