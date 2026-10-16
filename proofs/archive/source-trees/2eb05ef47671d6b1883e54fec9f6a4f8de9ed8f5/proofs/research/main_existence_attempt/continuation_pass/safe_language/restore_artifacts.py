"""Verify complete ordered archive parts and restore exact original bytes.

All restored files are created in the requested output directory. By default
restore only the primary no-symmetry CNF and proof, sufficient for the main
UNSAT replay. --all restores the corroborating run and UNKNOWN checkpoint.
"""
from pathlib import Path
import argparse, gzip, hashlib, json, shutil, tempfile


def restore(destination,all_files=False,verify_only=False):
    source=Path(__file__).parent/'evidence_parts'
    manifest=json.loads((source/'MANIFEST.json').read_text())
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    out=[]
    with tempfile.TemporaryDirectory(prefix='safe-language-restore-') as temp:
        for artifact in manifest['artifacts']:
            if not all_files and not artifact['decoded_filename'].startswith('dfa4_neg2.'):
                continue
            archive=Path(temp)/'combined.gz';h=hashlib.sha256();size=0
            with archive.open('wb') as f:
                for part in artifact['parts']:
                    data=(source/part['file']).read_bytes()
                    assert len(data)==part['bytes']<=manifest['part_limit_bytes']
                    assert hashlib.sha256(data).hexdigest()==part['sha256']
                    h.update(data);size+=len(data);f.write(data)
            assert size==artifact['archive_bytes']
            assert h.hexdigest()==artifact['archive_sha256']
            target=destination/artifact['decoded_filename'];h=hashlib.sha256();size=0
            with gzip.open(archive,'rb') as f,open('/dev/null' if verify_only else target,'wb') as g:
                for data in iter(lambda:f.read(1<<20),b''):
                    h.update(data);size+=len(data);g.write(data)
            assert size==artifact['decoded_bytes']
            assert h.hexdigest()==artifact['decoded_sha256']
            out.append(dict(file=artifact['decoded_filename'] if verify_only else str(target),bytes=size,sha256=h.hexdigest()))
    print(json.dumps(dict(verified=True,verify_only=verify_only,artifacts=out),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('destination');p.add_argument('--all',action='store_true');p.add_argument('--verify-only',action='store_true')
    args=p.parse_args();restore(args.destination,args.all,args.verify_only)
