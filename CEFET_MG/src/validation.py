import numpy as np
from .goodness_of_fit import metrics
from .rk4_solver import solve

def predict(f,p,model):
    return solve(f.t.values,f.u.values,f[['h1','h2']].iloc[0].values,p,model)

def evaluate(f,yhat,scale,**labels):
    return [dict(**labels,tank=c,**metrics(f[c].values,yhat[:,j],scale[j]))
            for j,c in enumerate(['h1','h2'])]

def split_groups(runs,train_ids,test_ids):
    if set(train_ids)&set(test_ids): raise ValueError('Fuga entre grupos')
    return [runs[i-1] for i in train_ids],[runs[i-1] for i in test_ids]
