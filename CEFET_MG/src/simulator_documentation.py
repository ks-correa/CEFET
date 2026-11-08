"""Documentación de fase 3 derivada de resultados ya ejecutados."""
import json
import pandas as pd
from .data_processing import ROOT
from .simulation_engine import calibrated_config,U
from .reporting import table

OUT=ROOT/'reports/simulador'
def write(path,text):path.write_text(text,encoding='utf-8')
def update(path,addition):
    text=path.read_text(encoding='utf-8').split('## Actualización de fase 3')[0].rstrip()
    write(path,text+'\n\n## Actualización de fase 3\n\n'+addition+'\n')

def main():
    c=calibrated_config();metrics=pd.read_csv(OUT/'comparacion_escenarios.csv')
    regression=pd.read_csv(OUT/'regresion_U.csv');decisions=pd.read_json(OUT/'decisiones.json')
    example=metrics[(metrics.run==8)&(metrics.window=='excitacion')]
    averages=metrics[metrics.window=='excitacion'].groupby('scenario')[['RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','TV_u_pp','effort_pp2_s']].mean().reset_index()
    selected=decisions.groupby(['window','recommended'],dropna=False).size().to_frame('comparaciones').reset_index()
    scientific=regression.groupby('tank')[['MAE','RMSE','NRMSE','bias']].mean().reset_index()
    units={'qstar':'cm/s (Q/A1)','r':'adimensional (A1/A2)','k12':'s⁻¹','kout':'s⁻¹','kpump':'s⁻¹','b':'adimensional','c':'adimensional'}
    parameters=pd.DataFrame([dict(símbolo=k,valor=f'{v:.17g}',unidad=units[k],fuente='all_fits.json → U → principal') for k,v in zip(c.names,c.parameters)])
    parameters.to_csv(OUT/'parametros_U.csv',index=False)
    write(OUT/'resultados_y_decision.md',f'''# Resultados ejecutados y decisión de escenarios

Modelo U exacto, sin reajuste. Primero se fijaron `docs/protocolo_escenarios.md` y la regla
de comparación. Se simularon las diez excitaciones completas y nueve corridas con recuperación.
Los 57 CSV de trayectorias contienen niveles, mando registrado/modificado, entrada tras el
desfase, caudales efectivos, derivadas y residuos de balance. E1/E2 son contrafactuales, no mediciones.

## Regresión científica

{table(scientific)}

Estas cifras son medias por corrida de evaluación 8–10 completas. Diferencia máxima frente
a las trayectorias U originales: {regression.max_trajectory_difference_cm.max():.3g} cm.
Tolerancia exigida: 1e-9 cm de trayectoria y 1e-10 en métricas; el resultado observado es exacto.
No se recalibró ni se cambió la escala de entrenamiento.

## Excitación de la corrida 8

{table(example[['scenario','RMSE_ref_h1_cm','RMSE_ref_h2_cm','u_mean_pct','u_mean_difference_pp','TV_u_pp','effort_pp2_s']])}

Estos RMSE son de regulación respecto a 47.4/31.2 cm, distintos de RMSE de predicción.
Frente a E0, E1 reduce RMSE de regulación en h1 {abs(example.iloc[1].RMSE_ref_h1_cm_change_pct):.2f}%
y en h2 {abs(example.iloc[1].RMSE_ref_h2_cm_change_pct):.2f}%, con diferencia de mando medio
{example.iloc[1].u_mean_difference_pp:.4f} puntos porcentuales y reducción de TV del mando 20%.
No se explica la mejora simplemente por una gran disminución de mando medio.

## Diez excitaciones, media de indicadores por corrida

{table(averages)}

Resultado de la regla por ventana:

{table(selected)}

La regla predefinida selecciona E1 en las 19 comparaciones ejecutadas. Eso no demuestra que
E1 sea óptimo entre todas las políticas posibles ni que funcione físicamente en el laboratorio.
E1 es la recomendación académica local bajo estas preferencias y este modelo.

Hay compensaciones: E2 reduce más la variación total de h1 y el índice integral de esfuerzo
en la corrida 8 que E1, pero regula peor ambos niveles. Su máximo h1 es
{example.iloc[2].max_h1_cm:.4f} cm frente a {example.iloc[0].max_h1_cm:.4f} cm de E0;
su máximo h2 también aumenta. El suavizado causal no garantiza menores picos.
El índice integral de (u−50)² no mide energía eléctrica ni caudal en litros.
Las bandas ±2 cm son criterios de análisis, no seguridad certificada.

Limitaciones: circuito y áreas sin verificar, conductancias locales, desfase efectivo sin
certificación física, residuos autocorrelacionados, mala extrapolación de arranque y dependencia
de una única entrada repetida. E1/E2 modifican esa señal: su evaluación es contrafactual,
no una nueva validación experimental. Los cambios de parámetros en la app son exploratorios.
''')
    write(ROOT/'docs/anexos_proyecto.md',f'''# Anexos de la guía académica

## Anexo A Propuesta y datos del sistema

Título: modelado continuo de dos tanques CEFET-MG y comparación de señales de bomba.
Integrantes: completar los nombres de los dos estudiantes antes de entregar.
Sistema real: dos tanques cilíndricos acoplados de CEFET-MG, Divinópolis, Brasil; capacidad
nominal documentada de 200 L por tanque. No se deducen áreas a partir de esa capacidad.
Pregunta: ¿qué modificación causal del mando reduce desviaciones locales de ambos niveles?
Variables: h1/h2 cm, t s, u %. Herramienta: Python, RK4 y Streamlit.

**Uso de mediciones externas autorizado por el docente**, según la comunicación explícita
del usuario en las instrucciones de fase 3. No se recibió un acta ni fecha de autorización:
no se inventan firma o documento. No equivale a afirmar aprobación formal de cada detalle
de la propuesta. Los investigadores realizaron las mediciones, no los estudiantes.
Instrumento específico y fecha de adquisición no publicados en el material disponible.
La pareja verifica, modela y compara registros secundarios con trazabilidad SHA256.

## Anexo B Variables y parámetros

h1,h2: estados en cm; t: s; u: %; h*=(47.4,31.2) cm; u*=50%.
q=Q/A1: flujos efectivos cm/s, sin conversión a litros/s. Condiciones iniciales: primer
estado observado de la corrida seleccionada, aplicado una sola vez. Desfase δ=2 s,
efectivo; historia de mando previa a t=0: 50%. Parámetros exactos:

{table(parameters)}

Fuente: `reports/optimizacion_precision/all_fits.json`, modelo {U}, sección principal.
Los archivos originales no se editan al modificar parámetros en la aplicación.
El balance d(h1+h2/r)/dt=qin−qout es una identidad efectiva del modelo, sin volumen absoluto certificado.

## Anexo C Escenarios e indicadores

E0: señal experimental, condiciones iniciales de la misma corrida.
E1: 50+0.8(u0−50), hipótesis de atenuación del 20%.
E2: límite causal 10 pp/4 s; primera actualización desde 50%, posteriores según dt real.
Cada mando permanece constante hasta el siguiente registro; después se aplica δ=2 s.
Mismos parámetros, h0, tiempos, paso y referencias para los tres escenarios.
Principal: 800 s registrados; recuperación sólo en corridas 1–9, nunca se inventa en 10.

Indicadores y regla fijados en `docs/protocolo_escenarios.md`. Tablas completas ejecutadas
en `reports/simulador/comparacion_escenarios.csv`; decisión en resultados_y_decision.md.
No confundir reproducción de observaciones con desviación del objetivo de regulación.
''')
    write(ROOT/'docs/guia_simulador.md','''# Ejecutar y reproducir el simulador

Desde CEFET_MG, ejecutar `iniciar_simulador.ps1` con PowerShell. Busca el entorno .venv
local o el de la carpeta padre y abre Streamlit en http://127.0.0.1:8501.
Alternativamente: `../.venv/Scripts/python.exe -m streamlit run app.py`.

Instalación limpia con uv:

```powershell
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -r requirements-app.txt
.venv/Scripts/python.exe -m src.simulator_delivery
.venv/Scripts/python.exe -m streamlit run app.py
```

La barra lateral selecciona corrida, horizonte, modelo y paso. U es principal;
C/D/P permanecen como referencias. La corrida 10 sólo admite excitación.
Sistema hidráulico muestra E0/E1/E2 y reproduce estados RK4 con Iniciar/Pausar/Reiniciar,
velocidad y búsqueda temporal. El esquema no es una fotografía ni una geometría certificada.
En pantallas estrechas, cerrar la barra lateral para ampliar la escena.

Modelo matemático permite activar modo exploratorio y editar una copia de parámetros e
iniciales. Aplicar exploración calcula nuevos estados; restaurar copia calibrada recupera
los valores originales. Desactivar el modo usa siempre la configuración calibrada.
No se escribe en archivos calibrados. Las configuraciones exploratorias pierden el distintivo
calibrado y pueden fallar fuera del dominio local, lo que se muestra como error de configuración.

Resultados experimentales calcula métricas para la corrida y ventana elegidas. Validación
y ajuste presenta además los agregados históricos congelados y la ACF del caso activo.
Escenarios/Decisión usa exclusivamente U y deriva la recomendación de indicadores reales
calculados. Las descargas distinguen trayectorias, tabla comparativa y configuración.

Pruebas y evidencia, sin repetir calibraciones:

```powershell
.venv/Scripts/python.exe -m src.simulator_delivery
.venv/Scripts/python.exe -m pytest -q tests
.venv/Scripts/python.exe -m src.simulator_documentation
```

La prueba de navegador requiere requirements-dev.txt y `python -m playwright install chromium`.
Iniciar una instancia de comprobación separada:

```powershell
.venv/Scripts/python.exe -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=8765 --server.enableAgentApi=true
.venv/Scripts/python.exe scripts/verify_simulator.py
```

La API de agente sólo se habilita en esa instancia de prueba. No se activa en el lanzador.
`reports/simulador/` conserva regresión, indicadores, decisiones, integridad y capturas.
La autorización de datos externos se registra en anexo A. La aplicación no mide en vivo.
''')
    mapping=[('Portada','docs/anexos_proyecto.md','Completar nombres y fecha de sustentación'),
        ('Problema y pregunta','docs/definicion_problema.md','Decisión local de regulación'),
        ('Esquema del sistema','assets/tanks.html; figures/aplicacion_sistema.png','Esquema conceptual; topología no certificada'),
        ('Datos reales','data/raw/README.md; reports/auditoria_dataset.md','Mediciones de investigadores; sin fotos propias'),
        ('Variables y parámetros','reports/simulador/parametros_U.csv; docs/anexos_proyecto.md','Valores exactos y unidades efectivas'),
        ('Modelo matemático','src/precision_models.py (código 15); docs/modelo_matematico.md','Balances locales, no volumen absoluto certificado'),
        ('Implementación','src/simulation_engine.py; reports/simulador/tests.txt','RK4 reutilizado; entrada causal con δ=2 s'),
        ('Calibración','reports/optimizacion_precision/fit_U_bomba_carga_monotona__retardo.json','No se reajustó para escenarios'),
        ('Validación','reports/simulador/regresion_U.csv','Medias por corrida; evaluación interna previamente examinada'),
        ('Escenarios','docs/protocolo_escenarios.md','E0/E1/E2 y reglas fijadas antes de ejecutar'),
        ('Resultados','reports/simulador/comparacion_escenarios.csv; figures/escenarios_excitacion.png','Indicadores de regulación, distintos de errores predictivos'),
        ('Decisión y limitaciones','reports/simulador/resultados_y_decision.md','E1 según regla; compensaciones, sin prueba física'),
        ('Referencias y evidencias','Zenodo DOI 10.5281/zenodo.19856119; reports/simulador/integridad.json','Autoría externa; reproducibilidad y pruebas')]
    write(ROOT/'docs/evidencias_13_diapositivas.md','# Evidencias preparadas para las 13 diapositivas\n\nNo se produce todavía la presentación definitiva. Las rutas figures/ de esta tabla están en reports/simulador/.\n\n'+table(pd.DataFrame([dict(n=i+1,diapositiva=a,evidencia=b,nota=c) for i,(a,b,c) in enumerate(mapping)]))+'\n\nAmbos estudiantes deben ejecutar el análisis, explicar las ecuaciones y distinguir métricas predictivas de regulación. No se certifica un ensayo de sustentación que aún no realizaron.\n')
    requirements=[('≥2 tanques y registros reales','README experimental y auditoría','Cumplido con fuente externa'),
        ('Aceptación de datos externos','Comunicación explícita del usuario, fase 3; anexo A','Autorizado según usuario; sin acta adjunta'),
        ('Esquema y límites','App y docs/modelo_matematico.md','Cumplido como esquema conceptual; circuito exacto pendiente'),
        ('Variables, parámetros, unidades','Anexo B y parametros_U.csv','Cumplido para coeficientes efectivos'),
        ('Balance por tanque','Modelo U código 15 y app','Cumplido localmente; áreas no identificadas'),
        ('Implementación modificable','Motor común RK4 y copias exploratorias','Cumplido'),
        ('No negatividad y balances','Motor, pruebas y CSV de trayectorias','Cumplido en ejecuciones verificadas'),
        ('Calibración y evaluación reservada','Resultados históricos, grupos y regresión U','Cumplido como evaluación interna, no externa nueva'),
        ('MAE/RMSE e interpretación','App y regresion_U.csv','Cumplido'),
        ('Base y dos alternativas','E0/E1/E2; 19 comparaciones','Cumplido'),
        ('Indicadores y decisión','Regla previa y resultados_y_decision.md','Cumplido para contrafactuales locales'),
        ('13 diapositivas','docs/evidencias_13_diapositivas.md','Evidencias listas; presentación definitiva pendiente'),
        ('Ambos integrantes comprenden y reproducen','Guía de uso y anexos','Material listo; ensayo humano pendiente')]
    write(ROOT/'docs/matriz_cumplimiento_guia.md','# Matriz actual de cumplimiento de la guía\n\nGuía DOCX leída completa en fases 1 y 3, incluidos anexos y ponderaciones. Uso de datos externos autorizado por el docente según comunicación del usuario en fase 3. No se atribuyen mediciones a los estudiantes.\n\n'+table(pd.DataFrame(requirements,columns=['Requisito','Evidencia','Estado']))+'\n\nPonderaciones: datos 15%, modelo 20%, implementación 15%, calibración/validación 20%, escenarios 15%, decisión 10%, presentación 5%. No se inventa aprobación formal de una propuesta completa ni prueba de dominio de los integrantes.\n')
    update(ROOT/'docs/definicion_problema.md','El docente aceptó usar las mediciones externas, según comunicación del usuario. La pregunta se concreta en comparar E0, E1 y E2 para reducir desviaciones locales respecto a 47.4/31.2 cm. La regla, indicadores y bandas analíticas se fijaron antes de ejecutar; ver protocolo_escenarios.md. El resultado calculado y sus compensaciones están en reports/simulador/resultados_y_decision.md. Las mediciones siguen siendo de los investigadores de CEFET-MG.')
    update(ROOT/'docs/modelo_matematico.md','El modelo principal de la aplicación es U_bomba_carga_monotona__retardo, código 15 de src/precision_models.py; parámetros exactos en anexo B. La app expone sus ecuaciones completas. q12=max(0,q*+k12[(h1−h2)−16.2]); qout=max(0,q*+kout[h2−31.2]); Qin/A1=max(0,q*F(u(t−2)/100)/F(0.5)−kpump[h1−47.4]); F(z)=z+(b−1)z²+(1−2b+c)z³/3. dh1/dt=qin−q12; dh2/dt=r(q12−qout). El motor reutiliza RK4 verificado, particiona cambios discontinuos y usa u=50% antes del inicio. No corrige estados con mediciones futuras. La representación animada sólo reproduce esos estados y no integra ecuaciones propias.')
    update(ROOT/'README.md','Aplicación de fase 3 disponible: ejecutar `iniciar_simulador.ps1` o `python -m streamlit run app.py`. Dependencias en requirements-app.txt. Modelo principal U, referencias C/D/P, escenarios E0/E1/E2 y modo exploratorio sin sobrescribir calibración. Documentación en docs/guia_simulador.md y reports/simulador/. La presentación definitiva no se generó; sus 13 evidencias están preparadas. Las secciones anteriores son antecedentes de las etapas científicas.')
    readme=(ROOT/'README.md').read_text(encoding='utf-8').replace('No hay app ni presentación: corresponden a una etapa posterior al dictamen.','La aplicación de fase 3 está disponible; la presentación definitiva sigue pendiente.')
    write(ROOT/'README.md',readme)
    print('Documentación actualizada; evidencias de 13 diapositivas listas.')

if __name__=='__main__':main()
