"""Diagnóstico, verificación y figuras de todos los candidatos avanzados."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from .data_processing import ROOT
from .precision_study import OUT,dump,get_data,fit
from .precision_models import SPECS,simulate,event_grid,integrate_grid,rhs,hydraulic,pump
from .goodness_of_fit import metrics,residual_diagnostics
from .rk4_solver import solve as old_solve
from .models import rhs as old_rhs

def diagnose_baseline():
    raw=json.loads((ROOT/'reports/calibration.json').read_text()); result={}
    for name,mid in [('C_bomba',2),('D_conservativo',3)]:
        p=np.array(list(raw[name]['principal']['parameters'].values())); op=np.array([47.4,31.2]); j=[]
        for k in range(2):
            z=op.copy(); z[k]+=.0001; j.append((old_rhs(z,50.,p,mid)-old_rhs(op,50.,p,mid))/.0001)
        jac=np.array(j).T
        result[name]=dict(jacobian=jac.tolist(),eigenvalues_real_imag=[[float(v.real),float(v.imag)] for v in np.linalg.eigvals(jac)],
                          damping_to_coupling_h2=float(-jac[1,1]/jac[1,0]),
                          h1_head_derivative_ratio=float(-jac[0,0]/jac[0,1]))
    runs=get_data(); records=[]
    for rid,f in enumerate(runs,1):
        for name,mid in [('C_bomba',2),('D_conservativo',3)]:
            p=np.array(list(raw[name]['principal']['parameters'].values()))
            y=old_solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,mid)
            for j,c in enumerate(['h1','h2']):
                e=y[:,j]-f[c].values
                # Corr. entre residuo actual y entrada pasada, no identifica retardo causal por sí sola.
                for lag in range(0,6):
                    a=e[lag:]; b=f.u.values[:len(f)-lag] if lag else f.u.values
                    records.append(dict(model=name,run=rid,tank=c,lag_samples=lag,
                                        correlation=float(np.corrcoef(a,b)[0,1])))
    pd.DataFrame(records).to_csv(OUT/'baseline_lag_correlations.csv',index=False)
    dump(OUT/'baseline_diagnosis.json',result)

def main():
    OUT.mkdir(exist_ok=True,parents=True); figs=OUT/'figures'; figs.mkdir(exist_ok=True)
    diagnose_baseline()
    allfits=json.loads((OUT/'all_fits.json').read_text()); reg=json.loads((OUT/'registry.json').read_text())
    data=pd.read_csv(OUT/'metrics.csv'); runs=get_data(); verification=[]; sensitivity=[]; residues=[]
    quant=json.loads((ROOT/'data/processed/audit.json').read_text())['quantization_cm']
    for label,log in allfits.items():
        print('Diagnóstico',label,flush=True)
        baseline=label in ['C_bomba','D_conservativo']; cfg=reg.get(label)
        l=log['principal']; p=np.array(list(l['parameters'].values())); scale=l['scale_cm']
        def pred(f,step=1.,initial=None,params=None):
            pp=p if params is None else params
            if baseline:return old_solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values if initial is None else initial,pp,2 if label=='C_bomba' else 3,step)
            return simulate(f,pp,cfg['base'],step,l['delay'],l['tau'],initial)
        fig,ax=plt.subplots(3,3,figsize=(15,10))
        figd,ad=plt.subplots(2,5,figsize=(21,8))
        for row,rid in enumerate([8,9,10]):
            f=runs[rid-1]; y=pred(f); err=y-f[['h1','h2']].values
            for j,c in enumerate(['h1','h2']):
                ax[row,j].plot(f.t,f[c],label='Observado',lw=.9); ax[row,j].plot(f.t,y[:,j],label='Simulado',lw=.9)
                ax[row,j].set_ylabel(c+' (cm)'); ax[row,j].set_xlabel('Tiempo (s)'); ax[row,j].legend(fontsize=7)
                ax[row,j].set_title(f'Corrida {rid} | 0–{f.t.iloc[-1]:.0f} s')
                ad[j,0].plot(f.t,err[:,j],lw=.7,label=str(rid)); ad[j,0].set_xlabel('Tiempo (s)');ad[j,0].set_ylabel('Residuo (cm)')
                ad[j,1].scatter(y[:,j],err[:,j],s=2,alpha=.3);ad[j,1].set_xlabel('Simulado (cm)');ad[j,1].set_ylabel('Residuo (cm)')
                ad[j,2].hist(err[:,j],bins=25,density=True,histtype='step');ad[j,2].set_xlabel('Residuo (cm)');ad[j,2].set_ylabel('Densidad (1/cm)')
                sorted_e=np.sort(err[:,j]); ad[j,3].plot(sorted_e,np.arange(1,len(f)+1)/len(f));ad[j,3].set_xlabel('Residuo (cm)');ad[j,3].set_ylabel('F. empírica')
                for phase,mask in [('completa',np.ones(len(f),bool)),('excitacion',f.t<=800.01),('recuperacion',f.t>800.01)]:
                    if mask.sum()<25:continue
                    dd=residual_diagnostics(err[mask,j]); residues.append(dict(model=label,run=rid,tank=c,phase=phase,
                        acf1=dd['acf'][1],Q20=dd['Q'],p_descriptive=dd['p_descriptive'],acf=dd['acf']))
                    if phase=='completa':ad[j,4].plot(np.arange(21),dd['acf'],label=str(rid))
                ad[j,4].set_xlabel('Retardo (≈4 s/muestra)');ad[j,4].set_ylabel('ACF')
            ax[row,2].step(f.t,f.u,where='post',lw=.8); ax[row,2].set_ylabel('Bomba (%)');ax[row,2].set_xlabel('Tiempo (s)')
            for step in [4.,2.,1.,.5]:
                yy=pred(f,step); fine=pred(f,.5)
                verification.append(dict(model=label,run=rid,method='RK4',step=step,max_vs_half_cm=float(np.max(abs(yy-fine)))))
            if baseline:
                grid=f.t.values; controls=f.u.values; inds=np.arange(len(f)); z=f[['h1','h2']].iloc[0].values
                deriv=lambda state,control:old_rhs(state,control,p,2 if label=='C_bomba' else 3)
            else:
                grid,controls,inds=event_grid(f.t.values,f.u.values,l['delay']); code=SPECS[cfg['base']].code
                z=np.r_[f[['h1','h2']].iloc[0].values,pump(50.,p,code)]
                deriv=lambda state,control:rhs(state,control,p,code,l['tau'])
            ref=[z.copy()]
            for i in range(len(grid)-1):
                sol=solve_ivp(lambda t,v:deriv(v,float(controls[i])),[grid[i],grid[i+1]],z,method='DOP853',rtol=1e-11,atol=1e-12)
                if not sol.success:raise RuntimeError(sol.message)
                z=sol.y[:,-1];ref.append(z.copy())
            ref=np.array(ref)[inds,:2]
            verification.append(dict(model=label,run=rid,method='DOP853',step=0.,max_vs_half_cm=float(np.max(abs(ref-y)))))
            if not baseline:
                full=integrate_grid(grid,controls,f[['h1','h2']].iloc[0].values,p,code,1.,l['tau'])
                fl=np.array([hydraulic(v,p,code) for v in full]); command=np.array([pump(v,p,code) for v in controls])
                if code in (14,15):command=np.maximum(0.,command-p[4]*(full[:,0]-47.4))
                actual=full[:,2] if l['tau']>0 else command
                dd=np.array([rhs(v,float(u),p,code,l['tau']) for v,u in zip(full,controls)])
                balance=dd[:,0]+dd[:,1]/p[1]-(actual-fl[:,1])
                verification.append(dict(model=label,run=rid,method='balance_cm_s',step=0.,max_vs_half_cm=float(np.max(abs(balance)))))
                sample=pd.DataFrame(dict(t=grid,h1_sim=full[:,0],h2_sim=full[:,1],u_delayed=controls,
                                         Qin_A1=actual,Q12_A1=fl[:,0],Qout_A1=fl[:,1],balance_cm_s=balance))
                sample.to_csv(OUT/'predictions'/f'flows_{label}_{rid}.csv',index=False)
            for tank in range(2):
                for sign in [-1,1]:
                    yy0=f[['h1','h2']].iloc[0].values.copy();yy0[tank]+=sign*quant[f'h{tank+1}']/2
                    yp=pred(f,initial=yy0)
                    for j,c in enumerate(['h1','h2']):
                        sensitivity.append(dict(model=label,run=rid,test='inicial',perturbed=f'h{tank+1}',sign=sign,tank=c,
                            max_state_change_cm=float(np.max(abs(yp-y))),**metrics(f[c].values,yp[:,j],scale[j])))
            for j,key in enumerate(l['parameters']):
                pp=p.copy();delta=max(abs(pp[j])*.01,.001)
                if not baseline and pp[j]+delta>SPECS[cfg['base']].hi[j]:delta=-delta
                pp[j]+=delta
                yp=pred(f,params=pp)
                sensitivity.append(dict(model=label,run=rid,test='parametro',perturbed=key,sign=1,
                                        parameter_delta=float(delta),max_state_change_cm=float(np.max(abs(yp-y)))))
        fig.suptitle(f'{label} | desarrollo interno | corridas reservadas | estados libres')
        fig.tight_layout();fig.savefig(figs/f'trajectories_{label}.png',dpi=110);plt.close(fig)
        for j,c in enumerate(['h1','h2']):
            for k in range(5):ad[j,k].set_title(c)
            ad[j,0].legend(title='Corrida');ad[j,4].legend(title='Corrida')
        figd.suptitle(f'{label} | residuos simulado−real | corridas 8–10 | 0–1700/800 s')
        figd.tight_layout();figd.savefig(figs/f'residuals_{label}.png',dpi=110);plt.close(figd)
    pd.DataFrame(verification).to_csv(OUT/'numerical_verification.csv',index=False)
    pd.DataFrame(sensitivity).to_csv(OUT/'sensitivity.csv',index=False)
    dump(OUT/'residual_diagnostics.json',residues)
    # Repetir principal para todos los candidatos LS; perfiles/minimax deterministas se verifican también.
    repetition=[]
    for label,cfg in reg.items():
        l=allfits[label]['principal'];starts=2 if cfg['profiles'] else 4
        p,sc,ll=fit(runs[:7],cfg['base'],cfg['objective'],starts,l['delay'],l['tau'])
        delta=float(np.max(abs(p-np.array(l['p']))))
        repetition.append(dict(model=label,max_parameter_difference=delta,exact=bool(np.array_equal(p,l['p']))))
    dump(OUT/'reproducibility.json',repetition)
    print('Diagnósticos terminados',flush=True)

if __name__=='__main__':main()
