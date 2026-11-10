"""Explicit separation of archived documentary bytes and current scientific integrity."""
import subprocess
from .data_processing import ROOT
TAG = 'cefet-archivo-cientifico-completo'
ARCHIVED = ['LEEME_PRIMERO.md', 'docs/anexos_proyecto.md', 'docs/definicion_problema.md', 'docs/evidencias_13_diapositivas.md', 'docs/esquema_13_diapositivas_revisado.md', 'docs/guia_simulador.md', 'docs/matriz_cumplimiento_guia.md']

def archived_bytes(name):
    import json
    normalized = name.replace(chr(92), '/')
    migration = json.loads((ROOT / 'reports/consolidacion_final/integridad_vigente.json').read_text(encoding='utf-8'))
    args = ['git', 'cat-file', '--filters'] if migration['archive_filters'][normalized] else ['git', 'show']
    return subprocess.check_output(args + [f'{TAG}:CEFET_MG/{normalized}'], cwd=ROOT)

def verify_original_manifest(manifest):
    import hashlib, json
    migration = json.loads((ROOT / 'reports/consolidacion_final/integridad_vigente.json').read_text(encoding='utf-8'))
    migrated = set(migration['documentary_changes'])
    for name, digest in manifest.items():
        normalized = name.replace(chr(92), '/')
        content = archived_bytes(normalized) if normalized in migrated else (ROOT / normalized).read_bytes()
        assert hashlib.sha256(content).hexdigest() == digest, name

def historical_source(name):
    if name in ARCHIVED:
        return f'https://github.com/ks-correa/CEFET/blob/{TAG}/CEFET_MG/{name}'
    return name

def write_document(path, text):
    if path.relative_to(ROOT).as_posix() not in ARCHIVED:
        path.write_text(text, encoding='utf-8')
