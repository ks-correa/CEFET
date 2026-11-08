"""Estados cm; tiempo s; entrada %; caudales efectivos cm/s.

Las topologías hidráulicas son hipótesis, no geometría verificada.
"""
import numpy as np
from numba import njit

HOP = np.array([47.4, 31.2])
NAMES = ['A_lineal', 'B_hidraulico', 'C_bomba', 'D_conservativo']

def specification(model):
    if model in (0, 2):
        # b,c,d,e [1/s], k [cm/(s punto porcentual)], gamma adimensional
        x = [0.005, 0.005, 0.015, 0.02, 0.015]
        lo, hi = [1e-6]*5, [0.5]*5
        names = ['b', 'c', 'd', 'e', 'k']
    else:
        # s [sqrt(cm)/s], r=A1/A2 adimensional
        x, lo, hi, names = [0.4, 0.5], [0.001, 0.01], [5., 10.], ['s', 'r']
    if model in (2, 3):
        x += [1.]; lo += [0.2]; hi += [4.]; names += ['gamma']
    return np.array(x), np.array(lo), np.array(hi), names

@njit(cache=True)
def rhs(y, u, p, model):
    if model == 0 or model == 2:
        b,c,d,e,k = p[:5]
        a = b*c/d + e  # traza<0, determinante=e*d>0
        v = u-50. if model == 0 else 50.*((max(u,0.)/50.)**p[5]-1.)
        x1,x2 = y[0]-47.4,y[1]-31.2
        return np.array([-a*x1+b*x2+k*v, c*x1-d*x2])
    s,r = p[:2]
    gamma = 1. if model == 1 else p[2]
    qin = s*np.sqrt(16.2)*(max(u,0.)/50.)**gamma
    q12 = s*np.sqrt(max(y[0]-y[1],0.))
    qout = s*np.sqrt(16.2/31.2)*np.sqrt(max(y[1],0.))
    return np.array([qin-q12, r*(q12-qout)])

def fluxes(y, u, p, model):
    """Q/A1; sólo modelos B,D. No convertir a litros sin A1."""
    if model not in (1,3):
        return np.full((len(y),3), np.nan)
    s,r = p[:2]; g = 1. if model==1 else p[2]
    return np.column_stack([s*np.sqrt(16.2)*(np.maximum(u,0)/50)**g,
                            s*np.sqrt(np.maximum(y[:,0]-y[:,1],0)),
                            s*np.sqrt(16.2/31.2)*np.sqrt(np.maximum(y[:,1],0))])
