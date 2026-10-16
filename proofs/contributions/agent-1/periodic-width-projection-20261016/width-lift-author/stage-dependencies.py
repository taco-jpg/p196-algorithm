#!/usr/bin/env python3
"""Copy explicitly supplied, successfully compiled dependency sets with hashes.

Run only after the parent confirms the OuterCatalog object is valid. This script
does not infer compilation success from an object's existence.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

evidence = Path(__file__).resolve().parent
root = evidence.parents[4]
build = evidence / 'build'
build.mkdir(exist_ok=True)
records = {}
for argument in sys.argv[1:]:
    origin = Path(argument).resolve()
    for obj in sorted(origin.glob('*.olean')):
        if obj.stem in ['Agent1PeriodicWidthLift', 'WidthLiftAudit']:
            continue
        source = obj.with_suffix('.lean')
        if not source.exists():
            raise RuntimeError('Missing paired dependency source: ' + str(source))
        for path in [source, obj]:
            shutil.copy2(path, build / path.name)
        records[obj.stem] = {
            'module': obj.stem,
            'source_origin': str(source),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'object_origin': str(obj),
            'object_sha256': hashlib.sha256(obj.read_bytes()).hexdigest(),
        }
for required in ['Agent1PeriodicOuterCatalog', 'Agent1PeriodicWidth']:
    if required not in records:
        raise RuntimeError('Required valid dependency was not supplied: ' + required)
receipt = {
    'mode': 'author incremental reuse only; no fresh dependency rebuild',
    'base_worktree_head': subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
    'outer_catalog_status': 'parent-confirmed successful compiled object supplied explicitly',
    'dependencies': list(records.values()),
}
(evidence / 'reused-dependencies.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('Pinned dependency objects:', len(records))
