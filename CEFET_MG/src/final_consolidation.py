"""Resultados vigentes, regresión y sensibilidad; nunca reescribe archivos históricos."""
import hashlib,json,sys,importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data_processing import ROOT
from .simulation_engine import U,calibrated_config,load_run,run_simulation,prediction_metrics
from .final_scenarios import compare_scenarios,smoothing_complement,MAPPING
from .precision_models import rhs,pump

OUT=ROOT/'reports/consolidacion_final'

def protect_history():
    # Las entradas originales, documentación y programa anteriores se conservan byte a byte.
    from .constant_control_diagnostic import existing_manifest
    manifest=existing_manifest()
    return {name:sha for name,sha in manifest.items() if not (ROOT/name).is_relative_to(OUT)
            and not (ROOT/name).is_relative_to(ROOT/'docs/consolidacion_final')
            and not (ROOT/name).name.startswith(('final_','test_final_'))}

def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'figures').mkdir(exist_ok=True);(OUT/'robustez').mkdir(exist_ok=True)
    before=protect_history();(OUT/'manifest_historico.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    cfg=calibrated_config();rows=[];historical=[];choices=[];regression=[];traces={}
    old=pd.read_csv(ROOT/'reports/simulador/comparacion_escenarios.csv')
    constant=pd.read_csv(ROOT/'reports/diagnostico_control_constante/comparacion_complementaria.csv')
    for window in ['excitacion','completa']:
        for rid in range(1,11):
            if rid==10 and window=='completa':continue
            f=load_run(rid,window);tr,table,decision=compare_scenarios(f)
            sm,sm_metrics=smoothing_complement(f)
            for code in ['E0','E1','E2']:
                ref=(old[(old.run==rid)&(old.window==window)&(old.scenario==code)] if code!='E2'
                     else constant[(constant.run==rid)&(constant.window==window)&(constant.scenario=='D50')]).iloc[0]
                selected=table[table.scenario==code].iloc[0]
                for metric in ['RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']:
                    if not np.isclose(selected[metric],ref[metric],rtol=1e-12,atol=1e-10):raise RuntimeError('No coincide con evidencia previa')
                tr[code].to_csv(OUT/f'{window}_run{rid:02}_{code}.csv',index=False)
            table['run']=rid;table['window']=window;rows+=table.to_dict('records')
            sm_metrics['run']=rid;sm_metrics['window']=window;historical+=sm_metrics.to_dict('records')
            sm.to_csv(OUT/f'{window}_run{rid:02}_S_HIST.csv',index=False)
            choices.append(dict(run=rid,window=window,**decision))
            if window=='excitacion' and rid==8:traces=tr
    for rid in [8,9,10]:
        f=pd.read_csv(ROOT/f'data/processed/run_{rid:02}.csv');y=run_simulation(f,cfg)
        reference=pd.read_csv(ROOT/f'reports/optimizacion_precision/predictions/{U}_{rid:02}.csv')
        error=float(np.max(abs(y[['h1','h2']].values-reference[['h1_sim','h2_sim']].values)))
        for item in prediction_metrics(f,y,cfg).to_dict('records'):regression.append(dict(run=rid,max_trajectory_difference_cm=error,**item))
    pd.DataFrame(regression).to_csv(OUT/'validacion_U_sin_cambios.csv',index=False)
    results=pd.DataFrame(rows);results.to_csv(OUT/'comparacion_principal.csv',index=False)
    pd.DataFrame(historical).to_csv(OUT/'suavizado_historico.csv',index=False)
    (OUT/'decisiones_vigentes.json').write_text(json.dumps(choices,indent=2,ensure_ascii=False),encoding='utf-8')
    # Sensibilidad declarada: condiciones iniciales y perturbaciones de mando, sin nuevo control.
    cases=[]
    for delta in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]:
        cases.append((f'inicial_{delta[0]:+d}_{delta[1]:+d}',delta,None))
    for name in ['pulso_mas2','pulso_menos2','sesgo_menos2']:cases.append((name,(0,0),name))
    sensitivity=[];verdicts=[];ranges=[]
    measured=pd.concat([load_run(i) for i in range(1,11)])
    for rid in range(1,11):
        f=load_run(rid)
        for name,delta,disturb in cases:
            initial=f[['h1','h2']].iloc[0].values+np.array(delta);d=np.zeros(len(f))
            if disturb=='pulso_mas2':d[(f.t>=400)&(f.t<440)]=2.
            if disturb=='pulso_menos2':d[(f.t>=400)&(f.t<440)]=-2.
            if disturb=='sesgo_menos2':d[f.t>=400]=-2.
            tr,table,decision=compare_scenarios(f,initial=tuple(initial),disturbance=d)
            table['run']=rid;table['case']=name;sensitivity+=table.to_dict('records')
            verdicts.append(dict(run=rid,case=name,recommended=decision['recommended'],exploratory=True))
            for code,y in tr.items():
                for c in ['h1','h2']:
                    ranges.append(dict(run=rid,case=name,scenario=code,tank=c,min_cm=float(y[c].min()),max_cm=float(y[c].max()),
                      measured_min_cm=float(measured[c].min()),measured_max_cm=float(measured[c].max()),
                      samples_outside_measured_rectangle=int(((y[c]<measured[c].min())|(y[c]>measured[c].max())).sum())))
            if rid==8 and name in ['inicial_+1_+1','pulso_mas2','sesgo_menos2']:
                for code,y in tr.items():y.to_csv(OUT/'robustez'/f'run08_{name}_{code}.csv',index=False)
    pd.DataFrame(sensitivity).to_csv(OUT/'robustez/indicadores.csv',index=False)
    pd.DataFrame(ranges).to_csv(OUT/'robustez/rangos.csv',index=False)
    (OUT/'robustez/decisiones.json').write_text(json.dumps(verdicts,indent=2),encoding='utf-8')
    p=np.array(cfg.parameters);q,r,k12,kout,kpump,b,c=p
    jac=np.array([[-k12-kpump,k12],[r*k12,-r*(k12+kout)]])
    offset2=(pump(48.,p,15)-q)/(kpump*(1+kout/k12)+kout)
    eq48=[47.4+(1+kout/k12)*offset2,31.2+offset2]
    local=dict(jacobian=jac.tolist(),eigenvalues=[[float(v.real),float(v.imag)] for v in np.linalg.eigvals(jac)],
               nominal_equilibrium=[47.4,31.2],constant_48_equilibrium=eq48,
               equilibrium_48_residual=rhs(np.r_[eq48,q],48.,p,15).tolist(),
               caveat='Predicción local bajo sesgo de mando; no prueba de rechazo de perturbaciones físicas')
    (OUT/'robustez/analisis_local.json').write_text(json.dumps(local,indent=2),encoding='utf-8')
    # Gráfica principal con entrada retenida; jamás se interpola una entrada futura.
    fig,axes=plt.subplots(3,1,figsize=(12,9),sharex=True)
    for state,ax in zip(['h1','h2','u_command'],axes):
        for code,y in traces.items():
            if state=='u_command':ax.step(y.t,y[state],where='post',label=code,lw=1.1)
            else:ax.plot(y.t,y[state],label=code,lw=1.1)
        if state!='u_command':ax.axhline(47.4 if state=='h1' else 31.2,ls='--',color='#999',lw=.8,label='Referencia')
        ax.set_ylabel('Mando (%)' if state=='u_command' else state+' (cm)');ax.grid(alpha=.2);ax.legend(ncols=4)
    axes[0].set_title('Escenarios vigentes | U sin reajuste | corrida 8 | ≈800 s | contrafactuales')
    axes[-1].set_xlabel('Tiempo (s)');fig.tight_layout();fig.savefig(OUT/'figures/escenarios_vigentes.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(2,1,figsize=(12,7),sharex=True)
    for name in ['inicial_+1_+1','pulso_mas2','sesgo_menos2']:
        y=pd.read_csv(OUT/'robustez'/f'run08_{name}_E2.csv')
        for c,a in zip(['h1','h2'],ax):a.plot(y.t,y[c],label=name);a.set_ylabel(c+' (cm)');a.grid(alpha=.2)
    for ref,a in zip([47.4,31.2],ax):a.axhline(ref,color='#999',ls='--');a.legend()
    ax[0].set_title('E2 constante con intervenciones simuladas exploratorias | corrida 8 | ≈800 s')
    ax[-1].set_xlabel('Tiempo (s)');fig.tight_layout();fig.savefig(OUT/'figures/sensibilidad_E2.png',dpi=150);plt.close(fig)
    after=protect_history();changed=[name for name,sha in before.items() if after.get(name)!=sha]
    (OUT/'integridad.json').write_text(json.dumps(dict(unchanged=not changed,changed=changed,files_compared=len(before)),indent=2),encoding='utf-8')
    config=dict(model=cfg.name,parameters=dict(zip(cfg.names,cfg.parameters)),step_s=1.,delay_s=cfg.delay,
                scenario_mapping=MAPPING,retrospective_revision=True,python=sys.version,
                versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','numba','streamlit']})
    (OUT/'configuracion_vigente.json').write_text(json.dumps(config,indent=2,ensure_ascii=False),encoding='utf-8')
    if changed:raise RuntimeError('Historia alterada')
    print('Comparaciones nominales:',len(choices),'exploratorias:',len(verdicts))
    print(pd.DataFrame(verdicts).groupby(['case','recommended'],dropna=False).size().to_string())
    print('Equilibrio a 48%:',eq48,'historia intacta:',not changed)

if __name__=='__main__':main()
