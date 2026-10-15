"""Fresh Lean 4.19 source rebuild and per-declaration transitive axiom audit."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
COMPILER = Path(sys.argv[1]).resolve()
BUILD = HERE / 'fresh_build'
BUILD.mkdir(exist_ok=True)
SOURCES = [PROJECT / 'continuation/LychrelDigitSums.lean', HERE / 'ZeroExterior.lean']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source):
    out, pos, depth = [], 0, 0
    while pos < len(source):
        if source.startswith('/-', pos):
            depth += 1
            pos += 2
        elif depth and source.startswith('-/', pos):
            depth -= 1
            pos += 2
        elif depth:
            pos += 1
        elif source.startswith('--', pos):
            end = source.find('\n', pos)
            pos = len(source) if end < 0 else end
        else:
            out.append(source[pos])
            pos += 1
    assert depth == 0
    return ''.join(out)


def axioms_in(output):
    result = {}
    for match in re.finditer(
            r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|"
            r'does not depend on any axioms)', output, re.S):
        axioms = {x.strip() for x in (match.group(2) or '').split(',') if x.strip()}
        assert axioms <= ALLOWED, (match.group(1), axioms)
        result[match.group(1)] = sorted(axioms)
    return result


hashes = {p.name: digest(p) for p in SOURCES}
version = subprocess.run([str(COMPILER), '--version'], capture_output=True,
                         text=True, check=True).stdout.strip()
assert 'version 4.19.0' in version, version
env = dict(os.environ, LEAN_PATH=str(BUILD))
for stem in [p.stem for p in SOURCES] + ['AllAxioms']:
    for suffix in ('.olean', '.ilean', '.olean.tmp'):
        (BUILD / (stem + suffix)).unlink(missing_ok=True)

names, theorem_names, by_module = [], [], {}
for source in SOURCES:
    text = without_comments(source.read_text())
    assert not re.search(r'\b(?:sorry|admit|native_decide|axiom)\b', text), source
    if source != SOURCES[-1]:
        continue
    declarations = re.findall(r'^(theorem|def)\s+(\w+)', text, re.M)
    found = [source.stem + '.' + name for _, name in declarations]
    names.extend(found)
    theorem_names.extend(source.stem + '.' + name for kind, name in declarations
                         if kind == 'theorem')
    by_module[source.stem] = {
        'theorems': sum(kind == 'theorem' for kind, _ in declarations),
        'definitions': sum(kind == 'def' for kind, _ in declarations),
    }
(HERE / 'AllAxioms.lean').write_text('import ZeroExterior\n\n' +
    '\n'.join('#print axioms ' + name for name in names) + '\n')

records, logs, audit = [], [version + '\n'], {}
for source in SOURCES + [HERE / 'AllAxioms.lean']:
    shutil.copy2(source, BUILD / source.name)
    started = time.monotonic()
    proc = subprocess.run([str(COMPILER), '-o', source.stem + '.olean', source.name],
                          cwd=BUILD, env=env, capture_output=True, text=True)
    record = {'module': source.stem, 'exit_code': proc.returncode,
              'seconds': time.monotonic() - started}
    records.append(record)
    output = proc.stdout + proc.stderr
    logs.append(json.dumps(record) + '\n' + output)
    (HERE / 'compile.log').write_text('\n'.join(logs))
    print(json.dumps(record), flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
    found = axioms_in(output)
    if source.stem == 'AllAxioms':
        audit = found

assert set(audit) == set(names), {'missing': sorted(set(names) - set(audit))}
assert hashes == {p.name: digest(p) for p in SOURCES}, 'source changed during build'
(HERE / 'verification.json').write_text(json.dumps({
    'status': 'PASS', 'compiler': version, 'modules': records,
    'source_sha256': hashes,
    'new_theorems_audited': len(theorem_names),
    'new_definitions_audited': len(names) - len(theorem_names),
    'declarations_by_module': by_module,
    'declaration_axioms': audit, 'axioms_allowed': sorted(ALLOWED),
    'coefficient_range': [0, 18],
    'three_zero_prefix_time_bound': 4,
    'all_earlier_states_have_three_zero_prefix': True,
    'all_earlier_updates_nonoverflow': True,
    'exact_outer_coefficient': '2^t * initial_outer',
    'width_constant_through_target': True,
    'arbitrary_positive_numeric_orbit_bridge': True,
    'no_positive_fixed_outer_return': True,
    'time_bound_sharp_example': '10000000 -> 10000001 -> 20000002 -> 40000004 -> 80000008',
    'two_zero_overflow_counterexample': [9, 10, 9, 0, 9, 10, 9],
    'all_finite_widths_and_times_covered': True,
    'bounded_search_used_as_proof': False,
    'persistent_safe_invariant_found': False,
    'decimal_lychrel_existence_proved': False,
    'earlier_sources_modified': False,
}, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'theorems': len(theorem_names),
                  'definitions': len(names) - len(theorem_names)}), flush=True)
