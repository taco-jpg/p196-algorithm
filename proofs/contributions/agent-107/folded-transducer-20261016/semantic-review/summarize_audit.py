#!/usr/bin/env python3
"""从真实完整日志汇总审计；不把生成辅助声明计作人工书写的新定理。"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('manifest', type=Path)
args = parser.parse_args()
data = json.loads(args.manifest.read_text())
assert data['status'] == 'INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS'
entry = next(row for row in reversed(data['executions']) if row['exit_code'] == 0 and ('axioms' in row['name'] or 'AxiomAudit' in row['name']))
text = (args.manifest.parent / entry['stdout_log']).read_text()
origins = dict((name, module) for module, name in re.findall(r'^DECLARATION_ORIGIN (\S+): (\S+)$', text, re.M))
audited = []
for name, no_axioms, axioms in re.findall(r"^'([^']+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])$", text, re.M):
    ax = [] if no_axioms == 'does not depend on any axioms' else axioms.split(', ')
    audited.append({'name': name, 'module': origins.get(name), 'axioms': ax})
assert len(audited) == len(origins)
repo = Path(__file__).resolve().parents[5]
source_counts = {
    source['module']: len(re.findall(r'^theorem\s+', (repo / source['source']).read_text(), re.M))
    for source in data['source_files'] if source['module'].startswith('Agent107Transducer')
}
summary = {
    'status': data['status'],
    'build_dir_initially_empty': data['build_dir_initially_empty'],
    'manifest': str(args.manifest), 'last_audit_log': entry['stdout_log'],
    'new_source_module_count': len(source_counts),
    'explicit_source_theorem_declarations': sum(source_counts.values()),
    'source_theorem_counts': source_counts,
    'audited_module_origin_theorems_including_private_and_generated': len(audited),
    'audited_count_by_module': dict(Counter(row['module'] for row in audited)),
    'actual_axiom_union': sorted(set(ax for row in audited for ax in row['axioms'])),
    'axiom_set_counts': dict(Counter(', '.join(row['axioms']) or '(none)' for row in audited)),
    'preserved_failed_executions': [row for row in data['executions'] if row['exit_code'] != 0],
    'theorem_audits': audited,
}
out = Path(__file__).resolve().parent / 'independent-audit-summary.json'
out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: value for key, value in summary.items() if key not in ['theorem_audits', 'preserved_failed_executions']}, ensure_ascii=False, indent=2))
