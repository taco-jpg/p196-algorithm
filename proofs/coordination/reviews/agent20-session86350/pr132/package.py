from pathlib import Path, PurePosixPath
import gzip, tarfile, hashlib, json, stat, io, subprocess, sys
SOURCE=Path('/dev/shm/p196-agent20-86350e418736/pr132-evidence')
OUT=Path('/dev/shm/p196-agent20-86350e418736/pr132-publication')
EXPECTED_REPORT='a3a9eb4dde09d6151bca966cd5d6a74576cd60a60ead99039df1de39c8ba9463'
def digest(data):
    return hashlib.sha256(data).hexdigest()
def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def record(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':digest(b),'git_blob_sha1':blob(b)}
def emit(msg):
    print(msg,flush=True)
assert digest((SOURCE/'REPORT.md').read_bytes())==EXPECTED_REPORT
files={}
directories=[]
for path in sorted(SOURCE.rglob('*')):
    rel=path.relative_to(SOURCE).as_posix()
    st=path.lstat()
    if stat.S_ISDIR(st.st_mode):
        directories.append(rel)
    elif stat.S_ISREG(st.st_mode):
        files[rel]={'original_path':str(path),**record(path),'original_mode':oct(stat.S_IMODE(st.st_mode)),'original_mtime_ns':st.st_mtime_ns}
    else:
        raise AssertionError('Unsupported source object: '+rel)
assert len(files)==289
assert sum(x['bytes'] for x in files.values())==4653910
index=json.loads((SOURCE/'EVIDENCE_FILES.json').read_text())
assert set(index)==set(files)-{'EVIDENCE_FILES.json'}
for rel,expected in index.items():
    assert expected['bytes']==files[rel]['bytes'],rel
    assert expected['sha256']==files[rel]['sha256'],rel
emit('SOURCE_INVENTORY PASS indexed_files=288 all_files=289 bytes=4653910 directories='+str(len(directories)))
archive=OUT/'pr132-verification-evidence.tar.gz'
with archive.open('xb') as raw:
    with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as zipped:
        with tarfile.open(fileobj=zipped,mode='w|',format=tarfile.GNU_FORMAT) as tar:
            for rel in sorted(directories+list(files)):
                info=tarfile.TarInfo(rel)
                info.uid=info.gid=info.mtime=0
                info.uname=info.gname=''
                if rel in files:
                    data=(SOURCE/rel).read_bytes()
                    assert digest(data)==files[rel]['sha256'],rel
                    info.size=len(data)
                    info.mode=0o644
                    tar.addfile(info,io.BytesIO(data))
                else:
                    info.type=tarfile.DIRTYPE
                    info.mode=0o755
                    tar.addfile(info)
archive_record=record(archive)
assert archive_record['bytes']<=20_000_000
emit('ARCHIVE PASS '+json.dumps(archive_record,sort_keys=True))
restore_source = r"""from pathlib import Path, PurePosixPath
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
"""
(OUT/'restore_and_verify.py').write_text(restore_source)
(OUT/'REPORT.md').write_bytes((SOURCE/'REPORT.md').read_bytes())
manifest={
    'schema':'pr132-existing-evidence-lossless-package-v1',
    'repository':'taco-jpg/p196-algorithm',
    'target_branch':'p196/coordination',
    'pr':132,
    'publication_head':'43219b02c191325d0263b4ad2fa1f4ebb1470a5c',
    'evidence_origin':'/root/pr132_evidence',
    'packager':'/root/pr132_publication',
    'agent':20,
    'session':'86350e418736',
    'original_root':str(SOURCE),
    'scope':'Lossless retention of already collected verification evidence. No Lean execution, source modification, repeated review, branch mutation, PR mutation, or comment.',
    'source_inventory':{'path':'EVIDENCE_FILES.json','indexed_files':288,'sha256':files['EVIDENCE_FILES.json']['sha256'],'validation':'PASS'},
    'file_count':len(files),
    'file_payload_bytes':sum(x['bytes'] for x in files.values()),
    'directory_count':len(directories),
    'archive':{'filename':archive.name,'format':'GNU tar with gzip compression; sorted members; zero uid/gid/mtime; empty owner names; regular files 0644; directories 0755; empty gzip filename and zero gzip mtime',**archive_record},
    'report':{'filename':'REPORT.md','byte_identical_to_original':True,**record(OUT/'REPORT.md')},
    'recovery':{'instructions':'RECOVERY.md','script':'restore_and_verify.py','command':'python3 restore_and_verify.py PACKAGE_MANIFEST.json pr132-verification-evidence.tar.gz restored-evidence','scope':'Exact file names, directory names, contents, sizes and SHA256 values are restored and checked. Original ownership and timestamps are not applied; original file mode and mtime are recorded for provenance.'},
    'directories':directories,
    'files':files
}
(OUT/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
recovery=f"""# PR132 Evidence Recovery

This package retains every regular file and directory in the original completed evidence tree, including the original inventory, retrieval metadata, failed history, validation scripts, and raw validation outputs. The readable REPORT.md is an exact copy of the archived original report.

- Original root: {SOURCE}
- Files: {len(files)}
- Directories: {len(directories)}
- Original file payload: {sum(x['bytes'] for x in files.values())} bytes
- Archive: {archive.name}
- Archive size: {archive_record['bytes']} bytes
- Archive SHA-256: {archive_record['sha256']}
- Archive Git blob SHA-1: {archive_record['git_blob_sha1']}
- Report SHA-256: {EXPECTED_REPORT}
- Pinned PR132 head: 43219b02c191325d0263b4ad2fa1f4ebb1470a5c

## Restore and verify

Place PACKAGE_MANIFEST.json, restore_and_verify.py, and the archive in one directory. Use Python 3 and an unused output directory:

    python3 restore_and_verify.py PACKAGE_MANIFEST.json pr132-verification-evidence.tar.gz restored-evidence

The script first checks the compressed archive's exact size and SHA-256, rejects absolute or traversing paths, rejects duplicate entries and special objects, restores every expected file and directory, and verifies the complete path sets plus every restored file's size and SHA-256. A successful run prints RESTORATION PASS.

PACKAGE_MANIFEST.json lists each original absolute path, relative path, byte size, SHA-256, Git blob identity, original mode, and original modification time. The archive normalizes ownership, permissions, and timestamps. Recovery guarantees file content and path equality; it does not reinstate original ownership or timestamps.

The packaging run additionally compared every restored file directly with its original bytes and rechecked that the original tree did not change. Its exact output is retained in package.stdout.log, package.stderr.log, restore.stdout.log, and restore.stderr.log; PACKAGE_VALIDATION.json records the result and command.

## Evidence scope

Fresh Lean execution in this session remains **NOT_RUN**. This operation validates packaging and byte restoration only. The archived existing-evidence report retains its attributed historical compiler logs, theorem-axiom outputs, independent review, failures, and stated limitations. Immutable blob creation does not attach a branch, update a pull request, or merge code. The delivery owner performs any subsequent guarded coordination attachment.

## Independent source index check

After restoration, restored-evidence/EVIDENCE_FILES.json remains the original 288-file index, excluding only itself. The outer package manifest indexes all 289 files, including that original inventory.
"""
(OUT/'RECOVERY.md').write_text(recovery)
cmd=[sys.executable,str(OUT/'restore_and_verify.py'),str(OUT/'PACKAGE_MANIFEST.json'),str(archive),str(OUT/'restored-evidence')]
with (OUT/'restore.stdout.log').open('wb') as stdout,(OUT/'restore.stderr.log').open('wb') as stderr:
    result=subprocess.run(cmd,stdout=stdout,stderr=stderr,check=False)
assert result.returncode==0,'Restoration subprocess failed'
emit((OUT/'restore.stdout.log').read_text().rstrip())
assert (OUT/'restore.stderr.log').read_bytes()==b''
for rel,entry in files.items():
    original=(SOURCE/rel).read_bytes()
    restored=(OUT/'restored-evidence'/rel).read_bytes()
    assert original==restored,rel
    assert len(original)==entry['bytes'] and digest(original)==entry['sha256'],rel
source_files={p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()}
source_dirs={p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_dir()}
assert source_files==set(files)
assert source_dirs==set(directories)
emit('DIRECT_ORIGINAL_RESTORED_BYTE_COMPARISON PASS files=289')
emit('SOURCE_TREE_UNCHANGED PASS')
validation={
    'status':'PASS',
    'source_inventory_check':'PASS',
    'archive_restoration':'PASS',
    'direct_original_restored_byte_comparison':'PASS',
    'source_tree_unchanged':'PASS',
    'file_count':len(files),
    'directory_count':len(directories),
    'file_payload_bytes':sum(x['bytes'] for x in files.values()),
    'archive':archive_record,
    'manifest':record(OUT/'PACKAGE_MANIFEST.json'),
    'report':record(OUT/'REPORT.md'),
    'recovery_instructions':record(OUT/'RECOVERY.md'),
    'recovery_script':record(OUT/'restore_and_verify.py'),
    'restoration_command':cmd,
    'restoration_exit_code':result.returncode,
    'restoration_stdout':record(OUT/'restore.stdout.log'),
    'restoration_stderr':record(OUT/'restore.stderr.log'),
    'fresh_Lean_execution':'NOT_RUN',
    'remote_branch_or_PR_mutation':'NONE',
    'publication':'Not yet attempted by this script; immutable Git blob receipts are recorded separately.'
}
(OUT/'PACKAGE_VALIDATION.json').write_text(json.dumps(validation,indent=2,sort_keys=True)+'\n')
emit('PACKAGE_VALIDATION PASS')
