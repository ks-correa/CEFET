# Simulación continua de dos tanques acoplados con datos experimentales de CEFET-MG

**Integrantes:** Kevin Santiago Correa Acosta (67001271) · Santiago Cárdenas Rubio (67001160)  
**Asignatura:** Modelado y Simulación · **Institución:** Universidad Católica de Colombia · **Fecha:** 8 de noviembre de 2026

---

## Descripción

Este proyecto desarrolla, calibra, valida y emplea un modelo matemático continuo en ecuaciones diferenciales ordinarias (EDO) para estudiar la dinámica acoplada de dos tanques hidráulicos interconectados a partir de mediciones experimentales reales.

- **Pregunta de decisión:** *¿Cómo influye la variabilidad de la señal de bombeo en la estabilidad de los niveles de dos tanques hidráulicos interconectados y qué condición de operación permite minimizar sus desviaciones respecto al equilibrio nominal?*
- **Alcance de la comparación:** Se evalúan tres condiciones operativas sobre el mismo modelo calibrado y bajo condiciones iniciales, pasos de integración y horizontes idénticos, con el propósito de identificar la alternativa nominal que minimiza las desviaciones respecto a los niveles de referencia $(h_1^*, h_2^*) = (47.4\text{ cm}, 31.2\text{ cm})$ en ausencia de demandas externas documentadas.

---

## Datos experimentales

Los registros experimentales provienen del conjunto publicado por investigadores del **CEFET-MG** (*Centro Federal de Educação Tecnológica de Minas Gerais*, campus Divinópolis, Brasil):

