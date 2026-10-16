#!/usr/bin/env python3
"""Read published candidate blobs and connect two completed, separate receipts.

This script does not invoke Lean or a solver. The upper-bound execution remains
attributed to runtime_scout, and the witness execution to strategy_review.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys


COMMIT = '8f254e9b43bb319a6c43b208cd181ffc005153ec'
UPPER_COMMIT = 'dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4'
CONTRIBUTION = 'proofs/contributions/agent-104/620-depth12-witness-20261016'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--git-source', type=Path, required=True)
    parser.add_argument('--upper-evidence', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    independent = Path(__file__).resolve().parent
    contribution = independent.parent
    repository = contribution.parents[3]
    registry_path = independent / 'Agent104620Witness.registry.json'
    registry = json.loads(registry_path.read_text())
    modules = registry['projects']['agent104_620_witness']['modules']
    lower_path = independent / 'lean-replay-001/canonical/verification.json'
    lower = json.loads(lower_path.read_text())
    require(lower['status'] == 'PASS' and lower['source_commit'] == COMMIT,
            'completed witness report at published source')
    require(sha(lower_path) == 'e55bd3eda8af6a5c51c4627b3026b005adabbf947648abaa7169567fccdf5468',
            'original witness report must be unchanged')
    related = ['search_bounded.py', 'run_sweep.py',
               'search/sweep-001/width11/result.json',
               'search/sweep-001/width11/query.smt2',
               'search/sweep-001/width11/model.txt',
               'development/attempt-001/verification.json',
               'development/attempt-001/Agent104620Witness.lean',
               'development/attempt-001/compile.log']
    paths = ['proofs/Agent104620Witness.lean'] + [CONTRIBUTION + '/' + p for p in related]
    request = ''.join(COMMIT + ':' + p + '\n' for p in paths).encode()
    command = ['git', '-C', str(args.git_source.resolve()), 'cat-file', '--batch']
    completed = subprocess.run(command, input=request, capture_output=True, check=True)
    stream = io.BytesIO(completed.stdout)
    links = {}
    for path in paths:
        header = stream.readline().decode().strip().split()
        require(len(header) == 3 and header[1] == 'blob', ('published blob', path, header))
        blob, _, length = header
        data = stream.read(int(length))
        require(stream.read(1) == b'\n', 'Git batch delimiter')
        require(data == (repository / path).read_bytes(), ('actual published bytes', path))
        require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blob,
                ('published blob identity', path))
        links[path] = {'git_blob': blob, 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(), 'source_ref': COMMIT}
    require(stream.read() == b'', 'Git batch fully consumed')
    upper_directory = args.upper_evidence.resolve()
    upper_path = upper_directory / 'canonical/verification.json'
    upper = json.loads(upper_path.read_text())
    upper_project = upper['projects']['agent104-prefix620-kernel']
    outer_path = upper_directory / 'build.json'
    outer = json.loads(outer_path.read_text())
    upper_links_path = upper_directory / 'SOURCE_SNAPSHOT_LINKAGE.json'
    upper_links = json.loads(upper_links_path.read_text())
    require(upper['status'] == upper_project['status'] == 'PASS', 'upper canonical PASS')
    require(outer['status'] == 'PASS_CANONICAL_SELECTED_620_CLOSURE', 'upper outer PASS')
    require(outer['selected_source_commit'] == outer['published_source']['commit'] == UPPER_COMMIT,
            'upper actual published source linkage')
    require(sha(upper_path) == outer['canonical']['report_sha256'] ==
            '52992057d5f3051a6db6413ed724375e06f903ef8ea78a145ef23693f2edba30', 'upper raw receipt')
    commands = upper_project['commands']
    require(len(upper_project['sources']) == outer['compiled_module_count'] == 523,
            'upper compiled module count')
    require(len(commands) == 524 and all(c['exit_code'] == 0 for c in commands), 'upper commands')
    audit_path = upper_directory / 'canonical' / commands[-1]['log']
    require(sha(audit_path) == commands[-1]['log_sha256'], 'upper retained audit log')
    audit = audit_path.read_text()
    headers = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) :', audit, re.M)
    declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$', audit, re.M)
    require([(m, n) for m, n, _ in declarations] == headers and
            len(headers) == upper_project['theorem_count'] == 3047,
            'upper audit headers and bracketed axiom lists')
    axioms = {a.strip() for _, _, names in declarations for a in names.split(',') if a.strip()}
    require(axioms == {'Classical.choice', 'Quot.sound', 'propext'}, 'upper theorem axiom union')
    shared = {}
    for name, entry in modules.items():
        if name == 'Agent104620Witness':
            continue
        upper_entry = upper_links['modules'][name]
        compiled = upper_project['sources'][name]
        require(entry['sha256'] == upper_entry['sha256'] == upper_entry['canonical_inventory_sha256'] ==
                compiled['sha256'] == compiled['build_sha256'], ('shared compiled source', name))
        require(entry['git_blob'] == upper_entry['git_blob'], ('shared source Git identity', name))
        shared[name] = {'sha256': entry['sha256'], 'git_blob': entry['git_blob']}
    require(len(shared) == 10, 'ten shared dependency modules')
    require(set(upper_project['endpoints']) <= {n for _, n, _ in declarations}, 'upper endpoints audited')
    report = {
        'schema_version': 1, 'status': 'PASS_PUBLISHED_WITNESS_AND_SEPARATE_UPPER_RECEIPT_LINKAGE',
        'reviewer': '/root/strategy_review',
        'relationship': 'Non-author reviewer within the same session and shared GitHub account; not external peer review.',
        'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'command': sys.argv,
        'checker_sha256': sha(Path(__file__)),
        'published_witness_commit': COMMIT,
        'published_witness_tree': '3462705b99963f53dc92136a803645f20cf9d989',
        'published_candidate_blobs_actually_read': links,
        'published_blob_read_command': command,
        'published_blob_read_stdin_utf8': request.decode(),
        'published_blob_stdout_sha256': hashlib.sha256(completed.stdout).hexdigest(),
        'witness_modules': modules, 'witness_registry_sha256': sha(registry_path),
        'witness_canonical_report_sha256': sha(lower_path),
        'witness_source_linkage_sha256': sha(independent / 'lean-replay-001/source-linkage.json'),
        'witness_semantic_endpoints': registry['claims'][0]['endpoints'],
        'witness_integer_report_sha256': sha(independent / 'replay-001/verification.json'),
        'witness_review_summary_sha256': sha(independent / 'independent-review-summary.json'),
        'ten_shared_dependencies_byte_identical': shared,
        'separate_upper_bound': {
            'executor': '/root/runtime_scout', 'executed_by_this_link_checker': False,
            'published_source_commit': UPPER_COMMIT, 'pull_request': 135,
            'canonical_report_sha256': sha(upper_path), 'outer_build_report_sha256': sha(outer_path),
            'source_snapshot_linkage_sha256': sha(upper_links_path),
            'audit_log_sha256': sha(audit_path), 'compiled_modules': 523, 'commands': 524,
            'theorems': 3047, 'theorem_axiom_union': sorted(axioms),
            'raw_legacy_source_commit_preserved': upper['source_commit'],
            'raw_legacy_source_tree_clean_preserved': upper['source_tree_clean'],
            'actual_source_is_given_by_outer_published_source_and_each_module_record': True,
            'root': upper_links['modules']['Agent104Prefix620'],
            'audited_endpoints': upper_project['endpoints'],
        },
        'semantic_connection': 'Both endpoints use the unchanged PalStarts3 6 2 0 predicate and ordinary orbit. The upper theorem gives 12 as a uniform bound; the concrete witness makes every such bound at least 12.',
        'additional_lean_builds_started': 0,
        'cross_project_composition_theorem_added': False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    require(not args.output.exists(), 'output must be new')
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'published_candidate_blobs_checked': len(links),
                      'shared_dependencies': len(shared), 'upper_audit_theorems_read': len(headers),
                      'output_sha256': sha(args.output)}, indent=2))


if __name__ == '__main__':
    main()
