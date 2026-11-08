"""Modelos avanzados aislados: ningún cambio a C/D ni a archivos de primera etapa."""
from dataclasses import dataclass
import numpy as np
from numba import njit

@dataclass
class Spec:
    code:int
    names:tuple
    x:tuple
    lo:tuple
    hi:tuple
    hypothesis:str

BASE=('qstar','r','gamma'); X=(1.2,.3,.8); LO=(.01,.03,.2); HI=(10.,3.,2.)
SPECS={
 'E_lineal_raiz':Spec(0,BASE,X,LO,HI,'Transferencia proporcional al desnivel; salida gravitacional'),
 'F_exponentes':Spec(1,BASE+('m','n'),X+(.8,.5),LO+(.5,.5),HI+(1.,1.),'Leyes efectivas de cabeza con exponente entre laminar y raíz'),
 'G_resistencia_mixta':Spec(2,BASE+('lambda12',),X+(.5,),LO+(0.,),HI+(1.,),'Pérdida de carga lineal más cuadrática en conexión'),
 'H_doble_resistencia':Spec(3,BASE+('lambda12','lambda_out'),X+(.5,.1),LO+(0.,0.),HI+(1.,1.),'Resistencias mixtas en conexión y salida'),
 'I_bomba_monotona':Spec(4,('qstar','r','b','c'),(1.2,.3,.7,.5),(.01,.03,.03,.03),(10.,3.,20.,20.),'Transferencia lineal, salida raíz, curva cúbica monótona'),
 'J_flexible_restringido':Spec(5,('qstar','r','b','c','m','n'),(1.2,.3,.7,.5,.8,.5),(.01,.03,.03,.03,.5,.5),(10.,3.,20.,20.,1.,1.),'Exponentes acotados y curva cúbica monótona'),
 'K_zona_muerta':Spec(6,BASE+('deadzone_pct',),X+(1.,),LO+(0.,),HI+(15.,),'Zona muerta efectiva, no certificada; transferencia lineal'),
 'L_cabeza_efectiva':Spec(7,BASE+('offset_cm',),X+(0.,),LO+(-10.,),HI+(10.,),'Desfase efectivo de cotas entre tanques; no geometría identificada'),
 'M_cascada':Spec(8,BASE,X,LO,HI,'Descarga de T1 independiente de T2; cascada sin contrapresión'),
 'O_bomba_saturante':Spec(9,('qstar','r','beta'),(1.2,.3,.5),(.01,.03,.001),(10.,3.,3.),'Bomba exponencial saturante, conexión lineal'),
 'P_D_bomba_monotona':Spec(10,('qstar','r','b','c'),(1.2,.3,.7,.5),(.01,.03,.03,.03),(10.,3.,20.,20.),'Transferencia/salida raíz como D, curva cúbica monótona'),
 'Q_balance_local':Spec(11,('qstar','r','k12','kout','gamma'),(1.15,.3,.034,.014,.8),(.01,.03,.001,.001,.2),(10.,3.,.2,.2,2.),'Conductancias locales positivas, transferencia por desnivel y salida linealizadas'),
 'R_balance_monotono':Spec(12,('qstar','r','k12','kout','b','c'),(1.15,.3,.034,.014,.7,.5),(.01,.03,.001,.001,.03,.03),(10.,3.,.2,.2,20.,20.),'Balances con conductancias locales y bomba cúbica monótona'),
 'S_balance_empirico_C':Spec(13,('qstar','r','a','b','kout','gamma'),(1.15,.3,.035,.031,.014,.8),(.01,.03,.001,.001,.001,.2),(10.,3.,.2,.2,.2,2.),'Realización local conservativa de C con transferencia empírica no sólo función del desnivel'),
 'T_bomba_carga_local':Spec(14,('qstar','r','k12','kout','kpump','gamma'),(1.15,.34,.031,.01,.004,.8),(.01,.03,.001,.001,0.,.2),(10.,3.,.2,.2,.1,2.),'Balance local: bomba decreciente con carga h1 y transferencia por desnivel'),
 'U_bomba_carga_monotona':Spec(15,('qstar','r','k12','kout','kpump','b','c'),(1.15,.34,.031,.01,.004,.7,.5),(.01,.03,.001,.001,0.,.03,.03),(10.,3.,.2,.2,.1,20.,20.),'Balance local: bomba cúbica monótona con corrección de carga h1'),
}

@njit(cache=True)
def mixed_flow(v,lam):
    if v<=0.:return 0.
    return 2*v/(lam+np.sqrt(lam*lam+4*(1-lam)*v))

