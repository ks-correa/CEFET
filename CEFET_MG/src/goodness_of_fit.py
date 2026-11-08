import numpy as np
from scipy.stats import chi2

def metrics(y,p,scale):
    e=p-y; mse=np.mean(e**2); den=np.sum((y-y.mean())**2)
    return dict(MAE=float(np.mean(abs(e))),RMSE=float(np.sqrt(mse)),
                NRMSE=float(np.sqrt(mse)/scale),bias=float(e.mean()),
                max_abs=float(np.max(abs(e))),R2=float(1-np.sum(e**2)/den) if den>0 else None,
                peak_error=float(p.max()-y.max()),final_error=float(e[-1]))

def residual_diagnostics(e,lags=20):
    z=e-e.mean(); den=np.dot(z,z)
    acf=np.array([1.]+[np.dot(z[k:],z[:-k])/den if den>0 else 0. for k in range(1,lags+1)])
    n=len(e); q=n*(n+2)*np.sum(acf[1:]**2/(n-np.arange(1,lags+1)))
    return dict(acf=acf.tolist(),Q=float(q),p_descriptive=float(chi2.sf(q,lags)),lags=lags)
