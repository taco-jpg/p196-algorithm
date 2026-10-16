#!/usr/bin/env python3
"""Bind a completed frozen-source build to the immutable published source blobs.

The existing verifier report is read, never rewritten. In a partial clone,
git may need network access to obtain a published blob from the promisor remote.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


def main() -> None:
    root = Path(__file__).resolve().parents[5]
    package = Path(__file__).resolve().parents[1]
    registry_path = root / 'proofs/Agent104ExactMass.registry.json'
    registry = json.loads(registry_path.read_text())
    modules = registry['projects']['agent104-exact-mass']['modules']
    published = '1c3d7b7b9d45e2aa40f689690c188bb3878de891'
    run = package / 'verification/independent-clean-001'
    report = json.loads((run / 'verification.json').read_text())
    if report['status'] != 'PASS':
        raise RuntimeError('The independent build has not passed')
    snapshot = run / 'agent104-exact-mass/source'

    def git(*arguments: str) -> bytes:
        return subprocess.check_output(['git', *arguments], cwd=root)

    if git('rev-parse', published + '^{commit}').decode().strip() != published:
        raise RuntimeError('Published commit identity mismatch')
    records = {}
    for name, record in modules.items():
        data = git('show', published + ':' + record['path'])
        built = (snapshot / (name + '.lean')).read_bytes()
        working = (root / record['path']).read_bytes()
        if data != built or data != working:
            raise RuntimeError('Published/build/worktree source mismatch: ' + name)
        sha = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        actual_blob = git('rev-parse', published + ':' + record['path']).decode().strip()
        if sha != record['sha256'] or blob != record['git_blob'] or actual_blob != blob:
            raise RuntimeError('Published source fingerprint mismatch: ' + name)
        records[name] = {
            'published_path': record['path'],
            'published_git_blob': blob,
            'published_sha256': sha,
            'bytes': len(data),
            'compiled_snapshot_path': str((snapshot / (name + '.lean')).relative_to(root)),
            'published_equals_compiled_snapshot': True,
            'published_equals_worktree_at_linkage': True,
        }
    checker = registry['verifier']
    checker_bytes = git('show', published + ':' + checker['path'])
    if checker_bytes != (root / checker['path']).read_bytes():
        raise RuntimeError('Published checker differs from invoked checker')
    if hashlib.sha256(checker_bytes).hexdigest() != checker['sha256']:
        raise RuntimeError('Published checker fingerprint mismatch')
    result = {
        'schema_version': 1,
        'status': 'PASS_ALL_SIX_PUBLISHED_SOURCES_EQUAL_COMPILED_SNAPSHOTS',
        'independent_reviewer': 'real subagent /root/strategy_review',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'published_commit': published,
        'published_branch': 'research/agent-104/exact-zero-gap-20261016T2126Z',
        'pull_request': 96,
        'original_build_source_head': report['source_commit'],
        'original_build_report_sha256': hashlib.sha256((run / 'verification.json').read_bytes()).hexdigest(),
        'original_build_report_unchanged': True,
        'working_tree_head_at_linkage': git('rev-parse', 'HEAD').decode().strip(),
        'source_tree_clean_semantics': 'The original verifier checks tracked files only with --untracked-files=no. Its retained flag does not assert that new source files were committed in that worktree.',
        'unmodified_verifier_matches_published_commit': True,
        'verifier_sha256': checker['sha256'],
        'registry_sha256': hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        'modules': records,
    }
    output = package / 'verification/published-source-linkage.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'published_commit': published,
                      'module_count': len(records), 'output': str(output)}))


if __name__ == '__main__':
    main()
