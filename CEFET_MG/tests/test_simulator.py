from dataclasses import replace
import json,hashlib
import numpy as np
import pandas as pd
import pytest
from src.data_processing import ROOT
from src.simulation_engine import (U,P,MODELS,calibrated_config,exploratory_config,load_run,
                                   run_simulation,prediction_metrics)
from src.scenarios import transform_input,compare_scenarios,regulation_indicators,decide

def test_engine_regression_full_U_and_original_metrics():
    cfg=calibrated_config();assert cfg.name==U and cfg.delay==2.
    old=pd.read_csv(ROOT/'reports/optimizacion_precision/metrics.csv')
    for rid in [8,9,10]:
        f=pd.read_csv(ROOT/f'data/processed/run_{rid:02}.csv');y=run_simulation(f,cfg)
        previous=pd.read_csv(ROOT/f'reports/optimizacion_precision/predictions/{U}_{rid:02}.csv')
        np.testing.assert_array_equal(y[['h1','h2']],previous[['h1_sim','h2_sim']])
        for row in prediction_metrics(f,y,cfg).to_dict('records'):
            ref=old[(old.model==U)&(old.protocol=='principal')&(old.role=='evaluacion')&(old.run==rid)&(old.window=='completa')&(old.tank==row['tank'])].iloc[0]
            np.testing.assert_allclose([row[k] for k in ['MAE','RMSE','NRMSE','bias']],[ref[k] for k in ['MAE','RMSE','NRMSE','bias']],atol=1e-12)

def test_initial_causality_delay_and_future_states():
    f=load_run();y=run_simulation(f)
    np.testing.assert_array_equal(y[['h1','h2']].iloc[0],f[['h1','h2']].iloc[0])
    assert y.u_applied.iloc[0]==50 and y.u_applied.iloc[1]==f.u.iloc[0]
    g=f.copy();g.loc[g.index[1:],['h1','h2']]+=100
    np.testing.assert_array_equal(run_simulation(g)[['h1','h2']],y[['h1','h2']])
    g=f.copy();g.loc[g.index[20:],'u']=50.
    np.testing.assert_array_equal(run_simulation(g)[['h1','h2']].iloc[:21],y[['h1','h2']].iloc[:21])

def test_E1_exact_and_E2_causal_limits():
    f=load_run();t,u=f.t.values,f.u.values
    np.testing.assert_allclose(transform_input(t,u,'E1'),50+.8*(u-50))
    e2=transform_input(t,u,'E2');assert abs(e2[0]-50)<=10
    assert np.all(abs(np.diff(e2))<=2.5*np.diff(t)+1e-10)
    other=u.copy();other[20:]=0
    np.testing.assert_array_equal(transform_input(t,other,'E2')[:20],e2[:20])
    assert e2.min()>=0 and e2.max()<=100

def test_scenarios_comparable_E0_and_repeatable():
    f=load_run();cfg=calibrated_config();a,table,decision=compare_scenarios(f,cfg)
    np.testing.assert_array_equal(a['E0'][['h1','h2']],run_simulation(f,cfg)[['h1','h2']])
    for x in a.values():
        np.testing.assert_array_equal(x.t,f.t)
        assert x.attrs['parameters']==cfg.parameters and x.attrs['step']==1.
        assert np.isfinite(x.values).all() and x[['h1','h2']].min().min()>=0
        assert abs(x.balance_total).max()<1e-12
        np.testing.assert_array_equal(x[['h1','h2']].iloc[0],f[['h1','h2']].iloc[0])
    b,other,otherdecision=compare_scenarios(f,cfg)
    pd.testing.assert_frame_equal(table,other);assert decision==otherdecision

def test_indicator_units_and_time_bands():
    f=pd.DataFrame(dict(t=[0.,4.,8.],h1=[47.4]*3,h2=[31.2]*3,u_command=[50.]*3,u_applied=[50.]*3))
    result=regulation_indicators(f)
    assert result['RMSE_ref_h1_cm']==result['RMSE_ref_h2_cm']==result['TV_u_pp']==0
    assert result['inside_h1_s']==result['inside_h2_s']==8 and result['u_mean_pct']==50
    f.h1=[43.4,47.4,51.4];assert regulation_indicators(f)['inside_h1_s']==4

def test_exploration_does_not_mutate_calibration():
    original=calibrated_config();p=list(original.parameters);p[0]*=1.01
    altered=exploratory_config(original,p);assert altered.mode=='exploratorio'
    assert calibrated_config()==original
    assert run_simulation(load_run(),altered).attrs['mode']=='exploratorio'
    assert run_simulation(load_run(),initial=[47.,31.]).attrs['mode']=='exploratorio'
    with pytest.raises(ValueError):exploratory_config(original,[100]*len(p))

def test_no_invented_recovery_and_invalid_inputs():
    assert len(load_run(10))==201
    with pytest.raises(ValueError):load_run(10,'completa')
    f=load_run();f.loc[0,'u']=101
    with pytest.raises(ValueError):run_simulation(f)
    with pytest.raises(ValueError):run_simulation(load_run(),step=.1)

def test_all_model_references_available():
    for name in MODELS:
        y=run_simulation(load_run(),calibrated_config(name));assert np.isfinite(y[['h1','h2']]).all().all()

def test_scenarios_do_not_change_scientific_files():
    record=json.loads((ROOT/'reports/simulador/integridad.json').read_text())
    assert record['unchanged']
    for name,sha in record['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha

def test_decision_is_not_preassigned():
    _,table,_=compare_scenarios(load_run())
    worse=table.copy();worse.loc[worse.scenario!='E0',['RMSE_ref_h1_cm','RMSE_ref_h2_cm']]=1000
    assert decide(worse)['recommended'] is None

def test_streamlit_pages_and_exploratory_controls():
    from streamlit.testing.v1 import AppTest
    at=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
    assert not at.exception
    sections=at.radio(key='section').options
    for section in sections:
        at.radio(key='section').set_value(section).run()
        assert not at.exception,section
    at.radio(key='section').set_value('Modelo matemático').run()
    at.toggle(key='explore').set_value(True).run();assert not at.exception
    at.number_input(key=f'param_{U}_qstar').set_value(1.2)
    at.button(key='apply_parameters').click().run();assert not at.exception
    assert at.session_state['overrides'][U][0]==1.2
    at.button(key='restore_parameters').click().run();assert not at.exception
    assert U not in at.session_state['overrides']
    assert at.number_input(key=f'param_{U}_qstar').value==calibrated_config().parameters[0]
    at.selectbox(key='run').select(10).run();assert not at.exception
    assert at.selectbox(key='window').options==['Excitación · ≈800 s']
