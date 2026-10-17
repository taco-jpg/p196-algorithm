#!/usr/bin/env python3
"""Review retained successful Lean audit and exact inherited runtime inventory; no Lean execution."""
from pathlib import Path
import ast, hashlib, json, re, subprocess
review = Path(__file__).resolve().parent
root = review.parents[4]
evidence = review / 'baseline-001'
out = review / 'baseline-inventory-review-001'
out.mkdir(exist_ok=False)
(out / 'review_inventory.py').write_bytes(Path(__file__).read_bytes())
build = Path('/workspace/p196-agent1-session-20261016/reduced-core-review-build-001')
identity = json.loads((evidence / 'baseline-source-identity.json').read_text())
manifest = identity['sources']
compiler = json.loads((evidence / 'compiler.json').read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
commands = json.loads((evidence / 'results.json').read_text())
assert len(commands) == 47 and all(c['exit_code'] == 0 for c in commands)
assert all('--trust=0' in c['command'] for c in commands)
priorpath = 'proofs/contributions/agent-1/periodic-return-core-20261016/review/clean-001/implementation-inventory.json'
priorraw = (root / priorpath).read_bytes()
assert priorraw == subprocess.check_output(['git','show',identity['source_commit']+':'+priorpath],cwd=root)
prior = json.loads(priorraw)
assert prior['status'] == 'PASS'
prior_unsafe = set(map(tuple, prior['unsafe_axioms']))
assert len(prior_unsafe) == 32
pr = json.loads((root/'proofs/Agent1PeriodicReturnCore.registry.json').read_text())['projects']['agent1-periodic-return-core']['modules']
entries = {e['module']:e for e in manifest}
for name, pin in pr.items():
    assert all(entries[name][k] == pin[k] for k in ['path','sha256','git_blob','imports'])
failed = json.loads((evidence/'implementation-inventory.json').read_text())
assert failed['status'] == 'REVIEW_REQUIRED'
assert set(map(tuple,failed['unsafe_axioms'])) == prior_unsafe
control = {'status':'EXACT_INHERITED_RUNTIME_INVENTORY_MATCH','source_commit':identity['source_commit'],'prior_path':priorpath,'prior_sha256':sha(priorraw),'entries':sorted(map(list,prior_unsafe)),'source_pin_match_for_all_prior_modules':True,'reason':'These exact32 compiler implementation axioms were already inventoried in the published38-module review; none occurs in any checked theorem or safe-definition axiom set. They are not mathematical source axioms or accepted proof-chain foundations.','failed_driver_snapshot':str(evidence/'replay.py'),'failed_driver_sha256':sha((evidence/'replay.py').read_bytes()),'failed_postcheck_inventory_sha256':sha((evidence/'implementation-inventory.json').read_bytes()),'original_tool_session':98345,'original_tool_exit':1,'all47_actual_lean_commands_exit':0,'lean_execution_performed':False}
(review/'inherited-implementation-axioms.json').write_text(json.dumps(control,indent=2)+'\n')
(out/'classification.json').write_text(json.dumps(control,indent=2)+'\n')
tree=ast.parse((evidence/'replay.py').read_text())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='lean_code_tokens')
ns={};exec(compile(ast.Module(body=[node],type_ignores=[]),'scanner','exec'),ns)
lean_code_tokens=ns['lean_code_tokens']
root_public_definitions=[]
exports = []
for entry in manifest:
    if not entry['module'].startswith('Agent1'):
        continue
    source = (build / (entry['module'] + '.lean')).read_text()
    forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b|Lean\.ofReduceBool', lean_code_tokens(source))
    assert not forbidden, (entry['module'], forbidden)
    log = (evidence / 'ReviewAudit.log').read_text()
    namespace = ('Agent1.Periodic.SafetyBoundary' if entry['module'] == 'Agent1PeriodicSafetyBoundary' else 'Agent1.Periodic' if entry['module'].startswith('Agent1Periodic') else 'Agent1.RepeatedBlock')
    for name in re.findall(r'^theorem\s+(\w+)', lean_code_tokens(source), re.M):
        full = namespace + '.' + name
        assert ("'" + full + "' depends on axioms:") in log or ("'" + full + "' does not depend on any axioms") in log, full
        exports.append(full)
    assert not re.search(r'sorryAx|Lean\.ofReduceBool', log), entry['module']
