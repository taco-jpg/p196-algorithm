#!/usr/bin/env python3
"""Bind reused local receipts to their already-published immutable Git objects."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
PRIOR = 'b2b007a9b1606f21c6802d7e52060cbaf09ae3c8'
UPSTREAM = '159c5360dcb8e0698ba42b7cdf9dcfab29946c17'

def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}

listing = json.loads((ROOT / 'PRIOR_PUBLICATION_FILES.json').read_text())
listing = {r['name']: r for r in listing}
archive = json.loads((ROOT / 'PRIOR_ARCHIVE_REFERENCE.json').read_text())
archive_identity = ident(ROOT / 'PRIOR_ARCHIVE_REFERENCE.json')
assert archive_identity['git_blob'] == listing['COMBINATION_ARCHIVE.json']['sha']
members = {r['path']: r for r in archive['members']}
prior_inputs = []
for name in ['inventory-B.json', 'inventory-U.json', 'inventory-T.json',
             'changes-P-H.json', 'registry-and-verifier-inclusion.json']:
    identity = ident(TASK / 'combination' / name)
    member = 'pr172-combination/' + name
    assert all(identity[k] == members[member][k] for k in ['bytes', 'sha256'])
    prior_inputs.append({'local_path': str(TASK / 'combination' / name),
                         'archive_member': member, **identity})
binding = ident(TASK / 'CANONICAL_BINDING_RESULT.json')
assert binding['git_blob'] == listing['CANONICAL_BINDING_RESULT.json']['sha']
package = json.loads((ROOT / 'upstream/EVIDENCE_PACKAGE.json').read_text())
recovered = []
for name, item in package['files'].items():
    actual = ident(ROOT / 'upstream/recovered' / name)
    assert actual['bytes'] == item['bytes'] and actual['sha256'] == item['sha256']
    assert actual['git_blob'] == item['git_blob_sha1']
    recovered.append({'package_member': name, **actual})
result = {
 'status': 'PASS_REUSED_IMMUTABLE_INPUT_BINDING',
 'prior_publication_commit': PRIOR,
 'prior_archive_path': 'proofs/coordination/reviews/agent8-session2e594544e72c/pr172/' + archive['archive'],
 'prior_archive': {k: archive[k] for k in ['bytes', 'sha256', 'git_blob']},
 'prior_archive_reference': archive_identity,
 'prior_local_inputs_verified_against_published_archive_manifest': prior_inputs,
 'canonical_binding_result': {'commit': PRIOR, **binding},
 'upstream_publication_commit': UPSTREAM,
 'upstream_evidence_package': ident(ROOT / 'upstream/EVIDENCE_PACKAGE.json'),
 'all_33_recovered_files_verified': len(recovered) == 33,
 'recovered_file_identities': recovered,
 'package_scripts_executed': False, 'six_upstream_git_merges_reexecuted': False,
 'fresh_lean_execution': False,
 'scope': 'Content and retained-command binding only; no new mathematical review or actual integration.'}
(ROOT / 'REUSE_BINDING_RECEIPT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': result['status'], 'prior_inputs': len(prior_inputs),
                  'upstream_recovered_files': len(recovered),
                  'package_blob': result['upstream_evidence_package']['git_blob']}, indent=2))
