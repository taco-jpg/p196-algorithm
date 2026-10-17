#!/usr/bin/env python3
"""Losslessly re-encode the complete verified tar stream with bounded-memory XZ."""
from pathlib import Path
import gzip,hashlib,json,lzma,tarfile,time
root=Path(__file__).resolve().parent
base=root/'combination'
src=base/'pr172-combination-evidence.tar.gz'
dst=root/'pr172-combination-evidence.tar.xz'
start=time.time()
tar_digest=hashlib.sha256()
with gzip.open(src,'rb') as inp, lzma.open(dst,'wb',format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,preset=6) as out:
    while chunk:=inp.read(1024*1024):
        tar_digest.update(chunk);out.write(chunk)
readback=hashlib.sha256()
with lzma.open(dst,'rb') as inp:
    while chunk:=inp.read(1024*1024): readback.update(chunk)
assert readback.digest()==tar_digest.digest()
members=[]
with tarfile.open(dst,'r|xz') as archive:
    for m in archive:
        assert m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
        fp=archive.extractfile(m);digest=hashlib.sha256();size=0
        while chunk:=fp.read(1024*1024):digest.update(chunk);size+=len(chunk)
        members.append({'path':m.name,'bytes':size,'sha256':digest.hexdigest()})
        assert size==m.size
assert len(members)==72
raw=dst.read_bytes()
result={'status':'PASS_LOSSLESS_XZ_PUBLICATION_ARCHIVE','archive':dst.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'members':members,'uncompressed_member_bytes':sum(m['bytes'] for m in members),'identical_tar_stream_sha256':tar_digest.hexdigest(),'source_gzip':{'filename':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size},'encoding':'XZ preset6 with CRC64; the original deterministic USTAR byte stream is unchanged','original_files_removed':False,'elapsed_seconds':time.time()-start}
(root/'COMBINATION_ARCHIVE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='members'},indent=2))
