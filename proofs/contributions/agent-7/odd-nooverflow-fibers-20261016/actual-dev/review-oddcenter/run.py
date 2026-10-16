#!/usr/bin/env python3
"""Independently validate frozen center evidence and compile boundary fixtures."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

review = Path(__file__).resolve().parent
root = review.parent.parent
baseline = root / 'actual-dev/clean-004'
expected = '72f1c2e64a587e25f85482b6f61ceea0763218d60c7c7cc5eaa7d1d31ca65728'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root / 'OddCenter.lean') == expected
assert sha(baseline / 'source/OddCenter.lean') == expected
prior = json.loads((baseline / 'verification.json').read_text())
assert prior['status'] == 'PASS' and prior['reuse_attempt'] is None
assert all(c['exit_code'] == 0 for c in prior['commands'])
records = {r['module']: r for r in prior['source_records']}
reused = {}
for module in ['InverseFibers', 'PathCounts', 'WordBridge', 'OddCenter']:
    record = records[module]
    src = baseline / 'source' / (module + '.lean')
    obj = baseline / 'source' / (module + '.olean')
    assert sha(src) == record['sha256'] and sha(obj) == record['object_sha256']
    reused[module] = {'source_sha256': sha(src), 'object_sha256': sha(obj)}
lean = Path(prior['lean'])
assert sha(lean) == prior['lean_sha256']
author_audit = (baseline / 'logs/OddCenter.log').read_text()
audits = re.findall(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)$", author_audit, re.M)
assert len(audits) == 15
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
axiom_records = []
for name, axes in audits:
    values = [] if not axes else axes.split(', ')
    assert set(values) <= allowed
    axiom_records.append({'declaration': name, 'axioms': values})
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o', str(review / 'ReviewCenter.olean'), str(review / 'ReviewCenter.lean')]
env = dict(os.environ)
env['LEAN_PATH'] = str(baseline / 'source')
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(command, cwd=review, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(review / 'ReviewCenter.log').write_text(result.stdout)
report = {
    'reviewer': 'Agent #7 runtime/actual specialist (/root/runtime)',
    'reviewed_author': 'Agent #7 center specialist (/root/gap_inventory)',
    'reviewed_source': 'OddCenter.lean',
    'reviewed_source_sha256': expected,
    'independent_fresh_build': 'actual-dev/clean-004/verification.json',
    'independent_build_report_sha256': sha(baseline / 'verification.json'),
    'execution_note': 'clean-004 was actually executed independently by this specialist; this review reuses its unchanged pinned objects instead of repeating the entire build.',
    'shared_toolchain_note': 'Same recovered official Lean 4.19.0 runtime; no independent toolchain-download claim.',
    'lean_version': subprocess.check_output([str(lean), '--version'], text=True).strip(),
    'lean_sha256': sha(lean),
    'reused_fixture_dependencies': reused,
    'reviewed_export_axioms': axiom_records,
    'reviewed_export_audit_log_sha256': sha(baseline / 'logs/OddCenter.log'),
    'fixture_source_sha256': sha(review / 'ReviewCenter.lean'),
    'fixture_command': command,
    'fixture_lean_path': str(baseline / 'source'),
    'fixture_started_at': started,
    'fixture_finished_at': datetime.now(timezone.utc).isoformat(),
    'fixture_exit_code': result.returncode,
    'fixture_log_sha256': sha(review / 'ReviewCenter.log'),
    'status': 'PASS' if result.returncode == 0 else 'FAIL',
}
(review / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(result.stdout, end='')
raise SystemExit(result.returncode)
