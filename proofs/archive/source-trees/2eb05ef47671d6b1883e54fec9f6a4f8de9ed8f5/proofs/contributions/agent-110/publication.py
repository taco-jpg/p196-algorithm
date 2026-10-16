#!/usr/bin/env python3
"""Inventory the staged Agent110 contribution without altering research files."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
PREFIX = str(ROOT.relative_to(REPO))
OUTPUTS = {'PUBLICATION.json', 'SHA256SUMS'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


paths = subprocess.check_output(
    ['git', '-C', str(REPO), 'ls-files', '-z', '--', PREFIX]).decode().split('\0')
retained = []
for rel in sorted(p for p in paths if p):
    p = REPO / rel
    short = str(p.relative_to(ROOT))
    if short in OUTPUTS:
        continue
    raw = p.read_bytes()
    retained.append({'path': short, 'bytes': len(raw), 'sha256': digest(raw)})

compression = json.loads((ROOT / 'exterior-global/search/COMPRESSION.json').read_text())
for item in compression['records']:
    p = ROOT / 'exterior-global/search' / item['stored_path']
    packed = p.read_bytes()
    raw = gzip.decompress(packed)
    assert (len(packed), digest(packed)) == (item['stored_bytes'], item['stored_sha256'])
    assert (len(raw), digest(raw)) == (item['original_bytes'], item['original_sha256'])

excluded = []
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():
        continue
    rel = str(p.relative_to(ROOT))
    if p.suffix in {'.olean', '.ilean', '.o', '.so', '.pyc'} or '__pycache__' in p.parts:
        raw = p.read_bytes()
        excluded.append({'path': rel, 'bytes': len(raw), 'sha256': digest(raw),
                         'reason': 'Reproducible compiled object or runtime cache.'})

manifest = {
    'agent': 'Agent #110',
    'scope': 'All staged Agent110 source, proof attempts, raw solver evidence, reviews and logs.',
    'research_omissions': [],
    'retained': retained,
    'retained_file_count_excluding_inventory_outputs': len(retained),
    'retained_bytes_excluding_inventory_outputs': sum(r['bytes'] for r in retained),
    'compressed_research': compression['records'],
    'compressed_paths_relative_to': 'exterior-global/search/',
    'infrastructure_exclusions_within_contribution': excluded,
    'other_infrastructure': [
        'Official compiler installation and current-process path-adapter binary; original adapter source and hashes are retained.',
        'External development/reviewer build directories and copied dependency caches; fresh-build scripts, exact source hashes and substantive logs are retained.',
        'Uncompressed duplicate CNFs; every original byte is retained in the verified gzip mappings above.',
        'Operational Git/API transfer scratch; no credentials or chat transcripts are publication artifacts.'
    ],
    'historical_receipts': 'Earlier manifests are immutable snapshots of their recorded scope, including failures; later receipts do not relabel them.',
    'mathematical_status': 'Use the exact named theorem and corresponding independent review. Solver outcomes and WIP global targets are not Lean conclusions.',
    'inventory_note': 'This file and SHA256SUMS are excluded from self-hashing; Git supplies their identities. Run after staging new source/evidence files.'
}
(ROOT / 'PUBLICATION.json').write_text(json.dumps(manifest, indent=2) + '\n')
(ROOT / 'SHA256SUMS').write_text(''.join(r['sha256'] + '  ' + r['path'] + '\n' for r in retained))
print(json.dumps({'files': len(retained), 'bytes': manifest['retained_bytes_excluding_inventory_outputs'],
                  'compressed_inputs_verified': len(compression['records'])}))
