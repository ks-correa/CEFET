# Control de entrega de fase 3

**10/10 puntos de aceptación aprobados mediante las evidencias indicadas.**
Verificación realizada el 8 de noviembre de 2026. No implica aprobación docente de la
presentación definitiva ni validación externa nueva del modelo.

| n | aceptación | estado | evidencia |
|---|---|---|---|
| 1 | U reproduce la validación anterior | APROBADO | regresion_U.csv; tests/test_simulator.py |
| 2 | Dos tanques muestran niveles RK4 | APROBADO | browser_checks.json; figures/aplicacion_sistema.png |
| 3 | Parámetros modificables sin alterar calibración | APROBADO | tests.txt; integridad.json; modo exploratorio |
| 4 | E0, E1 y E2 se ejecutan | APROBADO | 57 trayectorias de 19 comparaciones |
| 5 | Condiciones comparables | APROBADO | protocolo_escenarios.md; pruebas de iniciales/parámetros/tiempo |
| 6 | Tabla con números de las simulaciones | APROBADO | comparacion_escenarios.csv |
| 7 | Decisión derivada de indicadores | APROBADO | src/scenarios.py::decide; prueba sin ganador preasignado |
| 8 | Streamlit funciona y conserva pruebas | APROBADO | agent_checks.json; browser_checks.json; tests.txt |
| 9 | Limitaciones y fuentes documentadas | APROBADO | [anexos archivados](https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/anexos_proyecto.md); resultados_y_decision.md; app |
| 10 | Evidencias de 13 diapositivas preparadas | APROBADO | https://github.com/ks-correa/CEFET/blob/cefet-archivo-cientifico-completo/CEFET_MG/docs/evidencias_13_diapositivas.md; sin presentación definitiva |

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