@njit(cache=True)
def pump(u,p,code):
    x=max(u,0.)/50.
    if code==11:return p[0]*x**p[4]
    if code==13:return p[0]*x**p[5]
    if code==14:return p[0]*x**p[5]
    if code==12 or code==15:
        b,c=(p[4],p[5]) if code==12 else (p[5],p[6]); z=x/2
        value=z+(b-1)*z*z+(1-2*b+c)*z*z*z/3
        ref=.5+(b-1)*.25+(1-2*b+c)/24
        return p[0]*value/ref
    if code==4 or code==5 or code==10:
        b,c=p[2],p[3]; z=x/2
        value=z+(b-1)*z*z+(1-2*b+c)*z*z*z/3
        ref=.5+(b-1)*.25+(1-2*b+c)/24
        return p[0]*value/ref
    if code==6:
        return p[0]*(max(u-p[3],0.)/(50-p[3]))**p[2]
    if code==9:
        return p[0]*(-np.expm1(-p[2]*x))/(-np.expm1(-p[2]))
    return p[0]*x**p[2]

@njit(cache=True)
def hydraulic(y,p,code):
    delta=max(y[0]-y[1],0.)/16.2; head=max(y[1],0.)/31.2
    if code==11 or code==12 or code==14 or code==15:
        q12=max(0.,p[0]+p[2]*(y[0]-y[1]-16.2)); qout=max(0.,p[0]+p[3]*(y[1]-31.2))
    elif code==13:
        q12=max(0.,p[0]+p[2]*(y[0]-47.4)-p[3]*(y[1]-31.2));qout=max(0.,p[0]+p[4]*(y[1]-31.2))
    elif code==0 or code==4 or code==6 or code==9:
        q12=p[0]*delta; qout=p[0]*np.sqrt(head)
    elif code==1:
        q12=p[0]*delta**p[3]; qout=p[0]*head**p[4]
    elif code==5:
        q12=p[0]*delta**p[4]; qout=p[0]*head**p[5]
    elif code==2 or code==3:
        q12=p[0]*mixed_flow(delta,p[3]); qout=p[0]*(mixed_flow(head,p[4]) if code==3 else np.sqrt(head))
    elif code==7:
        q12=p[0]*np.sqrt(max(y[0]-y[1]-p[3],0.)/(16.2-p[3])); qout=p[0]*np.sqrt(head)
    elif code==8:
        q12=p[0]*np.sqrt(max(y[0],0.)/47.4); qout=p[0]*np.sqrt(head)
    else:
        q12=p[0]*np.sqrt(delta); qout=p[0]*np.sqrt(head)
    return q12,qout

@njit(cache=True)
def rhs(y,u,p,code,tau=0.):
    q12,qout=hydraulic(y,p,code); command=pump(u,p,code)
    if code==14 or code==15:command=max(0.,command-p[4]*(y[0]-47.4))
    qin=y[2] if tau>0 else command
    return np.array([qin-q12,p[1]*(q12-qout),(command-y[2])/tau if tau>0 else 0.])

@njit(cache=True)
def integrate_grid(grid,controls,y0,p,code,step,tau):
    y=np.empty((len(grid),3)); y[0,0:2]=y0
    y[0,2]=pump(50.,p,code)  # historia local previa al experimento
    for i in range(len(grid)-1):
        effective=min(step,tau/4) if tau>0 else step
        n=int(np.ceil((grid[i+1]-grid[i])/effective)); h=(grid[i+1]-grid[i])/n; z=y[i].copy()
        for k in range(n):
            k1=rhs(z,controls[i],p,code,tau)
            k2=rhs(z+h*k1/2,controls[i],p,code,tau)
            k3=rhs(z+h*k2/2,controls[i],p,code,tau)
            k4=rhs(z+h*k3,controls[i],p,code,tau)
            z+=h*(k1+2*k2+2*k3+k4)/6
        y[i+1]=z
    return y

def event_grid(t,u,delay=0.,pre=50.):
    t=np.asarray(t,dtype=float); u=np.asarray(u,dtype=float)
    changes=np.r_[True,u[1:]!=u[:-1]]
    events=t[changes]+delay; values=u[changes]
    inside=events[(events>=t[0])&(events<=t[-1])]
    grid=np.unique(np.r_[t,inside]); idx=np.searchsorted(events,grid,side='right')-1
    controls=np.where(idx>=0,values[np.maximum(idx,0)],pre)
    return grid,controls,np.searchsorted(grid,t)

def simulate(f,p,name,step=1.,delay=0.,tau=0.,initial=None):
    if step<=0 or delay<0 or tau<0:raise ValueError('Paso positivo y dinámica causal')
    grid,u,indices=event_grid(f.t.values,f.u.values,delay)
    initial=f[['h1','h2']].iloc[0].values if initial is None else np.asarray(initial,dtype=float)
    full=integrate_grid(grid,u,initial,np.asarray(p),SPECS[name].code,step,tau)
    return full[indices,:2]
