#!/usr/bin/env python3
"""Reuse the published six-stage PR168 packet and execute only its PR172 extension."""
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
GIT = ROOT / 'objects.git'
B = '74a1c3922eb7af438fe40b23d2105ad07556e3f5'
H = 'b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80'
P = '7f23ce839fcc88acb235b1816c2c57dc12e16a33'
UPSTREAM_COMMIT = '159c5360dcb8e0698ba42b7cdf9dcfab29946c17'
C = 'c402fe3104c83fa74b330450c9635caed64ef67d'
S = 'fe482076a7a4bfab705a2f64a94133da3f489b4e'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1',
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', GIT_TERMINAL_PROMPT='0')
COMMANDS = []

def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def git(label, *args, expected=(0,)):
    argv = ['git', '--git-dir=' + str(GIT), *args]
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV, timeout=120)
    for suffix, data in [('stdout', p.stdout), ('stderr', p.stderr)]:
        (ROOT / (label + '.' + suffix)).write_bytes(data)
    COMMANDS.append({'label': label, 'argv': argv, 'returncode': p.returncode,
                     'stdout': label + '.stdout', 'stderr': label + '.stderr',
                     'stdout_bytes': len(p.stdout), 'stdout_sha256': hashlib.sha256(p.stdout).hexdigest()})
    save('commands.json', COMMANDS)
    assert p.returncode in expected, (argv, p.returncode, p.stderr.decode())
    return p.stdout

def entries(label, ref):
    result = {}
    for record in git(label, 'ls-tree', '-r', '-z', '--full-tree', ref).split(b'\0'):
        if record:
            metadata, path = record.split(b'\t', 1)
            mode, kind, sha = metadata.decode().split()
            result[path.decode()] = {'mode': mode, 'type': kind, 'object_id': sha}
    return result

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def diff(left, right):
    return [{'path': p, 'status': 'A' if p not in left else 'D' if p not in right else 'M',
             'before': left.get(p), 'after': right.get(p)}
            for p in sorted(left.keys() | right.keys()) if left.get(p) != right.get(p)]

def old_entries(name):
    d = json.loads((TASK / 'combination' / ('inventory-' + name + '.json')).read_text())
    return {p: {'mode': v['mode'], 'type': v['type'], 'object_id': v['sha']} for p, v in d.items()}

def status_counts(delta):
    return dict(collections.Counter(r['status'] for r in delta))

listing = json.loads((ROOT / 'upstream/REMOTE_FILES.json').read_text())
remote_binding = []
for row in listing:
    data = (ROOT / 'upstream' / row['name']).read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert len(data) == row['size'] and oid == row['sha']
    remote_binding.append({'path': row['path'], 'bytes': len(data), 'git_blob': oid,
                           'sha256': hashlib.sha256(data).hexdigest(), 'commit': UPSTREAM_COMMIT})
save('UPSTREAM_FILE_BINDING.json', remote_binding)
package = json.loads((ROOT / 'upstream/EVIDENCE_PACKAGE.json').read_text())
for name, row in package['files'].items():
    data = (ROOT / 'upstream/recovered' / name).read_bytes()
    assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['git_blob_sha1']
upstream = json.loads((ROOT / 'upstream/recovered/COMBINATION_CHECK.json').read_text())
preservation = json.loads((ROOT / 'upstream/recovered/PRESERVATION_DETAILS.json').read_text())
assert upstream['status'] == 'PASS_PROSPECTIVE_COMBINATION' and all(upstream['conditions'].values())
assert upstream['main'] == B and upstream['final_tree'] == S
assert upstream['final_local_unreferenced_commit'] == C
assert preservation['status'] == 'PASS_PRESERVATION_DETAILS' and all(preservation['checks'].values())
assert all(r['exit_code'] == 0 for r in upstream['commands'])
git('git-version', '--version')
refs_before = git('refs-before', 'show-ref', expected=(0, 1))
base = entries('tree-B', B)
assert len(base) == upstream['main_entry_count'] and fingerprint(base) == upstream['main_entries_sha256']
assert base == old_entries('B')
metadata_union = dict(base)
stage_bindings = []
for step in upstream['steps']:
    assert step['changed_existing_prior_paths'] == []
    for row in step['delta']:
        assert row['status'] == 'A' and row['before'] is None and row['path'] not in metadata_union
        metadata_union[row['path']] = row['after']
    assert len(metadata_union) == step['entry_count']
    assert fingerprint(metadata_union) == step['entries_sha256']
    stage_bindings.append({k: step[k] for k in ['pr', 'head', 'combined_tree', 'local_unreferenced_commit',
                                               'entry_count', 'entries_sha256', 'delta_status_counts']})
