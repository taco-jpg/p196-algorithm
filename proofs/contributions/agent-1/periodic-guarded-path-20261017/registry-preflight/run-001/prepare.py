#!/usr/bin/env python3
"""Exact source registry preflight. This script never executes Lean."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import time

ROOT = Path('/workspace/p196-agent1-guarded-path-20261017')
PROOFS = ROOT / 'proofs'
HERE = PROOFS / 'contributions/agent-1/periodic-guarded-path-20261017/registry-preflight'
MODULE = 'Agent1PeriodicGuardedPath'
REGISTRY = PROOFS / (MODULE + '.registry.json')
PROJECT = 'agent1-periodic-guarded-path'
BASELINE = '946c69edf3d2e6a87f5516db1fd0091eae29e663'
CLAIM = '9d6dc9caa3e77b9036b348ac6d77c3f49553ba30'
PRIORS = ['Agent1PeriodicReturnCore.registry.json', 'Agent1PeriodicZeroCycle.registry.json']
TOKENS = ['sorry', 'admit', 'sorryAx', 'native_decide', 'axiom',
          'implemented_by', 'extern', 'unsafe', 'ofReduceBool', 'trustCompiler']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def code_only(source):
    """Mask nested Lean comments and strings, preserving newlines/offsets."""
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


assert len(sys.argv) in (2, 3), 'Usage: prepare.py NEW_RUN [--author-checked]'
author_checked = len(sys.argv) == 3
if author_checked: assert sys.argv[2] == '--author-checked'
run = HERE / sys.argv[1]
assert run.parent == HERE, 'Run must be a direct child of the evidence directory'
assert (PROOFS / (MODULE + '.lean')).is_file(), 'Await actual author source'
run.mkdir(exist_ok=False)
shutil.copy2(Path(__file__), run / 'prepare.py')
started = time.time()
prior_sources = {}
origins = []
duplicates = []
for filename in PRIORS:
    raw = (PROOFS / filename).read_bytes()
    origins.append({'path': 'proofs/' + filename, 'sha256': sha(raw)})
    for project in json.loads(raw)['projects'].values():
        for name, entry in project['modules'].items():
            pin = {k: entry[k] for k in ('path', 'sha256', 'git_blob', 'imports')}
            if name in prior_sources:
                assert prior_sources[name] == pin, ('Conflicting inherited pins', name)
                duplicates.append({'module': name, 'registry': 'proofs/' + filename, 'identical': True})
            else:
                prior_sources[name] = pin

claimraw = (HERE / 'claim.json').read_bytes()
claim = json.loads(claimraw)
for path in ('proofs/' + MODULE + '.lean', 'proofs/' + MODULE + '.registry.json'):
    assert path in claim['intended_source_files'], ('Outside accepted claim', path)
modules = {}
captures = {}
visiting = set()
order = []
hits = []


def visit(name):
    if name in ('Std', 'Init', 'Lean') or name in modules: return
    assert name not in visiting, ('Import cycle', name)
    visiting.add(name)
    path = 'proofs/' + name + '.lean' if name == MODULE else prior_sources[name]['path']
    raw = (ROOT / path).read_bytes()
    code = code_only(raw.decode())
    captures[path] = raw
    imports = []
    for match in re.finditer(r'^\s*import\s+([^\n]+)', code, re.M):
        imports.extend(match[1].split())
    entry = {'path': path, 'sha256': sha(raw), 'git_blob': blob(raw), 'imports': imports}
    if name != MODULE:
        assert entry == prior_sources[name], ('Current source differs from inherited pin', name, entry)
    for token in TOKENS:
        for match in re.finditer(r'\b' + re.escape(token) + r'\b', code):
            hits.append({'module': name, 'token': token, 'line': code[:match.start()].count('\n') + 1})
    for dependency in imports: visit(dependency)
    visiting.remove(name)
    modules[name] = entry
    order.append(name)


visit(MODULE)
assert not hits, ('Prohibited executable source tokens', hits)
raw = captures[modules[MODULE]['path']]
code = code_only(raw.decode())
assert re.findall(r'^namespace\s+([^\n]+)', code, re.M) == ['Agent1.Periodic']
endpoints = ['Agent1.Periodic.' + name for name in re.findall(r'^theorem\s+(\w+)', code, re.M)]
assert endpoints, 'No actual public theorem declarations found'
declarations = [{'kind': kind, 'name': 'Agent1.Periodic.' + name}
                for kind, name in re.findall(r'^(theorem|def|abbrev|structure)\s+(\w+)', code, re.M)]
(run / (MODULE + '.lean')).write_bytes(raw)
scope = ('A supplied exact finite period-four quotient path with a natural copy schedule, literal exponent recurrence, and source guards k_i>=3 lifts an initial Canonical/full-column realization to the same ordinary seed through every endpoint. '
         'For any supplied initially original-valid finite path of length N, the literal recursive schedule starting at 2*N+3 supplies the guards and one positive canonical seed realizes all N steps. '
         'This formalizes the existing METHOD section4 finite-copy guard principle and reuses the original generic numeric representation theorem. '
         'The seed can depend on the path and N; no uniform infinite seed, safety, return existence, arbitrary abstract graph realization, affirmative interface search, or 196 conclusion.')
registry = {
    'schema_version': 1, 'catalogue_complete': False,
    'catalogue_blockers': [
        f'Scoped {len(modules)}-module contribution registry; not a repository-wide accepted catalogue.',
        'PROVISIONAL source metadata: author freeze, author audit, and complete fresh verification remain pending.'],
    'toolchain': {'version': '4.19.0', 'commit': '6caaee842e94',
                  'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound']},
    'projects': {PROJECT: {'scope': scope, 'roots': [MODULE], 'modules': modules}},
    'claims': [{'id': 'A1-PERIODIC-GUARDED-PATH', 'project': PROJECT, 'endpoints': endpoints}],
    'source_baseline': BASELINE, 'source_pin_origins': origins,
    'accepted_global_registry_modified': False,
    'verification_status': 'PROVISIONAL_SOURCE_PREFLIGHT_ONLY',
    'metadata_validation': {
        'exact_actual_import_dfs': True, 'module_count': len(modules), 'new_module_count': 1,
        'new_public_theorem_count': len(endpoints), 'matching_duplicate_prior_pins': len(duplicates),
        'source_tokens_checked': TOKENS, 'source_token_hits': hits,
        'lean_execution_performed_by_this_preflight': False,
        'claim_commit': CLAIM, 'claim_git_blob': blob(claimraw), 'claim_sha256': sha(claimraw)}}
if author_checked:
    frozenraw = (HERE / 'author-confirmation.json').read_bytes()
    frozen = json.loads(frozenraw)
    assert frozen['author_confirmation_received'] is True
    assert frozen['source_sha256'] == modules[MODULE]['sha256']
    assert frozen['compile_status'] == frozen['new_module_audit_status'] == 'PASS'
    for receipt in frozen['author_receipts']:
        assert sha((ROOT / receipt['path']).read_bytes()) == receipt['sha256']
    registry['catalogue_blockers'][1] = (
        'The new module has completed strict author compilation and a full new-module audit; '
        'parent and independent fresh combined verification remain pending.')
    registry['verification_status'] = 'FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING'
    registry['author_verification'] = {
        'new_module_compile': 'PASS', 'new_module_origin_audit': 'PASS',
        'fresh_combined_verification': 'PENDING',
        'evidence_path': str((HERE / 'author-confirmation.json').relative_to(ROOT)),
        'evidence_sha256': sha(frozenraw),
        'qualification': 'Actual author confirmation and receipts checked; this preflight executes no Lean.'}
    (run / 'author-confirmation.json').write_bytes(frozenraw)
assert all((ROOT / path).read_bytes() == value for path, value in captures.items()), 'Source changed during snapshot'
save(run / 'registry.json', registry)
shutil.copy2(run / 'registry.json', REGISTRY)
report = {
    'status': 'SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN' if author_checked else 'SOURCE_PREFLIGHT_PASS_PROVISIONAL',
    'started_at_epoch': started, 'finished_at_epoch': time.time(),
    'command': ['python3', str(Path(__file__))] + sys.argv[1:], 'cwd': str(Path.cwd()),
    'script_sha256': sha(Path(__file__).read_bytes()), 'registry_sha256': sha(REGISTRY.read_bytes()),
    'module_count': len(modules), 'exact_dfs_order': order,
    'new_public_theorems': endpoints, 'new_public_declarations': declarations,
    'duplicate_prior_pin_matches': duplicates, 'source_scan_hits': hits,
    'source_snapshots_stable_during_run': True,
    'qualification': 'Source metadata and optionally existing author receipts only; no Lean execution, Git mutation, publication, or accepted global registry change.'}
save(run / 'report.json', report)
print(json.dumps({key: report[key] for key in ('status', 'registry_sha256', 'module_count', 'new_public_theorems', 'source_scan_hits')}, indent=2))
