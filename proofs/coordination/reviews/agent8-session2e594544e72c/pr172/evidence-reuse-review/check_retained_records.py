"""Read-only checks of retained PR172 records; executes no repository program or Lean."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path('/workspace/scratch/2e594544e72c/agent8-pr172')
SOURCE = ROOT / 'source'
PACKAGE = SOURCE / 'proofs/contributions/agent-1/periodic-nine-cycle-20261017'
REVIEW = PACKAGE / 'review'
CLEAN = REVIEW / 'clean-001'
PARENT = PACKAGE / 'verification'
HEAD = 'b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80'
ORIGINAL = '24c29104b6855fe19ad593c0b78fd5ee766a7d26'
PROJECT = 'agent1-periodic-nine-cycle'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def read_json(path):
    return json.loads(path.read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def verify_manifest(base, name, expected):
    manifest = read_json(base / name)
    assert isinstance(manifest, dict) and len(manifest) == expected
    for path, entry in manifest.items():
        assert not Path(path).is_absolute() and '..' not in Path(path).parts
        data = (base / path).read_bytes()
        assert len(data) == entry['bytes'], path
        assert digest(data) == entry['sha256'], path
    return manifest

def mask_lean(text):
    # Local lexical inspection only; does not import or execute retained source.
    out = list(text)
    i, depth = 0, 0
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                out[i:i+2] = [' ', ' ']; depth += 1; i += 2
            elif text.startswith('-/', i):
                out[i:i+2] = [' ', ' ']; depth -= 1; i += 2
            else:
                if text[i] != '\n': out[i] = ' '
                i += 1
        elif text.startswith('/-', i):
            out[i:i+2] = [' ', ' ']; depth = 1; i += 2
        elif text.startswith('--', i):
            while i < len(text) and text[i] != '\n': out[i] = ' '; i += 1
        elif text[i] == '"':
            out[i] = ' '; i += 1
            while i < len(text):
                ch = text[i]
                if ch != '\n': out[i] = ' '
                i += 1
                if ch == '\\' and i < len(text):
                    if text[i] != '\n': out[i] = ' '
                    i += 1
                elif ch == '"': break
            else: raise AssertionError('Unterminated string')
        else: i += 1
    assert depth == 0
    return ''.join(out)

materialization = read_json(ROOT / 'SOURCE_MANIFEST.json')
assert materialization['source_head'] == HEAD
assert materialization['expected_files'] == materialization['verified_files'] == 288
assert not materialization['errors']
formal = next(r for r in read_json(ROOT / 'FORMAL_REVIEWS.json') if r['id'] == 5555494440)
assert formal['commit_id'] == HEAD and formal['state'] == 'COMMENTED'

review_manifest = verify_manifest(REVIEW, 'FILES.json', 120)
parent_package_manifest = verify_manifest(PARENT, 'PACKAGE-FILES.json', 81)
parent_manifest = verify_manifest(PARENT / 'parent-clean-001', 'FILES.json', 71)
assert digest((REVIEW / 'FILES.json').read_bytes()) == '1460748582eba52ec7755a93a29a24bb4f85043a12b0b621e89eb898dff47d87'
assert digest((REVIEW / 'frozen-receipt.json').read_bytes()) == 'd747c06561717cd4d10e29f6156c259a972b33c3d27381593bc02e76d597080b'
assert not any('fresh-build-' in str(p.relative_to(REVIEW)) for p in REVIEW.rglob('*'))
review_extra = {str(p.relative_to(REVIEW)) for p in REVIEW.rglob('*') if p.is_file()} - set(review_manifest)
assert review_extra == {'FILES.json', '.gitignore'}, review_extra
frozen = read_json(REVIEW / 'frozen-receipt.json')
for path, expected in frozen['review_evidence'].items():
    assert digest((REVIEW / path).read_bytes()) == expected, path

identity = read_json(REVIEW / 'final-source-identity.json')
assert identity['source_commit'] == ORIGINAL
assert (REVIEW / 'final-source-identity.json').read_bytes() == (CLEAN / 'final-source-identity.json').read_bytes()
assert (REVIEW / 'replay.py').read_bytes() == (CLEAN / 'replay.py').read_bytes()
assert read_json(CLEAN / 'sources.json') == identity['sources']
registry_bytes = (SOURCE / identity['registry_path']).read_bytes()
assert digest(registry_bytes) == identity['registry_sha256'] == 'd3fca8aa3b055bd287f347a21d132a02c41c6713cdd754fd42a90bf5afcccc80'
assert registry_bytes == (PARENT / 'registry.json').read_bytes()
registry = json.loads(registry_bytes)
registered = registry['projects'][PROJECT]['modules']
entries = {e['module']: e for e in identity['sources']}
assert len(entries) == len(registered) == identity['module_count'] == 34
assert identity['roots'] == registry['projects'][PROJECT]['roots'] == ['Agent1PeriodicNinesCycle']
actual_imports = {}
canonical_locally_present, canonical_not_in_added_payload = [], []
for name, entry in entries.items():
    data = (CLEAN / 'compiled-sources' / (name + '.lean')).read_bytes()
    assert digest(data) == entry['sha256'] == registered[name]['sha256'], name
    assert blob(data) == entry['git_blob'] == registered[name]['git_blob'], name
    assert entry['path'] == registered[name]['path'], name
    assert data == (PARENT / 'parent-clean-001' / PROJECT / 'source' / (name + '.lean')).read_bytes(), name
    code = mask_lean(data.decode())
    imports = [item for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for item in line.split()]
    assert imports == entry['imports'] == registered[name]['imports'], name
    actual_imports[name] = imports
    if (SOURCE / entry['path']).exists():
        assert data == (SOURCE / entry['path']).read_bytes(), name
        canonical_locally_present.append(entry['path'])
    else:
        canonical_not_in_added_payload.append(entry['path'])
seen, active, ordered = set(), set(), []
def visit(name):
    if name in {'Init', 'Std', 'Lean'} or name.startswith(('Init.', 'Std.', 'Lean.')): return
    assert name in entries and name not in active, name
    if name in seen: return
    active.add(name)
    for dep in actual_imports[name]: visit(dep)
    active.remove(name); seen.add(name); ordered.append(name)
visit('Agent1PeriodicNinesCycle')
assert seen == set(entries)
assert ordered == [e['module'] for e in identity['sources']]
new_exports = []
for name in identity['new_modules']:
    code = mask_lean((CLEAN / 'compiled-sources' / (name + '.lean')).read_text())
    declarations = re.findall(r'^(?:noncomputable\s+)?(theorem|def|abbrev|structure|inductive)\s+(\w+)', code, re.M)
    assert all(kind == 'theorem' for kind, _ in declarations)
    new_exports += ['Agent1.Periodic.' + n for _, n in declarations]
assert new_exports == identity['new_module_exports'] == identity['new_module_theorems']
assert len(new_exports) == 5 and not identity['new_module_definitions']
assert new_exports == [n for c in registry['claims'] if c['project'] == PROJECT for n in c['endpoints']]

commands = read_json(CLEAN / 'results.json')
compiler = read_json(CLEAN / 'compiler.json')
limits = read_json(CLEAN / 'resource-limits.json')
assert compiler['sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
assert compiler['version'] == 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
assert limits == {'address_space_mib_per_child': 8192, 'timeout_seconds_per_command': 600, 'lean_stack_kib': 'compiler default'}
assert len(commands) == 35 and [c['module'] for c in commands] == ordered + ['ReviewAudit']
for i, command in enumerate(commands):
    name = command['module']
    expected = [compiler['path'], '--trust=0', '-j1', '-DElab.async=false']
    if i < 34: expected += ['-o', name + '.olean']
    expected += [name + '.lean']
    assert command['command'] == expected, name
    assert command['exit_code'] == 0 and command['timed_out'] is False, name
    assert command['resource_limits'] == limits
    assert digest((CLEAN / (name + '.log')).read_bytes()) == command['log_sha256'], name
audit_source = (CLEAN / 'ReviewAudit.lean').read_text()
selected = json.loads(re.search(r'let selected : List String := (\[[^\n]*\])', audit_source).group(1))
assert selected == ordered
log = (CLEAN / 'ReviewAudit.log').read_text()
assert not re.search(r'CUSTOM_AXIOM|DISALLOWED_|MODULE_NOT_AUDITED|sorryAx|Lean\.ofReduceBool|error:', log)
def audit_records(label):
    matches = re.findall(r'^' + label + r' (\S+) (\S+) : \[([^\]]*)\]', log, re.M)
    result = [(m, n, set(a.strip() for a in ax.split(',') if a.strip())) for m,n,ax in matches]
    assert len(result) == len({(m,n) for m,n,_ in result})
    assert all(m in entries and ax <= ALLOWED for m,n,ax in result)
    return result
theorems = audit_records('AUDIT_THEOREM')
safe_defs = audit_records('AUDIT_SAFE_DEFINITION') + audit_records('AUDIT_SAFE_OPAQUE')
assert len(theorems) == 1547 and len(safe_defs) == 244
assert {m for m,_,_ in theorems} == set(entries)
assert set().union(*(ax for _,_,ax in theorems)) == ALLOWED
assert set().union(*(ax for _,_,ax in safe_defs)) == {'propext'}
assert re.findall(r'^FULL_MODULE_AUDIT (.+)$', log, re.M) == ['theorems=1547 union=[Classical.choice, Quot.sound, propext]']
assert re.findall(r'^FULL_DEFINITION_AUDIT (.+)$', log, re.M) == ['definitions=244 union=[propext]']
new_counts = Counter(m for m,_,_ in theorems if m in identity['new_modules'])
assert new_counts == {'Agent1PeriodicNinesPath': 16, 'Agent1PeriodicNinesCycle': 7}
assert not any(m in identity['new_modules'] for m,_,_ in safe_defs)
verification = read_json(CLEAN / 'verification.json')
assert verification['status'] == 'PASS' and verification['trust'] == 0
assert verification['compiler'] == compiler
assert verification['theorems_audited'] == len(theorems) and verification['safe_definitions_audited'] == len(safe_defs)
named = re.findall(r'^#check (\S+)$', audit_source, re.M)
assert named == verification['audited_named_exports'] and len(named) == len(set(named)) == 136
assert set(new_exports) <= set(named)
assert all(re.search(r'^' + re.escape(n) + r'(?:\s|\()', log, re.M) for n in named)
inventory = read_json(CLEAN / 'implementation-inventory.json')
nonsafe = re.findall(r'^NONSAFE_DEFINITION (\S+) (\S+)$', log, re.M)
unsafe_axioms = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', log, re.M)
unsafe_opaques = re.findall(r'^UNSAFE_OPAQUE (\S+) (\S+)$', log, re.M)
assert [list(x) for x in nonsafe] == verification['nonsafe_definitions_inventoried']
assert [list(x) for x in unsafe_axioms] == inventory['unsafe_axioms'] == verification['unsafe_implementation_axioms_inventoried']
assert not unsafe_opaques and not inventory['unsafe_opaques'] and not inventory['unclassified_nonsafe']
assert inventory['status'] == 'PASS' and len(nonsafe) == inventory['nonsafe_count'] == 978
cstage = [x for x in nonsafe if re.search(r'\._cstage[12](?:\.|$)', x[1])]
unsafe_rec = [x for x in nonsafe if x[1].endswith('._unsafe_rec')]
assert len(cstage) == inventory['cstage_helpers'] == 947
assert len(unsafe_rec) == inventory['unsafe_rec_helpers'] == 31
assert len(cstage) + len(unsafe_rec) == len(nonsafe) and len(unsafe_axioms) == 13
safe_names = {(m,n) for m,n,_ in safe_defs}
assert all((m,n[:-len('._unsafe_rec')]) in safe_names for m,n in unsafe_rec)
assert all(x['safe_base_audited'] and (x['module'],x['safe_base']) in safe_names for x in inventory['unsafe_rec_base_checks'])
assert not any(m in identity['new_modules'] for m,_ in nonsafe + unsafe_axioms + unsafe_opaques)

parent = read_json(PARENT / 'parent-clean-001/verification.json')
parent_project = parent['projects'][PROJECT]
assert parent['status'] == parent_project['status'] == 'PASS'
assert parent['source_commit'] == ORIGINAL and parent['registry_sha256'] == identity['registry_sha256']
assert parent_project['build_order'] == ordered and set(parent_project['sources']) == set(entries)
assert len(parent_project['commands']) == 35
for command in parent_project['commands']:
    assert command['exit_code'] == 0 and not any(a.startswith('--trust') for a in command['argv'])
    assert '-j1' in command['argv'] and '-DElab.async=false' in command['argv']
    assert digest((PARENT / 'parent-clean-001' / command['log']).read_bytes()) == command['log_sha256']
parent_log = (PARENT / 'parent-clean-001' / PROJECT / 'logs/ProjectAudit.log').read_text()
assert len(re.findall(r'^AUDIT_THEOREM ', parent_log, re.M)) == parent_project['theorem_count'] == 1547
addendum = read_json(PARENT / 'parent-result-addendum.json')
assert addendum['explicit_trust_zero'] is False and addendum['safe_definition_audit_claimed_here'] is False
assert digest((PARENT / 'parent-clean-001/FILES.json').read_bytes()) == addendum['original_manifest_sha256']
assert digest((PARENT / 'parent-clean-001/verification.json').read_bytes()) == addendum['original_report_sha256']
assert digest((PARENT / 'parent-console.log').read_bytes()) == addendum['original_console_sha256']
assert digest((PARENT / 'package.py').read_bytes()) == addendum['packaging_driver_sha256']
assert digest((PARENT / 'canonical-verifier.py').read_bytes()) == read_json(PARENT / 'publication-source-receipt.json')['checker_sha256']
console = (PARENT / 'parent-console.log').read_text().splitlines()
assert len(console) == 35 and all(line.endswith(' exit=0') for line in console)
failure = (PACKAGE / 'path-author/attempt-001/compile.log').read_text()
assert 'omega could not prove the goal' in failure and 'sorryAx' in failure
assert (PACKAGE / 'path-author/attempt-002/Agent1PeriodicNinesPath.lean').read_bytes() == (SOURCE / 'proofs/Agent1PeriodicNinesPath.lean').read_bytes()
assert (PACKAGE / 'numeric-author/attempt-003/Agent1PeriodicNinesCycle.lean').read_bytes() == (SOURCE / 'proofs/Agent1PeriodicNinesCycle.lean').read_bytes()

print(json.dumps({
    'status': 'PASS_LOCAL_RETAINED_RECORDS_CHECK',
    'head': HEAD, 'original_reviewed_source': ORIGINAL,
    'formal_review_id': formal['id'], 'formal_review_state': formal['state'],
    'verified_manifest_entries': {'independent_review': len(review_manifest), 'parent_package': len(parent_package_manifest), 'original_parent': len(parent_manifest)},
    'review_manifest_additional_files': sorted(review_extra),
    'source_closure_snapshots_checked': len(entries), 'literal_import_closure_exact': True,
    'canonical_source_paths_present_in_added_payload': canonical_locally_present,
    'canonical_source_paths_requiring_parent_final_head_binding': canonical_not_in_added_payload,
    'registry_sha256': digest(registry_bytes),
    'independent_recorded_commands': len(commands), 'independent_all_exact_argv_and_log_hashes_checked': True,
    'recorded_compiler': compiler, 'recorded_limits': limits,
    'raw_theorem_constants': len(theorems), 'raw_safe_definitions': len(safe_defs),
    'theorem_axiom_union': sorted(ALLOWED), 'safe_definition_axiom_union': ['propext'],
    'new_module_theorem_counts': dict(new_counts), 'public_agent1_types_printed': len(named),
    'new_public_endpoints': new_exports,
    'runtime_inventory': {'nonsafe': len(nonsafe), 'cstage': len(cstage), 'unsafe_rec': len(unsafe_rec), 'unsafe_axioms': len(unsafe_axioms), 'unsafe_opaques': len(unsafe_opaques), 'unclassified': 0},
    'parent_commands': len(parent_project['commands']), 'parent_explicit_trust_zero': False,
    'failed_author_elaboration_preserved': True,
    'accepted_new_sources_equal_final_author_snapshots': True,
    'fresh_lean_execution': False, 'retained_driver_execution': False,
    'remote_verification_performed_by_this_script': False
}, indent=2))
