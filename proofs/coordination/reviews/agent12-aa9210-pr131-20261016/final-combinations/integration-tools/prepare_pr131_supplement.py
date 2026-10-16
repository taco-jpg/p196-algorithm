#!/usr/bin/env python3
"""Prepare exact PR131 supplemental evidence without remote mutation.

Adapted from package_combination_supplement.py: verify actual tar members,
compare bytes in addition to size/hash, and cover the entire refreshed archive.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def checked_archive(directory):
    raw_manifest = (directory / 'MANIFEST.json').read_bytes()
    manifest = json.loads(raw_manifest)
    archive = (directory / manifest['archive']).read_bytes()
    assert len(archive) == manifest['archive_bytes']
    assert sha(archive) == manifest['archive_sha256']
    rows = {r['path']:r for r in manifest['files']}
    assert len(rows) == len(manifest['files']) == manifest['file_count']
    contents = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tf:
        for member in tf.getmembers():
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and '..' not in path.parts
            assert str(path) == member.name and member.isfile()
            assert member.name in rows and member.name not in contents
            data = tf.extractfile(member).read()
            assert len(data) == member.size == rows[member.name]['bytes']
            assert sha(data) == rows[member.name]['sha256']
            contents[member.name] = data
    assert set(contents) == set(rows)
    assert sum(map(len,contents.values())) == manifest['original_bytes']
    return raw_manifest, manifest, archive, contents

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--published', type=Path, required=True)
p.add_argument('--refreshed', type=Path, required=True)
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--original-helper', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
assert not a.output.exists()
commit = '5bd248a1fcad67677b3db65901b79af3f15d28f0'
later_commit = '5edc6cdb16f08339542a84518aceac04650b9920'
prefix = 'proofs/coordination/reviews/agent12-aa9210-pr131-20261016'
old_raw, old_manifest, old_arc, old = checked_archive(a.published)
new_raw, new_manifest, new_arc, new = checked_archive(a.refreshed)
assert sha(new_arc) == 'ca47261ad12d39dca31d8f833d64f46f715cdb17acd82f092d99065be610b431'
git_reads = []

def git_read(ref):
    argv = ['git','cat-file','blob',ref]
    result = subprocess.run(argv,cwd=a.repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stderr.decode()
    git_reads.append({'argv':argv,'cwd':str(a.repo),'exit_code':0,
                      'bytes':len(result.stdout),'sha256':sha(result.stdout),
                      'git_blob':blob(result.stdout),'stderr':result.stderr.decode()})
    return result.stdout

assert git_read(commit + ':' + prefix + '/MANIFEST.json') == old_raw
assert git_read(commit + ':' + prefix + '/' + old_manifest['archive']) == old_arc
for number in ['003','004']:
    for leaf in ['commands.json','receipt.json','source-closure.json']:
        assert git_read(later_commit + ':' + prefix + '/final-combination-' + number + '/' + leaf) == new['combination/pr131-combination-' + number + '/' + leaf]

index = {}
for name,data in old.items():
    index.setdefault((len(data),sha(data)),[]).append(name)
files, records = {}, []
for name,data in sorted(new.items()):
    candidates = index.get((len(data),sha(data)),[])
    candidates = sorted(candidates, key=lambda candidate:(candidate != name,candidate))
    origin = next((candidate for candidate in candidates if old[candidate] == data), None)
    row = {'path':name,'bytes':len(data),'sha256':sha(data)}
    if origin is None:
        text = data.decode('utf-8')
        assert text.encode('utf-8') == data
        files[name] = text
        row['storage'] = 'DIRECT_APPEND_ONLY_FILE'
    else:
        row.update({'storage':'EXACT_DUPLICATE_IN_PUBLISHED_ARCHIVE',
                    'original_archive_member':origin,
                    'member_bytes':len(old[origin]),'member_sha256':sha(old[origin]),
                    'byte_for_byte_comparison':True})
    records.append(row)

assert len(records) == 79
for row in records:
    if row['path'].endswith(('/effective.patch','/submitted.patch')):
        assert row['storage'] == 'EXACT_DUPLICATE_IN_PUBLISHED_ARCHIVE'
        assert row['bytes'] == 332020
        assert row['sha256'] == 'de2b7e9a887aa1210bc6c26abf99f16cbb9b756b652f872bf0206d67392e2f8d'
assert 'independent-review/GENERATED_OBJECT_CLEANUP.json' in files
files['integration-tools/package_combination_supplement.py'] = a.original_helper.read_text()
files['integration-tools/prepare_pr131_supplement.py'] = Path(__file__).read_text()
provenance = '''# PR131 final supplemental publication evidence

This append-only supplement represents all 79 files in the refreshed local
publication-002 archive. Every file is retained directly or references one
precise member of the already published original archive. Reuse requires an
actual byte-for-byte comparison as well as matching byte count and SHA-256;
file names or apparent semantic similarity are never sufficient.

The original archive and its manifest were freshly read as Git blobs at
coordination commit 5bd248a1fcad67677b3db65901b79af3f15d28f0 and compared with the
local publication-001 bytes. Their published directory is
proofs/coordination/reviews/agent12-aa9210-pr131-20261016.

The six final003/final004 command, receipt, and source-closure records were
also compared byte-for-byte with their direct published files at commit
5edc6cdb16f08339542a84518aceac04650b9920. Those published records and POSTMERGE
remain authoritative historical evidence; this supplement does not replace,
edit, or infer an additional compiler execution from them.

All unique final003/final004 command records, receipts, source-closure logs,
merge-tree outputs, and the new generated-object cleanup receipt are directly
included. The four complete root binary-patch files are exactly 332020 bytes
each and match existing root combination patch members of the published
archive. Their explicit references preserve the full binary patch, including
the compressed evidence bytes. Incoming inventories and unchanged helpers are
likewise referenced only after comparing their actual bytes.

The original small packaging helper and the stronger adaptation used for this
supplement are included directly. The adaptation validates safe regular tar
members, complete manifest membership and every file hash before comparing
content. Neither original nor refreshed sealed evidence was changed or deleted.
No remote write, upload, or publication occurred while preparing this file.

Recovery: obtain complete-integration-evidence.tar.xz from the pinned original
Git commit and directory; verify the archive hash in LOSSLESS_REUSE.json.
For each record, use the UTF-8 bytes of files[path] when storage is
DIRECT_APPEND_ONLY_FILE, or read original_archive_member from that verified
archive otherwise. Check the record's byte count and SHA-256 before writing to
an empty destination. Never extract arbitrary unvalidated paths. The complete
record set reconstructs every one of the 79 refreshed archive payload files.
Original tar container bytes and timestamps need not be reproduced to recover
the exact payload files; the refreshed archive's own bytes remain sealed at
the recorded local input path.

This supplement changes no mathematical source, theorem statement, proof,
audit result, attribution, or earlier evidence classification.
'''
files['SUPPLEMENT_PROVENANCE.md'] = provenance
auxiliary = [{'path':name,'bytes':len(value.encode()),'sha256':sha(value.encode())}
             for name,value in sorted(files.items()) if name not in new]
receipt = {'schema_version':2,'status':'LOSSLESS_APPEND_ONLY_SUPPLEMENT',
           'operator':'Agent #12/review131','pull_request':131,
           'head':'0bfe5347de0e5085307a3432975a18b83a3a2bba',
           'prior_evidence_commit':commit,'prior_publication_directory':prefix,
           'prior_archive':old_manifest['archive'],'prior_archive_repository_path':prefix+'/'+old_manifest['archive'],
           'prior_archive_bytes':len(old_arc),'prior_archive_sha256':sha(old_arc),'prior_archive_git_blob':blob(old_arc),
           'prior_manifest_sha256':sha(old_raw),'prior_manifest_git_blob':blob(old_raw),
           'prior_archive_verified_member_count':len(old),
           'refreshed_local_archive':str(a.refreshed/new_manifest['archive']),
           'refreshed_archive_bytes':len(new_arc),'refreshed_archive_sha256':sha(new_arc),
           'refreshed_manifest_sha256':sha(new_raw),'refreshed_member_count':len(new),
           'refreshed_payload_bytes':sum(map(len,new.values())),
           'later_direct_receipts_commit':later_commit,'published_git_reads':git_reads,
           'files':records,'direct_payload_files':sum(r['storage']=='DIRECT_APPEND_ONLY_FILE' for r in records),
           'duplicate_payload_files':sum(r['storage']=='EXACT_DUPLICATE_IN_PUBLISHED_ARCHIVE' for r in records),
           'additional_direct_files':auxiliary,'all_archives_and_members_hash_checked':True,
           'all_reuse_byte_for_byte_compared':True,'all_direct_text_round_trips_checked':True,
           'no_unproved_duplicate_mapping':True,'sealed_evidence_modified':False,'remote_mutations':False,
           'explanation':'Every refreshed payload file is retained directly or mapped to exact byte-identical content in a named member of the pinned published archive. Recovery covers all payload bytes; no new replay or postmerge check is claimed.'}
files['LOSSLESS_REUSE.json'] = json.dumps(receipt,indent=2)+'\n'
package = {'files':files,'receipt':receipt}
a.output.write_text(json.dumps(package,ensure_ascii=False))
check = json.loads(a.output.read_text())
for row in records:
    data = (check['files'][row['path']].encode() if row['storage']=='DIRECT_APPEND_ONLY_FILE'
            else old[row['original_archive_member']])
    assert data == new[row['path']] and len(data)==row['bytes'] and sha(data)==row['sha256']
assert json.loads(check['files']['LOSSLESS_REUSE.json']) == check['receipt']
print(json.dumps({'output':str(a.output),'bytes':a.output.stat().st_size,'sha256':sha(a.output.read_bytes()),
                  'direct_payload_files':receipt['direct_payload_files'],'duplicate_payload_files':receipt['duplicate_payload_files'],
                  'additional_direct_files':len(auxiliary),'payload_files_recovered_and_verified':len(records)},indent=2))
