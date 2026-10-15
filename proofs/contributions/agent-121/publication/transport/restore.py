"""Restore the exact Agent121 evidence snapshot; reject changed or unsafe paths."""
import hashlib, io, json, pathlib, tarfile
ROOT = pathlib.Path('proofs/contributions/agent-121')
PREFIX = ROOT.as_posix() + '/'
ARCHIVE_SHA = 'a8ae0cb8efdc46857b74a825ee04e4eb91ef73d92ae12c39f978ceea79116b4a'
MANIFEST_SHA = 'ae20790385c36c38fb8048cb570916f506803569b28bda1b7db258d3b485a480'
def digest(b): return hashlib.sha256(b).hexdigest()
parts = [ROOT / 'publication/transport' / ('evidence.part%02d' % i) for i in range(9)]
blob = b''.join(p.read_bytes() for p in parts)
assert len(blob) == 63272 and digest(blob) == ARCHIVE_SHA, 'Archive identity mismatch'
files = {}
with tarfile.open(fileobj=io.BytesIO(blob), mode='r:xz') as tar:
    for m in tar.getmembers():
        p = pathlib.PurePosixPath(m.name)
        assert m.isfile() and not p.is_absolute() and '..' not in p.parts
        assert m.name.startswith(PREFIX) and m.name not in files
        files[m.name] = tar.extractfile(m).read()
assert len(files) == 142 and sum(map(len, files.values())) == 849208
original_manifest = files[PREFIX + 'MANIFEST.json']
assert digest(original_manifest) == MANIFEST_SHA
records = json.loads(original_manifest)['files']
assert len(records) == 141
assert {PREFIX+r['path'] for r in records} == set(files)-{PREFIX+'MANIFEST.json'}
for r in records:
    b = files[PREFIX+r['path']]
    assert len(b) == r['bytes'] and digest(b) == r['sha256'], r['path']
# Validate every existing destination before writing any research byte.
for name, data in files.items():
    p = pathlib.Path(name)
    assert not p.exists() or p.read_bytes() == data, 'Refuse changed destination: '+name
for name, data in files.items():
    p = pathlib.Path(name); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
report = {'status':'PASS','archive_sha256':ARCHIVE_SHA,'file_count':142,'file_bytes':849208,
          'original_manifest_sha256':MANIFEST_SHA,
          'files':[{'path':n,'bytes':len(b),'sha256':digest(b)} for n,b in sorted(files.items())]}
(ROOT/'publication/original-byte-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: restored all 142 original files, 849208 bytes, exact manifest matches')
