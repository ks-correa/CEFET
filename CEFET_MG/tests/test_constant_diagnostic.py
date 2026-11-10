from src.documentary_archive import verify_original_manifest, archived_bytes
import json,hashlib
import numpy as np
import pandas as pd
from src.data_processing import ROOT
from src.constant_control_diagnostic import OUT,corrected_E2
from src.simulation_engine import load_run,calibrated_config,run_simulation
from src.precision_models import rhs,pump

def test_preexisting_files_preserved_including_original_protocols():
    original=json.loads((OUT/'manifest_previo.json').read_text())
    assert len(original)>600
    normalized={p.replace('\\','/') for p in original}
    assert 'docs/protocolo_escenarios.md' in normalized
    assert 'reports/simulador/decisiones.json' in normalized
    verify_original_manifest(original)

def test_constant_uses_same_configuration_and_compares_every_window():
    cfg=calibrated_config();record=json.loads((OUT/'configuracion.json').read_text())
    assert tuple(record['parameters'].values())==cfg.parameters
    assert record['step_s']==1 and record['delay_s']==cfg.delay
    table=pd.read_csv(OUT/'comparacion_complementaria.csv')
    assert len(table)==76 and set(table.scenario)=={'E0','E1','E2','D50'}
    assert len(table.groupby(['run','window']))==19
    for (rid,window),group in table.groupby(['run','window']):
        assert group.duration_s.nunique()==1
        f=load_run(int(rid),window);y=pd.read_csv(OUT/f'{window}_run{int(rid):02}_D50.csv')
        np.testing.assert_array_equal(y.t,f.t)
        np.testing.assert_allclose(y[['h1','h2']].iloc[0],f[['h1','h2']].iloc[0],atol=1e-12)
        assert y.u_command.eq(50).all() and y.u_applied.eq(50).all()
        assert np.isfinite(y.values).all() and y[['h1','h2']].min().min()>0

def test_historical_results_copied_without_changing_metrics():
    old=pd.read_csv(ROOT/'reports/simulador/comparacion_escenarios.csv')
    diagnostic=pd.read_csv(OUT/'comparacion_complementaria.csv')
    columns=['run','window','scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']
    a=old[columns].sort_values(columns[:3]).reset_index(drop=True)
    b=diagnostic[diagnostic.scenario!='D50'][columns].sort_values(columns[:3]).reset_index(drop=True)
    pd.testing.assert_frame_equal(a,b)

def test_equilibrium_is_model_property_not_new_accuracy_measurement():
    p=np.array(calibrated_config().parameters);y=np.array([47.4,31.2,pump(50.,p,15)])
    np.testing.assert_allclose(rhs(y,50.,p,15),0.,atol=1e-14)
    table=pd.read_csv(OUT/'comparacion_complementaria.csv')
    constant=table[table.scenario=='D50']
    assert constant.TV_u_pp.eq(0).all() and constant.effort_pp2_s.eq(0).all()
    np.testing.assert_allclose(constant.u_mean_pct,50.,atol=1e-12,rtol=0)
    assert 'NRMSE' not in table.columns  # No se inventa error de predicción para el contrafactual.

def test_complementary_decision_and_mean_diagnostic_are_separate():
    choices=json.loads((OUT/'decisiones_complementarias.json').read_text())
    assert all(x['original_choice']=='E1' for x in choices)
    assert all(x['supplementary_choice']=='D50' for x in choices)
    original=json.loads((ROOT/'reports/simulador/decisiones.json').read_text())
    assert all(x['recommended']=='E1' for x in original)
    m=pd.read_csv(OUT/'interpretacion_media.csv')
    assert abs(m.mean_gap_corrected_E1_pp).max()<.002
    assert (m.mean_gap_E2_E1_pp>0).all()
    f=load_run(8);g=f.copy();g.loc[g.index[50:],'u']=50
    offset=json.loads((OUT/'configuracion.json').read_text())['offsets']['excitacion']['offset_pp']
    np.testing.assert_array_equal(corrected_E2(f,offset)[:50],corrected_E2(g,offset)[:50])

def test_new_diagnostic_reproducibility_and_reference_integrator():
    q=json.loads((OUT/'integridad_y_verificacion.json').read_text())
    assert q['unchanged'] and all(x['exact'] for x in q['reproducibility'])
    assert max(x['max_difference_cm'] for x in q['DOP853'])<2e-6
    f=load_run(8);f['u']=50
    np.testing.assert_array_equal(run_simulation(f).values,run_simulation(f).values)
