"""Independent recompile and complete theorem audit after check.py succeeds.

Usage: python3 root_recheck.py /absolute/path/to/lean-4.19.0
The dependency source copies must match the fresh source-build record.
Only the new module is rebuilt here; that trust boundary is explicit.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
LEAN = str(Path(sys.argv[1]).resolve())
DEPENDENCIES = HERE / 'fresh_build'
BUILD = HERE / 'root_build'
BUILD.mkdir(exist_ok=True)
source = HERE / 'RawSymmetryObstruction.lean'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
prior = json.loads((HERE / 'verification.json').read_text())
assert prior['status'] == 'PASS'
for filename, expected in prior['source_sha256'].items():
    assert hashlib.sha256((DEPENDENCIES / filename).read_bytes()).hexdigest() == expected
assert prior['source_sha256'][source.name] == source_hash
expected_theorems = re.findall(r'^theorem\s+(\w+)', source.read_text(), re.M)
assert len(expected_theorems) == len(set(expected_theorems)) == 42
audit = 'import RawSymmetryObstruction\n\n' + '\n'.join(
    '#print axioms RawSymmetryObstruction.' + name for name in expected_theorems) + '\n'
(BUILD / 'RootAxioms.lean').write_text(audit)
(HERE / 'RootAxioms.lean').write_text(audit)
shutil.copy2(source, BUILD / source.name)
for name in ('RawSymmetryObstruction.olean', 'RootAxioms.olean'):
    (BUILD / name).unlink(missing_ok=True)
env = dict(os.environ, LEAN_PATH=str(BUILD) + os.pathsep + str(DEPENDENCIES))
version = subprocess.run([LEAN, '--version'], check=True, capture_output=True, text=True).stdout.strip()
assert 'version 4.19.0' in version
logs, results = [version], []
for name in ('RawSymmetryObstruction', 'RootAxioms'):
    run = subprocess.run([LEAN, '-o', name + '.olean', name + '.lean'],
                         cwd=BUILD, env=env, capture_output=True, text=True)
    logs.append(name + '\n' + run.stdout + run.stderr)
    (HERE / 'root_compile.log').write_text('\n'.join(logs))
    results.append({'module': name, 'exit_code': run.returncode})
    print(json.dumps(results[-1]), flush=True)
    if run.returncode:
        raise SystemExit(run.returncode)
output = run.stdout + run.stderr
found = {}
for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
    axioms = sorted(x.strip() for x in (match.group(2) or '').split(',') if x.strip())
    assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
    found[match.group(1)] = axioms
assert set(found) == {'RawSymmetryObstruction.' + name for name in expected_theorems}
assert found == prior['theorem_axioms']
assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
result = {'status': 'PASS', 'compiler': version, 'modules': results,
          'new_theorems_audited': len(found), 'source_sha256': source_hash,
          'dependency_source_hashes_checked': prior['source_sha256'],
          'dependency_scope': 'reuses freshly rebuilt, source-hash-checked dependency modules; independently recompiles new raw-symmetry module and audit',
          'theorem_axioms': found, 'main_existence_proved': False}
(HERE / 'root_verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'new_theorems_audited': len(found)}))
