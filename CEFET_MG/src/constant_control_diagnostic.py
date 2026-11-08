"""Diagnóstico aislado. Ejecutar python -m src.constant_control_diagnostic."""
import hashlib,json,sys,importlib.metadata
import numpy as np
import pandas as pd
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data_processing import ROOT
from .simulation_engine import load_run,calibrated_config,run_simulation
from .scenarios import transform_input,regulation_indicators,decide
from .reporting import table

OUT=ROOT/'reports/diagnostico_control_constante'

def existing_manifest():
    # Incluye protocolos, app, scripts y fuentes preexistentes. Excluye sólo salidas propias y cachés.
    paths=[]
    for folder in ['data','reports','docs','src','tests','assets']:
        paths.extend((ROOT/folder).rglob('*'))
    paths.extend([ROOT/'app.py',ROOT/'requirements.txt',ROOT/'requirements-app.txt'])
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.is_file() and not p.is_relative_to(OUT)
            and '__pycache__' not in p.parts and p.suffix not in ['.log','.nbc','.nbi','.pyc']}

def mean_command(t,u):
    return float(np.sum(np.diff(t)*np.asarray(u)[:-1])/(t.iloc[-1]-t.iloc[0]))

def corrected_E2(frame,offset):
    e2=transform_input(frame.t,frame.u,'E2')
    return transform_input(frame.t,np.clip(e2+offset,0,100),'E2')

def fit_offset(window):
    frames=[load_run(i,window) for i in range(1,8)]
    target=np.mean([mean_command(f.t,transform_input(f.t,f.u,'E1')) for f in frames])
    def objective(offset):
        return np.mean([mean_command(f.t,corrected_E2(f,offset)) for f in frames])-target
    offset=brentq(objective,-5,5,xtol=1e-12)
    return float(offset),float(target),float(objective(offset))

