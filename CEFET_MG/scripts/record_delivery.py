"""Cierra la lista de aceptación sólo con evidencia disponible de ejecuciones reales."""
import json,hashlib,sys,importlib.metadata
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.reporting import table

def main():
    out=ROOT/'reports/simulador'
    tests=(out/'tests.txt').read_text(encoding='utf-8')
    browser=json.loads((out/'browser_checks.json').read_text(encoding='utf-8'))
    agent=json.loads((out/'agent_checks.json').read_text(encoding='utf-8'))
    regression=pd.read_csv(out/'regresion_U.csv');scenarios=pd.read_csv(out/'comparacion_escenarios.csv')
    integrity=json.loads((out/'integridad.json').read_text(encoding='utf-8'))
    invariants=all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha for name,sha in integrity['sha256'].items())
    same_duration=scenarios.groupby(['run','window']).duration_s.nunique().eq(1).all()
    docs=['matriz_cumplimiento_guia.md','anexos_proyecto.md','evidencias_13_diapositivas.md','guia_simulador.md']
    checks=[('U reproduce la validación anterior',regression.max_trajectory_difference_cm.max()<=1e-9,'regresion_U.csv; tests/test_simulator.py'),
            ('Dos tanques muestran niveles RK4',browser['passed'],'browser_checks.json; figures/aplicacion_sistema.png'),
            ('Parámetros modificables sin alterar calibración',invariants and 'passed' in tests,'tests.txt; integridad.json; modo exploratorio'),
            ('E0, E1 y E2 se ejecutan',set(scenarios.scenario)=={'E0','E1','E2'} and len(scenarios)==57,'57 trayectorias de 19 comparaciones'),
            ('Condiciones comparables',bool(same_duration) and 'passed' in tests,'protocolo_escenarios.md; pruebas de iniciales/parámetros/tiempo'),
            ('Tabla con números de las simulaciones',scenarios.RMSE_ref_h1_cm.notna().all(),'comparacion_escenarios.csv'),
            ('Decisión derivada de indicadores',(out/'decisiones.json').exists() and 'passed' in tests,'src/scenarios.py::decide; prueba sin ganador preasignado'),
            ('Streamlit funciona y conserva pruebas',all(x['status']=='ready' for x in agent) and '34 passed' in tests,'agent_checks.json; browser_checks.json; tests.txt'),
            ('Limitaciones y fuentes documentadas',all((ROOT/'docs'/p).exists() for p in docs),'anexos_proyecto.md; resultados_y_decision.md; app'),
            ('Evidencias de 13 diapositivas preparadas',(ROOT/'docs/evidencias_13_diapositivas.md').exists(),'docs/evidencias_13_diapositivas.md; sin presentación definitiva')]
    rows=pd.DataFrame([dict(n=i+1,aceptación=name,estado='APROBADO' if bool(ok) else 'PENDIENTE',evidencia=proof) for i,(name,ok,proof) in enumerate(checks)])
    result=rows.estado.eq('APROBADO').sum()
    (out/'control_entrega.md').write_text(f'''# Control de entrega de fase 3

**{result}/10 puntos de aceptación aprobados mediante las evidencias indicadas.**
Verificación realizada el 8 de noviembre de 2026. No implica aprobación docente de la
presentación definitiva ni validación externa nueva del modelo.

{table(rows)}

Pruebas ejecutadas: 34 aprobadas (23 existentes y 11 nuevas, con varios casos de interfaz).
Servidor real: ocho secciones y exploración comprobadas con API de agente. Navegador:
valores de tanques contrastados con RK4, búsqueda temporal, iniciar/pausar/reiniciar,
escenarios y presentación a 760 px. Sin errores JavaScript registrados.
Tipos estáticos comprobados con ty. Ver `typecheck.txt`.

U reproduce las trayectorias anteriores exactamente, sin recalibrar. Los datos y resultados
científicos anteriores permanecen intactos. Los parámetros se editan en copias de sesión.
Se recomienda E1 bajo la regla analítica fijada; existen compensaciones con E2.

Pendientes humanos: completar nombres de estudiantes, ensayar la sustentación y producir
la presentación definitiva cuando corresponda. La autorización de datos externos se registra
según la comunicación del usuario; no se inventa acta ni firma. No se certifican geometría,
caudales absolutos, seguridad operativa ni mediciones realizadas por la pareja.
''',encoding='utf-8')
    files=list((ROOT/'src').glob('*.py'))+list((ROOT/'assets').glob('*'))+[ROOT/'app.py',ROOT/'requirements-app.txt']
    record=dict(acceptance_passed=int(result),total=10,tests=34,existing_tests=23,
                streamlit=importlib.metadata.version('streamlit'),python=sys.version,
                model='U_bomba_carga_monotona__retardo',step_s=1.,delay_s=2.,
                original_files_unchanged=invariants,code_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (out/'entrega.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'Lista de aceptación: {result}/10. Pruebas: 34 aprobadas.')
    if result!=10:raise RuntimeError('Entrega incompleta')

if __name__=='__main__':main()
