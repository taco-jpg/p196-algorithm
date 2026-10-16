#!/usr/bin/env python3
"""Independently inspect the retained canonical witness receipt and all logs."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(test, detail):
    if not test:
        raise AssertionError(detail)


def main():
    independent = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', type=Path, default=independent / 'lean-replay-001')
    parser.add_argument('--registry', type=Path,
                        default=independent / 'Agent104620Witness.registry.json')
    parser.add_argument('--output', type=Path,
                        default=independent / 'independent-review-summary.json')
    args = parser.parse_args()
    replay = args.replay.resolve()
    canonical = replay / 'canonical'
    registry_path = args.registry.resolve()
    registry = json.loads(registry_path.read_text())
    launch = json.loads((replay / 'launch.json').read_text())
    report_path = canonical / 'verification.json'
    report = json.loads(report_path.read_text())
    project = report['projects']['agent104_620_witness']
    require(report['status'] == project['status'] == launch['status'] == 'PASS', 'replay status')
    require(report['source_commit'] == launch['published_commit'] == '8f254e9b43bb319a6c43b208cd181ffc005153ec', 'published source commit')
    require(report['source_tree_clean'], 'source checkout cleanliness')
    require(report['registry_sha256'] == launch['registry_sha256'] == sha(registry_path), 'registry hash')
    require(launch['canonical_report_sha256'] == sha(report_path), 'canonical report hash')
    require(launch['canonical_exit_code'] == 0, 'canonical process exit')
    inventory = json.loads((canonical / 'FILES.json').read_text())
    for path, expected in inventory.items():
        file = canonical / path
        require(file.stat().st_size == expected['bytes'] and sha(file) == expected['sha256'], ('retained file inventory', path))
    modules = registry['projects']['agent104_620_witness']['modules']
    require(set(project['sources']) == set(modules) and len(modules) == 11, 'source module domain')
    linkage = json.loads((replay / 'source-linkage.json').read_text())
    require(linkage['status'] == 'PASS_BYTE_EXACT_PUBLISHED_SOURCE_LINKAGE', 'source linkage status')
    checkout = Path(launch['source_checkout'])
    for name, expected in modules.items():
        source = project['sources'][name]
        require(source['sha256'] == source['build_sha256'] == expected['sha256'], ('compiled source pin', name))
        require(source['imports'] == expected['imports'], ('source imports', name))
        require(sha(canonical / 'agent104_620_witness/source' / (name + '.lean')) == expected['sha256'], ('retained source', name))
        require(sha(checkout / expected['path']) == expected['sha256'], ('published checkout source', name))
        require(linkage['files'][expected['path']]['git_blob'] == expected['git_blob'], ('published source Git ID', name))
    require(sha(checkout / 'proofs/verify_project__214bf7673efe116b.py') ==
            'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a', 'unmodified original verifier')
    commands = project['commands']
    require(len(commands) == 12, 'eleven modules plus audit command count')
    require([command['label'] for command in commands] == project['build_order'] + ['ProjectAudit'], 'command domain/order')
    for command in commands:
        require(command['exit_code'] == 0 and sha(canonical / command['log']) == command['log_sha256'], ('command receipt', command['label']))
    audit = (canonical / commands[-1]['log']).read_text()
    # Lean pretty-prints long axiom lists over multiple lines. Read each whole
    # bracketed list, and still require every original audit header exactly once.
    declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$', audit, re.M)
    headers = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) :', audit, re.M)
    require([(module, name) for module, name, _ in declarations] == headers, 'all audit headers parsed')
    require(len(declarations) == project['theorem_count'] == 1364, 'full module-origin count')
    require(len({name for _, name, _ in declarations}) == len(declarations), 'duplicate audit declaration')
    by_module = Counter({name: 0 for name in modules})
    axiom_union = set()
    theorem_data = {}
    for module, name, text in declarations:
        require(module in modules, ('unexpected origin module', module))
        axioms = {part.strip() for part in text.split(',')} if text.strip() else set()
        require(axioms <= {'Classical.choice', 'Quot.sound', 'propext'}, ('disallowed axiom', name, axioms))
        axiom_union.update(axioms)
        by_module[module] += 1
        theorem_data[name] = {'module': module, 'axioms': sorted(axioms)}
    endpoints = [endpoint for claim in registry['claims'] for endpoint in claim['endpoints']]
    require(endpoints == project['endpoints'] and len(endpoints) == 7, 'seven public endpoints')
    for i, endpoint in enumerate(endpoints):
        data = theorem_data[endpoint]
        require(data['module'] == 'Agent104620Witness', ('endpoint originating module', endpoint))
        expected_axioms = [] if i < 2 else ['Quot.sound', 'propext']
        require(data['axioms'] == expected_axioms, ('public theorem axiom set', endpoint))
    require(axiom_union == {'Classical.choice', 'Quot.sound', 'propext'}, 'full axiom union')
    summary = {
        'schema_version': 1,
        'status': 'PASS_INDEPENDENT_EMPTY_BUILD_AND_FULL_MODULE_ORIGIN_AUDIT',
        'reviewer': '/root/strategy_review',
        'relationship': 'Real non-author reviewer within the same session and shared GitHub account; not external peer review.',
        'summarized_at_utc': datetime.now(timezone.utc).isoformat(),
        'published_source_commit': report['source_commit'],
        'source_tree_clean': report['source_tree_clean'],
        'original_verifier_agent_field_preserved': report['agent'],
        'unmodified_verifier_sha256': launch['unmodified_verifier_sha256'],
        'canonical_report_sha256': sha(report_path),
        'registry_sha256': sha(registry_path),
        'source_linkage_sha256': sha(replay / 'source-linkage.json'),
        'compiled_modules': 11, 'commands_checked': len(commands),
        'nonobject_inventory_files_checked': len(inventory),
        'all_original_published_sources_match_compiled_snapshots': True,
        'author_object_files_reused': False,
        'full_module_origin_theorem_count': len(declarations),
        'theorems_by_module': dict(by_module),
        'axiom_union': sorted(axiom_union),
        'public_endpoints': {endpoint: theorem_data[endpoint] for endpoint in endpoints},
        'lean_worker_count': 1,
        'canonical_elapsed_seconds': launch['canonical_elapsed_seconds'],
        'source_snapshot_and_logs': str(canonical),
        'initial_parser_format_failure_retained': 'parser-attempt-001/; 94 axiom lists wrapped across lines, fixed in reviewer postprocessor only; canonical verifier and receipt unchanged.',
        'scope_limit': 'This witness closure establishes a concrete depth-12 realization and a lower bound on any uniform family bound. The separate 620 upper-bound closure is not imported here.',
    }
    path = args.output.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({key: summary[key] for key in [
        'status', 'compiled_modules', 'commands_checked', 'full_module_origin_theorem_count',
        'theorems_by_module', 'axiom_union', 'canonical_report_sha256']}, indent=2))


if __name__ == '__main__':
    main()
