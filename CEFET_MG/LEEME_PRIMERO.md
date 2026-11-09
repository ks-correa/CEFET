# Registro de integridad de datos crudos iniciales (`LEEME_PRIMERO.md`)

> **Nota de navegación:** La documentación principal del proyecto se encuentra en [`../README.md`](../README.md) y la guía rápida de ejecución y reproducción en [`README.md`](README.md). Este archivo se conserva porque la prueba automatizada `tests/test_project.py::test_raw_integrity` verifica contra él las huellas SHA-256 de los archivos originales de entrada.

## Archivos originales del paquete experimental

Datos experimentales originales de «D-Stabilization of a Coupled-Tank System Using Experimental Data» (CEFET-MG; Silva, Coelho y Leite, Zenodo, DOI `10.5281/zenodo.19856119`):

- `data/raw/h1.csv` y `data/raw/h2.csv`: 81 filas por tanque (`t_ref` y `Experimento1..10`).
- `data/raw/U.csv`: 80 señales de bomba por intervalo.
- `data/raw/complete_data.csv`: 4502 observaciones de la captura experimental completa.
- `data/raw/README.md`: documentación experimental original (niveles en cm, señal de bomba en %, muestreo $T_s = 4\text{ s}$).
- `data/raw/operational_parameters.json`: archivo truncado en el depósito original; conservado únicamente como evidencia de auditoría documental.
- `referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx`: guía docente original de la asignatura Modelado y Simulación.

## Huellas SHA256 verificadas por `tests/test_project.py`

- data/raw/h1.csv: 8bcc8e870c19c9f54de122e65963fc52fe1fd23a95f6335a297a51d3d4daf81e
- data/raw/h2.csv: dff73ca67048dc031bc9f6834115ae759e7f73b217ff09aea04f0411e24a3925
- data/raw/U.csv: 2a6da4ae0f990ad94003444ca7ac8e2a7a5c14dfab1951be1fa741260be54cf3
- data/raw/complete_data.csv: 6b2470f4a0ed64d3cfeb82ee7ec5e6803c6297e48d2a6cfe5af0a7787cebbd78
- data/raw/README.md: 671553956771bf1c249fcc8e655e72e1f6b752c56914c29a2cb55312e0744219
- data/raw/operational_parameters.json: 565aed05d19e19d6eddbf82234cb3076c98308645c5a3d4ce8f4fc8dd2adb810
- referencias/Guia_Proyecto_Simulacion_Tanques_Parejas.docx: 21cb59dd2597a4473ace1dd9551ae7d4f9f13cab259c8035478d3bc109871fa9
