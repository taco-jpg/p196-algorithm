#!/usr/bin/env python3
"""Diagnostic comparison of compiled Lean enumeration with original Python.

Input certificate and checker are existing retained sources. This check is
not a kernel certificate and is not used by the formal completeness theorem.
"""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

here = Path(__file__).resolve().parent
repo = here.parents[4]
reference = repo / 'proofs/contributions/2026-10-15-seven-column-prefix'
spec = importlib.util.spec_from_file_location('reference', reference / 'verify_certificates.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
cert = json.loads((reference / 'certificate_739.json').read_text())
words = [tuple(row['word']) for row in cert['nodes'] if len(row['word']) == 7]
mode = sys.argv[3] if len(sys.argv) > 3 else 'original'
assert mode in ('original', 'fast')
stem = 'runtime-739' if mode == 'original' else 'runtime-fast-739'
program = 'RuntimeCrosscheck.lean' if mode == 'original' else 'RuntimeCrosscheckFast.lean'
build = Path(sys.argv[2])
build.mkdir(exist_ok=True, parents=True)
input_path = build / (stem + '-input.txt')
output_path = build / (stem + '-output.txt')
input_path.write_text(''.join(','.join(map(str, w)) + '\n' for w in words))
env = dict(__import__('os').environ, LEAN_PATH=str(build))
start = time.monotonic()
subprocess.run([sys.argv[1], '--run', str(here / program),
                str(input_path), str(output_path)], env=env, check=True)
elapsed = time.monotonic() - start
lines = output_path.read_text().splitlines()
assert len(lines) == len(words)
unique_edges = 0
list_entries = 0
for p, line in zip(words, lines):
    left, right = line.split('=')
    assert tuple(map(int, left.split(','))) == p
    qs = [tuple(map(int, item.split(','))) for item in right.split(';')] if right else []
    expected = checker.prefix_predecessors(p)
    assert set(qs) == expected, (p, set(qs) - expected, expected - set(qs))
    unique_edges += len(set(qs))
    list_entries += len(qs)
raw = output_path.read_bytes()
with gzip.GzipFile(filename='', fileobj=(here / (stem + '-output.txt.gz')).open('wb'),
                   mode='wb', mtime=0) as f:
    f.write(raw)
summary = {
    'status': 'PASS', 'scope': 'runtime diagnostic; kernel theorem audited separately',
    'target_nodes': len(words), 'unique_long_inverse_edges': unique_edges,
    'enumerator_list_entries': list_entries, 'lean_seconds': elapsed,
    'lean_version': subprocess.check_output([sys.argv[1], '--version'], text=True).strip(),
    'reference_certificate_sha256': hashlib.sha256((reference / 'certificate_739.json').read_bytes()).hexdigest(),
    'raw_output_bytes': len(raw), 'raw_output_sha256': hashlib.sha256(raw).hexdigest(),
    'compressed_output': (stem + '-output.txt.gz'),
    'compressed_bytes': (here / (stem + '-output.txt.gz')).stat().st_size,
    'compressed_sha256': hashlib.sha256((here / (stem + '-output.txt.gz')).read_bytes()).hexdigest(),
    'recovery_command': f'gzip -dc {stem}-output.txt.gz > {stem}-output.txt',
    'mode': mode
}
(here / (stem + '-summary.json')).write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
