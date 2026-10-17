#!/usr/bin/env python3
"""Immutable source-only registry preflights; this script never executes Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PROOFS = ROOT / 'proofs'
PROJECT = 'agent1-periodic-cycle-adapter'
ROOT_MODULE = 'Agent1PeriodicCycleNumeric'
NEW = ['Agent1PeriodicCyclePath', 'Agent1PeriodicCycleGuard', ROOT_MODULE]
REGISTRY = PROOFS / (ROOT_MODULE + '.registry.json')
BASELINE = '3b018f7032b537cd7f6218fb9ad979842bb286d0'
CLAIM = 'b4dc82e6d8d521b4295236f171b8d9e1a1d690cd'
PRIORS = ['Agent1PeriodicGuardedPath.registry.json',
          'Agent1PeriodicReturnClock.registry.json',
          'Agent1PeriodicSafety.registry.json']
OLD_ROOTS = ['Agent1PeriodicGuardedPath', 'Agent1PeriodicReturnClock',
             'Agent1PeriodicSafetyNumeric']
TOKENS = ['sorry', 'admit', 'sorryAx', 'native_decide', 'axiom',
          'implemented_by', 'extern', 'unsafe', 'ofReduceBool', 'trustCompiler']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def code_only(source):
    """Mask nested Lean comments and strings while retaining line positions."""
    out = list(source)
    i = depth = 0
    string = False
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                out[i:i+2] = '  '; depth += 1; i += 2
            elif source.startswith('-/', i):
                out[i:i+2] = '  '; depth -= 1; i += 2
            else:
                if source[i] != '\n': out[i] = ' '
                i += 1
        elif string:
            if source[i] == '\\':
                out[i] = ' '; i += 1
                if i < len(source): out[i] = ' '; i += 1
            else:
                if source[i] == '"': string = False
                if source[i] != '\n': out[i] = ' '
                i += 1
        elif source.startswith('/-', i):
            out[i:i+2] = '  '; depth = 1; i += 2
        elif source.startswith('--', i):
            while i < len(source) and source[i] != '\n':
                out[i] = ' '; i += 1
        elif source[i] == '"':
            out[i] = ' '; string = True; i += 1
        else:
            i += 1
    assert not depth and not string, 'Unterminated comment/string'
    return ''.join(out)


def imports_of(code):
    return [n for m in re.finditer(r'^\s*import\s+([^\n]+)', code, re.M)
            for n in m[1].split()]


def git_bytes(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)


parser = argparse.ArgumentParser()
parser.add_argument('run')
parser.add_argument('--inherited-only', action='store_true')
parser.add_argument('--author-checked', action='store_true')
args = parser.parse_args()
assert not (args.inherited_only and args.author_checked)
run = HERE / args.run
assert run.parent == HERE and run.name.startswith('run-')
run.mkdir(exist_ok=False)
shutil.copy2(__file__, run / 'prepare.py')
started = time.time()

# Prior registries, aliases and source bytes must all match the actual baseline.
prior = {}
origins = []
duplicates = []
for filename in PRIORS:
    path = 'proofs/' + filename
    raw = (ROOT / path).read_bytes()
    assert raw == git_bytes(path), ('Prior registry changed from baseline', path)
    origin = {'path': path, 'sha256': sha(raw), 'git_blob': blob(raw),
              'baseline_commit': BASELINE}
    origins.append(origin)
    for project in json.loads(raw)['projects'].values():
        for name, entry in project['modules'].items():
            pin = {k: entry[k] for k in ('path', 'sha256', 'git_blob', 'imports')}
            if name in prior:
                assert prior[name] == pin, ('Conflicting prior alias/source pin', name)
                duplicates.append({'module': name, 'registry': path, 'identical': True})
            else:
                prior[name] = pin

claimraw = (HERE / 'claim.json').read_bytes()
claim = json.loads(claimraw)
claimed = claim['intended_source_files']
for name in NEW:
    assert 'proofs/' + name + '.lean' in claimed, ('Outside accepted claim', name)
assert str(REGISTRY.relative_to(ROOT)) in claimed

modules = {}
captures = {}
visiting = set()
order = []
hits = []
baseline_matches = []


def visit(name):
    if name in ('Std', 'Init', 'Lean') or name in modules:
        return
    assert name not in visiting, ('Import cycle', name)
    visiting.add(name)
    path = 'proofs/' + name + '.lean' if name in NEW else prior[name]['path']
    raw = (ROOT / path).read_bytes()
    code = code_only(raw.decode())
    captures[path] = raw
    entry = {'path': path, 'sha256': sha(raw), 'git_blob': blob(raw),
             'imports': imports_of(code)}
    if name not in NEW:
        assert entry == prior[name], ('Source differs from prior pin', name)
        assert raw == git_bytes(path), ('Source differs from baseline', name)
        baseline_matches.append(name)
    for token in TOKENS:
        for match in re.finditer(r'\b' + re.escape(token) + r'\b', code):
            hits.append({'module': name, 'token': token,
                         'line': code[:match.start()].count('\n') + 1})
    for dependency in entry['imports']:
        visit(dependency)
    visiting.remove(name)
    modules[name] = entry
    order.append(name)


for name in (OLD_ROOTS if args.inherited_only else [ROOT_MODULE]):
    visit(name)
assert not hits, ('Prohibited executable source tokens', hits)
if args.inherited_only:
    assert len(modules) == 27, ('Unexpected inherited closure size', len(modules))
else:
    assert set(NEW).issubset(modules), ('Expected actual new module missing', NEW)

declarations = []
for name in NEW:
    if name not in modules:
        continue
    raw = captures[modules[name]['path']]
    code = code_only(raw.decode())
    assert re.findall(r'^namespace\s+([^\n]+)', code, re.M) == ['Agent1.Periodic']
    public = re.findall(r'^\s*(?:@\[[^\]]*\]\s*)*(theorem|def|abbrev|structure)\s+(\w+)',
                        code, re.M)
    assert public, ('No actual public declarations', name)
    declarations.extend({'module': name, 'kind': kind,
                         'name': 'Agent1.Periodic.' + identifier}
                        for kind, identifier in public)
    (run / (name + '.lean')).write_bytes(raw)

metadata = {
    'status': 'INHERITED_SOURCE_PREFLIGHT_PASS' if args.inherited_only else
              'SOURCE_PREFLIGHT_PASS_PROVISIONAL',
    'started_at_epoch': started, 'finished_at_epoch': time.time(),
    'command': ['python3', str(Path(__file__).resolve())] +
               ([args.run, '--inherited-only'] if args.inherited_only else
                [args.run] + (['--author-checked'] if args.author_checked else [])),
    'cwd': str(Path.cwd()), 'script_sha256': sha(Path(__file__).read_bytes()),
    'baseline_commit': BASELINE, 'claim_commit': CLAIM,
    'claim_git_blob': blob(claimraw), 'claim_sha256': sha(claimraw),
    'prior_registry_origins': origins,
    'module_count': len(modules), 'exact_dfs_order': order,
    'new_public_declarations': declarations,
    'new_public_theorems': [d['name'] for d in declarations if d['kind'] == 'theorem'],
    'duplicate_prior_pin_matches': duplicates,
    'source_scan_tokens': TOKENS, 'source_scan_hits': hits,
    'baseline_source_byte_matches': sorted(baseline_matches),
    'lean_execution_performed': False,
    'qualification': 'Source metadata and optionally existing author receipts only; '
                     'no Lean execution, Git mutation, publication, or global accepted-registry change.'}
save(run / 'modules.json', modules)
if not args.inherited_only:
    scope = (
        'Conditional realization of repeated copies of one supplied positive-length exact '
        'period-four full quotient cycle from original-valid initial data. Literal natural '
        'copy guards retain a fixed initial exponent and one ordinary seed for all times. '
        'Explicit safePeriodic=true at every finite cycle state supplies all-time '
        'nonpalindromicity of the successor seed through existing numeric safety. '
        'This formalizes the original METHOD section4 positive-cycle criterion. '
        'No qualifying cycle is constructed; no unconditional decimal existence, 196 result, '
        'arbitrary graph-cycle realization, safety-preservation theorem, or finite-witness '
        'quantifier swap is asserted.')
    registry = {
        'schema_version': 1, 'catalogue_complete': False,
        'catalogue_blockers': [
            f'Scoped {len(modules)}-module contribution registry; not a repository-wide catalogue.',
            'PROVISIONAL source metadata: author freeze/audits and fresh combined verification pending.'],
        'toolchain': {'version': '4.19.0', 'commit': '6caaee842e94',
                      'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound']},
        'projects': {PROJECT: {'scope': scope, 'roots': [ROOT_MODULE], 'modules': modules}},
        'claims': [{'id': 'A1-PERIODIC-CYCLE-ADAPTER', 'project': PROJECT,
                    'endpoints': [d['name'] for d in declarations]}],
        'source_baseline': BASELINE, 'source_pin_origins': origins,
        'accepted_global_registry_modified': False,
        'verification_status': 'PROVISIONAL_SOURCE_PREFLIGHT_ONLY',
        'metadata_validation': {
            'exact_actual_import_dfs': True, 'module_count': len(modules),
            'new_module_count': len(NEW), 'new_public_declaration_count': len(declarations),
            'new_public_theorem_count': len(metadata['new_public_theorems']),
            'matching_duplicate_prior_pins': len(duplicates),
            'source_tokens_checked': TOKENS, 'source_token_hits': hits,
            'lean_execution_performed_by_this_preflight': False,
            'claim_commit': CLAIM, 'claim_git_blob': blob(claimraw), 'claim_sha256': sha(claimraw)}}
    if args.author_checked:
        raw = (HERE / 'author-confirmation.json').read_bytes()
        confirmation = json.loads(raw)
        assert confirmation['author_confirmation_received'] is True
        assert set(confirmation['modules']) == set(NEW)
        for name, info in confirmation['modules'].items():
            assert info['source_sha256'] == modules[name]['sha256']
            assert info['compile_status'] == info['new_module_audit_status'] == 'PASS'
            for receipt in info['receipts']:
                assert sha((ROOT / receipt['path']).read_bytes()) == receipt['sha256']
        registry['catalogue_blockers'][1] = (
            'All three new modules completed strict author compilation and full new-module '
            'audits; parent and independent fresh combined verification remain pending.')
        registry['verification_status'] = 'FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING'
        registry['author_verification'] = {
            'new_modules_compile': 'PASS', 'new_module_origin_audits': 'PASS',
            'fresh_combined_verification': 'PENDING',
            'evidence_path': str((HERE / 'author-confirmation.json').relative_to(ROOT)),
            'evidence_sha256': sha(raw),
            'qualification': 'Actual author confirmations and receipts checked; no Lean run by this preflight.'}
        metadata['status'] = 'SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN'
        (run / 'author-confirmation.json').write_bytes(raw)
    save(run / 'registry.json', registry)
    shutil.copy2(run / 'registry.json', REGISTRY)
    metadata['registry_sha256'] = sha(REGISTRY.read_bytes())
assert all((ROOT / path).read_bytes() == raw for path, raw in captures.items()), 'Source changed during preflight'
metadata['source_snapshots_stable_during_run'] = True
save(run / 'report.json', metadata)
print(json.dumps({key: metadata[key] for key in (
    'status', 'module_count', 'new_public_theorems', 'source_scan_hits')}, indent=2))
