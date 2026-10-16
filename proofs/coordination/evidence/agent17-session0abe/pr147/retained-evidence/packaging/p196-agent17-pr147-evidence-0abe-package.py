#!/usr/bin/env python3
"""Losslessly preserve already completed PR147 evidence; no source review or Lean."""
from pathlib import Path
import collections, datetime, hashlib, json, tarfile
BASE=Path('/dev/shm')
NAME='p196-agent17-pr147-evidence-0abe'
SOURCE=BASE/NAME
ARCHIVE=BASE/(NAME+'.tar.xz')
REPORT=BASE/(NAME+'-packaging-verification.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
def file_record(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':sha(data)}
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert SOURCE.is_dir()
assert not ARCHIVE.exists(), 'Do not overwrite an existing archive.'
assert not REPORT.exists(), 'Do not overwrite an existing verification.'
original_manifest_path=SOURCE/'NEW-ARTIFACTS.json'
original_manifest_bytes=original_manifest_path.read_bytes()
original_manifest=json.loads(original_manifest_bytes)
original_manifest_entries=original_manifest['files']
assert len(original_manifest_entries)==263
all_paths=sorted(SOURCE.rglob('*'))
assert all(p.is_dir() or p.is_file() for p in all_paths)
assert not any(p.is_symlink() for p in all_paths)
files=[p for p in all_paths if p.is_file()]
originals={str(p.relative_to(SOURCE)):file_record(p) for p in files}
assert len(originals)==264
assert set(originals)==set(original_manifest_entries)|{'NEW-ARTIFACTS.json'}
for path,expected in original_manifest_entries.items():
    assert originals[path]==expected, ('Original manifest mismatch',path)
assert originals['NEW-ARTIFACTS.json']=={'bytes':len(original_manifest_bytes),'sha256':sha(original_manifest_bytes)}
original_stats={str(p.relative_to(SOURCE)):{'mode':p.stat().st_mode&0o7777,'mtime':p.stat().st_mtime} for p in files}
with tarfile.open(ARCHIVE,'x:xz',format=tarfile.PAX_FORMAT,preset=9) as tf:
    tf.add(SOURCE,arcname=NAME,recursive=True)
expected_member_names={NAME+'/'+path for path in originals}
member_records={}
nonregular=[]
with tarfile.open(ARCHIVE,'r:xz') as tf:
    members=tf.getmembers()
    names=[m.name for m in members]
    assert len(names)==len(set(names)), 'Duplicate archive members'
    actual_regular={m.name for m in members if m.isfile()}
    assert actual_regular==expected_member_names
    for m in members:
        assert m.name==NAME or m.name.startswith(NAME+'/')
        assert '..' not in Path(m.name).parts
        if not m.isfile():
            assert m.isdir(), ('Unexpected nonregular member',m.name,m.type)
            nonregular.append({'member':m.name,'type':'directory'})
            continue
        rel=m.name[len(NAME)+1:]
        data=tf.extractfile(m).read()
        rec={'bytes':len(data),'sha256':sha(data)}
        assert m.size==len(data)
        assert rec==originals[rel], ('Archive byte mismatch',rel)
        assert m.mode==original_stats[rel]['mode']
        assert m.mtime==original_stats[rel]['mtime']
        if rel in original_manifest_entries:
            assert rec==original_manifest_entries[rel]
        member_records[rel]={'archive_member':m.name,'bytes':rec['bytes'],'sha256':rec['sha256'],'matches_original':True,'matches_original_manifest':True if rel in original_manifest_entries else 'manifest itself, separately hashed','mode':m.mode,'mtime':m.mtime}
    archived_manifest=tf.extractfile(NAME+'/NEW-ARTIFACTS.json').read()
    assert archived_manifest==original_manifest_bytes
after_paths=sorted(SOURCE.rglob('*'))
assert [str(p.relative_to(SOURCE)) for p in after_paths]==[str(p.relative_to(SOURCE)) for p in all_paths]
after={str(p.relative_to(SOURCE)):file_record(p) for p in after_paths if p.is_file()}
assert after==originals, 'Original directory changed during packaging'
after_stats={str(p.relative_to(SOURCE)):{'mode':p.stat().st_mode&0o7777,'mtime':p.stat().st_mtime} for p in after_paths if p.is_file()}
assert after_stats==original_stats, 'Original file metadata changed during packaging'
report={'status':'PASS','operation':'Lossless packaging of already qualified evidence only','started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_directory':str(SOURCE),'archive':{'path':str(ARCHIVE),**file_record(ARCHIVE)},'packaging_script':{'path':str(Path(__file__).resolve()),**file_record(Path(__file__).resolve())},'original_manifest':{'path':str(original_manifest_path),'entries':len(original_manifest_entries),**originals['NEW-ARTIFACTS.json']},'regular_member_count':len(member_records),'expected_regular_member_count':len(originals),'exact_regular_member_set_match':True,'regular_member_names_unique':True,'all_regular_member_bytes_sizes_sha256_match_originals':True,'all_263_original_manifest_entries_match_originals_and_archive':True,'original_manifest_file_itself_preserved_byte_for_byte':True,'original_files_metadata_preserved_in_archive':True,'original_directory_unchanged':True,'lean_processes_executed':0,'source_or_evidence_review_repeated':False,'remote_mutations':0,'regular_members':member_records,'nonregular_members':nonregular}
REPORT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

