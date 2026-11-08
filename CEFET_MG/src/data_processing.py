from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def load():
    return {p.stem:pd.read_csv(p) for p in (ROOT/'data/raw').glob('*.csv')}

def audit():
    ds=load(); d=ds['complete_data']; a,b,u=ds['h1'],ds['h2'],ds['U']
    out=ROOT/'data/processed'; out.mkdir(parents=True,exist_ok=True)
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (ROOT/'data/raw').iterdir() if p.is_file()}
    (out/'sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    starts=np.where(np.isclose(d.u,u.U.iloc[0]) & ~np.isclose(d.u.shift(1),u.U.iloc[0]))[0]
    runs=[]; mapping=[]
    for j,start in enumerate(starts):
        stop=min(start+425,len(d)-1)
        f=d.iloc[start:stop+1].copy(); f['source_row']=np.arange(start,stop+1)
        f['t_absolute']=f.t; f.t-=f.t.iloc[0]; f['run']=j+1
        runs.append(f)
        assert np.allclose(f.u.iloc[:80],u.U)
        assert np.array_equal(f[['h1','h2']].iloc[:81].values,
                              np.column_stack([a.iloc[:,j+1],b.iloc[:,j+1]]))
        f.to_csv(out/f'run_{j+1:02}.csv',index=False)
        mapping.append(dict(run=j+1,start_row=int(start),end_row=int(stop),
                            duration_s=float(f.t.iloc[-1]),h1_initial=float(f.h1.iloc[0]),
                            h2_initial=float(f.h2.iloc[0]),short_exact_match=True,
                            excitation_intervals=200,recovery_complete=bool(j<9)))
    pd.DataFrame(mapping).to_csv(out/'run_mapping.csv',index=False)
    d.iloc[:starts[0]+1].to_csv(out/'startup.csv',index=False)
    stats={}
    for name,f in ds.items():
        dt=np.diff(f.iloc[:,0]); f.describe().to_csv(out/f'{name}_statistics.csv')
        stats[name]=dict(shape=list(f.shape),columns=list(f.columns),
                         types={c:str(t) for c,t in f.dtypes.items()},
                         missing=int(f.isna().sum().sum()),duplicate_rows=int(f.duplicated().sum()),
                         duplicate_times=int(f.iloc[:,0].duplicated().sum()),
                         dt_min=float(dt.min()),dt_max=float(dt.max()),
                         time_reversals=int((dt<=0).sum()),gaps_gt6=int((dt>6).sum()))
    stats['quantization_cm']={c:float(np.min(np.diff(np.unique(d[c])))) for c in ['h1','h2']}
    stats['repetition_std_cm']={c:float(ds[c].iloc[:,1:].std(axis=1,ddof=1).mean()) for c in ['h1','h2']}
    (out/'audit.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    return ds,runs,stats,mapping
