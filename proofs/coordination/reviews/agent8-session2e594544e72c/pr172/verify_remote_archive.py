#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,time,urllib.request
root=Path(__file__).resolve().parent
url='https://raw.githubusercontent.com/taco-jpg/p196-algorithm/b2b007a9b1606f21c6802d7e52060cbaf09ae3c8/proofs/coordination/reviews/agent8-session2e594544e72c/pr172/pr172-combination-evidence.tar.xz'
start=time.time();h256=hashlib.sha256();hgit=hashlib.sha1(b'blob 1193304\0');total=0
out=root/'remote-readback'/'pr172-combination-evidence.tar.xz';out.parent.mkdir(exist_ok=True)
with urllib.request.urlopen(url,timeout=30) as inp, out.open('wb') as target:
    while chunk:=inp.read(65536):
        target.write(chunk);h256.update(chunk);hgit.update(chunk);total+=len(chunk)
assert total==1193304
assert h256.hexdigest()=='909d54b92ce27ef81311776349ba9f74e548ebd478446785fcbcc0ce104d4cfb'
assert hgit.hexdigest()=='21b93b9f9f4e2d2efc83030f03f0d56507b28e6a'
result={'status':'PASS_EXACT_REMOTE_ARCHIVE_BYTES','url':url,'bytes':total,'sha256':h256.hexdigest(),'git_blob':hgit.hexdigest(),'elapsed_seconds':time.time()-start,'reason':'The GitHub contents tool returned the correct blob metadata but empty content for this over-1MB binary; exact public raw-content retrieval verifies all bytes.'}
(root/'REMOTE_ARCHIVE_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
