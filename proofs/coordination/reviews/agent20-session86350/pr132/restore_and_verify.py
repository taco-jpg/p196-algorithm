from pathlib import Path, PurePosixPath
import hashlib, json, sys, tarfile
if len(sys.argv)!=4:
    raise SystemExit('Usage: python3 restore_and_verify.py PACKAGE_MANIFEST.json ARCHIVE.tar.gz NEW_DESTINATION')
manifest_path, archive_path, destination=map(Path,sys.argv[1:])
manifest=json.loads(manifest_path.read_text())
def sha(data):
    return hashlib.sha256(data).hexdigest()
archive_bytes=archive_path.read_bytes()
assert len(archive_bytes)==manifest['archive']['bytes'],'Archive size mismatch'
assert sha(archive_bytes)==manifest['archive']['sha256'],'Archive SHA256 mismatch'
expected=manifest['files']
expected_dirs=set(manifest['directories'])
assert not destination.exists(),'Destination must not exist'
destination.mkdir(parents=True)
seen_files=set()
seen_dirs=set()
with tarfile.open(archive_path,'r:gz') as tar:
    for member in tar:
        p=PurePosixPath(member.name)
        assert not p.is_absolute() and '..' not in p.parts and '.' not in p.parts,member.name
        assert str(p)==member.name.rstrip('/'),member.name
        rel=str(p)
        target=destination/rel
        if member.isdir():
            assert rel in expected_dirs and rel not in seen_dirs,rel
            seen_dirs.add(rel)
            target.mkdir(parents=True,exist_ok=True)
        elif member.isfile():
            assert rel in expected and rel not in seen_files,rel
            seen_files.add(rel)
            data=tar.extractfile(member).read()
            assert len(data)==expected[rel]['bytes'],rel
            assert sha(data)==expected[rel]['sha256'],rel
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:
                f.write(data)
        else:
            raise AssertionError('Unsupported archive object: '+rel)
assert seen_files==set(expected),'Archive file set mismatch'
assert seen_dirs==expected_dirs,'Archive directory set mismatch'
actual_files={p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
actual_dirs={p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_dir()}
assert actual_files==set(expected),'Restored file set mismatch'
assert actual_dirs==expected_dirs,'Restored directory set mismatch'
for rel,entry in expected.items():
    data=(destination/rel).read_bytes()
    assert len(data)==entry['bytes'],rel
    assert sha(data)==entry['sha256'],rel
print('RESTORATION PASS files='+str(len(actual_files))+' directories='+str(len(actual_dirs))+' bytes='+str(sum(x['bytes'] for x in expected.values())))
print('ARCHIVE_SHA256 '+manifest['archive']['sha256'])
print('REPORT_SHA256 '+manifest['report']['sha256'])
