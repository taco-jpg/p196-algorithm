#!/usr/bin/env python3
"""Inventory this contribution, or verify its retained byte manifest."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GENERATED = {'INVENTORY.json', 'MANIFEST.sha256'}
EXCLUDED_PREFIXES = (
    '__pycache__/',
    'development/population/python_cache/',
    'development/growth/build/',
    'review/allbase-reviewer/fresh-build-001/',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        lines = (ROOT / 'MANIFEST.sha256').read_text().splitlines()
        for line in lines:
            expected, name = line.split('  ', 1)
            path = ROOT / name
            assert path.is_file() and digest(path) == expected, name
        inventory = json.loads((ROOT / 'INVENTORY.json').read_text())
        for item in inventory['files']:
            if item['decision'] == 'retained':
                path = ROOT / item['path']
                assert path.stat().st_size == item['bytes'], item['path']
                assert digest(path) == item['sha256'], item['path']
        print('PASS:', len(lines), 'retained manifest entries')
        return
    records = []
    for path in sorted(p for p in ROOT.rglob('*') if p.is_file()):
        name = path.relative_to(ROOT).as_posix()
        if name in GENERATED:
            continue
        reason = 'Research source, complete result, development attempt, or verification evidence'
        decision = 'retained'
        if name.startswith(EXCLUDED_PREFIXES) or path.suffix in {'.olean', '.ilean', '.pyc'}:
            decision = 'excluded'
            reason = 'Rebuildable compiled object, cache, or duplicate dependency/build copy'
        if name == 'development/population_check.lean':
            assert path.read_bytes() == (ROOT / 'development/population/ApiProbe.lean').read_bytes()
            decision = 'excluded'
            reason = 'Byte-identical copy of retained development/population/ApiProbe.lean'
        records.append({'path': name, 'bytes': path.stat().st_size,
                        'sha256': digest(path), 'decision': decision, 'reason': reason})
    checkpoint = json.loads((ROOT / 'checkpoint.json').read_text())
    result = {
        'agent': 'Agent #106',
        'task': 'agent106-run-births-formal',
        'source_commit': checkpoint['source_commit'],
        'scope': 'All files in this contribution directory at this publication snapshot',
        'generated_metadata': sorted(GENERATED),
        'outside_scope_infrastructure': [
            'Official compiler installation and downloaded runtime archive',
            'Scratch-only copied source/compiled build directories; original sources and substantive logs retained here',
            'Operational Git/API publication helpers and repository checkout metadata',
        ],
        'counts': {decision: sum(r['decision'] == decision for r in records)
                   for decision in ('retained', 'excluded')},
        'files': records,
    }
    (ROOT / 'INVENTORY.json').write_text(json.dumps(result, indent=2) + '\n')
    retained = [r['path'] for r in records if r['decision'] == 'retained'] + ['INVENTORY.json']
    (ROOT / 'MANIFEST.sha256').write_text(''.join(
        digest(ROOT / name) + '  ' + name + '\n' for name in sorted(retained)))
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
