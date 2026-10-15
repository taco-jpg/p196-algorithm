#!/usr/bin/env python3
"""Independent fixed-source Lean reconstruction; does not import check.py or use git."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path('/workspace/scratch/b14cfbb70606/agent105')
OUT = Path(__file__).resolve().parent
BUILD = Path('/workspace/scratch/b14cfbb70606/agent105-independent-build')
LEAN = Path('/workspace/scratch/b14cfbb70606/agent105-runtime/lean-4.19.0-linux/bin/lean')
SHIM = Path('/workspace/scratch/b14cfbb70606/agent105-runtime/app-path-compat.so')
CONTRIB = ROOT / 'proofs/contributions/agent-105/actual-high-return'
SOURCES = [
    ROOT / 'proofs/research/continuation/LychrelDigitSums.lean',
    ROOT / 'proofs/contributions/2026-10-15-high-carry-reduction-formal/HighCarryReduction.lean',
    ROOT / 'proofs/contributions/2026-10-15-high-return-rank-formal/HighReturnRank.lean',
    *[CONTRIB / (name + '.lean') for name in
      ['NeutralExterior', 'HighReturnPrefix', 'SmallWidth', 'NumericHigh', 'ActualHighReturn']],
]
# This census was fixed independently after reading the source declarations.
TARGETS = {
    'HighReturnRank': ['finite_check', 'checked_vertex', 'rank_le_three', 'edge_decreases', 'no_four_edges'],
    'Agent105.NeutralExterior': ['carry_neutral_segment', 'first_non_neutral',
        'neutral_overflow_has_low_pair', 'low_outer_high_next_no_overflow'],
    'Agent105.HighReturnPrefix': ['successor_actual', 'first_admissible', 'first_prefix',
        'actual_control_lt_two', 'prefix_carries', 'actual_no_overflow_constraint',
        'actual_prefix_formulas', 'code_properties', 'actual_prefix_edge', 'actual_prefix_rank_decreases'],
    'Agent105.SmallWidth': ['next_congr_upto', 'iterPairs_congr_upto',
        'constant_no_two_returns', 'no_two_high_returns'],
    'Agent105.NumericHigh': ['canonical_width_eq', 'canonical_columns_eq',
        'highCarryWord_iff_of_eq', 'numericHigh_iff', 'numericHigh_iff_represented',
        'numericHigh_orbit_iff', 'numericHigh_orbit_iff_columns'],
    'Agent105.ActualHighReturn': ['iterPairs_add', 'iterPairs_width_ge',
        'high_return_no_second_overflow', 'high_return_state', 'actual_return_rank_decreases',
        'actual_high_returns_le_three', 'numeric_high_returns_le_three',
        'numeric_high_returns_after_le_three', 'no_perpetual_high_returns'],
}
ALLOW = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

report = {'status': 'RUNNING', 'started_utc': now(), 'commands': [],
    'build_directory': str(BUILD), 'audit_scope': TARGETS, 'allowlist': sorted(ALLOW),
    'script_sha256': digest(Path(__file__).read_bytes()),
    'compiler': {'path': str(LEAN), 'sha256': digest(LEAN.read_bytes())},
    'startup_shim': {'path': str(SHIM), 'sha256': digest(SHIM.read_bytes())}}
originals = {}
env = dict(os.environ)
env.pop('LEAN_SYSROOT', None)
env['LEAN_PATH'] = str(BUILD)
env['LD_PRELOAD'] = str(SHIM)

def save():
    (OUT / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')

def run(label, args):
    log = OUT / (label + '.log')
    entry = {'label': label, 'argv': [str(x) for x in args], 'cwd': str(BUILD),
        'environment': {'LEAN_PATH': env['LEAN_PATH'], 'LD_PRELOAD': env['LD_PRELOAD'],
                        'LEAN_SYSROOT': None}, 'started_utc': now(), 'log': str(log)}
    report['commands'].append(entry)
    save()
    start = time.monotonic()
    with log.open('wb') as stream:
        try:
            p = subprocess.run(args, cwd=BUILD, env=env, stdout=stream,
                               stderr=subprocess.STDOUT, timeout=1800)
            entry['exit_code'] = p.returncode
        except subprocess.TimeoutExpired:
            entry['exit_code'] = None
            entry['timeout_seconds'] = 1800
            raise
        finally:
            entry['elapsed_seconds'] = round(time.monotonic() - start, 6)
            entry['finished_utc'] = now()
            stream.flush()
            entry['log_sha256'] = digest(log.read_bytes())
            save()
    print(f"{label}: exit {p.returncode}, {entry['elapsed_seconds']} seconds", flush=True)
    if p.returncode:
        raise RuntimeError(f'{label} failed; see {log}')
    return log.read_text()

try:
    BUILD.mkdir(exist_ok=False)
    assert list(BUILD.iterdir()) == []
    report['initial_build_directory_entries'] = []
    originals = {source: source.read_bytes() for source in SOURCES}
    report['sources'] = [{'path': str(s.relative_to(ROOT)), 'bytes': len(data),
        'sha256': digest(data)} for s, data in originals.items()]
    for source, data in originals.items():
        (BUILD / source.name).write_bytes(data)
    report['initial_copied_entries'] = sorted(p.name for p in BUILD.iterdir())
    assert all(p.suffix == '.lean' for p in BUILD.iterdir())
    save()
    version = run('00-version', [LEAN, '--version']).strip()
    report['compiler']['version'] = version
    if 'version 4.19.0,' not in version:
        raise RuntimeError('Wrong Lean version')
    report['compiled_objects'] = []
    for i, source in enumerate(SOURCES, 1):
        target = BUILD / (source.stem + '.olean')
        assert not target.exists()
        run(f'{i:02}-{source.stem}', [LEAN, '-o', target.name, source.name])
        assert target.is_file()
        report['compiled_objects'].append({'name': target.name, 'bytes': target.stat().st_size,
            'sha256': digest(target.read_bytes())})
        save()

    qualified = [prefix + '.' + name for prefix, names in TARGETS.items() for name in names]
    assert len(qualified) == len(set(qualified)) == 39
    # For these six files, every theorem is top-level and public. Cross-check the
    # independently fixed census against the observed declaration headings.
    for prefix, names in TARGETS.items():
        source = next(s for s in SOURCES if s.stem == prefix.split('.')[-1])
        observed = re.findall(r'^theorem\s+(\S+)', originals[source].decode(), re.M)
        if observed != names:
            raise RuntimeError(f'Declaration census changed in {source}: {observed}')
    audit = 'import ActualHighReturn\n\n' + '\n'.join('#print axioms ' + x for x in qualified) + '\n'
    (OUT / 'IndependentAxioms.lean').write_text(audit)
    (BUILD / 'IndependentAxioms.lean').write_text(audit)
    output = run('09-IndependentAxioms', [LEAN, 'IndependentAxioms.lean'])
    results = {}
    pattern = re.compile(r"'([^\n]+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
    end = 0
    for m in pattern.finditer(output):
        if output[end:m.start()].strip():
            raise RuntimeError(f'Unexpected axiom output: {output[end:m.start()]!r}')
        end = m.end()
        name, raw = m.groups()
        if name in results:
            raise RuntimeError('Duplicate axiom record: ' + name)
        axioms = [] if not raw else [a.strip() for a in raw.split(',')]
        if not set(axioms) <= ALLOW:
            raise RuntimeError('Forbidden axiom: ' + m.group(0))
        results[name] = axioms
    if output[end:].strip():
        raise RuntimeError(f'Unparsed trailing axiom output: {output[end:]!r}')
    if set(results) != set(qualified):
        raise RuntimeError('Axiom audit target mismatch')
    report['axiom_audit'] = results
    report['new_public_theorem_count'] = 34
    report['existing_rank_theorem_count'] = 5

    exact = '''import ActualHighReturn

-- These assignments force the compiled theorem types to match the intended
-- quantifiers and assumptions, without a certificate or representation premise.
example (n R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R → Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (2 * j))) :
    R ≤ 3 := Agent105.ActualHighReturn.numeric_high_returns_le_three n R hn hH

example (n start R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R →
      Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) :
    R ≤ 3 := Agent105.ActualHighReturn.numeric_high_returns_after_le_three n start R hn hH

example (n start : Nat) (hn : 0 < n) :
    ¬ (∀ j, Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) :=
  Agent105.ActualHighReturn.no_perpetual_high_returns n start hn

set_option pp.universes true in
#check Agent105.ActualHighReturn.numeric_high_returns_le_three
set_option pp.universes true in
#check Agent105.ActualHighReturn.numeric_high_returns_after_le_three
#print Agent105.NumericHigh.NumericHigh
#print HighCarryReduction.HighCarryWord
#print DecimalDigits.Canonical
#print DecimalDigits.columnSum
#print DecimalDigits.reflected
#print Lychrel196.orbit
#print Lychrel196.step
#print Lychrel196.reverse10
'''
    (OUT / 'ExactStatements.lean').write_text(exact)
    (BUILD / 'ExactStatements.lean').write_text(exact)
    run('10-ExactStatements', [LEAN, 'ExactStatements.lean'])
    report['exact_statement_checks'] = 'PASS'
    report['rebuild'] = 'PASS'
except BaseException as error:
    report['status'] = 'FAIL'
    report['error'] = f'{type(error).__name__}: {error}'
finally:
    after = {str(s.relative_to(ROOT)): digest(s.read_bytes()) if s.exists() else None for s in originals}
    copied = {s.name: digest((BUILD / s.name).read_bytes()) if (BUILD / s.name).exists() else None for s in originals}
    report['source_sha256_after'] = after
    report['build_source_sha256_after'] = copied
    report['sources_unchanged'] = all(after[str(s.relative_to(ROOT))] == digest(d) and copied[s.name] == digest(d)
                                    for s, d in originals.items())
    if not report['sources_unchanged']:
        report['status'] = 'FAIL'
        report['error'] = 'Source bytes changed during independent build'
    report['finished_utc'] = now()
    # Materialize logs before declaring success.
    logs = ['COMMAND ' + json.dumps(c, ensure_ascii=False) + '\n' + Path(c['log']).read_text()
            for c in report['commands']]
    (OUT / 'full_build.log').write_text('\n\n'.join(logs) + '\n')
    report['full_build_log_sha256'] = digest((OUT / 'full_build.log').read_bytes())
    if report.get('rebuild') == 'PASS' and report['sources_unchanged'] and report['status'] != 'FAIL':
        report['status'] = 'PASS'
    save()
    print(json.dumps({'status': report['status'], 'report': str(OUT / 'report.json'),
                      'error': report.get('error')}, ensure_ascii=False), flush=True)

raise SystemExit(0 if report['status'] == 'PASS' else 1)
