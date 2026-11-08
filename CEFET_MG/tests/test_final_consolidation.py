import hashlib
import json
import numpy as np
import pandas as pd
from src.data_processing import ROOT
from src.final_scenarios import SCENARIOS, compare_scenarios, transform_input, smoothing_complement
from src.scenarios import transform_input as original_input, decide
from src.simulation_engine import load_run, calibrated_config

OUT = ROOT / 'reports/consolidacion_final'

def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))

def test_final_history_and_validation_preserved():
    for name, digest in read('manifest_historico.json').items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    assert read('integridad.json')['unchanged']
    scores = pd.read_csv(OUT / 'validacion_U_sin_cambios.csv')
    assert scores.max_trajectory_difference_cm.max() == 0

def test_final_scenario_mapping_and_causality():
    f = load_run(8)
    assert set(SCENARIOS) == {'E0', 'E1', 'E2'}
    for code in ['E0', 'E1']:
        np.testing.assert_array_equal(transform_input(f.t, f.u, code), original_input(f.t, f.u, code))
    np.testing.assert_array_equal(transform_input(f.t, f.u, 'S_HIST'), original_input(f.t, f.u, 'E2'))
    assert (transform_input(f.t, f.u, 'E2') == 50).all()
    future = f.u.copy(); future.iloc[50:] = 70
    for code in [*SCENARIOS, 'S_HIST']:
        np.testing.assert_array_equal(transform_input(f.t, f.u, code)[:50], transform_input(f.t, future, code)[:50])

def test_final_reproduction_and_decision_not_preassigned():
    cfg = calibrated_config()
    f = load_run(8)
    trajectories, table, verdict = compare_scenarios(f)
    stored = pd.read_csv(OUT / 'comparacion_principal.csv')
    stored = stored[(stored.run == 8) & (stored.window == 'excitacion')]
    for code, y in trajectories.items():
        np.testing.assert_array_equal(y.t, f.t)
        np.testing.assert_allclose(y[['h1', 'h2']].iloc[0], f[['h1', 'h2']].iloc[0])
        np.testing.assert_allclose(y.values, pd.read_csv(OUT / f'excitacion_run08_{code}.csv').values, rtol=1e-13, atol=1e-12)
        for metric in ['RMSE_ref_h1_cm', 'RMSE_ref_h2_cm', 'TV_u_pp', 'u_mean_pct']:
            np.testing.assert_allclose(table.loc[table.scenario == code, metric], stored.loc[stored.scenario == code, metric])
    sm, _ = smoothing_complement(f)
    np.testing.assert_allclose(sm.values, pd.read_csv(OUT / 'excitacion_run08_S_HIST.csv').values, rtol=1e-13, atol=1e-12)
    assert cfg == calibrated_config() and verdict['recommended'] == 'E2'
    worse = table.copy()
    worse.loc[worse.scenario != 'E0', ['RMSE_ref_h1_cm', 'RMSE_ref_h2_cm']] = 1000
    assert decide(worse)['recommended'] is None

def test_final_exploration_scope_and_limits():
    nominal = read('decisiones_vigentes.json')
    sensitivity = read('robustez/decisiones.json')
    assert len(nominal) == 19 and all(x['recommended'] == 'E2' for x in nominal)
    assert len(sensitivity) == 90 and all(x['exploratory'] for x in sensitivity)
    local = read('robustez/analisis_local.json')
    assert all(x[0] < 0 for x in local['eigenvalues'])
    assert local['constant_48_equilibrium'][0] < 45
    ranges = pd.read_csv(OUT / 'robustez/rangos.csv')
    assert ranges.samples_outside_measured_rectangle.sum() > 0
    assert ranges[ranges.scenario == 'E2'].samples_outside_measured_rectangle.sum() == 0

def test_final_outline_has_thirteen_traceable_slides():
    slides = read('esquema_definitivo_13.json')
    assert [x['n'] for x in slides] == list(range(1, 14))
    for slide in slides:
        for field in ['title', 'objective', 'content', 'evidence', 'source', 'limitations', 'verifiable_data', 'oral_explanation']:
            assert slide[field]
        assert all(source.startswith('https://') or (ROOT / source).exists() for source in slide['source'])

def test_final_streamlit_all_pages_and_current_decision():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / 'app_final.py'), default_timeout=30).run()
    assert not at.exception
    sections = at.radio(key='section').options
    assert len(sections) == 9
    for section in sections:
        at.radio(key='section').set_value(section).run()
        assert not at.exception, section
    at.radio(key='section').set_value('Decisión').run()
    assert any('E2 cumple la regla local' in item.value for item in at.info)
    at.radio(key='section').set_value('Sistema hidráulico').run()
    at.segmented_control(key='scenario').set_value('E2').run()
    assert not at.exception
