# Modelado y simulación de tanques acoplados CEFET-MG

Proyecto académico de modelado dinámico de dos tanques hidráulicos a partir de registros experimentales publicados por investigadores de CEFET-MG. Incluye integración mediante RK4, calibración y evaluación del modelo U, comparación de escenarios y una aplicación interactiva en Streamlit.

La implementación y los datos están en [`CEFET_MG/`](CEFET_MG/).

## Ejecución

Desde la raíz del repositorio, en PowerShell, crear un entorno virtual e instalar las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\CEFET_MG\requirements-app.txt
```

Iniciar la aplicación vigente:

```powershell
.\CEFET_MG\iniciar_entrega_final.ps1
```

Abrir [http://127.0.0.1:8501](http://127.0.0.1:8501). Si el entorno ya está preparado, basta con ejecutar el comando de inicio.

## Escenarios y alcance

- **E0:** señal de bombeo experimental registrada, con respuesta calculada por el modelo.
- **E1:** señal atenuada alrededor del 50 %.
- **E2:** operación constante al 50 %.

El suavizado histórico se conserva por separado como `S_HIST`. E2 es la mejor alternativa nominal evaluada dentro del modelo U, cerca del equilibrio y sin demandas externas documentadas. Las políticas alternativas son simulaciones; no se presentan como ensayos físicos ni como validación externa. La calibración y los resultados históricos se conservan.

## Documentación y evidencias

- [Instrucciones del proyecto](CEFET_MG/README.md).
- [Informe científico final](CEFET_MG/reports/consolidacion_final/informe_final.md).
- [Informe de cumplimiento y comprobaciones](CEFET_MG/reports/consolidacion_final/informe_cumplimiento.md).
- [Esquema de las 13 diapositivas para revisión](CEFET_MG/docs/consolidacion_final/esquema_definitivo_13.md).
- [Índice de versiones y antecedentes](CEFET_MG/docs/consolidacion_final/indice_versiones.md).
- [Origen y descripción de los datos experimentales](CEFET_MG/data/raw/README.md).

## Pruebas

Desde la raíz del repositorio:

```powershell
Set-Location .\CEFET_MG
..\.venv\Scripts\python.exe -m pytest -q tests
```

El punto de entrada vigente es `app_final.py`. `app.py` permanece como implementación histórica.