- **Autores y publicación:** Guilherme Silva, Marcela Coelho y Valter Leite (2026), *D-Stabilization of a Coupled-Tank System Using Experimental Data*, Zenodo, v1.0.0.
- **DOI / Enlace:** [`10.5281/zenodo.19856119`](https://zenodo.org/records/19856119).
- **Documentación original del dataset:** [`CEFET_MG/data/raw/README.md`](CEFET_MG/data/raw/README.md).
- **Cantidad de registros y corridas:**
  - [`CEFET_MG/data/raw/complete_data.csv`](CEFET_MG/data/raw/complete_data.csv): **4502 registros** continuos con intervalo de muestreo aproximado $T_s \approx 4\text{ s}$.
  - [`CEFET_MG/data/processed/run_01.csv`](CEFET_MG/data/processed/run_01.csv) a [`run_10.csv`](CEFET_MG/data/processed/run_10.csv): **10 corridas experimentales** segmentadas sin duplicación de filas originales (`run_01` a `run_09` incluyen fase de excitación de $\approx 800\text{ s}$ y recuperación hasta $\approx 1700\text{ s}$; `run_10` contiene la fase de excitación de $\approx 800\text{ s}$).
- **Variables:**
  - $h_1(t), h_2(t)$: niveles de agua en los tanques 1 y 2 ($\text{cm}$), con punto de operación nominal $(47.4\text{ cm}, 31.2\text{ cm})$.
  - $u(t)$: comando porcentual de la bomba de alimentación ($\%$, rango $0\text{–}100\%$), con mando de equilibrio nominal $u^* = 50\%$.

---

## Modelo matemático

Tras explorar 30 variantes estructurales y de estimación sobre las corridas de desarrollo (1–7), se seleccionó el modelo **`U_bomba_carga_monotona__retardo`** (código `15` en [`CEFET_MG/src/precision_models.py`](CEFET_MG/src/precision_models.py)), formulado mediante balances efectivos locales por tanque:

$$\frac{dh_1}{dt} = q_{\text{in}}(t) - q_{12}(h_1, h_2), \qquad \frac{dh_2}{dt} = r\,\bigl(q_{12}(h_1, h_2) - q_{\text{out}}(h_2)\bigr)$$

donde los flujos específicos efectivos ($q = Q/A_1$ en $\text{cm/s}$) y la curva cúbica monótona de bombeo $F(z)$ con desfase efectivo de entrada $\delta = 2\text{ s}$ ($z = u(t - \delta)/100$) son:

$$q_{12} = \max\!\bigl(0,\; q_* + k_{12}[(h_1 - h_2) - 16.2]\bigr), \qquad q_{\text{out}} = \max\!\bigl(0,\; q_* + k_{\text{out}}(h_2 - 31.2)\bigr)$$

$$F(z) = z + (b - 1)z^2 + \frac{1 - 2b + c}{3}z^3, \qquad q_{\text{in}} = \max\!\left(0,\; q_*\frac{F(z)}{F(0.5)} - k_{\text{pump}}(h_1 - 47.4)\right)$$

El sistema verifica la identidad efectiva de balance total $\frac{d}{dt}(h_1 + h_2/r) = q_{\text{in}} - q_{\text{out}}$. La integración numérica se realiza simultáneamente con **Runge-Kutta de cuarto orden (RK4)** con paso máximo de $1\text{ s}$, particionado exacto en los instantes de cambio de mando y retención causal $u(t < 0) = 50\%$.

### Siete parámetros calibrados (precisión original en [`parametros_U_vigentes.csv`](CEFET_MG/reports/consolidacion_final/parametros_U_vigentes.csv))

| Parámetro | Valor calibrado | Unidad | Significado físico efectivo |
|---|---:|---|---|
| `qstar` | `1.1901768213433377` | $\text{cm/s}$ | Flujo efectivo en el equilibrio nominal ($Q^*/A_1$) |
| `r` | `0.28068693475733053` | adimensional | Razón efectiva de áreas entre tanques ($A_1/A_2$) |
| `k12` | `0.039766247050466483` | $\text{s}^{-1}$ | Conductancia efectiva de transferencia entre tanques |
| `kout` | `0.011857107887654482` | $\text{s}^{-1}$ | Conductancia efectiva de descarga del tanque 2 |
| `kpump` | `0.0032622340261774787` | $\text{s}^{-1}$ | Sensibilidad efectiva de carga en la entrada del tanque 1 |
| `b` | `0.71741375825579845` | adimensional | Coeficiente cuadrático de la curva monótona de bomba |
| `c` | `0.58172099393448107` | adimensional | Coeficiente cúbico de la curva monótona de bomba |

---

## Escenarios

En la entrega vigente ([`CEFET_MG/src/final_scenarios.py`](CEFET_MG/src/final_scenarios.py) y [`protocolo_vigente.md`](CEFET_MG/docs/consolidacion_final/protocolo_vigente.md)) se comparan tres escenarios principales bajo las mismas condiciones iniciales observadas y el mismo modelo `U` sin recalibrar:

- **`E0` (Base experimental):** señal de bombeo experimental registrada $u_0(t)$ retenida causalmente.
- **`E1` (Señal atenuada):** reducción del $20\%$ en las excursiones respecto al punto medio, $u_1(t) = 50 + 0.80\,(u_0(t) - 50)$.
- **`E2` (Bombeo constante al 50 %):** operación constante en el mando de equilibrio nominal, $u_2(t) = 50\%$.
- **`S_HIST` (Escenario histórico complementario):** limitación causal de rampa de $10\text{ pp}$ por cada $4\text{ s}$ evaluada en la fase preliminar; se conserva por trazabilidad en la sección de análisis complementarios.

---

## Resultados

El proyecto distingue estrictamente entre el **error predictivo** del modelo (frente a las mediciones reales) y la **desviación de regulación** de los escenarios (respecto al equilibrio nominal):

### 1. Validación predictiva del modelo `U` (corridas de evaluación 8–10, [`validacion_U_sin_cambios.csv`](CEFET_MG/reports/consolidacion_final/validacion_U_sin_cambios.csv))

| Tanque | MAE ($\text{cm}$) | RMSE predictivo ($\text{cm}$) | NRMSE ($\text{RMSE}/\sigma_{\text{train}}$) | Sesgo ($\text{cm}$) |
|---|---:|---:|---:|---:|
| $h_1$ | `0.62896` | `0.87253` | `0.14581` | `-0.28446` |
| $h_2$ | `0.18748` | `0.24169` | `0.079027` | `0.12545` |

### 2. Comparación de escenarios (RMSE de regulación respecto a $47.4\text{ cm}$ y $31.2\text{ cm}$, [`comparacion_principal.csv`](CEFET_MG/reports/consolidacion_final/comparacion_principal.csv))

| Escenario | $\text{RMSE}_{\text{ref}, h_1}$ ($\text{cm}$) · Corrida 8 | $\text{RMSE}_{\text{ref}, h_2}$ ($\text{cm}$) · Corrida 8 | Media 10 excitaciones $h_1$ ($\text{cm}$) | Media 10 excitaciones $h_2$ ($\text{cm}$) | Mando medio ($\%$) | $\text{TV}_u$ ($\text{pp}$) |
|---|---:|---:|---:|---:|---:|---:|
| **`E0`** | `9.1026` | `5.0073` | `9.1006` | `5.0052` | `48.748` | `1454.9` |
| **`E1`** | `7.0168` | `3.7754` | `7.0157` | `3.7742` | `48.998` | `1163.9` |
| **`E2`** | **`0.19707`** | **`0.19702`** | **`0.16169`** | **`0.16620`** | **`50.000`** | **`0.0`** |

- **Decisión sustentada:** **`E2` (bombeo constante al 50 %)** resulta seleccionado en las **19 comparaciones nominales** (10 ventanas de excitación y 9 corridas completas con recuperación) y mantiene la preferencia en las **90 exploraciones de sensibilidad local** (desplazamientos iniciales de $\pm 1\text{ cm}$ y perturbaciones de mando de $\pm 2\text{ pp}$). Un sesgo sostenido de $-2\text{ pp}$ desplaza el equilibrio predicho a $(44.056, 28.624)\text{ cm}$, evidenciando que el mando constante en lazo abierto no implica rechazo activo de perturbaciones externas.

---

## Ejecutar el simulador

Desde la raíz del repositorio en **PowerShell**:

```powershell
# 1. (Opcional si .venv ya existe) Crear entorno virtual e instalar dependencias
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\CEFET_MG\requirements-app.txt

# 2. Iniciar la aplicación interactiva vigente en http://127.0.0.1:8501
.\CEFET_MG\iniciar_entrega_final.ps1
```

O ejecutando Streamlit directamente desde `CEFET_MG/`:

```powershell
Set-Location .\CEFET_MG
..\.venv\Scripts\python.exe -m streamlit run app_final.py
```

---

## Estructura del repositorio

```text
CEFET/
├── README.md                                  # Presentación general del proyecto y síntesis técnica
└── CEFET_MG/                                  # Directorio principal del proyecto
    ├── README.md                              # Guía rápida de ejecución y reproducción
    ├── app_final.py                           # Aplicación interactiva Streamlit vigente (entrega final)
    ├── iniciar_entrega_final.ps1              # Lanzador PowerShell del simulador vigente
    ├── requirements.txt                       # Dependencias científicas fijadas (NumPy, Pandas, SciPy, Numba, Pytest)
    ├── requirements-app.txt                   # Dependencias de la aplicación (incluye Streamlit)
    ├── requirements-dev.txt                   # Dependencias de verificación automatizada (Playwright, ty)
    ├── pytest.ini                             # Configuración de pruebas automatizadas
    ├── assets/                                # Componentes visuales HTML/CSS/JS de los tanques acoplados
    ├── data/
    │   ├── raw/                               # Dataset original CEFET-MG (complete_data.csv, h1.csv, h2.csv, U.csv, README.md)
    │   └── processed/                         # 10 corridas procesadas (run_01..run_10.csv), mapeo, estadísticas y sha256.json
    ├── referencias/
    │   └── Guia_Proyecto_Simulacion_Tanques_Parejas.docx  # Guía docente de la asignatura
    ├── src/                                   # Código fuente científico, motor RK4, modelos y escenarios
    │   ├── precision_models.py                # Ecuaciones diferenciales y RK4 simultáneo (incluye modelo U, código 15)
    │   ├── simulation_engine.py               # Motor unificado de simulación y configuración calibrada/exploratoria
    │   ├── final_scenarios.py                 # Escenarios vigentes E0, E1, E2 y complemento histórico S_HIST
    │   ├── final_consolidation.py             # Reproducción de las 19 comparaciones nominales y 90 sensibilidades
    │   ├── final_documentation.py             # Generación trazable de reportes y esquemas vigentes
    │   └── ...                                # Módulos de calibración, validación y etapas históricas reproducibles
    ├── docs/
    │   ├── consolidacion_final/               # Documentación vigente de la entrega final (Anexos A-B-C, modelo, protocolo, decisión)
    │   └── *.md                               # Protocolos y documentos históricos preservados por integridad SHA-256
    ├── reports/
    │   ├── consolidacion_final/               # Resultados vigentes, informe_final.md, figuras, robustez y evidencias de pruebas
    │   ├── optimizacion_precision/            # Evidencia de las 30 variantes calibradas (all_fits.json, métricas y gráficas)
    │   ├── diagnostico_control_constante/     # Diagnóstico D50 y ablación de media de mando
    │   ├── simulador/                         # Resultados históricos de la fase 3 preliminar
    │   └── figures/                           # Gráficas de exploración del dataset y línea base inicial
    ├── scripts/                               # Scripts de verificación de servidor, navegador y cierre de entrega
    └── tests/                                 # Batería de 48 pruebas automatizadas de integridad, RK4, modelos y UI
```

---

## Pruebas y reproducibilidad

Para ejecutar la batería completa de **48 pruebas automatizadas** (integridad SHA-256 de datos y antecedentes, convergencia RK4, causalidad del desfase de 2 s, conservación efectiva, reproducción de métricas de `U`, escenarios `E0`/`E1`/`E2` y pruebas de interfaz `AppTest`):

```powershell
Set-Location .\CEFET_MG
..\.venv\Scripts\python.exe -m pytest -q tests
```

Las evidencias de verificación ejecutadas se localizan en [`CEFET_MG/reports/consolidacion_final/`](CEFET_MG/reports/consolidacion_final/):

- [`tests.txt`](CEFET_MG/reports/consolidacion_final/tests.txt): registro histórico de las 46 pruebas aprobadas; la verificación documental actual está en `auditoria_depuracion.json`.
- [`typecheck.txt`](CEFET_MG/reports/consolidacion_final/typecheck.txt): verificación estática de tipos.
- [`integridad.json`](CEFET_MG/reports/consolidacion_final/integridad.json) y [`manifest_historico.json`](CEFET_MG/reports/consolidacion_final/manifest_historico.json): verificación de huellas SHA-256 sin alteración de resultados científicos.
- [`browser_checks.json`](CEFET_MG/reports/consolidacion_final/browser_checks.json) y [`agent_checks.json`](CEFET_MG/reports/consolidacion_final/agent_checks.json): comprobación automatizada de la aplicación Streamlit.

---

## Referencias

1. **Dataset oficial en Zenodo (DOI `10.5281/zenodo.19856119`):** [https://zenodo.org/records/19856119](https://zenodo.org/records/19856119)
2. **README original del dataset experimental:** [`CEFET_MG/data/raw/README.md`](CEFET_MG/data/raw/README.md)
3. **Guía docente del proyecto:** [`CEFET_MG/referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`](CEFET_MG/referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx)
4. **Documentación de `scipy.optimize.least_squares`:** [https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)
5. **Captura experimental completa (`complete_data.csv`):** [`CEFET_MG/data/raw/complete_data.csv`](CEFET_MG/data/raw/complete_data.csv)
6. **Repositorio del proyecto:** [https://github.com/ks-correa/CEFET](https://github.com/ks-correa/CEFET)
7. **Informe científico final consolidado:** [`CEFET_MG/reports/consolidacion_final/informe_final.md`](CEFET_MG/reports/consolidacion_final/informe_final.md)
8. **Anexos A, B y C vigentes:** [`CEFET_MG/docs/consolidacion_final/anexos_A_B_C.md`](CEFET_MG/docs/consolidacion_final/anexos_A_B_C.md)
9. **Documentación detallada vigente:** [`CEFET_MG/docs/consolidacion_final/`](CEFET_MG/docs/consolidacion_final/) ([`definicion_problema.md`](CEFET_MG/docs/consolidacion_final/definicion_problema.md), [`modelo_y_variables.md`](CEFET_MG/docs/consolidacion_final/modelo_y_variables.md), [`rk4_calibracion_validacion.md`](CEFET_MG/docs/consolidacion_final/rk4_calibracion_validacion.md), [`protocolo_vigente.md`](CEFET_MG/docs/consolidacion_final/protocolo_vigente.md), [`escenarios_resultados_decision.md`](CEFET_MG/docs/consolidacion_final/escenarios_resultados_decision.md), [`solidez_y_limitaciones.md`](CEFET_MG/docs/consolidacion_final/solidez_y_limitaciones.md), [`registro_metodologico.md`](CEFET_MG/docs/consolidacion_final/registro_metodologico.md), [`indice_versiones.md`](CEFET_MG/docs/consolidacion_final/indice_versiones.md))

La depuración documental y la recuperación de los antecedentes están explicadas en [el índice de versiones](CEFET_MG/docs/consolidacion_final/indice_versiones.md). La etiqueta publicada `cefet-archivo-cientifico-completo` conserva los 44 Markdown originales.
