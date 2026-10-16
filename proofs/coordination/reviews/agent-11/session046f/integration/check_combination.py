#!/usr/bin/env python3
"""Check a conflict-free integration tree preserves both contribution and base."""
import argparse
import hashlib
import json
import pathlib
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--base', required=True)
p.add_argument('--head', required=True)
p.add_argument('--tree', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()

def git(*args):
    return subprocess.check_output(['git', '-C', a.repo, *args])

def entries(ref):
    result = {}
    for raw in git('ls-tree', '-rz', '--full-tree', ref).split(b'\0'):
        if not raw:
            continue
        metadata, path = raw.split(b'\t', 1)
        mode, kind, oid = metadata.decode().split()
        result[path.decode()] = {'mode': mode, 'kind': kind, 'oid': oid}
    return result

ancestor = git('merge-base', a.base, a.head).decode().strip()
old, base, head, combined = map(entries, [ancestor, a.base, a.head, a.tree])
changed = sorted(x for x in set(old) | set(head) if old.get(x) != head.get(x))
errors = []
for path in changed:
    if combined.get(path) != head.get(path):
        errors.append({'path': path, 'reason': 'Contribution result differs from exact head'})
for path in (set(base) | set(combined)) - set(changed):
    if combined.get(path) != base.get(path):
        errors.append({'path': path, 'reason': 'Unrelated current-base content changed'})
delta = sorted(x for x in set(base) | set(combined) if base.get(x) != combined.get(x))
report = {
    'status': 'PASS' if not errors else 'FAIL',
    'scope': 'Exact Git tree preservation only; not a Lean execution or mathematical review.',
    'base': a.base, 'head': a.head, 'merge_base': ancestor, 'combined_tree': a.tree,
    'changed_contribution_paths': len(changed), 'current_base_paths': len(base),
    'combined_paths': len(combined), 'integration_delta_paths': len(delta),
    'contribution_inventory': {x: {'before': old.get(x), 'after': head.get(x)} for x in changed},
    'integration_delta': {x: {'before': base.get(x), 'after': combined.get(x)} for x in delta},
    'errors': errors,
}
out = pathlib.Path(a.output)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['status', 'base', 'head', 'combined_tree', 'changed_contribution_paths', 'integration_delta_paths']}))
print('receipt_sha256=' + hashlib.sha256(out.read_bytes()).hexdigest())
raise SystemExit(bool(errors))
