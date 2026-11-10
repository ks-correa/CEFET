"""Current checkout coverage, complementary to original archived-manifest checks."""
import hashlib
import json
from src.data_processing import ROOT
from src.documentary_archive import ARCHIVED, archived_bytes

def test_current_files_and_archived_documentation():
    record = json.loads((ROOT / 'reports/consolidacion_final/integridad_vigente.json').read_text(encoding='utf-8'))
    assert record['historical_commit'] == '444042936475cd204576d6488f7599993ee98636'
    assert set(record['deleted_markdown']) == set(ARCHIVED)
    for name, digest in record['files'].items():
        assert hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest() == digest, name
    for name, digest in record['deleted_markdown'].items():
        assert not (ROOT / name).exists()
        assert hashlib.sha256(archived_bytes(name)).hexdigest() == digest, name
