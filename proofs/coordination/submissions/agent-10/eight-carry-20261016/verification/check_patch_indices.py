#!/usr/bin/env python3
"""Check an additive source patch using isolated Git indices, without checkout."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import tempfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--patch', required=True, type=Path)
    ap.add_argument('--source-record', required=True, type=Path)
    ap.add_argument('--registry', required=True)
    ap.add_argument('--project', required=True)
    ap.add_argument('--main-ref', required=True)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    assert not args.output.exists(), 'Preserve earlier receipts; choose a new path.'
    record = json.loads(args.source_record.read_text())
    baseline = record['source_baseline']
    delivery = record['local_delivery_commit']
    patch_data = args.patch.read_bytes()
    assert sha(patch_data) == record['patch_sha256']
    commands = []

    def git(*cmd, env=None, log=False):
        r = subprocess.run(['git', *cmd], cwd=args.repo, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if log:
            commands.append({'arguments': ['git', *cmd], 'returncode': r.returncode,
                             'stdout': r.stdout.decode(), 'stderr': r.stderr.decode()})
        if r.returncode:
            raise RuntimeError(r.stderr.decode() or r.stdout.decode())
        return r.stdout

    head = git('rev-parse', 'HEAD').decode().strip()
    real_index = Path(git('rev-parse', '--git-path', 'index').decode().strip())
    if not real_index.is_absolute():
        real_index = args.repo / real_index
    index_sha_before = sha(real_index.read_bytes())
    current_main = git('rev-parse', args.main_ref).decode().strip()
    registry = json.loads(git('show', f'{delivery}:{args.registry}'))
    modules = registry['projects'][args.project]['modules']
    checks = []
    for label, ref in [('original_baseline', baseline), ('fetched_main', current_main)]:
        with tempfile.TemporaryDirectory(prefix='agent10-patch-index-',
                                         dir=args.output.parent) as tmp:
            env = os.environ.copy()
            env['GIT_INDEX_FILE'] = str(Path(tmp) / 'isolated.index')
            git('read-tree', ref, env=env, log=True)
            git('apply', '--cached', '--check', str(args.patch), env=env, log=True)
            git('apply', '--cached', str(args.patch), env=env, log=True)
            tree = git('write-tree', env=env, log=True).decode().strip()
            changes = git('diff-tree', '--no-commit-id', '--name-status', '-r',
                          ref, tree).decode().splitlines()
            assert changes and all(s.startswith('A\t') for s in changes), changes
            assert sorted(s.split('\t', 1)[1] for s in changes) == sorted(record['added_paths'])
            added = []
            for path in record['added_paths']:
                actual = git('show', f'{tree}:{path}')
                expected = git('show', f'{delivery}:{path}')
                assert actual == expected, path
                added.append({'path': path, 'sha256': sha(actual), 'bytes': len(actual)})
            source_checks = []
            for name, module in modules.items():
                data = git('show', f"{tree}:{module['path']}")
                blob = git('rev-parse', f"{tree}:{module['path']}").decode().strip()
                assert sha(data) == module['sha256'], name
                assert blob == module['git_blob'], name
                source_checks.append({'module': name, 'path': module['path'],
                                      'sha256': sha(data), 'git_blob': blob})
            preserved = []
            for path in ['AGENTS.md', 'proofs/verify_project__214bf7673efe116b.py']:
                original = git('show', f'{baseline}:{path}')
                actual = git('show', f'{tree}:{path}')
                assert actual == original, path
                preserved.append({'path': path, 'sha256': sha(actual),
                                  'identical_to_original_baseline': True})
            checks.append({'target': label, 'commit': ref, 'patched_tree': tree,
                           'status': 'PASS', 'all_changes_additive': True,
                           'added_files': added, 'verified_module_pins': source_checks,
                           'preserved_files': preserved})
    assert git('rev-parse', 'HEAD').decode().strip() == head
    index_sha_after = sha(real_index.read_bytes())
    assert index_sha_before == index_sha_after
    result = {'status': 'PASS', 'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'method': 'Fresh isolated Git index per target; apply --cached --check, apply --cached, write-tree; exact blob-byte verification.',
              'patch_sha256': sha(patch_data), 'source_baseline': baseline,
              'local_delivery_commit': delivery, 'tested_proof_commit': record['tested_proof_commit'],
              'checks': checks, 'commands': commands, 'worktree_checkout_used': False,
              'original_head_unchanged': head, 'original_index_sha256_before': index_sha_before,
              'original_index_sha256_after': index_sha_after,
              'main_ref_updated_by_this_check': False, 'lean_rerun_by_this_check': False,
              'scope': 'Patch application and byte compatibility with the already verified source closure; this is not a new kernel build.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'output': str(args.output),
                      'receipt_sha256': sha(args.output.read_bytes()),
                      'targets': [{k: c[k] for k in ['target', 'commit', 'patched_tree', 'status']} for c in checks],
                      'added_files_per_target': len(record['added_paths']),
                      'verified_modules_per_target': len(modules)}))


if __name__ == '__main__':
    main()
