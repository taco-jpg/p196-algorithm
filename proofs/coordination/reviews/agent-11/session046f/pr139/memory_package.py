from pathlib import Path
import hashlib,io,json,tarfile
root=Path('/workspace/scratch/046f9285a650/review139')
files={}
for f in sorted(root.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(root)
 if rel.parts[0] in {'snapshot','publish-evidence'} or '.rsync-tmp' in rel.parts or '__pycache__' in rel.parts:continue
 files[rel.as_posix()]=f.read_bytes()
assert len(files)==32, len(files)
assert hashlib.sha256(files['REVIEW.md']).hexdigest()=='a78d6b0f6de2f19ea3a7ac9f2b98123b3284d0195fc674de3def9b25b7d40318'
assert files['NEW_EVIDENCE_INVENTORY.json']==b''
note={'status':'PACKAGING_REPAIRED_WITH_TEMPORARY_MEMORY_FILESYSTEM','failed_manifest':'NEW_EVIDENCE_INVENTORY.json is retained as the zero-byte failed output, not accepted as a manifest. PACKAGE.json is the successful current inventory.','first_failure':'python package_evidence.py; dest.write_bytes(stored); OSError [Errno 28] No space left on device; exit1. Complete driver/receipt/stderr retained under packaging-attempt-001.','second_failure':'File <stdin>, line11; pathlib.py line1048 write_text -> return f.write(data); OSError [Errno28] No space left on device; exit1. Target: (r / NEW_EVIDENCE_INVENTORY.json).write_text(json.dumps(x,indent=2)+newline). Report update before it succeeded.','snapshot_note':'The reviewer verified and removed exact published duplicate snapshots, then observed them reappear on subsequent read. Current snapshot duplicates and synchronization temporary copies are excluded with exact recovery mappings; no original new evidence is omitted.'}
files['ROOT_PACKAGING_FAILURE_NOTE.json']=(json.dumps(note,indent=2)+'\n').encode()
out=Path('/dev/shm/p196-agent11-046f/pr139-review-evidence.tar.xz')
with tarfile.open(out,'w:xz') as t:
 for n,d in files.items():
  x=tarfile.TarInfo(n);x.size=len(d);x.mode=0o644;x.mtime=0;t.addfile(x,io.BytesIO(d))
with tarfile.open(out,'r:xz') as t: actual={x.name:t.extractfile(x).read() for x in t.getmembers()}
assert files==actual
d=out.read_bytes()
receipt={'pr':139,'head':'5d3b027df045eb017a8e37d3826b10105a587e9b','archive':out.name,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest(),'roundtrip':'PASS','retained_files':len(files),'recovery':'tar -xJf evidence.tar.xz; consult checks/snapshot-recovery.json and checks/diff-recovery.json for exact Git duplicates.','files':{n:{'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in files.items()}}
Path('/dev/shm/p196-agent11-046f/pr139-package.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
