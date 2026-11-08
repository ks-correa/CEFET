# Diagnóstico complementario separado

Leer informe_diagnostico.md y docs/esquema_13_diapositivas_revisado.md.
No se modificó el simulador ni los tres escenarios principales. No se creó PowerPoint.

Desde CEFET_MG y usando el entorno Python existente:

```powershell
$env:PYTHONIOENCODING='utf-8'
../.venv/Scripts/python.exe -m src.constant_control_diagnostic
../.venv/Scripts/python.exe -m pytest -q tests
../.venv/Scripts/python.exe -m src.constant_control_reporting
```

Si .venv es local, quitar ../. El primer comando guarda todos sus resultados en esta carpeta
y compara huellas de los archivos preexistentes. No vuelve a calibrar U. La repetición
sobrescribe sólo los resultados de este diagnóstico, nunca resultados previos de E0/E1/E2.
Las figuras son estáticas para la evidencia científica y están generadas a partir de CSV reales
del proyecto o de escenarios calculados, con etiquetas de contrafactual.
