"""Restore and verify the complete retained driver trace using only Python's standard library."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent

def restore(decompress=False):
    meta = json.loads((HERE / 'driver_trace_archive.json').read_text())
    target = HERE / meta['compressed_path']
    temporary = target.with_name(target.name + '.restoring')
    complete = hashlib.sha256()
    total = 0
    try:
        with temporary.open('wb') as output:
            for part in meta['parts']:
                data = (HERE / part['path']).read_bytes()
                assert len(data) == part['bytes'], part['path']
                assert hashlib.sha256(data).hexdigest() == part['sha256'], part['path']
                complete.update(data)
                total += len(data)
                output.write(data)
        assert total == meta['compressed_bytes']
        assert complete.hexdigest() == meta['compressed_sha256']
        uncompressed = hashlib.sha256()
        raw_bytes = 0
        with gzip.open(temporary, 'rb') as stream:
            while chunk := stream.read(1024 * 1024):
                uncompressed.update(chunk)
                raw_bytes += len(chunk)
        assert raw_bytes == meta['original_bytes']
        assert uncompressed.hexdigest() == meta['original_sha256']
        os.replace(temporary, target)
        if decompress:
            raw_target = HERE / meta['original_path']
            with gzip.open(target, 'rb') as source, raw_target.open('wb') as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
        return {'status': 'PASS', 'parts': len(meta['parts']),
                'compressed_bytes': total, 'compressed_sha256': complete.hexdigest(),
                'original_bytes': raw_bytes, 'original_sha256': uncompressed.hexdigest()}
    finally:
        if temporary.exists():
            temporary.unlink()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decompress', action='store_true')
    args = parser.parse_args()
    print(json.dumps(restore(args.decompress), indent=2))
