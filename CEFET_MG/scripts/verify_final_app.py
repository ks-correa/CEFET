"""Comprobación HTTP y navegador de la versión vigente, sin tocar evidencia histórica."""
import sys,json
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.simulation_engine import load_run
from src.final_scenarios import compare_scenarios

def main():
    url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766'
    out=ROOT/'reports/consolidacion_final';fig=out/'figures';fig.mkdir(exist_ok=True)
    api=requests.get(url+'/_stcore/agent/openapi.json',timeout=10).json()
    (out/'agent_openapi.json').write_text(json.dumps(api,indent=2),encoding='utf-8')
    session=None;checks=[]
    def interact(**kwargs):
        nonlocal session
        payload=dict(kwargs)
        if session:payload['session_id']=session
        response=requests.post(url+'/_stcore/agent/interact',json=payload,timeout=60);response.raise_for_status()
        body=response.json();session=body['session_id'];assert body['status']=='ready',body
        def nodes(obj):
            if isinstance(obj,dict):
                yield obj
                for v in obj.values():yield from nodes(v)
            elif isinstance(obj,list):
                for v in obj:yield from nodes(v)
        exceptions=[n for n in nodes(body['tree']) if n.get('type')=='exception'];assert not exceptions
        text=json.dumps(body['tree'],ensure_ascii=False)
        checks.append(dict(request=kwargs,status=body['status'],exceptions=exceptions,actions=body.get('actions',[])))
        return text
    interact()
    for section in ['Proyecto','Sistema hidráulico','Modelo matemático','Resultados experimentales','Escenarios','Análisis complementarios','Validación y ajuste','Decisión','Fuentes y reproducción']:
        text=interact(widget_state={'section':section})
        if section=='Decisión':assert 'E2 cumple la regla local' in text and 'E2 evita la excitación' in text
        if section=='Escenarios':assert 'mando constante al 50%' in text
    interact(widget_state={'section':'Sistema hidráulico'})
    interact(widget_state={'scenario':'E2 · Operación constante al 50%'})
    interact(widget_state={'run':10})
    interact(widget_state={'section':'Modelo matemático','explore':True})
    interact(widget_state={'param_U_bomba_carga_monotona__retardo_qstar':1.2},trigger={'key':'apply_parameters'})
    interact(widget_state={'section':'Decisión'})
    (out/'agent_checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1512,'height':1100})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(url);page.locator('.sim').wait_for(timeout=30000)
        page.get_by_text('E2 · Operación constante al 50%',exact=True).click()
        scene=page.locator('.sim');page.get_by_text('E2: entrada hipotética y respuesta contrafactual simulada; no ensayada físicamente.',exact=True).wait_for()
        expected=compare_scenarios(load_run())[0]['E2']
        page.locator('#seek').evaluate('(el)=>{el.value="50";el.dispatchEvent(new Event("input",{bubbles:true}));}')
        assert abs(float(scene.get_attribute('data-h1'))-expected.h1.iloc[50])<1e-9
        assert page.locator('#input').text_content()=='50.00 %'
        page.locator('#reset').click();page.locator('#play').click();page.wait_for_timeout(450);page.locator('#pause').click()
        index=scene.get_attribute('data-index');assert int(index)>0
        page.wait_for_timeout(150);assert scene.get_attribute('data-index')==index
        page.locator('#reset').click();page.screenshot(path=str(fig/'aplicacion_vigente.png'),full_page=True)
        page.get_by_text('Decisión',exact=True).click();page.get_by_text('E2 evita la excitación',exact=False).wait_for()
        page.screenshot(path=str(fig/'decision_vigente.png'),full_page=True)
        page.get_by_text('Análisis complementarios',exact=True).click();page.get_by_text('Historia y límites de la decisión',exact=True).wait_for()
        page.screenshot(path=str(fig/'complementarios.png'),full_page=True)
        assert not errors,errors;browser.close()
    (out/'browser_checks.json').write_text(json.dumps(dict(passed=True,page_errors=errors,E2_matches_RK4=True,decision='E2',historical_smoothing_separate=True),indent=2),encoding='utf-8')
    print('Versión vigente: E2 constante, decisión y complementarios verificados en servidor y navegador.')

if __name__=='__main__':main()
