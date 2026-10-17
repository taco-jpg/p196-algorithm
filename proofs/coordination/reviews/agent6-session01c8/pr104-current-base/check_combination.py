#!/usr/bin/env python3
"""Inspect PR104's exact Git combination without compiling or modifying sources."""
import hashlib
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

REPO = pathlib.Path('/workspace/scratch/01c8ccabdd45/p196-agent6')
OUT = pathlib.Path(__file__).resolve().parent
HEAD = 'c9a86a40ffd478f7c01ac68688896cba91f94dd1'
BASE = '74a1c3922eb7af438fe40b23d2105ad07556e3f5'
PRIOR_BASE = 'ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3'
PREFIX = 'proofs/contributions/agent-114/short-r-firsthit-20261016/'
REGISTRY = PREFIX + 'integration/BUILD_REGISTRY.json'
ENV = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1'}
commands = []

def git(*args, required=True):
    cmd = ['git', '-C', str(REPO), *args]
    p = subprocess.run(cmd, capture_output=True, env=ENV)
    commands.append({'argv': cmd, 'exit_code': p.returncode,
                     'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                     'stderr': p.stderr.decode(errors='replace')})
    if required and p.returncode:
        raise RuntimeError(str(cmd) + '\n' + p.stderr.decode(errors='replace'))
    return p

def entries(ref):
    result = {}
    for row in git('ls-tree', '-r', '-z', ref).stdout.split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, sha = meta.decode().split()
        result[path.decode()] = {'mode': mode, 'kind': kind, 'git_blob': sha}
    return result

result = {'schema_version': 1, 'agent': 'Agent #6', 'session': '01c8ccabdd45',
          'scope': 'Current-base tree preservation and unchanged source-closure binding only',
          'delivery_owner': 'Agent #31/session02893e4f368d',
          'main_write_slot': False, 'source_head': HEAD, 'base': BASE,
          'previously_tested_base': PRIOR_BASE, 'fresh_lean_execution': False,
          'actual_merge': False, 'started_at': datetime.now(timezone.utc).isoformat()}
try:
    merge = git('merge-tree', '--write-tree', BASE, HEAD)
    result['merge_tree_stdout'] = merge.stdout.decode()
    tree = merge.stdout.decode().strip()
    if len(tree) != 40 or any(c not in '0123456789abcdef' for c in tree):
        raise RuntimeError('Expected exactly one conflict-free tree SHA')
    result['combined_tree'] = tree
    before, after, source, prior = map(entries, (BASE, tree, HEAD, PRIOR_BASE))
    deleted = sorted(set(before) - set(after))
    modified = sorted(p for p in before.keys() & after.keys() if before[p] != after[p])
    added = sorted(set(after) - set(before))
    result['tree_preservation'] = {'base_entries': len(before), 'combined_entries': len(after),
                                 'modified': modified, 'deleted': deleted,
                                 'added': [{'path': p, **after[p]} for p in added],
                                 'all_additions_in_contribution_scope': all(p.startswith(PREFIX) for p in added),
                                 'all_added_entries_equal_reviewed_head': all(after[p] == source.get(p) for p in added)}
    if deleted or modified or len(added) != 21 or not all(p.startswith(PREFIX) and after[p] == source.get(p) for p in added):
        raise RuntimeError('Combined delta does not equal the exact 21 reviewed additions')
    registry_bytes = git('show', HEAD + ':' + REGISTRY).stdout
    registry = json.loads(registry_bytes)
    project = registry['projects']['agent114-short-r-first-eleven']
    checks = []
    for name, item in project['modules'].items():
        path, expected = item['path'], item['git_blob']
        observed = {label: collection.get(path) for label, collection in
                    [('prior_base', prior), ('base', before), ('head', source), ('combined', after)]}
        required_refs = ['head', 'combined'] if name == 'Agent114ShortRFirst11' else ['prior_base', 'base', 'head', 'combined']
        matches = all(observed[label] and observed[label]['git_blob'] == expected for label in required_refs)
        body = git('show', HEAD + ':' + path, required=False)
        byte_check = {'status': 'NOT_AVAILABLE_LOCALLY'}
        if body.returncode == 0:
            sha256 = hashlib.sha256(body.stdout).hexdigest()
            git_blob = hashlib.sha1(b'blob ' + str(len(body.stdout)).encode() + b'\0' + body.stdout).hexdigest()
            byte_check = {'status': 'PASSED' if sha256 == item['sha256'] and git_blob == expected else 'FAILED',
                          'bytes': len(body.stdout), 'sha256': sha256, 'git_blob': git_blob}
            if byte_check['status'] != 'PASSED':
                raise RuntimeError('Source byte mismatch for ' + name)
        checks.append({'module': name, 'path': path, 'expected_blob': expected,
                       'required_refs': required_refs, 'entries': observed,
                       'all_required_blob_identities_match': matches, 'source_bytes': byte_check})
        if not matches:
            raise RuntimeError('Source closure changed at ' + name)
    result['source_closure'] = checks
    verifier = registry['provenance']['verifier_path']
    verifier_blob = registry['provenance']['verifier_git_blob']
    result['verifier'] = {'path': verifier, 'expected_blob': verifier_blob,
                          'identities_match': all(c.get(verifier, {}).get('git_blob') == verifier_blob for c in [prior, before, source, after])}
    if not result['verifier']['identities_match']:
        raise RuntimeError('Verifier identity changed')
    for path in ['AGENTS.md', 'proofs/PUBLICATION_POLICY.md', 'proofs/ACCEPTED_BUILD.json']:
        if before.get(path) != after.get(path):
            raise RuntimeError('Preserved policy/build path changed: ' + path)
    result['review_references'] = ['https://github.com/taco-jpg/p196-algorithm/pull/104#pullrequestreview-5554899000',
                                   'https://github.com/taco-jpg/p196-algorithm/pull/104#pullrequestreview-5554297272']
    result['conclusion'] = 'PASS_CURRENT_BASE_REBIND; unchanged scoped independent proof and wiring evidence remains applicable'
    result['limitations'] = ['No fresh Lean, finite replay, archive recount, or global proof rebuild.',
                             'No source/PR/main mutation, ownership acquisition, or actual merge.',
                             'Current platform checks and actual writer authority are separate gates.',
                             'Refresh H and the actual main ref immediately before any eligible merge.']
    result['status'] = 'PASS'
except Exception as exc:
    result['status'] = 'FAILED'
    result['error'] = str(exc)
finally:
    result['completed_at'] = datetime.now(timezone.utc).isoformat()
    result['commands'] = commands
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result.get(k) for k in ['status', 'source_head', 'base', 'combined_tree', 'tree_preservation', 'error']}))
sys.exit(0 if result['status'] == 'PASS' else 1)
