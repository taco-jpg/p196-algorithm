#!/usr/bin/env python3
"""Read-only byte/mapping audit of parent-authored closing evidence."""
from pathlib import Path, PurePosixPath
import hashlib, json, tarfile
ROOT = Path('/dev/shm/p196-agent30-4ab29b6d0234')
OUT = ROOT / 'delivery_final_check'
PUB = ROOT / 'publication'

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}

def matches(data, row):
    actual = identity(data)
    return all(actual[k] == row[k] for k in actual if k in row)

def safe(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and str(path) == name and '\\' not in name

archive = PUB / 'parent-and-repair-evidence.tar.gz'
index_path = PUB / 'parent-and-repair-evidence-index.json'
index = json.loads(index_path.read_bytes())
issues = []
records = []
idx = {row['path']: row for row in index['files']}
exc = {row['path']: row for row in index['exclusions']}
if len(idx) != len(index['files']): issues.append('duplicate index path')
if len(exc) != len(index['exclusions']): issues.append('duplicate exclusion path')
if set(idx) & set(exc): issues.append('included/excluded overlap')
if not matches(archive.read_bytes(), index['archive']): issues.append('archive outer identity mismatch')
with tarfile.open(archive, 'r:gz') as tf:
    members = tf.getmembers()
    names = [m.name for m in members]
    if len(names) != len(set(names)): issues.append('duplicate archive name')
    if len(names) != index['member_count'] or set(names) != set(idx): issues.append('archive/index member-set mismatch')
    data = {}
    for m in members:
        if not m.isfile() or not safe(m.name):
            issues.append('nonregular or unsafe path ' + m.name)
            continue
        b = tf.extractfile(m).read()
        data[m.name] = b
        exact_index = m.name in idx and matches(b, idx[m.name]) and m.size == len(b)
        if m.name == 'EXCLUDED_REPRODUCIBLE_OUTPUTS.json':
            source = 'generated from index.exclusions'
            original = (json.dumps(index['exclusions'], indent=2) + '\n').encode()
        elif m.name == 'original-pr-body.md':
            source = 'publication/ORIGINAL_PR_BODY.md'
            original = (ROOT / source).read_bytes()
        else:
            source = m.name
            p = ROOT / source
            if p.is_symlink() or not p.is_file():
                issues.append('missing/nonregular source ' + source)
                original = None
            else: original = p.read_bytes()
        exact_source = original is not None and b == original
        if not exact_index or not exact_source: issues.append('index/source byte mismatch ' + m.name)
        records.append({'path':m.name, **identity(b), 'safe_regular_member':True,
                        'index_equal':exact_index, 'source':source, 'source_byte_equal':exact_source})

exclusions = []
for name,row in exc.items():
    p = ROOT / name
    ok = safe(name) and p.is_file() and not p.is_symlink() and matches(p.read_bytes(),row)
    reproducible = name.endswith('.olean') or name in {'integration/base-tree.json','integration/source-tree.json'} or name.endswith('.pyc') or '__pycache__' in PurePosixPath(name).parts
    if not ok or not reproducible: issues.append('exclusion identity/type mismatch ' + name)
    exclusions.append({'path':name,'exact_identity':ok,'reproducible_type':reproducible,'reason':row['reason']})

inventory = []
for dirname in ['parent-replay','parent-source','repair_review','prepared']:
    actual = set()
    for p in (ROOT/dirname).rglob('*'):
        if p.is_symlink(): issues.append('source tree symlink ' + str(p.relative_to(ROOT)))
        if p.is_file(): actual.add(str(p.relative_to(ROOT)))
    archived = {x for x in idx if x.startswith(dirname+'/')}
    excluded = {x for x in exc if x.startswith(dirname+'/')}
    missing = sorted(actual - archived - excluded)
    extra = sorted((archived | excluded) - actual)
    if missing or extra: issues.append('scope inventory mismatch ' + dirname)
    inventory.append({'directory':dirname,'regular_files':len(actual),'archived':len(archived),'excluded':len(excluded),'missing':missing,'extra':extra})

receipt = json.loads(data['parent-replay/replay-execution.json'])
log_refs = []
for command in receipt['commands']:
    for stream in ['stdout','stderr']:
        row = command[stream]
        name = 'parent-replay/'+row['file']
        ok = name in data and matches(data[name],row)
        if not ok: issues.append('receipt log not faithfully retained '+name)
        log_refs.append({'path':name,'matches_receipt':ok})
for row in receipt['outputs']:
    name='parent-replay/'+row['file']
    if name not in exc or not all(exc[name][k]==row[k] for k in ['bytes','sha256']):
        issues.append('output-object exclusion not bound to receipt '+name)
for suffix in ['summary','roots','dependency-graph','endpoints','unsafe-selected']:
    name='parent-replay/audit-'+suffix+'.json'
    if name not in data: issues.append('audit output omitted '+name)

copies = []
for outer,inner in [('PARENT_REPLAY_RECEIPT.json','parent-replay/replay-execution.json'),
                    ('INITIAL_COMBINATION.json','integration/original-combination.json'),
                    ('ORIGINAL_PR_BODY.md','original-pr-body.md'),
                    ('REPAIR_REVIEW.md','repair_review/REVIEW.md'),
                    ('REPAIR_REVIEW_MANIFEST.json','repair_review/FINAL_MANIFEST.json')]:
    ok=(PUB/outer).read_bytes()==data[inner]
    if not ok: issues.append('exposed copy mismatch '+outer)
    copies.append({'outer':outer,'archive_member':inner,'byte_equal':ok})
for directory,files in [('semantic',['SEMANTIC_REVIEW.md','SOURCE_MANIFEST.json']),('package_audit',['PACKAGE_REVIEW.md','PACKAGE_MANIFEST.json'])]:
    for name in files:
        ok=(PUB/name).read_bytes()==(ROOT/directory/name).read_bytes()
        if not ok: issues.append('review report exposed copy mismatch '+name)
        copies.append({'outer':name,'source':directory+'/'+name,'byte_equal':ok})

result = {'schema_version':1,'status':'PASS' if not issues else 'FAIL','issues':issues,
          'archive':{'path':str(archive),**identity(archive.read_bytes())},
          'index':{'path':str(index_path),**identity(index_path.read_bytes())},
          'packager':{'path':'prepared/package_parent_evidence.py',**identity((ROOT/'prepared/package_parent_evidence.py').read_bytes())},
          'member_count':len(records),'archive_file_set_equals_index':set(data)==set(idx),
          'all_members_equal_live_sources':all(x['source_byte_equal'] for x in records),
          'inventory':inventory,'exclusions':exclusions,'receipt_log_references':log_refs,'copies':copies,'members':records,
          'reviewer_lean_builds_executed':0,'parent_packager_reexecuted':False,'remote_writes':False}
(OUT/'PARENT_ARCHIVE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'members','receipt_log_references','exclusions'}},indent=2))
