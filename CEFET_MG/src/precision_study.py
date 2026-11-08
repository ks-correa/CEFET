"""python -m src.precision_study — resultados aislados en optimizacion_precision."""
import json,hashlib,time,sys,platform,importlib.metadata
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import least_squares,minimize
from .data_processing import ROOT
from .calibration import scale_for
from .models import NAMES as OLD_NAMES
from .rk4_solver import solve as old_solve
from .precision_models import SPECS,simulate
from .goodness_of_fit import metrics

OUT=ROOT/'reports/optimizacion_precision'
SEED=20261108

def dump(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')

def snapshot():
    paths=list((ROOT/'data/raw').glob('*'))
    paths+=list((ROOT/'reports').glob('*.*'))
    paths+=list((ROOT/'reports/figures').glob('*'))
    paths+=list((ROOT/'data/processed').glob('*'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}

def get_data():
    return [pd.read_csv(ROOT/f'data/processed/run_{i:02}.csv') for i in range(1,11)]

def residual_function(runs,name,scale,delay=0.,tau=0.):
    def fun(p):
        return np.concatenate([(simulate(f,p,name,delay=delay,tau=tau)-f[['h1','h2']].values)[1:]/scale for f in runs])
    return fun

def fit(runs,name,objective='ls',starts=4,delay=0.,tau=0.):
    s=SPECS[name]; x,lo,hi=map(np.array,(s.x,s.lo,s.hi)); scale=scale_for(runs)
    fun=residual_function(runs,name,scale,delay,tau); rng=np.random.default_rng(SEED)
    solutions=[]; logs=[]
    for k in range(starts):
        initial=np.clip(x*np.exp(rng.normal(0,.45,len(x))) if k else x,lo+1e-7,hi-1e-7)
        if 'offset_cm' in s.names and k:initial[-1]=rng.uniform(-5,5)
        sol=least_squares(lambda p:fun(p).ravel(),initial,bounds=(lo,hi),x_scale='jac',
                          max_nfev=400,ftol=1e-9,gtol=1e-9,xtol=1e-9)
        logs.append(dict(initial=initial.tolist(),p=sol.x.tolist(),cost=float(sol.cost),
                         success=bool(sol.success),nfev=sol.nfev,message=sol.message,optimality=float(sol.optimality)))
        solutions.append(sol)
    best=min(solutions,key=lambda z:z.cost); p=best.x.copy(); ls_anchor=p.copy()
    optimizer=None
    if objective!='ls':
        unit=np.maximum(abs(p),.1); n=len(p); z0=np.r_[p/unit,np.max(np.mean(fun(p)**2,axis=0))]
        def penalty(v):
            if objective!='regularizado':return 0.
            positive=lo>0
            return 1e-4*np.mean(np.log(np.maximum(v[:n][positive]*unit[positive],1e-12)/ls_anchor[positive])**2)
        sol=minimize(lambda v:v[-1]+penalty(v),z0,method='SLSQP',
                     bounds=list(zip(lo/unit,hi/unit))+[(0.,None)],
                     constraints=[dict(type='ineq',fun=lambda v:v[-1]-np.mean(fun(v[:n]*unit)**2,axis=0))],
                     options=dict(maxiter=350,ftol=1e-10))
        p=sol.x[:n]*unit
        optimizer=dict(success=bool(sol.success),message=sol.message,iterations=sol.nit,
                       criterion=float(sol.fun),constraint_slack=(sol.x[-1]-np.mean(fun(p)**2,axis=0)).tolist())
    # Jacobiano del residuo original en el óptimo elegido, incluidos límites unilaterales.
    base=fun(p).ravel(); jac=[]
    for j in range(len(p)):
        delta=1e-5*max(abs(p[j]),.1); pp=p.copy()
        delta=min(delta,hi[j]-p[j]) if p[j]+delta<hi[j] else -min(delta,p[j]-lo[j])
        if abs(delta)<1e-12:delta=-1e-6
        pp[j]+=delta; jac.append((fun(pp).ravel()-base)/delta)
    jac=np.array(jac).T; unit=np.maximum(abs(p),.1); singular=np.linalg.svd(jac*unit,compute_uv=False)
    log=dict(p=p.tolist(),parameters=dict(zip(s.names,p.tolist())),scale_cm=scale.tolist(),
             objective=objective,delay=delay,tau=tau,starts=logs,optimizer=optimizer,
             ls_anchor=ls_anchor.tolist(),jac_singular_values=singular.tolist(),
             condition=float(singular[0]/max(singular[-1],1e-300)),
             active_bounds=[s.names[j] for j in range(len(p)) if min(p[j]-lo[j],hi[j]-p[j])<1e-5],
             train_mse_normalized=np.mean(fun(p)**2,axis=0).tolist())
    return p,scale,log

def score(f,y,scale,**labels):
    rows=[]
    windows=[('completa',np.ones(len(f),bool)),('excitacion',f.t<=800.01),
             ('recuperacion',f.t>800.01),('inicial_320',f.t<=320.01),('tardia_320',f.t>320.01)]
    for window,mask in windows:
        if mask.sum()<2:continue
        for j,c in enumerate(['h1','h2']):
            rows.append(dict(**labels,window=window,tank=c,**metrics(f[c].values[mask],y[mask,j],scale[j])))
    return rows

def run_candidate(runs,name,label=None,objective='ls',profiles=None):
    label=name if label is None else label; rows=[]; logs={}; preds=OUT/'predictions'; preds.mkdir(exist_ok=True)
    print('Ajuste',label,flush=True)
    def fitting(train):
        if profiles is None:return fit(train,name,objective)
        candidates=[]
        for delay,tau in profiles:
            p,s,l=fit(train,name,objective,starts=2,delay=delay,tau=tau)
            candidates.append((p,s,l))
        chosen=min(candidates,key=lambda item:sum(item[2]['train_mse_normalized']))
        chosen[2]['profile_costs']=[dict(delay=z[2]['delay'],tau=z[2]['tau'],mse=z[2]['train_mse_normalized']) for z in candidates]
        return chosen
    p,scale,log=fitting(runs[:7]); logs['principal']=log
    for rid,f in enumerate(runs,1):
        yp=simulate(f,p,name,delay=log['delay'],tau=log['tau'])
        rows+=score(f,yp,scale,protocol='principal',model=label,run=rid,role='desarrollo' if rid<=7 else 'evaluacion')
        saved=f[['t','h1','h2','u','source_row']].copy(); saved[['h1_sim','h2_sim']]=yp
        saved.to_csv(preds/f'{label}_{rid:02}.csv',index=False)
    logs['cv']={}
    for fold in range(5):
        held=[2*fold+1,2*fold+2]; train=[f for i,f in enumerate(runs,1) if i not in held]
        p,sc,l=fitting(train); logs['cv'][str(fold)]=l
        for rid in held:
            f=runs[rid-1]; yp=simulate(f,p,name,delay=l['delay'],tau=l['tau'])
            rows+=score(f,yp,sc,protocol='cv',model=label,run=rid,role='evaluacion',fold=fold)
    p,sc,l=fitting([f.loc[f.t<=320.01].copy() for f in runs[:7]]); logs['temporal']=l
    for rid in [8,9,10]:
        f=runs[rid-1]; yp=simulate(f,p,name,delay=l['delay'],tau=l['tau'])
        rows+=score(f,yp,sc,protocol='temporal',model=label,run=rid,role='evaluacion')
    startup=pd.read_csv(ROOT/'data/processed/startup.csv'); l=logs['principal']; p=np.array(l['p'])
    yp=simulate(startup,p,name,delay=l['delay'],tau=l['tau'])
    rows+=score(startup,yp,l['scale_cm'],protocol='arranque',model=label,run=0,role='extrapolacion')
    dump(OUT/f'fit_{label}.json',logs)
    return rows,logs

def baselines(runs):
    raw=json.loads((ROOT/'reports/calibration.json').read_text()); rows=[]; logs={}
    for name in ['C_bomba','D_conservativo']:
        model=OLD_NAMES.index(name); logs[name]=raw[name]
        for protocol in ['principal','cv','temporal']:
            for rid,f in enumerate(runs,1):
                if protocol=='temporal' and rid<8:continue
                l=raw[name]['cv'][str((rid-1)//2)] if protocol=='cv' else raw[name][protocol]
                p=np.array(list(l['parameters'].values())); scale=l['scale_cm']
                yy=old_solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,model)
                rows+=score(f,yy,scale,protocol=protocol,model=name,run=rid,
                            role='desarrollo' if protocol=='principal' and rid<8 else 'evaluacion')
        f=pd.read_csv(ROOT/'data/processed/startup.csv'); l=raw[name]['principal']; p=np.array(list(l['parameters'].values()))
        yy=old_solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,model)
        rows+=score(f,yy,l['scale_cm'],protocol='arranque',model=name,run=0,role='extrapolacion')
    return rows,logs

def main():
    OUT.mkdir(parents=True,exist_ok=True); before=snapshot(); dump(OUT/'original_manifest.json',before)
    versions={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','matplotlib','numba','pytest']}
    dump(OUT/'environment.json',dict(python=sys.version,platform=platform.platform(),packages=versions,seed=SEED))
    dump(OUT/'config.json',dict(seed=SEED,starts=4,step=1.,candidates={n:vars(s) for n,s in SPECS.items()},
                              principal_train=list(range(1,8)),principal_test=[8,9,10],
                              sigma='unique source rows ddof=1, unchanged from stage1',
                              status='Exploración de desarrollo previamente examinada'))
    runs=get_data(); rows,logs=baselines(runs); registry={}
    started=time.time()
    # Se conserva el orden histórico del cribado; la extensión se ejecuta separadamente.
    for name in list(SPECS)[:11]:
        r,l=run_candidate(runs,name); rows+=r; logs[name]=l; registry[name]=dict(base=name,objective='ls',profiles=None)
        pd.DataFrame(rows).to_csv(OUT/'metrics.csv',index=False)
    data=pd.DataFrame(rows)
    cv=data[(data.protocol=='cv')&(data.window=='completa')&data.model.isin(SPECS)]
    ranking=cv.groupby(['model','tank']).NRMSE.mean().groupby('model').max().sort_values()
    finalists=list(ranking.index[:2]); dump(OUT/'ls_ranking.json',ranking.to_dict())
    for name in finalists:
        for obj in ['minimax','regularizado']:
            label=name+'__'+obj; r,l=run_candidate(runs,name,label,obj)
            rows+=r; logs[label]=l; registry[label]=dict(base=name,objective=obj,profiles=None)
    best=finalists[0]
    # Cada ajuste de CV repite la selección del perfil con sus propios datos de entrenamiento.
    for label,profiles in [(best+'__retardo',[(v,0.) for v in [0.,.5,1.,2.,4.,8.]]),
                           (best+'__actuador',[(0.,v) for v in [0.,1.,2.,4.,8.]])]:
        r,l=run_candidate(runs,best,label,profiles=profiles)
        rows+=r; logs[label]=l; registry[label]=dict(base=best,objective='ls',profiles=profiles)
    pd.DataFrame(rows).to_csv(OUT/'metrics.csv',index=False)
    dump(OUT/'all_fits.json',logs); dump(OUT/'registry.json',registry)
    after=snapshot(); changed=[k for k,v in before.items() if after.get(k)!=v]
    dump(OUT/'integrity.json',dict(originals_unchanged=not changed,changed=changed,files_compared=len(before)))
    dump(OUT/'execution.json',dict(seconds=time.time()-started,models=len(registry)+2))
    if changed:raise RuntimeError('Se modificó la primera etapa')
    print('Estudio terminado',time.time()-started,flush=True)

if __name__=='__main__':main()
