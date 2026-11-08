import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from .models import specification
from .rk4_solver import solve

def scale_for(runs):
    combined=pd.concat(runs,ignore_index=True)
    if 'source_row' in combined:
        combined=combined.drop_duplicates('source_row')
    return combined[['h1','h2']].values.std(axis=0,ddof=1)

def calibrate(runs,model,seed=20261108,starts=4):
    scale=scale_for(runs); x,lo,hi,names=specification(model)
    def residual(p):
        return np.concatenate([((solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,model)
                                 -f[['h1','h2']].values)[1:]/scale).ravel() for f in runs])
    rng=np.random.default_rng(seed); opts=[]; logs=[]
    for i in range(starts):
        initial=np.clip(x*(np.exp(rng.normal(0,0.65,len(x))) if i else 1),lo*1.01,hi*.99)
        fit=least_squares(residual,initial,bounds=(lo,hi),x_scale='jac',max_nfev=500,
                          ftol=1e-9,xtol=1e-9,gtol=1e-9)
        opts.append(fit)
        logs.append(dict(start=i,initial=initial.tolist(),parameters=fit.x.tolist(),
                         cost=float(fit.cost),success=bool(fit.success),message=fit.message,
                         nfev=fit.nfev,optimality=float(fit.optimality)))
    best=min(opts,key=lambda v:v.cost)
    # Jacobiano escalado: sensibilidad relativa; no es CI bajo ruido autocorrelacionado.
    singular=np.linalg.svd(best.jac*best.x,compute_uv=False)
    return best.x,scale,dict(parameters=dict(zip(names,best.x.tolist())),
                            scale_cm=scale.tolist(),starts=logs,
                            singular_values=singular.tolist(),
                            condition=float(singular[0]/singular[-1]),
                            active_bounds=best.active_mask.tolist())
