"""Repite el análisis y comprueba identidad de artefactos deterministas."""
import hashlib,json,subprocess,sys
from .data_processing import ROOT

def snapshot():
    files=[ROOT/'reports/metrics.csv',ROOT/'reports/calibration.json',ROOT/'reports/selected_model.json']
    files+=list((ROOT/'data/processed').glob('*.csv'))
    files+=list((ROOT/'reports').glob('prediction_*.csv'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}

def main():
    before=snapshot()
    with (ROOT/'reports/reproduction_execution.log').open('w',encoding='utf-8') as log:
        subprocess.run([sys.executable,'-m','src.experiments'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    after=snapshot(); changed=[p for p in before if before[p]!=after.get(p)]
    result=dict(identical=not changed,files_compared=len(before),changed=changed,sha256=after)
    (ROOT/'reports/reproducibility.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print({k:v for k,v in result.items() if k!='sha256'})
    if changed:raise RuntimeError('Resultados no idénticos')

if __name__=='__main__':main()