prior = entries('tree-upstream-final', C)
assert prior == metadata_union and fingerprint(prior) == upstream['steps'][-1]['entries_sha256']
raw_commit = git('upstream-diagnostic-commit', 'cat-file', 'commit', C).decode()
assert raw_commit.splitlines()[0] == 'tree ' + S
parents = [line[7:] for line in raw_commit.splitlines() if line.startswith('parent ')]
assert parents == upstream['steps'][-1]['ordered_parents']
ancestor = git('merge-base-upstream-H', 'merge-base', '--all', C, H).decode().strip()
assert ancestor == P
git('P-ancestor-upstream', 'merge-base', '--is-ancestor', P, C)
git('P-ancestor-H', 'merge-base', '--is-ancestor', P, H)
merge = git('merge-tree-upstream-H', 'merge-tree', '--write-tree', C, H).decode().splitlines()
assert len(merge) == 1 and len(merge[0]) == 40
T = merge[0]
combined = entries('tree-ordered-PR172', T)
assert all(combined.get(p) == v for p, v in prior.items())
assert all(combined.get(p) == v for p, v in base.items())
new_delta = diff(prior, combined)
old_delta = json.loads((TASK / 'combination/changes-P-H.json').read_text())
expected_new = [{'path': r['path'], 'status': 'A', 'before': None,
                 'after': {'mode': r['after']['mode'], 'type': r['after']['type'], 'object_id': r['after']['sha']}}
                for r in old_delta]
assert new_delta == expected_new and len(new_delta) == 288
save('PR172_ORDERED_DELTA.json', new_delta)
save('CURRENT_MAIN_TO_ORDERED_DELTA.json', diff(base, combined))
gap_to_prior = diff(old_entries('U'), prior)
gap_to_final = diff(old_entries('T'), combined)
assert gap_to_prior == gap_to_final
save('DIRECT_VERSUS_ORDERED_GAP.json', gap_to_final)
stale_details = {r['path']: r for r in preservation['stale_inherited_snapshot_comparisons']}
gap_modifications = [r for r in gap_to_final if r['status'] == 'M']
for row in gap_modifications:
    assert row['path'] in stale_details
    assert row['before'] == stale_details[row['path']]['ancestor']
    assert row['after'] == stale_details[row['path']]['actual']
save('STALE_SNAPSHOT_RESOLUTIONS.json', gap_modifications)
binding = json.loads((TASK / 'CANONICAL_BINDING_RESULT.json').read_text())
module_rows = []
for row in binding['rows']:
    value = combined[row['path']]
    assert value['object_id'] == row['reviewed_git_blob'] and value['mode'] == row['H']['mode']
    module_rows.append({'module': row['module'], 'path': row['path'], 'combined': value})
save('DEPENDENCY_INCLUSION.json', module_rows)
controls = json.loads((TASK / 'combination/registry-and-verifier-inclusion.json').read_text())
for row in controls:
    value = combined[row['path']]
    assert value['object_id'] == row['combined']['sha'] and value['mode'] == row['combined']['mode']
refs_after = git('refs-after', 'show-ref', expected=(0, 1))
assert refs_after == refs_before
grouped_gap = collections.Counter('/'.join(r['path'].split('/')[:4]) for r in gap_to_final if r['status'] == 'A')
result = {'status': 'PASS_ORDERED_EXTENSION_WITH_REUSED_PR168_EVIDENCE',
          'main': B, 'PR172_head': H, 'PR172_original_base': P,
          'upstream_coordination_commit': UPSTREAM_COMMIT,
          'reused_upstream_tree': S, 'reused_upstream_diagnostic_commit': C,
          'upstream_stages_reused_not_reexecuted': stage_bindings,
          'actual_extension_merge_base': ancestor, 'actual_extension_tree': T,
          'new_git_merge_tree_executions': 1, 'new_git_commits_created': 0,
          'prior_entry_count': len(prior), 'combined_entry_count': len(combined),
          'main_entry_count': len(base), 'main_entries_preserved': True,
          'upstream_entries_preserved': True, 'combined_entries_sha256': fingerprint(combined),
          'PR172_delta_counts': status_counts(new_delta),
          'main_to_combined_counts': status_counts(diff(base, combined)),
          'gap_exists_in_prior_direct_simulation': bool(gap_to_final),
          'direct_to_ordered_counts': status_counts(gap_to_final),
          'gap_added_directory_counts': dict(sorted(grouped_gap.items())),
          'stale_metadata_paths_retaining_newer_upstream_blobs': [r['path'] for r in gap_modifications],
          'all_34_reviewed_modules_exact': len(module_rows) == 34,
          'canonical_registry_and_verifier_exact': True,
          'source_refs_unchanged': True, 'remote_mutations': False, 'fresh_lean_execution': False,
          'actual_prerequisite_or_main_acceptance': False,
          'limitation': 'Prospective ordered source/evidence preservation only. Actual integration and refreshed platform/ownership gates remain separate.'}
save('ORDERED_COMBINATION_RESULT.json', result)
print(json.dumps(result, indent=2))
