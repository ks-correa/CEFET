"""Ejecutar desde raíz: python -m src.experiments."""
import json,sys,platform,importlib.metadata,time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from .data_processing import ROOT,audit
from .models import NAMES,HOP,rhs,fluxes
from .rk4_solver import solve
from .calibration import calibrate
from .validation import predict,evaluate,split_groups
from .goodness_of_fit import residual_diagnostics

def write_json(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

def main():
    started=time.time(); out=ROOT/'reports'; out.mkdir(exist_ok=True)
    figs=out/'figures'; figs.mkdir(exist_ok=True)
    ds,runs,stats,mapping=audit()
    versions={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','matplotlib','numba','pytest']}
    write_json(out/'environment.json',dict(python=sys.version,platform=platform.platform(),packages=versions))
    (ROOT/'requirements.txt').write_text('\n'.join(f'{p}=={v}' for p,v in versions.items())+'\n',encoding='utf-8')
    fig,axes=plt.subplots(3,1,figsize=(12,8),sharex=True)
    for c,ax in zip(['h1','h2','u'],axes):
        ax.plot(ds['complete_data'].t,ds['complete_data'][c],lw=.7)
        ax.set_ylabel(c+(' (%)' if c=='u' else ' (cm)')); ax.grid(alpha=.3)
    axes[0].set_title('Captura experimental completa CEFET-MG | 0–18004 s | sin modelo')
    axes[-1].set_xlabel('Tiempo absoluto (s)'); fig.tight_layout(); fig.savefig(figs/'exploracion.png'); plt.close(fig)
    rows=[]; logs={}; fits={}; predictions={}
    train,test=split_groups(runs,list(range(1,8)),[8,9,10])
    for model,name in enumerate(NAMES):
        print('Principal',name,flush=True)
        p,scale,log=calibrate(train,model); fits[model]=(p,scale); logs[name]={'principal':log}
        for rid,f in enumerate(runs,1):
            yp=predict(f,p,model); predictions[model,rid]=yp
            for window,mask in [('completa',np.ones(len(f),bool)),('inicial_320',f.t<=320.01),
                                ('tardia_320',f.t>320.01),('excitacion',f.t<=800.01),('recuperacion',f.t>800.01)]:
                if mask.sum()<2: continue
                rows+=evaluate(f.loc[mask],yp[mask],scale,protocol='principal',model=name,
                               run=rid,role='desarrollo' if rid<=7 else 'evaluacion',window=window)
            fl=fluxes(yp,f.u.values,p,model)
            saved=f[['t','t_absolute','source_row','h1','h2','u']].copy()
            saved[['h1_sim','h2_sim']]=yp; saved[['Qin_A1','Q12_A1','Qout_A1']]=fl
            if model in (1,3):
                deriv=np.array([rhs(y,float(u),p,model) for y,u in zip(yp,f.u)])
                saved['balance_effective_cm_s']=deriv[:,0]+deriv[:,1]/p[1]-(fl[:,0]-fl[:,2])
            saved.to_csv(out/f'prediction_{name}_{rid:02}.csv',index=False)
        # Evaluación cruzada: no cambia parámetros del ajuste principal.
        logs[name]['cv']={}
        for fold in range(5):
            testids=[2*fold+1,2*fold+2]; trainids=[i for i in range(1,11) if i not in testids]
            tr,te=split_groups(runs,trainids,testids)
            cp,cs,cl=calibrate(tr,model,starts=4); logs[name]['cv'][str(fold)]=cl
            for rid,f in zip(testids,te):
                yp=predict(f,cp,model)
                for window,mask in [('completa',np.ones(len(f),bool)),('excitacion',f.t<=800.01)]:
                    rows+=evaluate(f.loc[mask],yp[mask],cs,protocol='cv',model=name,run=rid,
                                   role='evaluacion',window=window,fold=fold)
        print('Temporal',name,flush=True)
        tp,ts,tl=calibrate([f.loc[f.t<=320.01].copy() for f in train],model)
        logs[name]['temporal']=tl
        for rid,f in zip([8,9,10],test):
            yp=predict(f,tp,model); mask=f.t>320.01
            rows+=evaluate(f.loc[mask],yp[mask],ts,protocol='temporal',model=name,run=rid,
                           role='evaluacion',window='tardia_320')
        startup=ds['complete_data'].iloc[:mapping[0]['start_row']+1]
        rows+=evaluate(startup,predict(startup,p,model),scale,protocol='arranque',model=name,
                       run=0,role='extrapolacion',window='completa')
    # Referencias causales: ninguna incorpora observaciones futuras.
    scale=fits[0][1]
    for rid,f in enumerate(runs,1):
        for name,level in [('persistencia',f[['h1','h2']].iloc[0].values),('equilibrio',HOP)]:
            yp=np.tile(level,(len(f),1))
            for window,mask in [('completa',np.ones(len(f),bool)),('excitacion',f.t<=800.01)]:
                rows+=evaluate(f.loc[mask],yp[mask],scale,protocol='principal',model=name,run=rid,
                               role='desarrollo' if rid<=7 else 'evaluacion',window=window)
    results=pd.DataFrame(rows); results.to_csv(out/'metrics.csv',index=False)
    write_json(out/'calibration.json',logs)
    # Resultado por grupos: no ponderar como independientes las series repetidas.
    summary=results.groupby(['protocol','model','role','window','tank'])[['MAE','RMSE','NRMSE','bias']].mean()
    summary.to_csv(out/'metrics_summary.csv')
    cv=results.query("protocol=='cv' and window=='completa'").groupby('model').NRMSE.mean().sort_values()
    selected=cv.index[0]; mid=NAMES.index(selected); p,scale=fits[mid]
    # Selección descriptiva por CV; si todos fallan no se declara modelo aceptado.
    write_json(out/'selected_model.json',dict(model=selected,parameters=p.tolist(),scale_cm=scale.tolist(),
                selection='menor NRMSE medio CV, sólo candidato diagnóstico si falla el umbral'))
    convergence=[]
    for rid in [8,9,10]:
        f=runs[rid-1]; ref=predict(f,p,mid)
        for step in [4.,2.,1.,.5]:
            yp=solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,mid,step)
            convergence.append(dict(run=rid,step=step,max_vs_step1_cm=float(np.max(abs(yp-ref)))))
        z=f[['h1','h2']].iloc[0].values; reference=[z.copy()]
        for i in range(len(f)-1):
            sol=solve_ivp(lambda t,y:rhs(y,float(f.u.iloc[i]),p,mid),[f.t.iloc[i],f.t.iloc[i+1]],z,
                          method='DOP853',rtol=1e-11,atol=1e-12)
            z=sol.y[:,-1]; reference.append(z.copy())
        convergence.append(dict(run=rid,step='SciPy_DOP853',max_vs_step1_cm=float(np.max(abs(np.array(reference)-ref)))))
    pd.DataFrame(convergence).to_csv(out/'convergence.csv',index=False)
    diagnostics={}
    for rid in [8,9,10]:
        f=runs[rid-1]; yp=predictions[mid,rid]; err=yp-f[['h1','h2']].values
        fig,ax=plt.subplots(4,1,figsize=(12,10),sharex=True)
        for j,c in enumerate(['h1','h2']):
            ax[j].plot(f.t,f[c],label='Experimental observado',lw=1)
            ax[j].plot(f.t,yp[:,j],label='Simulación libre',lw=1)
            ax[j].set_ylabel(c+' (cm)'); ax[j].legend()
        ax[2].step(f.t,f.u,where='post'); ax[2].set_ylabel('Bomba (%)')
        ax[3].plot(f.t,err[:,0],label='h1'); ax[3].plot(f.t,err[:,1],label='h2')
        ax[3].set_ylabel('Simulado−real (cm)'); ax[3].legend(); ax[3].set_xlabel('Tiempo desde inicio (s)')
        ax[0].set_title(f'{selected} | corrida {rid} | 0–{f.t.iloc[-1]:.0f} s | evaluación interna')
        for a in ax:a.grid(alpha=.3)
        fig.tight_layout(); fig.savefig(figs/f'trajectory_{rid}.png'); plt.close(fig)
        fig,ax=plt.subplots(2,3,figsize=(13,7))
        diagnostics[str(rid)]={}
        for j,c in enumerate(['h1','h2']):
            dd=residual_diagnostics(err[:,j]); diagnostics[str(rid)][c]=dd
            ax[j,0].scatter(yp[:,j],err[:,j],s=5); ax[j,0].set_xlabel('Nivel simulado (cm)'); ax[j,0].set_ylabel('Residuo (cm)')
            ax[j,1].hist(err[:,j],bins=25,density=True); ax[j,1].set_xlabel('Residuo (cm)'); ax[j,1].set_ylabel('Densidad (1/cm)')
            ax[j,2].stem(range(21),dd['acf']); ax[j,2].set_xlabel('Retardo (muestras ≈4 s)'); ax[j,2].set_ylabel('ACF')
            for k in range(3):ax[j,k].set_title(c)
        fig.suptitle(f'Residuos {selected} | corrida {rid} | 0–{f.t.iloc[-1]:.0f} s')
        fig.tight_layout(); fig.savefig(figs/f'residuals_{rid}.png'); plt.close(fig)
    write_json(out/'residuals.json',diagnostics)
    ss=results.query("protocol=='principal' and role=='evaluacion' and window=='completa'")
    fig,ax=plt.subplots(1,2,figsize=(13,5))
    for a,metric in zip(ax,['RMSE','NRMSE']):
        ss.groupby(['model','tank'])[metric].mean().unstack().plot.bar(ax=a)
        a.set_ylabel(metric+(' (cm)' if metric=='RMSE' else ' (adimensional)')); a.tick_params(axis='x',rotation=30)
        a.set_title('Corridas 8–10 completas | promedio por corrida')
    fig.tight_layout(); fig.savefig(figs/'model_comparison.png'); plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,5))
    results.query("protocol=='cv' and window=='completa'").pivot_table(index='run',columns=['model','tank'],values='NRMSE').plot(ax=ax)
    ax.set_title('Evaluación cruzada interna | corridas completas | todos los modelos'); ax.set_ylabel('NRMSE'); ax.set_xlabel('Corrida reservada'); ax.axhline(.3,color='k',ls='--')
    fig.tight_layout(); fig.savefig(figs/'errors_by_run.png'); plt.close(fig)
    print(summary.to_string(),flush=True)
    write_json(out/'execution.json',dict(seconds=time.time()-started,seed=20261108))

if __name__=='__main__':main()
