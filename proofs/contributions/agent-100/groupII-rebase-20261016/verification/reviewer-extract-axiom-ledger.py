#!/usr/bin/env python3
"""Read complete multiline axiom lists and cross-check the fresh audit logs."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
PRINTED = re.compile(r"^'([^']+)'\s+depends on axioms:\s*\[", re.M)
EMPTY = re.compile(r"^'([^']+)'\s+does not depend on any axioms", re.M)
AUDITED = re.compile(r'^AUDIT_THEOREM\s+(\S+)\s+(\S+)\s*:\s*\[', re.M)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bracket_list(text: str, start: int) -> list[str]:
    """Consume through the actual closing bracket, never just the first line."""
    if text[start] != '[':
        raise ValueError('Expected opening bracket')
    depth = 0
    for end in range(start, len(text)):
        if text[end] == '[':
            depth += 1
        elif text[end] == ']':
            depth -= 1
            if depth == 0:
                values = [part.strip() for part in text[start + 1:end].split(',') if part.strip()]
                if len(values) != len(set(values)) or set(values) - ALLOWED:
                    raise ValueError('Duplicate or unexpected axiom in full list: ' + repr(values))
                return values
    raise ValueError('Unterminated axiom list')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--executor', required=True)
    args = parser.parse_args()
    registry_bytes = args.registry.read_bytes()
    registry = json.loads(registry_bytes)
    run = args.run.resolve()
    report_bytes = (run / 'verification.json').read_bytes()
    report = json.loads(report_bytes)
    if report['status'] != 'PASS':
        raise ValueError('The independent canonical verification must first PASS')
    project = 'groupii-rebase'
    expected = [e for c in registry['claims'] if c['project'] == project for e in c['endpoints']]
    if len(expected) != 22 or len(set(expected)) != len(expected):
        raise ValueError('Expected exactly 22 distinct explicit new exports')
    logs = run / project / 'logs'
    audit_bytes = (logs / 'ProjectAudit.log').read_bytes()
    audit_text = audit_bytes.decode()
    module_ledger = {}
    for match in AUDITED.finditer(audit_text):
        module, name = match.group(1), match.group(2)
        if name in module_ledger:
            raise ValueError('Duplicate audit declaration: ' + name)
        module_ledger[name] = {'module': module, 'axioms': bracket_list(audit_text, match.end() - 1)}
    audited_count = report['projects'][project]['theorem_count']
    if len(module_ledger) != audited_count:
        raise ValueError('Complete multiline audit ledger count does not match canonical report')
    printed = {}
    log_pins = {}
    for module in registry['projects'][project]['modules']:
        path = logs / (module + '.log')
        raw = path.read_bytes()
        log_pins[str(path.relative_to(run))] = sha(raw)
        text = raw.decode()
        for match in PRINTED.finditer(text):
            name = match.group(1)
            record = {'print_module': module, 'axioms': bracket_list(text, match.end() - 1)}
            if name in printed and set(printed[name]['axioms']) != set(record['axioms']):
                raise ValueError('Conflicting raw printed lists for ' + name)
            printed[name] = record
        for match in EMPTY.finditer(text):
            name = match.group(1)
            if name in printed and printed[name]['axioms']:
                raise ValueError('Conflicting empty/nonempty printed lists for ' + name)
            printed[name] = {'print_module': module, 'axioms': []}
    explicit = {}
    for name in expected:
        if name not in printed or name not in module_ledger:
            raise ValueError('Missing explicit endpoint in printed/full module logs: ' + name)
        direct, full = printed[name], module_ledger[name]
        if set(direct['axioms']) != set(full['axioms']):
            raise ValueError('Printed and module-origin lists differ: ' + name)
        explicit[name] = {'module': full['module'], 'printed_axioms': direct['axioms'],
                          'module_audit_axioms': full['axioms'], 'same_complete_axiom_set': True}
    inherited = {}
    for name in ['Agent100.GroupII.returnedComponent_core_table',
                 'Agent100.GroupII.returnedComponent_not_same_shape']:
        if name not in printed or name not in module_ledger:
            raise ValueError('Missing inherited corrected endpoint: ' + name)
        if set(printed[name]['axioms']) != ALLOWED or set(module_ledger[name]['axioms']) != ALLOWED:
            raise ValueError('Inherited corrected endpoint must report all three actual axioms: ' + name)
        inherited[name] = {'printed_axioms': printed[name]['axioms'],
                           'module_audit_axioms': module_ledger[name]['axioms'],
                           'same_complete_axiom_set': True}
    union = sorted({a for rec in module_ledger.values() for a in rec['axioms']})
    result = {
        'status': 'PASS_COMPLETE_MULTILINE_LISTS_CROSSCHECKED',
        'executor': args.executor,
        'method': 'Balanced-bracket extraction across line breaks from fresh raw logs; set comparison of printed endpoints against full module-origin theorem ledger.',
        'registry_sha256': sha(registry_bytes),
        'verification_sha256': sha(report_bytes),
        'audit_log_sha256': sha(audit_bytes),
        'extractor_sha256': sha(Path(__file__).read_bytes()),
        'explicit_new_export_count': len(explicit),
        'complete_module_origin_theorem_count': len(module_ledger),
        'theorems_by_module': dict(sorted(Counter(r['module'] for r in module_ledger.values()).items())),
        'actual_axiom_union': union,
        'new_explicit_exports': explicit,
        'inherited_historical_ledger_correction': inherited,
        'full_module_origin_ledger': module_ledger,
        'raw_module_log_sha256': log_pins,
        'historical_ledger_copied': False,
    }
    if args.output.exists():
        raise ValueError('Do not overwrite a prior ledger attempt')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'explicit_new_export_count',
        'complete_module_origin_theorem_count', 'actual_axiom_union']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
