"""Completa la extensión adaptativa sin sobrescribir resultados previos."""
import json,time
import numpy as np
import pandas as pd
from .precision_study import OUT,dump,get_data,run_candidate,snapshot
from .precision_models import SPECS

def main():
    runs=get_data(); rows=pd.read_csv(OUT/'metrics.csv').to_dict('records')
    logs=json.loads((OUT/'all_fits.json').read_text()); registry=json.loads((OUT/'registry.json').read_text())
    for name in ['Q_balance_local','R_balance_monotono','S_balance_empirico_C','T_bomba_carga_local','U_bomba_carga_monotona']:
        r,l=run_candidate(runs,name);rows+=r;logs[name]=l;registry[name]=dict(base=name,objective='ls',profiles=None)
        pd.DataFrame(rows).to_csv(OUT/'metrics.csv',index=False)
    d=pd.DataFrame(rows);cv=d[(d.protocol=='cv')&(d.window=='completa')&d.model.isin(SPECS)]
    ranking=cv.groupby(['model','tank']).NRMSE.mean().groupby('model').max().sort_values()
    dump(OUT/'ls_ranking_extended.json',ranking.to_dict());top=list(ranking.index[:2])
    for name in top:
        for obj in ['minimax','regularizado']:
            label=name+'__'+obj
            if label in logs:continue
            r,l=run_candidate(runs,name,label,obj);rows+=r;logs[label]=l;registry[label]=dict(base=name,objective=obj,profiles=None)
    best=top[0]
    for suffix,profiles in [('retardo',[(v,0.) for v in [0.,.5,1.,2.,4.,8.]]),
                            ('actuador',[(0.,v) for v in [0.,1.,2.,4.,8.]])]:
        label=best+'__'+suffix
        if label in logs:continue
        r,l=run_candidate(runs,best,label,profiles=profiles);rows+=r;logs[label]=l
        registry[label]=dict(base=best,objective='ls',profiles=profiles)
    pd.DataFrame(rows).to_csv(OUT/'metrics.csv',index=False)
    dump(OUT/'all_fits.json',logs);dump(OUT/'registry.json',registry)
    before=json.loads((OUT/'original_manifest.json').read_text());after=snapshot()
    changed=[k for k,v in before.items() if after.get(k)!=v]
    dump(OUT/'integrity.json',dict(originals_unchanged=not changed,changed=changed,files_compared=len(before)))
    config=json.loads((OUT/'config.json').read_text());config['extended_candidates']={n:vars(s) for n,s in SPECS.items()}
    dump(OUT/'config.json',config)
    if changed:raise RuntimeError('Se modificaron resultados originales')
    print('Extensión terminada; modelos totales',len(logs),flush=True)

if __name__=='__main__':main()
