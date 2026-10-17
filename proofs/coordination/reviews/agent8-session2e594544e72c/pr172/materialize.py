#!/usr/bin/env python3
"""Materialize complete added-file PR patches and exact fetched blobs, checking Git identity."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, re

root=Path(__file__).resolve().parent
files=json.loads((root/'pr-files.json').read_text())
direct={x['sha']:x for x in json.loads((root/'direct-files.json').read_text())}
manifest=[]
errors=[]
assert len(files)==288 and len({f['filename'] for f in files})==288
for f in files:
    name=f['filename']; p=PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and f['status']=='added'
    if f['sha'] in direct:
        x=direct[f['sha']]
        data=base64.b64decode(x['content']) if x['encoding']=='base64' else x['content'].encode('utf-8')
        method='GitHub exact-head content; deduplicated by Git blob'
    elif f.get('patch'):
        pieces=[]
        for line in f['patch'].splitlines():
            if line.startswith('@@'): continue
            if line=='\\ No newline at end of file':
                assert pieces and pieces[-1].endswith('\n')
                pieces[-1]=pieces[-1][:-1]
            elif line.startswith('+'): pieces.append(line[1:]+'\n')
            else: raise AssertionError((name,'unexpected added-only patch line',line[:80]))
        data=''.join(pieces).encode('utf-8')
        method='Complete GitHub added-file patch reconstructed'
    else:
        errors.append({'path':name,'sha':f['sha'],'problem':'missing content'});continue
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=f['sha']:
        errors.append({'path':name,'sha':f['sha'],'got':blob,'problem':'identity mismatch or truncated patch'});continue
    dest=root/'source'/name; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append({'path':name,'bytes':len(data),'git_blob':blob,'sha256':hashlib.sha256(data).hexdigest(),'method':method})
result={'pr':172,'source_head':'b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80','expected_files':288,'verified_files':len(manifest),'total_bytes':sum(x['bytes'] for x in manifest),'files':manifest,'errors':errors,'fresh_lean_execution':False}
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
raise SystemExit(0 if not errors and len(manifest)==288 else 1)
