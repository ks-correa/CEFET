from src.documentary_archive import verify_original_manifest, archived_bytes
import json
import hashlib
import numpy as np
import pandas as pd
import pytest
from src.data_processing import ROOT
from src.precision_models import SPECS,simulate,pump,hydraulic,event_grid
from src.precision_study import OUT,get_data,snapshot
from src.calibration import scale_for
from src.rk4_solver import solve as old_solve

def test_original_files_and_results_preserved():
    before=json.loads((OUT/'original_manifest.json').read_text())
    assert before
    verify_original_manifest(before)

def test_frozen_reference_scores_unchanged():
    old=pd.read_csv(ROOT/'reports/metrics.csv');new=pd.read_csv(OUT/'metrics.csv')
    keys=['protocol','model','role','window','tank','run']
    old=old[old.model.isin(['C_bomba','D_conservativo'])]
    merged=old.merge(new,on=keys,suffixes=('_old','_new'))
    assert len(merged)==len(old)
    for metric in ['MAE','RMSE','NRMSE','bias','max_abs','R2','peak_error','final_error']:
        np.testing.assert_allclose(merged[metric+'_old'],merged[metric+'_new'],rtol=1e-12,atol=1e-12)

def test_delay_event_causality():
    t=np.array([0.,4.,8.]);u=np.array([10.,90.,50.])
    grid,controls,idx=event_grid(t,u,2.)
    np.testing.assert_array_equal(grid,[0.,2.,4.,6.,8.])
    np.testing.assert_array_equal(controls,[50.,10.,10.,90.,90.])
    np.testing.assert_array_equal(idx,[0,2,4])

def test_future_level_observations_never_correct_simulation():
    f=get_data()[7];g=f.copy();g.loc[g.index[1:],['h1','h2']]+=100
    name='R_balance_monotono';p=np.array(SPECS[name].x)
    np.testing.assert_array_equal(simulate(f,p,name),simulate(g,p,name))
    with pytest.raises(ValueError):simulate(f,p,name,delay=-1)

def test_pump_monotonicity_and_hydraulic_equilibrium():
    for name,s in SPECS.items():
        p=np.array(s.x);values=np.array([pump(float(u),p,s.code) for u in np.linspace(0,100,201)])
        assert values.min()>=0 and np.diff(values).min()>=-1e-12
        np.testing.assert_allclose(pump(50.,p,s.code),p[0])
        np.testing.assert_allclose(hydraulic(np.array([47.4,31.2]),p,s.code),[p[0],p[0]])

def test_C_balance_realizations_are_algebraic_controls():
    l=json.loads((ROOT/'reports/calibration.json').read_text())['C_bomba']['principal']
    b,c,d,e,k,gamma=list(l['parameters'].values());a=b*c/d+e
    f=get_data()[7];original=old_solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,np.array([b,c,d,e,k,gamma]),2)
    for name,p in [('S_balance_empirico_C',[50*k,c/a,a,b,d/(c/a)-b,gamma]),
                   ('T_bomba_carga_local',[50*k,c/b,b,d/(c/b)-b,a-b,gamma])]:
        assert min(p)>0
        np.testing.assert_allclose(simulate(f,np.array(p),name),original,atol=1e-10)

def test_fold_scales_are_training_only():
    runs=get_data();logs=json.loads((OUT/'all_fits.json').read_text())
    for label,l in logs.items():
        for fold in range(5):
            held=[2*fold+1,2*fold+2]
            train=[f for rid,f in enumerate(runs,1) if rid not in held]
            np.testing.assert_allclose(l['cv'][str(fold)]['scale_cm'],scale_for(train),atol=1e-12)

def test_numerics_and_conservation_all_models():
    q=pd.read_csv(OUT/'numerical_verification.csv')
    assert q[q.method=='DOP853'].max_vs_half_cm.max()<1e-3
    assert q[q.method=='balance_cm_s'].max_vs_half_cm.max()<1e-12
    for p in (OUT/'predictions').glob('flows_*.csv'):
        f=pd.read_csv(p)
        assert f[['h1_sim','h2_sim','Qin_A1','Q12_A1','Qout_A1']].min().min()>=0

def test_advanced_reproducibility():
    q=json.loads((OUT/'reproducibility.json').read_text())
    assert len(q)>=16
    assert all(r['exact'] for r in q)

def test_no_discarded_candidates_hidden():
    d=pd.read_csv(OUT/'metrics.csv')
    for name in SPECS:
        assert name in d.model.values
        q=d[(d.model==name)&(d.protocol=='cv')&(d.window=='completa')]
        assert set(q.run)==set(range(1,11)) and len(q)==20
    assert np.isfinite(d[['MAE','RMSE','NRMSE','bias']]).all().all()
