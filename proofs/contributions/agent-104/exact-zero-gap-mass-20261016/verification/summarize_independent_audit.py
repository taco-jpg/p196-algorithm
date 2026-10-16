#!/usr/bin/env python3
"""Cross-check retained clean-build evidence and publish a reviewer summary.

This post-processing does not change the unmodified verifier's report or logs.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


def main() -> None:
    root = Path(__file__).resolve().parents[5]
    package = Path(__file__).resolve().parents[1]
    run = package / 'verification/independent-clean-001'
    report_path = run / 'verification.json'
    report = json.loads(report_path.read_text())
    registry_path = root / 'proofs/Agent104ExactMass.registry.json'
    registry = json.loads(registry_path.read_text())
    if report['status'] != 'PASS' or report['repository_wide_pass']:
        raise RuntimeError('Expected a completed scoped PASS')
    project = report['projects']['agent104-exact-mass']
    if project['status'] != 'PASS' or len(project['commands']) != 7:
        raise RuntimeError('Incomplete six-module build and audit')
    for command in project['commands']:
        data = (run / command['log']).read_bytes()
        if command['exit_code'] != 0 or hashlib.sha256(data).hexdigest() != command['log_sha256']:
            raise RuntimeError('Command or log mismatch: ' + command['label'])
    inventory = json.loads((run / 'FILES.json').read_text())
    for path, record in inventory.items():
        data = (run / path).read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise RuntimeError('Retained evidence inventory mismatch: ' + path)
    log = (run / 'agent104-exact-mass/logs/ProjectAudit.log').read_text()
    parsed = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]', log, re.M)
    if len(parsed) != 1254 or len(parsed) != project['theorem_count']:
        raise RuntimeError('Unexpected theorem count')
    union: set[str] = set()
    by_module: Counter[str] = Counter()
    by_name: dict[str, object] = {}
    for module, name, axioms in parsed:
        axlist = sorted(a.strip() for a in axioms.split(',') if a.strip())
        union.update(axlist)
        by_module[module] += 1
        if name in by_name:
            raise RuntimeError('Duplicate audited theorem: ' + name)
        by_name[name] = {'module_origin': module, 'axioms': axlist}
    if union != {'Classical.choice', 'Quot.sound', 'propext'}:
        raise RuntimeError('Unexpected theorem axiom union')
    endpoints = {}
    for claim in registry['claims']:
        for name in claim['endpoints']:
            expected = ('Agent104ExactZeroGap' if name.startswith('Agent104.ExactZeroGap.')
                        else 'Agent104FiniteMassBound')
            if name not in by_name or by_name[name]['module_origin'] != expected:
                raise RuntimeError('Incorrect endpoint module origin: ' + name)
            endpoints[name] = by_name[name]
    if len(endpoints) != 11:
        raise RuntimeError('Incomplete public endpoint list')
    selected_modules = set(registry['projects']['agent104-exact-mass']['modules'])
    if set(by_module) - selected_modules:
        raise RuntimeError('An audited theorem came from outside the selected closure')
    compiled_modules = {command['label'] for command in project['commands']
                        if command['label'] != 'ProjectAudit'}
    if compiled_modules != selected_modules:
        raise RuntimeError('Compiled module set differs from the full closure')
    # A definitions-only module need not own any theorem declarations.
    for module in selected_modules:
        by_module.setdefault(module, 0)
    linkage_path = package / 'verification/published-source-linkage.json'
    linkage = json.loads(linkage_path.read_text())
    if linkage['status'] != 'PASS_ALL_SIX_PUBLISHED_SOURCES_EQUAL_COMPILED_SNAPSHOTS':
        raise RuntimeError('Published source linkage has not passed')
    report_hash = hashlib.sha256(report_path.read_bytes()).hexdigest()
    if report_hash != linkage['original_build_report_sha256']:
        raise RuntimeError('The original build report changed after publication linkage')
    summary = {
        'schema_version': 1,
        'status': 'PASS_INDEPENDENT_FROZEN_SOURCE_KERNEL_BUILD_AND_MODULE_ORIGIN_AUDIT',
        'reviewer': 'real subagent /root/strategy_review',
        'proof_module_author': 'Agent #104 / root',
        'unmodified_verifier': registry['verifier'],
        'registry_sha256': hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        'verification_report_sha256': report_hash,
        'build_source_head': report['source_commit'],
        'published_source_commit': linkage['published_commit'],
        'published_source_linkage_sha256': hashlib.sha256(linkage_path.read_bytes()).hexdigest(),
        'project_object_files_reused': False,
        'module_count': len(by_module),
        'theorem_count': len(parsed),
        'theorems_by_module': dict(sorted(by_module.items())),
        'axiom_union': sorted(union),
        'public_endpoints': endpoints,
        'command_count': len(project['commands']),
        'all_command_exit_codes_zero': True,
        'all_command_log_hashes_rechecked': True,
        'retained_non_olean_inventory_rechecked': True,
        'repository_wide_pass': False,
        'scope': project['scope'],
        'python_control_evidence_is_separate': True,
        'semantic_review': 'review/SEMANTIC_REVIEW.md',
        'control_result': 'review/independent_zero_gap_control.json',
        'published_source_linkage': 'verification/published-source-linkage.json',
    }
    output = package / 'verification/independent-review-summary.json'
    output.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'status': summary['status'], 'modules': len(by_module),
                      'theorems': len(parsed), 'theorems_by_module': dict(by_module),
                      'endpoints': len(endpoints), 'axiom_union': sorted(union)}))


if __name__ == '__main__':
    main()
