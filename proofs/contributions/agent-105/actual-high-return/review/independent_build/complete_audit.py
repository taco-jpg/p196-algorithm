#!/usr/bin/env python3
"""Complete the audit of the preserved, genuinely fresh first reconstruction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
BUILD = Path('/workspace/scratch/b14cfbb70606/agent105-independent-build-attempt-001')
first = json.loads((OUT / 'attempt_001/report.json').read_text())
report = dict(first)
report['status'] = 'RUNNING'
report.pop('error', None)
report['adopted_build'] = 'attempt_001: all eight source compilations exited zero in an initially empty directory'
report['preserved_build_directory'] = str(BUILD)
report['prior_attempts'] = [
    {'report': 'attempt_001/report.json', 'result': '8 fresh compilations and Lean axiom printing succeeded; parser rejected wrapped axiom output'},
    {'report': 'attempt_002/report.json', 'result': 'rejected: unexpected preexisting objects appeared after first compilation; not accepted as a fresh build'},
]
report['completion_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
report['commands'] = [dict(c, log=str(OUT / 'attempt_001' / Path(c['log']).name)) for c in first['commands']]
LEAN = Path(report['compiler']['path'])
SHIM = Path(report['startup_shim']['path'])
env = dict(os.environ)
env.pop('LEAN_SYSROOT', None)
env['LEAN_PATH'] = str(BUILD)
env['LD_PRELOAD'] = str(SHIM)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save():
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')

def verify_frozen():
    assert sha(LEAN) == report['compiler']['sha256']
    assert sha(SHIM) == report['startup_shim']['sha256']
    assert len(first['compiled_objects']) == 8
    for source in first['sources']:
        assert sha(ROOT / source['path']) == source['sha256'], source['path']
        assert sha(BUILD / Path(source['path']).name) == source['sha256'], source['path']
    for obj in first['compiled_objects']:
        assert sha(BUILD / obj['name']) == obj['sha256'], obj['name']

def run(label, name):
    argv = [str(LEAN), name]
    log = OUT / (label + '.log')
    record = {'label': label, 'argv': argv, 'cwd': str(BUILD), 'log': str(log),
        'environment': {'LEAN_PATH': str(BUILD), 'LD_PRELOAD': str(SHIM), 'LEAN_SYSROOT': None},
        'started_utc': datetime.now(timezone.utc).isoformat()}
    report['commands'].append(record)
    save()
    started = time.monotonic()
    with log.open('wb') as stream:
        p = subprocess.run(argv, cwd=BUILD, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
    record.update(exit_code=p.returncode, elapsed_seconds=round(time.monotonic()-started,6), log_sha256=sha(log),
        finished_utc=datetime.now(timezone.utc).isoformat())
    save()
    print(f'{label}: exit {p.returncode}, {record["elapsed_seconds"]} seconds', flush=True)
    assert p.returncode == 0, label
    return log.read_text()

try:
    verify_frozen()
    report['first_build_sources_and_objects_match_before_completion'] = True
    expected = [p + '.' + n for p, ns in first['audit_scope'].items() for n in ns]
    assert len(expected) == len(set(expected)) == 39
    audit = 'import ActualHighReturn\n\n' + '\n'.join('#print axioms ' + n for n in expected) + '\n'
    assert (BUILD / 'IndependentAxioms.lean').read_text() == audit
    output = run('11-IndependentAxioms-corrected-parser', 'IndependentAxioms.lean')
    pattern = re.compile(r"'([^\n]+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
    results = {}
    end = 0
    for m in pattern.finditer(output):
        assert not output[end:m.start()].strip(), output[end:m.start()]
        end = m.end()
        name, raw = m.groups()
        assert name not in results, name
        axioms = [] if not raw else [a.strip() for a in raw.split(',')]
        assert set(axioms) <= {'propext','Classical.choice','Quot.sound'}, axioms
        results[name] = axioms
    assert not output[end:].strip(), output[end:]
    assert set(results) == set(expected)
    report['axiom_audit'] = results
    report['new_public_theorem_count'] = 34
    report['existing_rank_theorem_count'] = 5
    exact = (OUT / 'ExactStatements.lean').read_text()
    (BUILD / 'ExactStatements.lean').write_text(exact)
    report['exact_statement_source_sha256'] = sha(OUT / 'ExactStatements.lean')
    run('12-ExactStatements', 'ExactStatements.lean')
    report['exact_statement_checks'] = 'PASS'
    verify_frozen()
    report['first_build_sources_and_objects_match_after_completion'] = True
    report['rebuild'] = 'PASS (adopted first build only)'
    report['status'] = 'PASS'
except BaseException as error:
    report['status'] = 'FAIL'
    report['error'] = f'{type(error).__name__}: {error}'
finally:
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    report['source_sha256_after'] = {s['path']: sha(ROOT / s['path']) for s in first['sources']}
    report['sources_unchanged'] = all(report['source_sha256_after'][s['path']] == s['sha256'] for s in first['sources'])
    if not report['sources_unchanged']:
        report['status'] = 'FAIL'
    # Failure during log materialization cannot publish a PASS report.
    final_status = report['status']
    report['status'] = 'FINALIZING'
    save()
    (OUT / 'full_build.log').write_text('\n\n'.join('COMMAND '+json.dumps(c)+'\n'+Path(c['log']).read_text()
        for c in report['commands'])+'\n')
    report['full_build_log_sha256'] = sha(OUT / 'full_build.log')
    report['status'] = final_status
    save()
    print(json.dumps({'status':report['status'], 'report':str(OUT / 'report.json'), 'error':report.get('error')}),flush=True)

raise SystemExit(0 if report['status']=='PASS' else 1)
