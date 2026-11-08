"""Comprobaciones numéricas y perturbaciones, sin recalibrar con evaluación."""
import json
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from .data_processing import ROOT
from .models import NAMES,rhs,fluxes
from .rk4_solver import solve
from .goodness_of_fit import metrics,residual_diagnostics

def main():
    out=ROOT/'reports'; logs=json.loads((out/'calibration.json').read_text())
    audits=json.loads((ROOT/'data/processed/audit.json').read_text())
    rows=[]; diag={}
    for model,name in enumerate(NAMES):
        log=logs[name]['principal']; p=np.array(list(log['parameters'].values())); scale=log['scale_cm']
        for rid in [8,9,10]:
            f=pd.read_csv(ROOT/f'data/processed/run_{rid:02}.csv')
            y0=f[['h1','h2']].iloc[0].values; y=solve(f.t.values,f.u.values,y0,p,model)
            fine=solve(f.t.values,f.u.values,y0,p,model,.5)
            # DOP853 reinicia sólo su integrador, no su estado con observaciones.
            z=y0.copy(); reference=[z.copy()]
            for i in range(len(f)-1):
                sol=solve_ivp(lambda t,v:rhs(v,float(f.u.iloc[i]),p,model),[f.t.iloc[i],f.t.iloc[i+1]],z,
                              method='DOP853',rtol=1e-11,atol=1e-12)
                if not sol.success:raise RuntimeError(sol.message)
                z=sol.y[:,-1]; reference.append(z.copy())
            for step in [4.,2.,1.,.5]:
                yy=solve(f.t.values,f.u.values,y0,p,model,step)
                rows.append(dict(model=name,run=rid,test='convergencia',perturbation=step,
                                 max_state_change_cm=float(np.max(abs(yy-fine)))))
            rows.append(dict(model=name,run=rid,test='SciPy_DOP853',perturbation=0,
                             max_state_change_cm=float(np.max(abs(y-np.array(reference))))))
            for tank in range(2):
                for sign in [-1,1]:
                    pert=y0.copy(); pert[tank]+=sign*audits['quantization_cm'][f'h{tank+1}']/2
                    yp=solve(f.t.values,f.u.values,pert,p,model)
                    for j,c in enumerate(['h1','h2']):
                        rows.append(dict(model=name,run=rid,test=f'inicial_h{tank+1}',perturbation=sign,
                                         tank=c,max_state_change_cm=float(np.max(abs(yp-y))),
                                         **metrics(f[c].values,yp[:,j],scale[j])))
            # Sensibilidad local unilateral a +1% de cada parámetro, sin nuevo ajuste.
            for k,key in enumerate(log['parameters']):
                pp=p.copy(); pp[k]*=1.01; yp=solve(f.t.values,f.u.values,y0,pp,model)
                rows.append(dict(model=name,run=rid,test='parametro_1pct',perturbation=key,
                                 max_state_change_cm=float(np.max(abs(yp-y)))))
            if model in (1,3):
                fl=fluxes(y,f.u.values,p,model)
                derivative=np.array([rhs(v,float(u),p,model) for v,u in zip(y,f.u)])
                identity=derivative[:,0]+derivative[:,1]/p[1]-fl[:,0]+fl[:,2]
                rows.append(dict(model=name,run=rid,test='balance_algebraico_cm_s',perturbation=0,
                                 max_state_change_cm=float(np.max(abs(identity)))))
            if model==3:
                diag[str(rid)]={c:residual_diagnostics(y[:,j]-f[c].values) for j,c in enumerate(['h1','h2'])}
        if model==3:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            f=pd.read_csv(ROOT/'data/processed/run_08.csv'); y=solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,3)
            fig,ax=plt.subplots(3,1,figsize=(12,8),sharex=True)
            for j,c in enumerate(['h1','h2']):
                ax[j].plot(f.t,f[c],label='Experimental observado'); ax[j].plot(f.t,y[:,j],label='Simulación libre D')
                ax[j].set_ylabel(c+' (cm)'); ax[j].legend(); ax[j].grid(alpha=.3)
            ax[2].step(f.t,f.u,where='post'); ax[2].set_ylabel('Bomba (%)'); ax[2].set_xlabel('Tiempo desde inicio (s)')
            ax[0].set_title('D conservativo | corrida 8 | 0–1700 s | circuito hipotético')
            fig.tight_layout(); fig.savefig(out/'figures/conservative_8.png'); plt.close(fig)
    pd.DataFrame(rows).to_csv(out/'robustness.csv',index=False)
    (out/'residuals_conservative.json').write_text(json.dumps(diag,indent=2),encoding='utf-8')
    print('Robustez y diagnóstico D guardados.')

if __name__=='__main__':main()
