$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$runtimeLocal = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
$runtimeParent = Join-Path (Split-Path $PSScriptRoot -Parent) '.venv/Scripts/python.exe'
if (Test-Path -LiteralPath $runtimeLocal) { $runtimeTask = $runtimeLocal }
elseif (Test-Path -LiteralPath $runtimeParent) { $runtimeTask = $runtimeParent }
else { throw 'Crear un entorno Python e instalar requirements-app.txt. Consultar docs/guia_simulador.md.' }
& $runtimeTask -m streamlit run (Join-Path $PSScriptRoot 'app.py') --server.address=127.0.0.1 --server.port=8501
