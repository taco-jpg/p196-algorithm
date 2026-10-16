#!/usr/bin/env python3
"""Stage only the import closure of ReturnCore from confirmed compiled sources."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys

evidence = Path(__file__).resolve().parent
root = evidence.parents[4]
build = evidence / 'build'
build.mkdir(exist_ok=True)
available = {}
for arg in sys.argv[1:]:
    directory = Path(arg).resolve()
    for obj in sorted(directory.glob('*.olean')):
        source = obj.with_suffix('.lean')
        if not source.exists():
            continue
        module = obj.stem
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if module in available and available[module][2] != digest:
            raise RuntimeError('Conflicting source bytes for module ' + module)
        available[module] = (source, obj, digest)

records = []
visited = set()

def imports(source):
    result = []
    for match in re.finditer(r'^\s*import\s+([^\n]+)', source, re.M):
        result.extend(match.group(1).split('--')[0].split())
    return result

def visit(module):
    if module.split('.')[0] in ['Init', 'Std', 'Lean'] or module in visited:
        return
    source, obj, digest = available[module]
    visited.add(module)
    for dep in imports(source.read_text()):
        visit(dep)
    for path in [source, obj]:
        destination = build / path.name
        if path.resolve() != destination.resolve():
            shutil.copy2(path, destination)
    records.append({'module': module, 'source_origin': str(source),
                    'source_sha256': digest, 'object_origin': str(obj),
                    'object_sha256': hashlib.sha256(obj.read_bytes()).hexdigest()})

for dependency in imports((root / 'proofs/Agent1PeriodicReturnCore.lean').read_text()):
    visit(dependency)
(evidence / 'reused-dependencies.json').write_text(json.dumps({
    'policy': 'author incremental closure; all supplied objects confirmed compiled; no fresh closure claim',
    'condensation_note': 'Exact original CondensationBound was freshly compiled unchanged in condensation-dependency-001.',
    'dependency_count': len(records), 'dependencies': records
}, indent=2) + '\n')
print('Pinned closure dependencies:', len(records))
