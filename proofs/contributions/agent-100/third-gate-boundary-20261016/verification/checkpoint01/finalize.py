#!/usr/bin/env python3
"""Package an already completed third-gate build; this script never invokes Lean."""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
PROJECT = 'third-gate-boundary'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-output', type=Path, required=True)
    args = parser.parse_args()
    out = args.build_output.resolve()
    root = Path(subprocess.check_output(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip())
    registry = json.loads((HERE / 'registry.json').read_text())
    report = json.loads((out / 'verification.json').read_text())
    invocation = json.loads((out / 'agent100-replay-invocation.json').read_text())
    publication = json.loads((HERE / 'publication-provenance.json').read_text())
    project = report['projects'][PROJECT]
    assert report['status'] == project['status'] == 'PASS'
    assert invocation['exit_code'] == 0 and invocation['check_only'] is False
    assert report['registry_sha256'] == sha((HERE / 'registry.json').read_bytes())
    modules = registry['projects'][PROJECT]['modules']
    assert len(modules) == 12 and 'Agent100GroupIIDefect' not in modules
    assert len(project['commands']) == 13 and all(x['exit_code'] == 0 for x in project['commands'])
    for name, pin in modules.items():
        original = (root / pin['path']).read_bytes()
        staged = (out / PROJECT / 'source' / (name + '.lean')).read_bytes()
        assert original == staged and sha(original) == pin['sha256'], name
        assert hashlib.sha1(f'blob {len(original)}\0'.encode() + original).hexdigest() == pin['git_blob'], name
    audit = (out / PROJECT / 'logs/ProjectAudit.log').read_text()
    constants = {}
    for module, name, raw in re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$', audit, re.M):
        axioms = [x.strip() for x in raw.split(',') if x.strip()]
        assert set(axioms) <= ALLOWED and name not in constants
        constants[name] = {'module': module, 'axioms': axioms}
    assert len(constants) == project['theorem_count']
    all_names = [endpoint for c in registry['claims'] for endpoint in c['endpoints']]
    assert len(all_names) == len(set(all_names)) == 73
    assert set(all_names) <= set(constants)
    inventory = json.loads((HERE / 'statement-inventory.json').read_text())
    new_names = [s['name'] for rec in inventory['modules'].values() for s in rec['statements']]
    assert len(new_names) == 28 and set(new_names) <= set(all_names)
    named = {name: constants[name] for name in new_names}
    write_json('named-endpoint-axioms.json', named)
    write_json('inherited-endpoint-axioms.json', {name: constants[name] for name in all_names if name not in named})
    history = []
    contribution = HERE.parent.parent
    for path in sorted((contribution / 'development').rglob('*')):
        if not path.is_file() or path.suffix not in ['.lean', '.log', '.json']:
            continue
        raw = path.read_bytes()
        rec = {'path': str(path.relative_to(root)), 'bytes': len(raw), 'sha256': sha(raw),
               'classification': 'HISTORICAL_DEVELOPMENT_EXCLUDED_FROM_ACCEPTED_VALIDATION'}
        if path.suffix == '.log':
            errors = [line for line in raw.decode(errors='replace').splitlines() if 'error:' in line]
            rec['observed_error_lines'] = errors
            rec['observed_error_line_count'] = len(errors)
        history.append(rec)
    write_json('history-exclusions.json', {'policy': 'All failed attempts and all author self-checks are historical records, excluded from accepted independent clean-build validation.', 'files': history})
    per_module = dict(Counter(c['module'] for c in constants.values()))
    union = sorted({ax for c in constants.values() for ax in c['axioms']})
    new_union = sorted({ax for c in named.values() for ax in c['axioms']})
    controls = {n: c for n, c in named.items() if c['module'] == 'Agent100ThirdGateControls'}
    assert len(controls) == 8
    controls_empty = sum(not c['axioms'] for c in controls.values())
    assert controls_empty == 6
    result = {
        'executor': 'Agent #100 runtime_setup independent child',
        'source_authors': {'Agent100ThirdGateBoundary': 'Agent #100 groupii_dynamics child', 'Agent100ThirdGateNumeric': 'Agent #100 parent', 'Agent100ThirdGateControls': 'Agent #100 groupii_dynamics child'},
        'status': 'PASS', 'claim_commit': registry['claim_commit'], 'claim_blob': registry['claim_blob'],
        'published_source_commit': publication['published_source_commit'],
        'publication_provenance': 'publication-provenance.json: parent remote readback confirmation plus independent matching local Git object bytes.',
        'source_worktree_baseline_commit': report['source_commit'],
        'head_at_postbuild_byte_check': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'source_provenance_note': 'Baseline records the actual worktree base at verification start. New source identities are exact SHA256/Git blob pins and archived bytes, not an assertion that the baseline commit contained them. Parent separately records publication commits.',
        'source_pins': {n: modules[n] for n in inventory['modules']},
        'registry_sha256': sha((HERE / 'registry.json').read_bytes()),
        'fresh_modules': project['build_order'], 'fresh_output_directory': str(out),
        'reused_previous_oleans': False, 'full_clean_build_count': 1,
        'new_named_exports_checked': 28, 'new_named_exports_by_module': {n: x['theorem_count'] for n,x in inventory['modules'].items()},
        'inherited_named_exports_checked': 45, 'all_named_exports_checked': 73,
        'named_export_axiom_union': new_union, 'theorem_constants_audited': len(constants),
        'per_module_constants_including_auxiliaries': per_module, 'full_closure_axiom_union': union,
        'unsafe_implementation_axioms': project['unsafe_implementation_axioms'],
        'unsafe_implementation_note': 'Unsafe implementation symbols are inventoried separately. Every theorem collectAxioms result passed the three foundational axioms allow-list.',
        'controls_exports_with_no_axioms': controls_empty,
        'controls_other_exports_axioms': {n: c['axioms'] for n,c in controls.items() if c['axioms']},
        'theorem_count_scope': 'Includes generated auxiliary theorem constants and all selected dependency modules; not a count of independent mathematical discoveries.',
        'command_exit_codes': {x['label']: x['exit_code'] for x in project['commands']},
        'compiler': report['compiler'], 'source_unchanged_after_build': True,
        'verification_report_sha256': sha((out / 'verification.json').read_bytes()),
        'invocation_receipt_sha256': sha((out / 'agent100-replay-invocation.json').read_bytes()),
        'original_verifier_identity_note': 'Unchanged original verifier report says Agent #1; the invocation receipt and this result identify the actual Agent #100 runtime_setup executor.',
        'repository_wide_pass': False, 'statement_review': 'All 28 new signatures reviewed: actual finite-width time-six outer mismatch 14/15, shortest spacer included, universal ordinary realizations, threshold counterexamples and width-two realization. No time-five/six nonpalindrome or infinite conclusion.',
        'historical_development_files_preserved_but_excluded': len(history),
        'accepted_validation_excludes': ['failed author development attempts', 'successful author self-checks as a substitute for independent validation', 'all cached oleans', 'independent control-agent finite Python checks as a substitute for Lean proof', 'time-five/six nonpalindrome or infinite renewal/Lychrel/196 claims'],
        'remote_actions': False,
    }
    write_json('preparation-status.json', {'status': 'COMPLETED_INDEPENDENT_FRESH_BUILD_PASS', 'final_module_count': 12, 'roots': project['roots'], 'new_named_exports': 28, 'compiler_executed': True, 'accepted_validation': 'Scoped third-gate checkpoint only'})
    entries = {}
    for path in sorted(out.rglob('*')):
        if path.is_file() and (path.suffix in ['.json', '.lean', '.log']):
            entries['build/' + str(path.relative_to(out))] = path.read_bytes()
    for name in ['registry.json', 'replay.py', 'prepare.py', 'finalize.py', 'statement-inventory.json', 'statement-review.md', 'named-endpoint-axioms.json', 'inherited-endpoint-axioms.json', 'history-exclusions.json', 'preparation-status.json', 'portable-replay-check.json', 'publication-provenance.json', 'README.md']:
        entries['harness/' + name] = (HERE / name).read_bytes()
    old = root / 'proofs/contributions/agent-100/groupII-overlap-20261016/verification'
    for relative in ['dependencies/replay.py', 'dependencies/source-pins.json', 'dependencies/registry.json', 'checkpoint02/registry.json']:
        entries['inherited-harness/' + relative] = (old / relative).read_bytes()
    entries['harness/upstream-verifier.py'] = (root / 'proofs/verify_project__214bf7673efe116b.py').read_bytes()
    for rec in history:
        entries['history-excluded/' + str(Path(rec['path']).relative_to(contribution.relative_to(root)))] = (root / rec['path']).read_bytes()
    archive = HERE / 'evidence.tar.xz'
    with tarfile.open(archive, 'w:xz') as tar:
        for name, raw in sorted(entries.items()):
            info = tarfile.TarInfo(name)
            info.size = len(raw)
            info.mtime = 0
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(raw))
    with tarfile.open(archive, 'r:xz') as tar:
        assert len(tar.getmembers()) == len(entries)
        for member in tar.getmembers():
            assert member.isfile() and not Path(member.name).is_absolute() and '..' not in Path(member.name).parts
            assert tar.extractfile(member).read() == entries[member.name]
    archive_sha = sha(archive.read_bytes())
    write_json('evidence-manifest.json', {'archive': archive.name, 'sha256': archive_sha, 'bytes': archive.stat().st_size, 'member_count': len(entries), 'archive_readback_all_bytes_match': True, 'files': {n: {'bytes':len(b),'sha256':sha(b)} for n,b in sorted(entries.items())}, 'outside_archive': ['result.json', 'evidence-manifest.json'], 'note': 'Binary oleans are intentionally omitted; exact source and logs are preserved. Replay is from the matching Git checkout, with compiler path supplied by caller.'})
    result.update({'archive': archive.name, 'archive_sha256': archive_sha, 'archive_members': len(entries), 'archive_bytes': archive.stat().st_size})
    write_json('result.json', result)
    print(json.dumps({'status': 'PASS', 'theorem_constants':len(constants), 'new_exports':28, 'all_exports':73, 'unsafe_inventory':len(project['unsafe_implementation_axioms']), 'axioms':union, 'archive_sha256':archive_sha, 'archive_members':len(entries), 'archive_bytes':archive.stat().st_size}, indent=2))

if __name__ == '__main__':
    main()
