# Ejecutar y reproducir el simulador

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
