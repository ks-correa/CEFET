"""RK4 simultáneo con retención causal y partición en discontinuidades."""
import numpy as np
from numba import njit
from .models import rhs

@njit(cache=True)
def simulate(t, u, y0, p, model, step=1.):
    # Cada intervalo observado tiene entrada constante u[i], nunca u[i+1].
    y = np.empty((len(t),2)); y[0] = y0
    for i in range(len(t)-1):
        n = int(np.ceil((t[i+1]-t[i])/step))
        h = (t[i+1]-t[i])/n
        z = y[i].copy()
        for j in range(n):
            k1=rhs(z,u[i],p,model)
            k2=rhs(z+h*k1/2,u[i],p,model)
            k3=rhs(z+h*k2/2,u[i],p,model)
            k4=rhs(z+h*k3,u[i],p,model)
            z=z+h*(k1+2*k2+2*k3+k4)/6
        y[i+1]=z
    return y

def solve(t, u, y0, p, model, step=1.):
    t,u,y0,p=map(lambda x: np.asarray(x,dtype=float),(t,u,y0,p))
    if step<=0 or len(t)<2 or np.any(np.diff(t)<=0) or len(u)<len(t)-1:
        raise ValueError('Tiempo estrictamente creciente, entrada por intervalo y paso positivo requeridos')
    if not all(np.isfinite(x).all() for x in (t,u,y0,p)):
        raise ValueError('Valores no finitos')
    return simulate(t,u,y0,p,model,step)
