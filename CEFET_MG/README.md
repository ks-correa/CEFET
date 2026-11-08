# CEFET-MG Entrega consolidada vigente

Ejecutar **iniciar_entrega_final.ps1** o `python -m streamlit run app_final.py`.
La aplicación vigente usa E0 experimental, E1 atenuado y E2 constante al 50%.
El antiguo suavizado está en Análisis complementarios como S_HIST.

La constante es la mejor alternativa nominal evaluada dentro de U, cerca del equilibrio
y sin demandas externas documentadas. No se afirma óptimo global, ahorro eléctrico,
ensayo físico de políticas nuevas ni rechazo de perturbaciones del montaje.

- Documentación vigente: docs/consolidacion_final/.
- Esquema definitivo para revisión: docs/consolidacion_final/esquema_definitivo_13.md.
- Informe científico: reports/consolidacion_final/informe_final.md.
- Comprobaciones ejecutadas: reports/consolidacion_final/informe_cumplimiento.md.
- Índice de antecedentes preservados: docs/consolidacion_final/indice_versiones.md.

Reproducir sin recalibrar:

```powershell
uv pip install --python ../.venv/Scripts/python.exe -r requirements-app.txt
../.venv/Scripts/python.exe -m src.final_consolidation
../.venv/Scripts/python.exe -m src.final_documentation
../.venv/Scripts/python.exe -m pytest -q tests
../.venv/Scripts/python.exe -m streamlit run app_final.py
```

Si .venv es local, quitar ../. Los paquetes científicos fijados siguen siendo los originales.
app.py, iniciar_simulador.ps1 y src/scenarios.py se conservan como versión histórica,
no como punto de entrada de esta entrega. Los resultados anteriores no se sobrescriben.
El README anterior se preserva en reports/consolidacion_final/historico/.
Datos de investigadores externos, uso autorizado por el docente según comunicación del
usuario. No hay mediciones de la pareja ni presentación PowerPoint definitiva generada.
