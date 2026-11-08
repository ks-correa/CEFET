import hashlib,json
import numpy as np
import pytest
from scipy.linalg import expm
from src.data_processing import ROOT,load
from src.models import rhs,specification,fluxes
from src.rk4_solver import solve
from src.calibration import calibrate
from src.goodness_of_fit import metrics
from src.validation import split_groups

def test_raw_integrity():
    m=json.loads((ROOT/'data/processed/sha256.json').read_text())
    for name,sha in m.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
    original=(ROOT/'LEEME_PRIMERO.md').read_text(encoding='utf-8')
    for sha in m.values():assert sha in original

def test_alignment_and_units():
    ds=load(); assert len(ds['U'])==len(ds['h1'])-1
    np.testing.assert_allclose(ds['U'].t_ref,ds['h1'].t_ref.iloc[:-1])
    assert ds['complete_data'].u.between(0,100).all()
    readme=(ROOT/'data/raw/README.md').read_text()
    assert '(cm)' in readme and 'Ts = 4' in readme
    for i in range(1,11):
        f=__import__('pandas').read_csv(ROOT/f'data/processed/run_{i:02}.csv')
        np.testing.assert_array_equal(f.h1.iloc[:81],ds['h1'].iloc[:,i])

def test_rk4_against_exact_linear_solution_and_convergence():
    p=specification(0)[0]; b,c,d,e,k=p; mat=np.array([[-(b*c/d+e),b],[c,-d]])
    t=np.array([0.,80.]); y0=np.array([49.,30.]); op=np.array([47.4,31.2])
    exact=op+expm(mat*80)@(y0-op)
    errors=[np.max(abs(solve(t,[50.],y0,p,0,h)[-1]-exact)) for h in [8.,4.,2.]]
    assert errors[0]>10*errors[1]>100*errors[2]
    assert errors[-1]<1e-7

def test_causality_and_equilibrium():
    p=specification(3)[0]; op=np.array([47.4,31.2]); t=np.arange(5.)
    np.testing.assert_allclose(solve(t,np.ones(5)*50,op,p,3),np.tile(op,(5,1)))
    y=solve(t,[40,40,40,40,99],op,p,3)
    z=solve(t,[40,40,40,40,0],op,p,3)
    np.testing.assert_array_equal(y,z)

def test_conservation_and_nonnegativity():
    p=specification(3)[0]; t=np.arange(101.)
    y=solve(t,np.ones(101)*30,[47.,31.],p,3)
    assert y.min()>=0
    fl=fluxes(y,np.ones(101)*30,p,3)
    d=np.array([rhs(z,30.,p,3) for z in y])
    np.testing.assert_allclose(d[:,0]+d[:,1]/p[1],fl[:,0]-fl[:,2],atol=1e-12)

def test_metrics_and_groups():
    m=metrics(np.array([1.,2.,3.]),np.array([2.,3.,4.]),2.)
    assert m['MAE']==m['RMSE']==1 and m['NRMSE']==.5 and m['bias']==1
    with pytest.raises(ValueError):split_groups([None]*10,[1,2],[2,3])

def test_calibration_reproducibility_and_improvement():
    import pandas as pd
    f=pd.read_csv(ROOT/'data/processed/run_01.csv').iloc[:81]
    p,s,l=calibrate([f],1,starts=2)
    q,ss,ll=calibrate([f],1,starts=2)
    np.testing.assert_array_equal(p,q)
    assert all(x['success'] for x in l['starts'])
    y=solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,1)
    assert np.mean((y-f[['h1','h2']].values)**2)<np.mean((f[['h1','h2']].values-f[['h1','h2']].iloc[0].values)**2)

def test_model_outputs_and_protocol_separation():
    import pandas as pd
    result=pd.read_csv(ROOT/'reports/metrics.csv')
    for name in ['A_lineal','B_hidraulico','C_bomba','D_conservativo','persistencia','equilibrio']:
        assert name in result.model.values
    primary=result.query("protocol=='principal'")
    assert set(primary.query("role=='desarrollo'").run)==set(range(1,8))
    assert set(primary.query("role=='evaluacion'").run)=={8,9,10}
    for f in (ROOT/'reports').glob('prediction_*.csv'):
        d=pd.read_csv(f); assert np.isfinite(d[['h1_sim','h2_sim']]).all().all()
        assert d[['h1_sim','h2_sim']].min().min()>=0

def test_complete_reproduction():
    record=json.loads((ROOT/'reports/reproducibility.json').read_text())
    assert record['identical'] and record['files_compared']>=40
    assert record['changed']==[]

def test_all_models_numerical_reference_and_robustness():
    import pandas as pd
    data=pd.read_csv(ROOT/'reports/robustness.csv')
    ref=data[data.test=='SciPy_DOP853']
    assert len(ref)==12
    assert ref.max_state_change_cm.max()<1e-4
    pert=data[data.test.str.startswith('inicial')]
    assert np.isfinite(pert.NRMSE).all()
    assert pert.max_state_change_cm.max()<.3

def test_recommended_model_meets_each_evaluation():
    import pandas as pd
    model=json.loads((ROOT/'reports/modelo_recomendado.json').read_text())['model']
    data=pd.read_csv(ROOT/'reports/metrics.csv')
    q=data[(data.model==model)&(data.role=='evaluacion')&data.protocol.isin(['principal','cv'])&data.window.isin(['completa','excitacion'])]
    assert len(q)==52
    assert (q.NRMSE<=.3).all()

def test_training_scale_uses_unique_original_rows():
    import pandas as pd
    from src.calibration import scale_for
    a=pd.read_csv(ROOT/'data/processed/run_01.csv')
    b=pd.read_csv(ROOT/'data/processed/run_02.csv')
    expected=pd.concat([a,b]).drop_duplicates('source_row')[['h1','h2']].values.std(axis=0,ddof=1)
    np.testing.assert_allclose(scale_for([a,b]),expected)

def test_full_excitation_is_repeated_without_independent_duplicates():
    import pandas as pd
    runs=[pd.read_csv(ROOT/f'data/processed/run_{i:02}.csv') for i in range(1,11)]
    for f in runs[1:]:
        np.testing.assert_array_equal(runs[0].u.iloc[:200],f.u.iloc[:200])
    assert all(f.source_row.is_unique for f in runs)
    assert all(runs[i].source_row.iloc[-1]==runs[i+1].source_row.iloc[0] for i in range(9))
