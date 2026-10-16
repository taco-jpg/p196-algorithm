#!/usr/bin/env python3
"""Losslessly transcode the complete gzip JSONL trace to deterministic XZ."""
import gzip
import hashlib
import json
import lzma
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'two-column-cases.jsonl.gz'
target = root / 'two-column-cases.jsonl.xz'
expected = '8fb2a448bb9f19905cecccb914a047d5fd114ea144fb0bfbbd51e7d6be5e1abc'
decoded_hash = hashlib.sha256()
decoded_bytes = 0
with gzip.open(source, 'rb') as incoming, lzma.open(target, 'wb', preset=6) as outgoing:
    while block := incoming.read(1024 * 1024):
        decoded_hash.update(block)
        decoded_bytes += len(block)
        outgoing.write(block)
assert decoded_hash.hexdigest() == expected
roundtrip = hashlib.sha256()
roundtrip_bytes = 0
with lzma.open(target, 'rb') as incoming:
    while block := incoming.read(1024 * 1024):
        roundtrip.update(block)
        roundtrip_bytes += len(block)
assert roundtrip.hexdigest() == expected and roundtrip_bytes == decoded_bytes
record = {
    'status': 'LOSSLESS_COMPLETE_TRACE_TRANSCODE_PASS',
    'file': target.name,
    'format': 'XZ/LZMA2 preset 6; complete original JSONL byte stream',
    'stored_bytes': target.stat().st_size,
    'stored_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'decoded_bytes': decoded_bytes,
    'decoded_sha256': roundtrip.hexdigest(),
    'original_gzip_retained': True,
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(root / 'two-column-xz.json').write_text(json.dumps(record, indent=2) + '\n')
p = root / 'two-column-summary.json'
summary = json.loads(p.read_text())
summary['trace']['xz'] = record
p.write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(record, indent=2))
