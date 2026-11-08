# Modelado continuo de dos tanques CEFET-MG

Primera etapa científica ejecutada. Dictamen: **VIABLE CON LIMITACIONES** en el régimen
de las excitaciones completas repetidas. No es válido para arranque ni para identificar
el régimen tardío usando sólo 320 s. No hay validación externa ni aprobación docente aportada.

## Reproducir en PowerShell

Desde esta carpeta, con Python 3.14 y uv instalado:

```powershell
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
$env:PYTHONIOENCODING='utf-8'
.venv/Scripts/python.exe -m src.experiments
.venv/Scripts/python.exe -m src.reporting
.venv/Scripts/python.exe -m pytest -q
```

La ejecución inicial usó el entorno `.venv` en la carpeta padre; también puede usarse
`../.venv/Scripts/python.exe` con los mismos paquetes fijados. Numba acelera el mismo
RK4; el primer uso compila. No descarga datos ni modifica originales. Semilla 20261108.
Los informes se regeneran después de los experimentos para mantener cifras trazables.

Leer `reports/viabilidad.md`, `reports/auditoria_dataset.md`, `reports/bondad_ajuste.md`,
`docs/protocolo_previo.md`, `docs/modelo_matematico.md`, `docs/definicion_problema.md`
y `docs/matriz_cumplimiento_guia.md`. Resultados completos en CSV/JSON y figures/.

Fuente: Silva, Coelho y Leite. Dataset D-Stabilization of a Coupled-Tank System Using
Experimental Data. Zenodo, v1.0.0, 2026. https://doi.org/10.5281/zenodo.19856119
Mediciones de investigadores externos; los estudiantes sólo modelan registros publicados.
Confirmar con el profesor la aceptación de esta modalidad.

Ambos estudiantes deben ejecutar los comandos y poder explicar: balance y unidades,
por qué no se identifican áreas absolutas, RK4 causal, grupos sin fuga, normalización de
entrenamiento, errores por régimen y diferencia entre evaluación interna y evidencia externa.
La aplicación de fase 3 está disponible; la presentación definitiva sigue pendiente.


Comprobaciones adicionales (después del análisis principal):

```powershell
.venv/Scripts/python.exe -m src.robustness
.venv/Scripts/python.exe -m src.reproduce
.venv/Scripts/python.exe -m src.reporting
.venv/Scripts/python.exe -m pytest -q
```

La reproducción vuelve a ejecutar todo el análisis y compara huellas de los resultados.
El modelo recomendado por parsimonia está en `reports/modelo_recomendado.json` (D);
el candidato diagnóstico de menor error se conserva en `selected_model.json` (C).

## Actualización de fase 3

Aplicación de fase 3 disponible: ejecutar `iniciar_simulador.ps1` o `python -m streamlit run app.py`. Dependencias en requirements-app.txt. Modelo principal U, referencias C/D/P, escenarios E0/E1/E2 y modo exploratorio sin sobrescribir calibración. Documentación en docs/guia_simulador.md y reports/simulador/. La presentación definitiva no se generó; sus 13 evidencias están preparadas. Las secciones anteriores son antecedentes de las etapas científicas.
