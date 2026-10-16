#!/usr/bin/env python3
"""Validate existing canonical evidence and prepare publication metadata only."""
from datetime import datetime, timezone
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[3]
VERIFY = PACKAGE / 'verification'
CANON = VERIFY / 'canonical-001'
PROJECT = 'agent7-odd-nooverflow-fibers'
REPORT_SHA = '73b2589136626623121f50bafff87986b89e6bbf2b08399503edcb1422d76e64'
REGISTRY_SHA = 'ca9d1fa657f6fc786fa14ed0df2456333280ee8a5eb1a58cadeebb902ff16926'
VERIFIER_SHA = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
SOURCE_COMMIT = 'af9ddce989030508e9fc2895f2f44fbbfcf2aed9'
CLEANUP_SHA = '78f16a0ea0de44ad0b7b35475f686b409484d271c93bcfeef6f4ee586c753136'
ALLOWED = ['propext', 'Classical.choice', 'Quot.sound']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def entry(path):
    return {'path': path.relative_to(PACKAGE).as_posix(),
            'bytes': path.stat().st_size, 'sha256': sha(path)}

def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    report_path = CANON / 'verification.json'
    registry_path = PACKAGE / 'PROJECT_REGISTRY.json'
    verifier_path = REPO / 'proofs/verify_project__214bf7673efe116b.py'
    assert sha(report_path) == REPORT_SHA
    assert sha(registry_path) == REGISTRY_SHA
    assert sha(verifier_path) == VERIFIER_SHA
    report = json.loads(report_path.read_text())
    registry = json.loads(registry_path.read_text())
    spec = registry['projects'][PROJECT]
    pr = report['projects'][PROJECT]
    assert report['status'] == pr['status'] == 'PASS'
    assert report['mathematical_proof_check'] and not report['repository_wide_pass']
    assert report['source_commit'] == SOURCE_COMMIT and report['source_tree_clean']
    assert report['registry_sha256'] == REGISTRY_SHA and not report['catalogue_complete']
    assert len(spec['modules']) == 15 and pr['roots'] == ['OddComplete']
    inventory = json.loads((CANON / 'FILES.json').read_text())
    for name, record in inventory.items():
        path = CANON / name
        assert path.stat().st_size == record['bytes'] and sha(path) == record['sha256']
    assert len(pr['commands']) == 16 and all(c['exit_code'] == 0 for c in pr['commands'])
    for command in pr['commands']:
        assert sha(CANON / command['log']) == command['log_sha256']
    assert set(pr['build_order']) == set(spec['modules']) and len(pr['build_order']) == 15
    snapshots = []
    for module, record in spec['modules'].items():
        original = REPO / record['path']
        snapshot = CANON / PROJECT / 'source' / (module + '.lean')
        assert original.read_bytes() == snapshot.read_bytes()
        assert sha(original) == record['sha256'] == pr['sources'][module]['sha256']
        assert record['sha256'] == pr['sources'][module]['build_sha256']
        snapshots.append((module, snapshot, original, record))
    commit_paths = [SOURCE_COMMIT + ':' + rec['path'] for rec in spec['modules'].values()]
    expected_blobs = [rec['git_blob'] for rec in spec['modules'].values()]
    for path in [registry_path, verifier_path]:
        commit_paths.append(SOURCE_COMMIT + ':' + path.relative_to(REPO).as_posix())
        data = path.read_bytes()
        expected_blobs.append(hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest())
    checked = subprocess.run(['git', 'cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)'],
        input='\n'.join(commit_paths) + '\n', text=True, capture_output=True, check=True, cwd=REPO)
    for line, expected in zip(checked.stdout.splitlines(), expected_blobs, strict=True):
        actual, kind, size = line.split()
        assert actual == expected and kind == 'blob'
    for path, digest in report['compiler']['files'].items():
        assert sha(Path(path)) == digest
    audit_path = CANON / PROJECT / 'source/ProjectAudit.lean'
    audit_log_path = CANON / PROJECT / 'logs/ProjectAudit.log'
    audit = audit_path.read_text()
    audit_log = audit_log_path.read_text()
    rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$', audit_log, re.M)
    assert len(rows) == len({name for module, name, axes in rows}) == 450 == pr['theorem_count']
    union = set()
    for module, name, axes in rows:
        assert module in spec['modules']
        axes = [a.strip() for a in axes.strip()[1:-1].split(',') if a.strip()]
        assert set(axes) <= set(ALLOWED)
        union.update(axes)
    assert union == set(ALLOWED)
    summaries = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=(.*)$', audit_log, re.M)
    assert summaries == [('450', pr['axiom_union'])]
    unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit_log, re.M)
    assert [list(pair) for pair in unsafe] == pr['unsafe_implementation_axioms']
    endpoints = [e for c in registry['claims'] if c['project'] == PROJECT for e in c['endpoints']]
    assert re.findall(r'^#check (\S+)$', audit, re.M) == endpoints == pr['endpoints']
    assert len(endpoints) == 115
    cleanup_target = VERIFY / 'cleanup/COMPILED_OBJECT_CLEANUP.json'
    cleanup_source = Path('/tmp/agent7-compiled-cleanup-20261016.json')
    if not cleanup_source.is_file():
        cleanup_source = cleanup_target
    assert sha(cleanup_source) == CLEANUP_SHA
    cleanup = json.loads(cleanup_source.read_text())
    cleanup_target.parent.mkdir(parents=True, exist_ok=True)
    if not cleanup_target.exists():
        cleanup_target.write_bytes(cleanup_source.read_bytes())
    assert sha(cleanup_target) == CLEANUP_SHA
    prefix = PACKAGE.relative_to(REPO).as_posix() + '/'
    canonical_removed = [e for e in cleanup['removed']
                         if e['path'].startswith(prefix + 'verification/canonical-001/')]
    assert len(canonical_removed) == 15 and sum(e['bytes'] for e in canonical_removed) == 6983952
    for rec in canonical_removed:
        path = REPO / rec['path']
        if path.exists():
            assert path.stat().st_size == rec['bytes'] and sha(path) == rec['sha256']
    prepared_at = datetime.now(timezone.utc).isoformat()
    validation = {
        'schema_version': 1, 'validator': 'Agent #7 /root/runtime',
        'base_path': PACKAGE.relative_to(REPO).as_posix(),
        'validation_kind': 'Read-only inspection of completed execution evidence; no Lean build rerun',
        'prepared_at_utc': prepared_at, 'status': 'PASS',
        'original_report_sha256': REPORT_SHA, 'original_report_preserved_exactly': True,
        'registry_sha256': REGISTRY_SHA, 'verifier_sha256': VERIFIER_SHA,
        'source_commit': SOURCE_COMMIT,
        'committed_source_registry_and_verifier_git_blobs_checked': len(commit_paths),
        'registered_source_snapshots_identical_to_committed_sources': 15,
        'original_FILES_entries_verified': len(inventory),
        'recorded_successful_commands_with_matching_log_hashes': 16,
        'registered_public_endpoint_checks': 115, 'module_origin_theorem_constants': 450,
        'module_origin_counts': dict(collections.Counter(module for module, name, axes in rows)),
        'allowed_axioms': ALLOWED, 'observed_unsafe_implementation_constant_count': len(unsafe),
        'cleanup_receipt_sha256': CLEANUP_SHA, 'canonical_object_hash_records': 15,
        'canonical_object_hash_basis': 'Parent cleanup receipt, matched by reviewer against its separately captured pre-deletion hashes on 2026-10-16.',
        'lean_or_registry_or_verifier_source_edits': False,
    }
    dump(VERIFY / 'EVIDENCE_VALIDATION.json', validation)
    replay = ['python3', 'proofs/verify_project__214bf7673efe116b.py',
              '--registry', registry_path.relative_to(REPO).as_posix(),
              '--project', PROJECT, '--lean', pr['commands'][0]['argv'][0],
              '--output', '/absolute/path/to/a-new-canonical-output-directory']
    commands = {
        'schema_version': 1, 'source_report': entry(report_path),
        'base_path': PACKAGE.relative_to(REPO).as_posix(),
        'compiler_commands': pr['commands'],
        'compiler_cwd': str(CANON / PROJECT / 'source'),
        'compiler_cwd_basis': 'The unchanged retained verifier executes its recorded commands with cwd set to the generated project source directory.',
        'replay_argv': replay,
        'replay_argv_status': 'Reconstructed reproducible invocation. The exact original outer shell command is not contained in the retained report.',
        'builds_rerun_for_this_receipt': False,
    }
    dump(VERIFY / 'CANONICAL_COMMANDS.json', commands)
    receipt = {
        'schema_version': 1,
        'base_path': PACKAGE.relative_to(REPO).as_posix(),
        'actual_executor': {'agent': 7, 'task_path': '/root', 'role': 'parent contribution author and canonical verifier executor'},
        'receipt_preparer': {'agent': 7, 'task_path': '/root/runtime', 'role': 'same-team cross-author reviewer; author of imported OddActual'},
        'executor_attribution_basis': 'Parent Agent #7 /root explicitly reported executing this canonical run. The preparer independently inspected its retained report, compiler commands, logs, audit source, source snapshots, registry and committed Git blobs.',
        'cross_author_affiliation': 'Both executor and reviewer belong to the same Agent #7 collaboration tree. The reviewer authored OddActual and reviewed parent-authored canonical/sharp/complete wrappers and the counting specialist output-range bridge.',
        'prepared_at_utc': prepared_at,
        'original_report': entry(report_path),
        'original_report_agent_field': report['agent'],
        'original_agent_label_explanation': 'The unchanged retained verifier initializes a historical Agent #1 label. It is preserved exactly and does not identify the actor who ran this execution.',
        'original_report_rewritten': False,
        'source_commit': SOURCE_COMMIT, 'source_tree_clean_recorded': True,
        'clean_flag_definition': 'The retained verifier checks git status --porcelain --untracked-files=no. This receipt additionally verifies that the recorded source commit contains all 15 registered source files, the registry and verifier at their exact Git blob identities.',
        'registry': entry(registry_path),
        'verifier': {'path': verifier_path.relative_to(REPO).as_posix(), 'sha256': VERIFIER_SHA},
        'status': 'PASS', 'mathematical_proof_check': True, 'repository_wide_pass': False,
        'project': PROJECT, 'roots': pr['roots'], 'scope': pr['scope'],
        'started_at_utc': datetime.fromtimestamp(report['started_at_epoch'], timezone.utc).isoformat(),
        'finished_at_utc': datetime.fromtimestamp(report['finished_at_epoch'], timezone.utc).isoformat(),
        'compiler': report['compiler'],
        'canonical_lean_flags': ['-j1', '-DElab.async=false'],
        'canonical_trust_zero_flag_passed': False,
        'modules': 15, 'public_new_module_endpoint_checks': 115, 'audited_theorem_constants': 450,
        'mathematical_axiom_union': ALLOWED,
        'unsafe_implementation_constants': pr['unsafe_implementation_axioms'],
        'unsafe_implementation_explanation': 'The audit records 13 compiler-generated unsafe implementation constants. All 450 mathematical theorem dependency traversals contain only the approved foundational axioms.',
        'commands_record': 'verification/CANONICAL_COMMANDS.json',
        'evidence_validation': 'verification/EVIDENCE_VALIDATION.json',
        'separate_reviewer_execution': {
            'path': 'actual-dev/review-sharp/final-001/verification.json',
            'sha256': '2132ab2176dec34039ca22da1f461e5136d318a54e632154ac1458bd340b6d9d',
            'executor': 'Agent #7 /root/runtime', 'flags': ['--trust=0', '-j1', '-DElab.async=false'],
            'project_modules': 15, 'project_theorem_constants': 450,
            'additional_reviewer_fixtures': 18, 'all_audited_theorem_constants': 468,
            'individual_public_axiom_audits': 214,
        },
        'cleanup_receipt': entry(cleanup_target),
        'cleanup_note': 'Parent reclaimed only hashed untracked compiler objects after disk exhaustion. Source, logs, generated audit source, reports and failed attempts are preserved. No build was rerun for this packet.',
    }
    dump(VERIFY / 'AGENT7_EXECUTION_RECEIPT.json', receipt)
    comment = f"""Review type: COMMENT.

Reviewer: Agent #7 /root/runtime, in the same collaboration tree as parent author Agent #7 /root. I authored the imported OddActual dependency and performed cross-author semantic review of the parent-authored canonical, sharpness and complete wrappers, together with a separate fresh execution of their full closure.

No blocking findings remain at source {SOURCE_COMMIT}. The final membership theorem covers every raw requested output r and is equivalent to the literal canonical odd-width, zero-final-carry source predicate. The exact reconstruction guard prevents modulo aliases; the output-range converse proves completeness of the rejected-target branch. Literal-center parity, full-word positivity at width one, duplicate freedom, the prescribed-center exception at m=0, and sharp attainment are handled correctly.

The parent canonical replay passed with the unchanged Lean 4.19.0 verifier: 15 modules, 115 public new-module endpoint checks, and 450 theorem constants audited by module origin. All theorem dependencies lie in propext, Classical.choice and Quot.sound. The retained report SHA256 is {REPORT_SHA}; its historical Agent #1 label is preserved and explained by verification/AGENT7_EXECUTION_RECEIPT.json. My separate --trust=0 run checked the same 450 project theorem constants plus 18 boundary fixtures, including malformed targets and exact arbitrary-output fibers.

The result counts distinct coefficient words for one actual reverse-add update, with sharp maximum (fib (m+1)+1)/2 at width 2*m+1. This COMMENT records the cross-author review and executed evidence; repository-wide accepted-build integration remains outside this scoped packet.
"""
    (VERIFY / 'REVIEW_COMMENT.md').write_text(comment)
    retained, omitted = [], []
    for module, snapshot, original, rec in snapshots:
        item = entry(snapshot)
        item.update(reason='Byte-identical copy of the registered source committed at the canonical execution source commit. Canonical source and both content identities remain retained.',
                    canonical_source=original.relative_to(PACKAGE).as_posix(),
                    canonical_source_commit=SOURCE_COMMIT,
                    canonical_source_git_blob=rec['git_blob'], canonical_source_sha256=rec['sha256'])
        omitted.append(item)
    omitted_paths = {e['path'] for e in omitted}
    for rec in canonical_removed:
        path = REPO / rec['path']
        source = path.with_suffix('.lean')
        item = {'path': path.relative_to(PACKAGE).as_posix(), 'bytes': rec['bytes'], 'sha256': rec['sha256'],
                'reason': 'Reproducible compiler object reclaimed by parent after exact hashing; source, command, compiler identity, logs and audit are preserved.',
                'source_snapshot': source.relative_to(PACKAGE).as_posix(), 'source_sha256': sha(source),
                'cleanup_receipt': 'verification/cleanup/COMPILED_OBJECT_CLEANUP.json'}
        omitted.append(item)
        omitted_paths.add(item['path'])
    manifest_path = VERIFY / 'PUBLICATION.json'
    for path in sorted(VERIFY.rglob('*')):
        if not path.is_file() or path == manifest_path or path.relative_to(PACKAGE).as_posix() in omitted_paths:
            continue
        item = entry(path)
        item['kind'] = 'generated_axiom_audit_source' if path.name == 'ProjectAudit.lean' else {
            '.log': 'original_compiler_or_audit_log', '.py': 'metadata_preparation_runner',
            '.md': 'suggested_formal_review_comment', '.json': 'original_or_companion_evidence_record',
        }.get(path.suffix, 'retained_evidence')
        retained.append(item)
    previous_stage = PACKAGE / 'actual-dev/STAGE_FILES.json'
    previous_paths = json.loads(previous_stage.read_text())
    assert len(previous_paths) == len(set(previous_paths)) == 101
    for path in previous_paths:
        assert (REPO / path).is_file()
    previous_manifest = json.loads((PACKAGE / 'actual-dev/PUBLICATION.json').read_text())
    for rec in previous_manifest['retained_files']:
        path = PACKAGE / rec['path']
        assert path.stat().st_size == rec['bytes'] and sha(path) == rec['sha256']
    final_stage = PACKAGE / 'FINAL_STAGE_FILES.json'
    paths = set(previous_paths)
    paths.update((PACKAGE / e['path']).relative_to(REPO).as_posix() for e in retained)
    paths.update(path.relative_to(REPO).as_posix() for path in
                 [PACKAGE / 'README.md', final_stage, manifest_path])
    dump(final_stage, sorted(paths))
    publication = {
        'schema_version': 1, 'agent': 7, 'prepared_by': '/root/runtime',
        'base_path': PACKAGE.relative_to(REPO).as_posix(),
        'scope': 'Final odd-fiber review and canonical verification publication packet',
        'source_commit': SOURCE_COMMIT, 'registry_sha256': REGISTRY_SHA,
        'original_canonical_report_sha256': REPORT_SHA,
        'original_canonical_report_and_inventory_unchanged': True,
        'retained_files': retained, 'omitted_reproducible_files': omitted,
        'previous_review_packet': {'stage_list': entry(previous_stage),
                                  'manifest': entry(PACKAGE / 'actual-dev/PUBLICATION.json'),
                                  'retained_paths_included': len(previous_paths)},
        'status_document': entry(PACKAGE / 'README.md'),
        'combined_stage_list': entry(final_stage),
        'combined_stage_count': len(paths),
        'cleanup': {'receipt': entry(cleanup_target), 'all_reclaimed_objects': len(cleanup['removed']),
                    'canonical_objects': len(canonical_removed), 'canonical_object_bytes': 6983952},
        'publication_note': 'All substantive source/log/report/audit evidence is retained. Only byte-identical committed source copies and reproducible compiler outputs are omitted. The original canonical report, FILES inventory, generated Lean audit and logs are untouched; actual executor attribution is a companion record. Parent performed the documented compiler-object cleanup. No Lean build, Lean source edit, registry/verifier edit, Git write or remote write was performed to prepare this packet.',
    }
    dump(manifest_path, publication)
    assert sha(report_path) == REPORT_SHA and sha(registry_path) == REGISTRY_SHA and sha(verifier_path) == VERIFIER_SHA
    for rec in retained:
        path = PACKAGE / rec['path']
        assert path.stat().st_size == rec['bytes'] and sha(path) == rec['sha256']
    assert all((REPO / path).is_file() for path in paths)
    print(json.dumps({'status': 'PASS', 'canonical_report_sha256': sha(report_path),
        'execution_receipt_sha256': sha(VERIFY / 'AGENT7_EXECUTION_RECEIPT.json'),
        'publication_manifest_sha256': sha(manifest_path), 'final_stage_list_sha256': sha(final_stage),
        'final_stage_count': len(paths), 'canonical_retained_count': len(retained),
        'canonical_omitted_count': len(omitted), 'cleanup_receipt_sha256': sha(cleanup_target)}, indent=2))

if __name__ == '__main__':
    main()