audit_log = (evidence / 'ReviewAudit.log').read_text()
match = re.search(r'FULL_MODULE_AUDIT theorems=(\d+) union=\[([^\]]*)\]', audit_log)
assert match, 'Missing complete audit summary'
definition_match = re.search(r'FULL_DEFINITION_AUDIT definitions=(\d+) union=\[([^\]]*)\]', audit_log)
assert definition_match, 'Missing safe definition audit summary'
for entry in manifest:
    assert sha((root / entry['path']).read_bytes()) == entry['sha256'], 'Source changed during build: ' + entry['path']
summary = {'status': 'PASS', 'reviewer': 'Agent #1 specialist verification_plan (registry preparer; no new proof authorship)',
           'source_modules': len(manifest), 'stage': 'BASELINE_DEPENDENCIES_ONLY', 'final_package_pass_claimed': False, 'trust': 0, 'compiler': compiler,
           'new_public_definitions_type_checked': root_public_definitions,
           'theorems_audited': int(match.group(1)), 'axiom_union': re.findall(r'[A-Za-z_][\w.]*', match.group(2)),
           'safe_definitions_audited': int(definition_match.group(1)),
           'safe_definition_axiom_union': re.findall(r'[A-Za-z_][\w.]*', definition_match.group(2)),
           'nonsafe_definitions_inventoried': re.findall(r'NONSAFE_DEFINITION (\S+) (\S+)', audit_log),
           'unsafe_opaques_inventoried': re.findall(r'UNSAFE_OPAQUE (\S+) (\S+)', audit_log),
           'unsafe_implementation_axioms_inventoried': re.findall(r'UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)', audit_log),
           'audited_named_exports': exports, 'periodic_exports': [x for x in exports if x.startswith('Agent1.Periodic.')], 'sources_unchanged_at_finish': True,
           'source_commit': identity['source_commit'], 'scope': 'Independent fresh baseline46 dependency stage only. The two new reduced-core modules are not part of this run; final package verification remains pending. Reviewer prepared the scoped registry and authored some earlier dependencies, but authored neither new proof. Every baseline object is built afresh here.'}
safe_names = set(re.findall(r'AUDIT_SAFE_DEFINITION (\S+) (\S+)', audit_log))
cstages, unsafe_rec, unknown = [], [], []
for mod, name in summary['nonsafe_definitions_inventoried']:
    if re.search(r'\._cstage[12](?:\.|$)', name):
        cstages.append([mod, name])
    elif name.endswith('._unsafe_rec'):
        base = name[:-len('._unsafe_rec')]
        unsafe_rec.append({'module': mod, 'implementation': name, 'safe_base': base,
                           'safe_base_audited': (mod, base) in safe_names})
    else:
        unknown.append([mod, name])
inventory = {'status': 'PASS' if not unknown and all(x['safe_base_audited'] for x in unsafe_rec) and not summary['unsafe_opaques_inventoried'] and set(map(tuple, summary['unsafe_implementation_axioms_inventoried'])) == prior_unsafe else 'REVIEW_REQUIRED',
             'nonsafe_count': len(summary['nonsafe_definitions_inventoried']),
             'cstage_helpers': len(cstages), 'unsafe_rec_helpers': len(unsafe_rec),
             'unsafe_rec_base_checks': unsafe_rec, 'unclassified_nonsafe': unknown,
             'unsafe_axioms': summary['unsafe_implementation_axioms_inventoried'],
             'unsafe_opaques': summary['unsafe_opaques_inventoried'],
             'meaning': 'Implementation inventory is separate from checked theorem/safe-definition dependencies.'}
(out / 'implementation-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
assert inventory['status'] == 'PASS', inventory
summary.update({'original_reviewer_driver_exit_code': 1, 'original_lean_commands_all_passed': True, 'inventory_classification_only_recovery': True, 'failed_postcheck_preserved': str(evidence / 'implementation-inventory.json'), 'inherited_unsafe_axiom_inventory_exact_match': True, 'inventory_review_performed_lean_execution': False})
(out / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k not in ['nonsafe_definitions_inventoried', 'audited_named_exports', 'periodic_exports']}, indent=2), flush=True)

