"""Check release byte identity and completeness, not mathematical truth."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    count = 0
    for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = ROOT/name
        assert path.is_file(), 'Missing published file: '+name
        assert sha(path)==expected, 'Changed published file: '+name
        count += 1
    original = json.loads((ROOT/'INVENTORY.json').read_text())
    kept = [r for r in original if r['publication']=='retained']
    for record in kept:
        path = ROOT/record['published_path']
        assert path.stat().st_size==record['bytes'], record['source_path']
        assert sha(path)==record['sha256'], record['source_path']
    # Independent contributions and archived research can import one another.
    # The presence check covers both published source locations.
    sources = list((ROOT/'research').rglob('*.lean'))
    sources += list((ROOT/'contributions').rglob('*.lean'))
    names = {p.stem for p in sources}
    imports = 0
    for path in sources:
        for module in re.findall(r'^import\s+(\S+)', path.read_text(), re.M):
            assert module=='Std' or module in names, (str(path),module)
            imports += 1
    print(json.dumps({'status':'PASS','manifest_files':count,
                     'unchanged_original_files':len(kept),
                     'lean_source_files':len(sources),'lean_imports':imports,
                     'mathematical_proof_check':False},indent=2))

if __name__=='__main__': main()
