#!/usr/bin/env python3
"""Recover the original hosted source/evidence tree, optionally including objects.

No Lean execution or network request occurs. With --zip, the exact original
56-file artifact is recovered and verified. Without it, only the seven excluded
compiled objects are omitted; every duplicate source is restored from retained bytes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    selection = json.loads((here / 'artifact-selection.json').read_text())
    retained = here / selection['retained_raw_prefix']
    outer = json.loads((retained / 'hosted-artifact-inventory.json').read_text())
    expected = dict(outer['files'])
    own = retained / 'hosted-artifact-inventory.json'
    expected['hosted-artifact-inventory.json'] = {'bytes': own.stat().st_size, 'sha256': sha(own)}
    archive = None
    if args.zip:
        assert args.zip.stat().st_size == selection['zip_bytes']
        assert sha(args.zip) == selection['zip_sha256'], 'Original ZIP hash mismatch'
        archive = zipfile.ZipFile(args.zip)
        assert set(archive.namelist()) == set(expected)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    omitted = []
    for name, pin in sorted(expected.items()):
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        if name not in selection['excluded']:
            blob = (retained / name).read_bytes()
        else:
            recovery = selection['excluded'][name]['recovery']
            if recovery['kind'] == 'copy_retained':
                blob = (retained / recovery['path']).read_bytes()
            elif archive is not None:
                blob = archive.read(recovery['member'])
            else:
                omitted.append(name)
                continue
        assert len(blob) == pin['bytes'] and hashlib.sha256(blob).hexdigest() == pin['sha256'], name
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    if archive is not None:
        archive.close()
    print(json.dumps({'status': 'PASS', 'restored_files': len(expected) - len(omitted),
                      'omitted_reproducible_objects': omitted, 'output': str(out)}, indent=2))


if __name__ == '__main__':
    main()
