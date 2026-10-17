#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,tarfile,time
root=Path(__file__).resolve().parent
names=['direct-files.json','pr-files.json']
out=root/'materialization-inputs.tar.xz'
members=[]
with tarfile.open(out,'w:xz',format=tarfile.USTAR_FORMAT,preset=6) as tar:
    for name in names:
        p=root/name; b=p.read_bytes(); info=tarfile.TarInfo(name);info.size=len(b);info.mode=0o644;info.mtime=0;info.uid=info.gid=0;info.uname=info.gname=''
        with p.open('rb') as f:tar.addfile(info,f)
        members.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
with tarfile.open(out,'r:xz') as tar:
    assert tar.getnames()==names
    for m in members:
        b=tar.extractfile(m['path']).read();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
b=out.read_bytes();result={'archive':out.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'members':members,'status':'PASS_EXACT_ARCHIVE_MEMBERS','scope':'Complete original GitHub file-list and exact-head contents used by materialize.py; no source mutation or new proof execution.'}
(root/'MATERIALIZATION_INPUT_ARCHIVE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
