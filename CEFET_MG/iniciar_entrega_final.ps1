$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$localRuntime = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
$parentRuntime = Join-Path (Split-Path $PSScriptRoot -Parent) '.venv/Scripts/python.exe'
if (Test-Path -LiteralPath $localRuntime) { $finalRuntime = $localRuntime }
elseif (Test-Path -LiteralPath $parentRuntime) { $finalRuntime = $parentRuntime }
else { throw 'Crear .venv e instalar requirements-app.txt. Consultar README.md.' }
& $finalRuntime -m streamlit run (Join-Path $PSScriptRoot 'app_final.py') --server.address=127.0.0.1 --server.port=8501
