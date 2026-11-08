"""Prueba sobre servidor real: python scripts/verify_simulator.py [URL]."""
import json,sys
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.simulation_engine import load_run,run_simulation

def main():
    url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765'
    out=ROOT/'reports/simulador';out.mkdir(exist_ok=True)
    api=requests.get(url+'/_stcore/agent/openapi.json',timeout=10).json()
    (out/'agent_openapi.json').write_text(json.dumps(api,indent=2),encoding='utf-8')
    session=None;checks=[]
    def interact(**kwargs):
        nonlocal session
        payload=dict(kwargs)
        if session:payload['session_id']=session
        response=requests.post(url+'/_stcore/agent/interact',json=payload,timeout=60)
        response.raise_for_status();body=response.json();session=body['session_id']
        assert body['status']=='ready',body
        def nodes(v):
            if isinstance(v,dict):
                yield v
                for child in v.values():yield from nodes(child)
            elif isinstance(v,list):
                for child in v:yield from nodes(child)
        exceptions=[n for n in nodes(body.get('tree',{})) if n.get('type')=='exception']
        assert not exceptions,exceptions
        checks.append(dict(request=kwargs,status=body['status'],exceptions=exceptions,
                           actions=body.get('actions',[])))
        return body
    interact()
    sections=['Proyecto','Sistema hidráulico','Modelo matemático','Resultados experimentales','Escenarios','Validación y ajuste','Decisión','Fuentes y reproducción']
    for section in sections:interact(widget_state={'section':section})
    interact(widget_state={'section':'Modelo matemático','explore':True})
    interact(widget_state={'param_U_bomba_carga_monotona__retardo_qstar':1.2},trigger={'key':'apply_parameters'})
    interact(widget_state={'explore':False,'run':10})
    interact(widget_state={'section':'Escenarios'})
    (out/'agent_checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1512,'height':1100},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(url);scene=page.locator('.sim');scene.wait_for(timeout=30000)
        expected=run_simulation(load_run())
        assert abs(float(scene.get_attribute('data-h1'))-expected.h1.iloc[0])<1e-9
        seek=page.locator('#seek')
        seek.evaluate('(el)=>{el.value="50";el.dispatchEvent(new Event("input",{bubbles:true}));}')
        assert abs(float(scene.get_attribute('data-h1'))-expected.h1.iloc[50])<1e-9
        page.locator('#reset').click();assert scene.get_attribute('data-index')=='0'
        page.locator('#play').click();page.wait_for_timeout(550);page.locator('#pause').click()
        index=scene.get_attribute('data-index');assert int(index)>0
        page.wait_for_timeout(200);assert scene.get_attribute('data-index')==index
        page.locator('#reset').click();page.screenshot(path=str(out/'figures/aplicacion_sistema.png'),full_page=True)
        page.get_by_text('Escenarios',exact=True).click();page.get_by_text('Tres entradas, condiciones comparables',exact=True).wait_for()
        page.screenshot(path=str(out/'figures/aplicacion_escenarios.png'),full_page=True)
        page.get_by_text('Sistema hidráulico',exact=True).click();page.locator('.sim').wait_for()
        # Sesión nueva: Streamlit adapta automáticamente la barra lateral al ancho inicial.
        mobile=browser.new_page(viewport={'width':760,'height':1050})
        mobile.on('pageerror',lambda error:errors.append(str(error)))
        mobile.goto(url);mobile.locator('.sim').wait_for(timeout=30000)
        mobile.screenshot(path=str(out/'figures/aplicacion_760px.png'),full_page=True);mobile.close()
        assert not errors,errors
        browser.close()
    (out/'browser_checks.json').write_text(json.dumps(dict(passed=True,checks=['RK4→tanques','seek exacto','iniciar','pausar','reiniciar','escenarios','vista 760px'],page_errors=errors),indent=2,ensure_ascii=False),encoding='utf-8')
    print('Servidor: secciones y exploración aprobadas. Navegador: animación sincronizada y capturas verificadas.')

if __name__=='__main__':main()
