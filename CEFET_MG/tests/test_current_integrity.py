"""Current checkout coverage, complementary to original archived-manifest checks."""
import hashlib
import json
import subprocess
import pytest
from src.data_processing import ROOT
from src.documentary_archive import ARCHIVED, archived_bytes

def test_current_files_and_archived_documentation():
    record = json.loads((ROOT / 'reports/consolidacion_final/integridad_vigente.json').read_text(encoding='utf-8'))
    assert record['historical_commit'] == '444042936475cd204576d6488f7599993ee98636'
    assert subprocess.check_output(
        ['git', 'rev-parse', record['historical_tag'] + '^{commit}'], cwd=ROOT,
        text=True,
    ).strip() == record['historical_commit']
    assert set(record['deleted_markdown']) == set(ARCHIVED)
    for name, digest in record['files'].items():
        assert hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest() == digest, name
    tracked = set(subprocess.check_output(
        ['git', 'ls-files'], cwd=ROOT.parent, text=True,
    ).splitlines())
    assert set(record['files']) == tracked - {
        'CEFET_MG/reports/consolidacion_final/integridad_vigente.json'
    }
    for name, digest in record['deleted_markdown'].items():
        assert not (ROOT / name).exists()
        assert hashlib.sha256(archived_bytes(name)).hexdigest() == digest, name


def test_original_manifest_rejects_changed_or_missing_scientific_data(tmp_path, monkeypatch):
    from src import documentary_archive
    migration = tmp_path / 'reports/consolidacion_final/integridad_vigente.json'
    migration.parent.mkdir(parents=True)
    migration.write_text(json.dumps({'documentary_changes': []}), encoding='utf-8')
    monkeypatch.setattr(documentary_archive, 'ROOT', tmp_path)
    name = 'data/raw/complete_data.csv'
    manifest = {name: hashlib.sha256(b'original data').hexdigest()}
    with pytest.raises(FileNotFoundError):
        documentary_archive.verify_original_manifest(manifest)
    data = tmp_path / name
    data.parent.mkdir(parents=True)
    data.write_bytes(b'altered data')
    with pytest.raises(AssertionError, match='complete_data.csv'):
        documentary_archive.verify_original_manifest(manifest)
    data.write_bytes(b'original data')
    documentary_archive.verify_original_manifest(manifest)
