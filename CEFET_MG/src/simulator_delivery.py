"""Regresión de U y escenarios ejecutados sin alterar la evidencia científica previa."""
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data_processing import ROOT
from .simulation_engine import calibrated_config,load_run,run_simulation,prediction_metrics,U
from .scenarios import compare_scenarios

OUT=ROOT/'reports/simulador'

def main():
    OUT.mkdir(exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    protected=list((ROOT/'data/raw').glob('*'))+list((ROOT/'reports/optimizacion_precision').rglob('*'))
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    config=calibrated_config();regression=[]
    previous=pd.read_csv(ROOT/'reports/optimizacion_precision/metrics.csv')
    for rid in [8,9,10]:
        f=pd.read_csv(ROOT/f'data/processed/run_{rid:02}.csv');sim=run_simulation(f,config)
        source=pd.read_csv(ROOT/f'reports/optimizacion_precision/predictions/{U}_{rid:02}.csv')
        difference=float(abs(sim[['h1','h2']].values-source[['h1_sim','h2_sim']].values).max())
        if difference>1e-9:raise RuntimeError('Regresión de trayectoria U')
        for row in prediction_metrics(f,sim,config).to_dict('records'):
            ref=previous[(previous.model==U)&(previous.protocol=='principal')&(previous.role=='evaluacion')&(previous.window=='completa')&(previous.run==rid)&(previous.tank==row['tank'])].iloc[0]
            if not np.allclose([row[k] for k in ['MAE','RMSE','NRMSE']],[ref[k] for k in ['MAE','RMSE','NRMSE']],atol=1e-10):raise RuntimeError('Regresión de métricas')
            regression.append(dict(run=rid,max_trajectory_difference_cm=difference,**row))
    pd.DataFrame(regression).to_csv(OUT/'regresion_U.csv',index=False)
    allrows=[];decisions=[]
    for window in ['excitacion','completa']:
        for rid in range(1,11):
            if rid==10 and window=='completa':continue
            f=load_run(rid,window);tr,table,decision=compare_scenarios(f)
            table['run']=rid;table['window']=window;allrows+=table.to_dict('records')
            decisions.append(dict(run=rid,window=window,**decision))
            for code,result in tr.items():result.to_csv(OUT/f'{window}_run{rid:02}_{code}.csv',index=False)
            if rid==8:
                fig,axes=plt.subplots(3,1,figsize=(12,9),sharex=True)
                for c,ax in zip(['h1','h2','u_command'],axes):
                    for code,result in tr.items():ax.plot(result.t,result[c],label=code,lw=1)
                    if c!='u_command':
                        ax.plot(f.t,f[c],color='#8a97a6',ls=':',lw=.7,label='Observado (E0)')
                        ax.axhline(47.4 if c=='h1' else 31.2,color='#0c2940',ls='--',lw=.7)
                    ax.set_ylabel(c+(' (%)' if c=='u_command' else ' (cm)'));ax.legend();ax.grid(alpha=.2)
                axes[0].set_title(f'U calibrado | corrida 8 | {window} | E1/E2 contrafactuales')
                axes[-1].set_xlabel('Tiempo (s)');fig.tight_layout();fig.savefig(OUT/f'figures/escenarios_{window}.png',dpi=150);plt.close(fig)
    pd.DataFrame(allrows).to_csv(OUT/'comparacion_escenarios.csv',index=False)
    (OUT/'decisiones.json').write_text(json.dumps(decisions,indent=2,ensure_ascii=False),encoding='utf-8')
    changed=[name for name,sha in manifest.items() if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha]
    (OUT/'integridad.json').write_text(json.dumps(dict(unchanged=not changed,changed=changed,sha256=manifest),indent=2),encoding='utf-8')
    if changed:raise RuntimeError('Archivos científicos modificados')
    print('Regresión U aprobada. Escenarios ejecutados:',len(decisions),'comparaciones; originales intactos.')

if __name__=='__main__':main()
