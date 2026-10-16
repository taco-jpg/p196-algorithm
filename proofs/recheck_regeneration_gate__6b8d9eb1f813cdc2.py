"""Root compilation and axiom audit of the exact all-gap regeneration gate."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, time

HERE = Path(__file__).resolve().parent
PASS = HERE.parent
SOURCE = PASS / 'lean/regeneration_gate'
BUILD = HERE / 'regeneration_gate_build'
BUILD.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
root_prior = json.loads((HERE / 'lean_rebuild.json').read_text())
branch = json.loads((SOURCE / 'verification.json').read_text())
assert root_prior['status'] == branch['status'] == 'PASS'
dependency_modules = ['LychrelDigitSums', 'IncomingCarrySensitivity', 'RawSymmetryObstruction', 'IntrinsicSeam']
for module in dependency_modules:
    source = HERE / 'lean_build' / (module + '.lean')
    digest = sha(source)
    assert digest == branch['source_sha256'][source.name]
    assert digest in root_prior['source_sha256'].values()
    for suffix in ('.lean', '.olean'):
        shutil.copyfile(HERE / 'lean_build' / (module + suffix), BUILD / (module + suffix))
modules = ['RegenerationGate', 'RegenerationGateDynamics']
frozen = {m + '.lean': sha(SOURCE / (m + '.lean')) for m in modules}
names = []
for m in modules:
    path = SOURCE / (m + '.lean')
    assert frozen[path.name] == branch['source_sha256'][path.name]
    assert not re.search(r'\b(?:sorry|admit|native_decide)\b|^axiom\s', path.read_text(), re.M)
    shutil.copyfile(path, BUILD / path.name)
    names += ['RegenerationGate.' + n for n in re.findall(r'^(?:theorem|def)\s+(\w+)', path.read_text(), re.M)]
assert len(names) == len(set(names)) == 34
audit = HERE / 'RegenerationGateAxioms.lean'
audit.write_text('import RegenerationGateDynamics\n' + ''.join('#print axioms ' + n + '\n' for n in names))
shutil.copyfile(audit, BUILD / audit.name)
compiler = '/workspace/scratch/fe6abe1df721/lean-runtime/lean'
env = dict(os.environ, LEAN_PATH=str(BUILD))
logs, rows, axioms = [], [], {}
for module in modules + [audit.stem]:
    (BUILD / (module + '.olean')).unlink(missing_ok=True)
    start = time.monotonic()
    result = subprocess.run([compiler, '-o', module + '.olean', module + '.lean'],
                            cwd=BUILD, env=env, text=True, capture_output=True)
    row = {'module': module, 'exit_code': result.returncode, 'seconds': time.monotonic() - start}
    rows.append(row)
    output = result.stdout + result.stderr
    logs.extend([json.dumps(row), output])
    (HERE / 'regeneration_gate_recheck.log').write_text('\n'.join(logs))
    assert result.returncode == 0, output
    print(json.dumps(row), flush=True)
    for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
        values = set(x.strip() for x in (match[2] or '').split(',') if x.strip())
        assert values <= {'propext', 'Classical.choice', 'Quot.sound'}
        axioms[match[1]] = sorted(values)
assert set(axioms) == set(names)
assert axioms == branch['declaration_axioms']
assert frozen == {m + '.lean': sha(SOURCE / (m + '.lean')) for m in modules}
receipt = {
    'status': 'PASS', 'source_sha256': frozen,
    'dependency_sha256': {m + '.lean': sha(BUILD / (m + '.lean')) for m in dependency_modules},
    'root_dependency_build_receipt': 'lean_rebuild.json',
    'new_module_compilations': rows, 'declaration_axioms': axioms,
    'written_semantic_review': 'Explicit carry recurrence, actual physical width, exact pair successor for every natural gap including zero, canonical positive realizations and ordinary safety at times 0, 1, 2.',
    'limitations': 'Target interfaces differ; no recurrent closure or later safety asserted.',
    'excluded_duplicate_infrastructure': ['regeneration_gate_build/'],
    'decimal_lychrel_existence_proved': False,
}
(HERE / 'regeneration_gate_review.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'declarations': len(names), 'source_sha256': frozen}), flush=True)