def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    before=existing_manifest()
    (OUT/'manifest_previo.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    cfg=calibrated_config();old=pd.read_csv(ROOT/'reports/simulador/comparacion_escenarios.csv')
    old_decisions=json.loads((ROOT/'reports/simulador/decisiones.json').read_text(encoding='utf-8'))
    rows=[];ablation=[];decisions=[];configs={};trajectories={}
    for window in ['excitacion','completa']:
        offset,target,training_mismatch=fit_offset(window)
        configs[window]=dict(offset_pp=offset,development_runs=list(range(1,8)),target_mean_pct=target,
                             training_mean_mismatch_pp=training_mismatch)
        for rid in range(1,11):
            if rid==10 and window=='completa':continue
            f=load_run(rid,window);g=f.copy();g['u']=50.
            constant=run_simulation(g,cfg,step=1.);new=dict(scenario='D50',run=rid,window=window,**regulation_indicators(constant))
            group=old[(old.run==rid)&(old.window==window)].copy()
            # Sólo columnas de indicadores originales, sin reinterpretar cambios porcentuales históricos.
            indicator_names=list(regulation_indicators(constant))
            group=group[['scenario','run','window']+indicator_names]
            block=pd.concat([group,pd.DataFrame([new])],ignore_index=True)
            original=next(x for x in old_decisions if x['run']==rid and x['window']==window)
            extended=decide(block)
            decisions.append(dict(run=rid,window=window,original_choice=original['recommended'],
                                  supplementary_choice=extended['recommended'],supplementary_text=extended['text']))
            rows+=block.to_dict('records')
            constant.to_csv(OUT/f'{window}_run{rid:02}_D50.csv',index=False)
            correction=f.copy();correction['u']=corrected_E2(f,offset)
            yc=run_simulation(correction,cfg,step=1.)
            yc.to_csv(OUT/f'{window}_run{rid:02}_E2_media_diagnostica.csv',index=False)
            ablation.append(dict(scenario='E2_media_diagnostica',run=rid,window=window,
                                 role='desarrollo_1_7' if rid<=7 else 'comparacion_8_10_previamente_examinada',
                                 offset_pp=offset,**regulation_indicators(yc)))
            if rid==8:
                tr={code:pd.read_csv(ROOT/f'reports/simulador/{window}_run{rid:02}_{code}.csv') for code in ['E0','E1','E2']}
                tr['D50']=constant;trajectories[window]=tr
                fig,axes=plt.subplots(3,1,figsize=(12,9),sharex=True)
                colors=['#8c99a2','#117f87','#bd7b35','#243f83']
                for c,ax in zip(['h1','h2','u_command'],axes):
                    for (code,y),color in zip(tr.items(),colors):
                        if c=='u_command':ax.step(y.t,y[c],where='post',label=code,color=color,lw=1.2)
                        else:ax.plot(y.t,y[c],label=code,color=color,lw=1.2)
                    if c!='u_command':ax.axhline(47.4 if c=='h1' else 31.2,ls='--',color='#9aadb7',lw=.8,label='Referencia')
                    ax.set_ylabel(c+(' (%)' if c=='u_command' else ' (cm)'));ax.legend(ncols=5);ax.grid(alpha=.2)
                axes[0].set_title(f'U sin reajuste | corrida 8 | {window} | comparación contrafactual')
                axes[-1].set_xlabel('Tiempo (s)');fig.tight_layout();fig.savefig(OUT/f'figures/constante_{window}.png',dpi=150);plt.close(fig)
                fig,axes=plt.subplots(3,1,figsize=(12,9),sharex=True)
                for c,ax in zip(['h1','h2','u_command'],axes):
                    for code,y in [('E1',tr['E1']),('E2',tr['E2']),('E2 media ajustada (diagnóstico)',yc)]:
                        if c=='u_command':ax.step(y.t,y[c],where='post',label=code,lw=1)
                        else:ax.plot(y.t,y[c],label=code,lw=1)
                    ax.set_ylabel(c+(' (%)' if c=='u_command' else ' (cm)'));ax.grid(alpha=.2);ax.legend()
                axes[0].set_title(f'Ablación de media con offset aprendido sólo en 1–7 | corrida 8 | {window}')
                axes[-1].set_xlabel('Tiempo (s)');fig.tight_layout();fig.savefig(OUT/f'figures/media_{window}.png',dpi=150);plt.close(fig)
    data=pd.DataFrame(rows);abl=pd.DataFrame(ablation)
    data.to_csv(OUT/'comparacion_complementaria.csv',index=False);abl.to_csv(OUT/'ablacion_media.csv',index=False)
    (OUT/'decisiones_complementarias.json').write_text(json.dumps(decisions,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'configuracion.json').write_text(json.dumps(dict(model=cfg.name,parameters=dict(zip(cfg.names,cfg.parameters)),
        delay_s=cfg.delay,step_s=1.,offsets=configs,python=sys.version,
        packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','numba','matplotlib']}),indent=2,ensure_ascii=False),encoding='utf-8')
    # Comparaciones pareadas que hacen explícito el papel del mando medio.
    mean_rows=[]
    for (rid,window),block in data.groupby(['run','window']):
        b=block.set_index('scenario');a=abl[(abl.run==rid)&(abl.window==window)].iloc[0]
        mean_rows.append(dict(run=rid,window=window,mean_E1=b.loc['E1','u_mean_pct'],mean_E2=b.loc['E2','u_mean_pct'],
            mean_corrected=a.u_mean_pct,mean_gap_E2_E1_pp=b.loc['E2','u_mean_pct']-b.loc['E1','u_mean_pct'],
            mean_gap_corrected_E1_pp=a.u_mean_pct-b.loc['E1','u_mean_pct'],
            RMSE_h1_E1=b.loc['E1','RMSE_ref_h1_cm'],RMSE_h1_E2=b.loc['E2','RMSE_ref_h1_cm'],RMSE_h1_corrected=a.RMSE_ref_h1_cm,
            RMSE_h2_E1=b.loc['E1','RMSE_ref_h2_cm'],RMSE_h2_E2=b.loc['E2','RMSE_ref_h2_cm'],RMSE_h2_corrected=a.RMSE_ref_h2_cm))
    means=pd.DataFrame(mean_rows);means.to_csv(OUT/'interpretacion_media.csv',index=False)
    summary=data.groupby(['window','scenario'])[['RMSE_ref_h1_cm','RMSE_ref_h2_cm','MAE_ref_h1_cm','MAE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']].mean().reset_index()
    summary.to_csv(OUT/'resumen_por_horizonte.csv',index=False)
    reproducibility=[]
    for rid in [8,9,10]:
        f=load_run(rid);f['u']=50.;a=run_simulation(f,cfg);b=run_simulation(f,cfg)
        reproducibility.append(dict(run=rid,exact=bool(np.array_equal(a.values,b.values))))
    # Verificación independiente por DOP853 para D50, sin observaciones futuras.
    from scipy.integrate import solve_ivp
    from .precision_models import rhs,pump
    p=np.array(cfg.parameters);reference=[]
    for rid in [8,9,10]:
        f=load_run(rid);g=f.copy();g['u']=50.;y=run_simulation(g,cfg)
        z=np.r_[f[['h1','h2']].iloc[0].values,pump(50.,p,15)]
        ref=solve_ivp(lambda t,v:rhs(v,50.,p,15),[0,float(f.t.iloc[-1])],z,t_eval=f.t.values,method='DOP853',rtol=1e-11,atol=1e-12)
        reference.append(dict(run=rid,max_difference_cm=float(abs(ref.y[:2].T-y[['h1','h2']].values).max())))
    after=existing_manifest();changed=[k for k,v in before.items() if after.get(k)!=v]
    integrity=dict(unchanged=not changed,changed=changed,files_compared=len(before),
                   reproducibility=reproducibility,DOP853=reference)
    (OUT/'integridad_y_verificacion.json').write_text(json.dumps(integrity,indent=2),encoding='utf-8')
    if changed:raise RuntimeError('Se modificaron archivos preexistentes')
    print(summary.to_string(index=False));print('Medias, corrida 8:',means[means.run==8].to_string(index=False))
    print('Preservación:',integrity['unchanged'],'archivos',len(before))

if __name__=='__main__':main()
