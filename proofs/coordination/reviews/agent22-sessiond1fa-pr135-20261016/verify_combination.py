#!/usr/bin/env python3
"""Bind PR135's reviewed source and complete additive tree to an actual merge tree.

This performs Git/source identity checks only. It does not execute Lean, mutate
remote refs, or replace independent semantic and execution-evidence review.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

P = 'proofs/contributions/agent-104/prefix620-kernel-20261016/'
ORIGINAL = '786ea690d8221503ae93dc3f981b1b56749ff40f'
FREEZE = 'dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4'
GENERIC = 'ae8bbdfd2a18e8910eebc25fd2a81661c01abc16'

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--base', required=True)
ap.add_argument('--head', required=True)
ap.add_argument('--output', required=True)
a = ap.parse_args()
out = Path(a.output)
out.mkdir(parents=True, exist_ok=False)
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1')
commands = []
report = {'agent': 'Agent #22', 'session': 'd1fa86c3a213', 'pr': 135,
          'scope': 'Complete additive merge-tree preservation and exact 523-source binding',
          'fresh_lean_execution': 'NOT_RUN', 'status': 'RUNNING',
          'environment_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}

def git(*args, data=None, check=True):
    cmd = ['git', '-C', a.repo, '-c', 'remote.origin.promisor=false', *args]
    cp = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        env=env, timeout=180)
    commands.append({'argv': cmd, 'exit_code': cp.returncode,
                     'stderr': cp.stderr.decode('utf-8', errors='replace')})
    if check and cp.returncode:
        raise RuntimeError(f'Git failed: {args}: {cp.stderr.decode(errors="replace")}')
    return cp

def raw(*args):
    return git(*args).stdout

def resolve(ref):
    s = raw('rev-parse', '--verify', ref + '^{commit}').decode().strip()
    if not re.fullmatch('[0-9a-f]{40}', s):
        raise ValueError('Invalid resolved commit')
    return s

def tree(ref):
    result = {}
    for row in raw('ls-tree', '-r', '-z', '--full-tree', ref).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            result[path.decode()] = (mode, kind, sha)
    return result

def manifest_digest(t):
    return hashlib.sha256(''.join(f'{p}\t{m}\t{k}\t{s}\n'
                                  for p, (m,k,s) in sorted(t.items())).encode()).hexdigest()

def blob(sha):
    return raw('cat-file', 'blob', sha)

def check_pin(label, data, pin):
    actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
              'git_blob': hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
    for key in ('bytes', 'sha256', 'git_blob'):
        if key in pin and actual[key] != pin[key]:
            raise ValueError(f'{label}: {key} mismatch')
    return actual

try:
    b, h = resolve(a.base), resolve(a.head)
    mb = raw('merge-base', b, h).decode().strip()
    report.update(base=b, source_head=h, merge_base=mb,
                  mathematical_freeze=FREEZE, generic_source=GENERIC)
    tb, th, tf = tree(b), tree(h), tree(FREEZE)
    changes = []
    for line in raw('diff', '--name-status', '--no-renames', mb, h).decode().splitlines():
        status, path = line.split('\t', 1)
        if status != 'A':
            raise ValueError(f'Incoming non-additive change requires separate review: {status} {path}')
        if not (re.fullmatch(r'proofs/Agent104Prefix620\w*\.lean', path) or path.startswith(P)):
            raise ValueError(f'Unexpected incoming path: {path}')
        if th[path][0:2] != ('100644', 'blob'):
            raise ValueError(f'Unexpected mode/type: {path}')
        changes.append(path)
    expected = dict(tb)
    duplicate = []
    for path in changes:
        if path in tb:
            if tb[path] != th[path]:
                raise ValueError(f'Conflicting existing base content: {path}')
            duplicate.append(path)
        expected[path] = th[path]
    merged = git('merge-tree', '--write-tree', '--messages', b, h, check=False)
    (out/'merge-tree.stdout').write_bytes(merged.stdout)
    (out/'merge-tree.stderr').write_bytes(merged.stderr)
    if merged.returncode != 0:
        raise ValueError(f'Merge-tree conflict or execution failure: exit {merged.returncode}')
    mt = merged.stdout.decode().splitlines()[0]
    if not re.fullmatch('[0-9a-f]{40}', mt):
        raise ValueError('Merge tree identifier missing')
    tc = tree(mt)
    if tc != expected:
        wrong = sorted(set(tc)^set(expected) | {p for p in tc.keys()&expected.keys() if tc[p]!=expected[p]})
        raise ValueError(f'Combined tree differs from complete expected preservation map: {wrong[:20]}')
    report.update(combined_tree=mt, base_entries=len(tb), head_entries=len(th),
                  combined_entries=len(tc), incoming_paths=len(changes),
                  already_identical_in_base=duplicate,
                  new_paths=len(tc)-len(tb), preserved_base_entries=len(tb),
                  combined_tree_manifest_sha256=manifest_digest(tc))
    gen_path = P+'generator/GENERATION_MANIFEST.json'
    dep_path = P+'verification/author-base/dependency-map.json'
    gen = json.loads(blob(th[gen_path][2]))
    deps = json.loads(blob(th[dep_path][2]))
    if len(gen['sources']) != 510 or len(deps['modules']) != 13:
        raise ValueError('Unexpected module counts')
    math_paths = {'proofs/'+name+'.lean' for name in gen['sources']}
    if math_paths != {p for p in changes if p.startswith('proofs/Agent104Prefix620') and p.endswith('.lean')}:
        raise ValueError('Active module manifest does not equal incoming active source set')
    bindings = []
    for name, pin in gen['sources'].items():
        path = 'proofs/'+name+'.lean'
        if not (th[path] == tf[path] == tc[path]):
            raise ValueError(f'Mathematical source changed from reviewed freeze: {path}')
        bindings.append({'module':name,'path':path,'source_ref':FREEZE,
                         **check_pin(name, blob(th[path][2]), pin)})
    for name, pin in deps['modules'].items():
        path = pin['source_path']
        if pin['source_ref'] != GENERIC:
            raise ValueError('Unexpected generic source reference')
        if not (th[path] == tb[path] == tc[path]):
            raise ValueError(f'Generic dependency differs in current base: {name}')
        if raw('rev-parse', GENERIC+':'+path).decode().strip() != pin['git_blob']:
            raise ValueError(f'Generic historical source mismatch: {name}')
        bindings.append({'module':name,'path':path,'source_ref':GENERIC,
                         **check_pin(name, blob(th[path][2]), pin)})
    controls = [gen_path, dep_path,
                P+'verification/independent620/rebuild.py',
                P+'verification/independent620/COMPLETION.md',
                P+'generator/generate_frozen620.py']
    for path in controls:
        if th[path] != tc[path]:
            raise ValueError(f'Verification-control source changed: {path}')
    if raw('rev-parse',h+':'+P+'corrections/agent22-verification-wording/README-at-786ea690.md').decode().strip() != raw('rev-parse',ORIGINAL+':'+P+'README.md').decode().strip():
        raise ValueError('Original README preservation mismatch')
    report.update(status='PASS', bound_modules=len(bindings), concrete_modules=510,
                  generic_modules=13, reviewed_source_binding='PASS',
                  entire_base_preservation='PASS', all_incoming_content_binding='PASS',
                  independent_review='Required separately; this script does not self-certify semantic or proof evidence',
                  verification_reuse='Source closure and recorded controls unchanged; use only separately qualified retained execution evidence')
    (out/'source-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
    (out/'incoming-paths.json').write_text(json.dumps([{'path':p,'mode':th[p][0],'type':th[p][1],'git_blob':th[p][2]} for p in changes],indent=2)+'\n')
except Exception as exc:
    report.update(status='FAIL', error=str(exc))
finally:
    report['commands'] = commands
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='commands'},indent=2))
    sys.exit(0 if report['status']=='PASS' else 1)
