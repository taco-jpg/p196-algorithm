"""Independent clean source compilation and exact per-declaration axiom audit."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
PASS = HERE.parent
PROJECT = PASS.parents[1]
COMPILER = Path('/workspace/scratch/fe6abe1df721/lean-runtime/lean')
BUILD = HERE / 'lean_build'
BUILD.mkdir(exist_ok=True)
SOURCES = [
    PROJECT / 'continuation/LychrelDigitSums.lean',
    PROJECT / 'main_existence_attempt/renewal_pass/lean/incoming_carry/IncomingCarrySensitivity.lean',
    PROJECT / 'main_existence_attempt/renewal_pass/lean/raw_symmetry/RawSymmetryObstruction.lean',
    PASS / 'lean/IntrinsicSeam.lean',
    PASS / 'lean/SeamAnnihilation.lean',
]
ALLOWED = {'propext', 'Quot.sound', 'Classical.choice'}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = {str(p.relative_to(PROJECT)): sha(p) for p in SOURCES}
declarations = []
for src in SOURCES[-2:]:
    for name in re.findall(r'^(?:theorem|def)\s+(\w+)', src.read_text(), re.M):
        declarations.append(src.stem + '.' + name)
audit = HERE / 'RootAxioms.lean'
audit.write_text('import SeamAnnihilation\n' + ''.join('#print axioms ' + n + '\n' for n in declarations))
for p in BUILD.glob('*.olean'):
    p.unlink()
env = dict(os.environ, LEAN_PATH=str(BUILD))
version = subprocess.run([str(COMPILER), '--version'], text=True, capture_output=True, check=True).stdout.strip()
assert 'version 4.19.0' in version
records, log, axioms = [], [version], {}
for source in SOURCES + [audit]:
    shutil.copyfile(source, BUILD / source.name)
    start = time.monotonic()
    p = subprocess.run([str(COMPILER), '-o', source.stem + '.olean', source.name], cwd=BUILD, env=env, text=True, capture_output=True)
    row = {'source': source.name, 'exit_code': p.returncode, 'seconds': time.monotonic() - start}
    records.append(row)
    output = p.stdout + p.stderr
    log.extend([json.dumps(row), output])
    (HERE / 'lean_rebuild.log').write_text('\n'.join(log))
    print(json.dumps(row), flush=True)
    assert p.returncode == 0, output
    if source == audit:
        for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
            ax = set(x.strip() for x in (m[2] or '').split(',') if x.strip())
            assert ax <= ALLOWED, (m[1], ax)
            axioms[m[1]] = sorted(ax)
assert set(axioms) == set(declarations)
assert before == {str(p.relative_to(PROJECT)): sha(p) for p in SOURCES}
(HERE / 'lean_rebuild.json').write_text(json.dumps({'status': 'PASS', 'compiler': version, 'modules': records, 'source_sha256': before, 'declaration_axioms': axioms, 'main_existence_proved': False}, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'audited_declarations': len(axioms)}), flush=True)
