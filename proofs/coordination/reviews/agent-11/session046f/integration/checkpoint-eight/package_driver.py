from pathlib import Path
import hashlib,io,json,tarfile
roots=[('initial',Path('/workspace/scratch/046f9285a650/integration')),('memory',Path('/dev/shm/p196-agent11-046f')),('packager',Path('/dev/shm/p196-agent11-046f/integration'))]
files={}
for prefix,root in roots:
 for f in sorted(root.iterdir()):
  if f.is_file() and f.suffix in {'.json','.py','.md'}:files[prefix+'/'+f.name]=f.read_bytes()
out=Path('/dev/shm/p196-agent11-046f/root-integration-evidence.tar.xz')
with tarfile.open(out,'w:xz') as t:
 for n,d in files.items():
  x=tarfile.TarInfo(n);x.size=len(d);x.mode=0o644;x.mtime=0;t.addfile(x,io.BytesIO(d))
with tarfile.open(out,'r:xz') as t:assert {x.name:t.extractfile(x).read() for x in t.getmembers()}==files
d=out.read_bytes();receipt={'archive':out.name,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest(),'roundtrip':'PASS','files':{n:{'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in files.items()}}
Path('/dev/shm/p196-agent11-046f/root-integration-package.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
