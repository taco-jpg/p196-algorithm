#!/usr/bin/env python3
"""Read back the immutable PR153 delivery supplement and verify its payload."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
DEST = ROOT.parent / 'pr153-delivery-remote-readback'
COMMIT = 'eb8bfd887211a8bc992b6e2dd0fa675eca306025'
PREFIX = 'proofs/coordination/evidence/agent20-session16fe/pr153/'

def identity(data):
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

def main():
    DEST.mkdir(exist_ok=False)
    manifest = ROOT/'DELIVERY_FILES.json'
    entries = json.loads(manifest.read_text())['files']
    entries.append(dict(remote_path=manifest.name, **identity(manifest.read_bytes())))
    def download(entry):
        name = entry['remote_path']
        url = f'https://raw.githubusercontent.com/taco-jpg/p196-algorithm/{COMMIT}/{PREFIX}{name}'
        try:
            request = urllib.request.Request(url, headers={'User-Agent':'Agent20-PR153-delivery-readback'})
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.status
                content = response.read(entry['bytes']+1)
            actual = identity(content)
            path = DEST/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            expected = {key:entry[key] for key in actual}
            return dict(path=name,url=url,http_status=status,expected=expected,actual=actual,
                        byte_identical=status==200 and actual==expected)
        except Exception as exc:
            return dict(path=name,url=url,byte_identical=False,exception=repr(exc))
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = sorted(pool.map(download,entries),key=lambda item:item['path'])
    passed = all(item['byte_identical'] for item in records)
    report = dict(schema=1,commit=COMMIT,prefix=PREFIX,files=records,all_remote_bytes_match=passed,
                  lean_executed=False,main_written=False)
    if passed:
        command = [sys.executable,str(DEST/'delivery/verify_delivery.py'),'--package',str(DEST/'delivery')]
        result = subprocess.run(command,capture_output=True,text=True)
        report['archive_verification'] = dict(command=command,returncode=result.returncode,
                                             stdout=result.stdout,stderr=result.stderr)
        watched = json.loads((DEST/'FINAL_WRITER_WATCH.json').read_text())['files']
        exact = all(identity(item['utf8_content'].encode('utf-8')) ==
                    {key:item[key] for key in ('bytes','sha256','git_blob_sha1')} for item in watched)
        report['final_writer_watch'] = dict(files=len(watched),all_embedded_bytes_match=exact)
        passed = result.returncode==0 and exact
    report['status'] = 'PASS_ALL_REMOTE_DELIVERY_BYTES_AND_MEMBERS' if passed else 'FAIL'
    (DEST/'DELIVERY_PUBLICATION_READBACK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],files=len(records),commit=COMMIT)))
    return 0 if passed else 1

if __name__ == '__main__':
    raise SystemExit(main())
