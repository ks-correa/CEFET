"""Cierra la entrega con evidencias ejecutadas; no altera resultados anteriores."""
import hashlib
import json
from pathlib import Path
import requests
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.documentary_archive import verify_original_manifest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/consolidacion_final'

def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))

def main():
    tests = (OUT / 'tests.txt').read_text(encoding='utf-16')
    assert '46 passed' in tests and 'failed' not in tests
    assert 'All checks passed!' in (OUT / 'typecheck.txt').read_text(encoding='utf-16')
    manifest = read('manifest_historico.json')
    verify_original_manifest(manifest)
    assert read('browser_checks.json')['passed']
    assert all(x['status'] == 'ready' and not x['exceptions'] for x in read('agent_checks.json'))
    assert len(read('esquema_definitivo_13.json')) == 13
    url = 'http://127.0.0.1:8501'
    assert requests.get(url + '/_stcore/health', timeout=10).text == 'ok'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width':1512,'height':1100})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(url)
        page.get_by_text('VERSIÓN VIGENTE', exact=False).wait_for()
        page.get_by_text('Decisión', exact=True).click()
        page.get_by_text('E2 cumple la regla local', exact=False).wait_for()
        page.screenshot(path=str(OUT / 'figures/servidor_activo.png'))
        assert not errors
        browser.close()
    active = dict(url=url, entrypoint='app_final.py', health='ok', decision='E2', browser_errors=errors)
    (OUT / 'server_active.json').write_text(json.dumps(active,indent=2),encoding='utf-8')
    rows = [
        ('Integridad de datos y antecedentes', 'Huellas SHA-256 de %s archivos coinciden; pruebas históricas intactas.' % len(manifest)),
        ('Conservación de parámetros U', 'Configuración exacta conservada; sin ejecutar calibración ni seleccionar nuevos parámetros.'),
        ('Reproducción de validación', 'Trayectorias de corridas 8–10 con diferencia máxima 0 cm frente a las predicciones archivadas.'),
        ('Balances efectivos', 'Pruebas existentes de intercambio compartido y balance total aprobadas; no certifican volumen físico absoluto.'),
        ('Causalidad', 'Retención causal, desfase y transformaciones comprobados; alterar entradas futuras no altera el prefijo.'),
        ('Tres escenarios vigentes', 'E0 observado, E1 atenuación, E2 constante; 19 comparaciones, mismos horizontes y condiciones. S_HIST separado.'),
        ('Correspondencia aplicación/resultados', 'AppTest nueve páginas; API HTTP; navegador: E2 coincide con RK4 y regla calculada. Servidor activo comprobado.'),
        ('Consistencia documental', 'Documentos vigentes recomiendan E2 nominal y declaran revisión retrospectiva. Índice marca informes E1 como históricos preservados.'),
        ('Reproducibilidad', 'Comparación reejecutada contra trayectorias e indicadores guardados; 46 pruebas aprobadas y tipos sin errores.'),
        ('Guía docente', 'Guía contrastada; exactamente 13 diapositivas con ocho campos y fuentes. Esquema preparado; PPT y sustentación pendientes.'),
    ]
    (OUT / 'cumplimiento.json').write_text(json.dumps(dict(tests_passed=46, historical_files_unchanged=len(manifest), checks=[dict(item=a,evidence=b) for a,b in rows], active=active),ensure_ascii=False,indent=2),encoding='utf-8')
    report = '# Informe final de cumplimiento — fase 4\n\n'
    report += 'La implementación y el esquema están listos para revisión. No se generó PowerPoint. Se conservaron los protocolos y resultados históricos; el conjunto vigente se revisó retrospectivamente tras D50, sin modificar la regla ni recalibrar U.\n\n'
    report += '**Resultado ejecutado:** 46 pruebas aprobadas (40 existentes y 6 nuevas), comprobación de tipos aprobada, API y navegador comprobados. Aplicación vigente: http://127.0.0.1:8501 (`app_final.py`; inicio reproducible con `iniciar_entrega_final.ps1`).\n\n'
    report += '| Comprobación | Evidencia y alcance |\n|---|---|\n'
    report += '\n'.join('| %s | %s |' % row for row in rows)
    report += '\n\n## Decisión y límites\n\nE2 constante al 50% fue elegida en 19 comparaciones nominales y 90 exploraciones pequeñas. Esta repetición no constituye validación externa ni demuestra optimalidad global. El equilibrio nominal está incorporado en U; sin demanda externa documentada, mantener el mando es una alternativa legítima. La señal original sirve para identificar la dinámica y no es una obligación operativa documentada.\n\n'
    report += 'La comparación histórica de medias E1/suavizado y su corrección permanecen en `reports/diagnostico_control_constante/`. No se atribuye toda la diferencia histórica a la suavidad: sus medias difieren. Suavizado y atenuación siguen siendo contrafactuales. Una demanda variable, consigna móvil o restricción de servicio podría exigir mando variable, pero no está documentada aquí.\n\n'
    report += 'El sesgo sostenido de −2 pp desplaza el equilibrio calculado a (44.056, 28.624) cm: no hay rechazo perfecto. Las exploraciones iniciales son ±1 cm y los pulsos ±2 pp durante 40 s, aplicados por igual. Se informan excursiones de E0/E1 fuera del rectángulo medido. No se acredita robustez física, ahorro eléctrico ni exactitud fuera del dominio examinado.\n\n'
    report += '## Entregables y pendientes\n\nEsquema: `docs/consolidacion_final/esquema_definitivo_13.md`. Documentación vigente e historial: `docs/consolidacion_final/indice_versiones.md`. Evidencia: `tests.txt`, `typecheck.txt`, `agent_checks.json`, `browser_checks.json`, `server_active.json`, `integridad.json` y figuras de este directorio.\n\nFaltan nombres de integrantes, fecha de sustentación y ensayo oral humano. La aceptación docente de datos externos procede de la comunicación del usuario; no se inventa un acta. No hay fotos propias ni plano certificado. Estas carencias se señalan también en las diapositivas.\n'
    (OUT / 'informe_cumplimiento.md').write_text(report,encoding='utf-8')
    print('Cierre verificado: 46 pruebas; integridad, interfaz y servidor vigente comprobados.')

if __name__ == '__main__':
    main()
