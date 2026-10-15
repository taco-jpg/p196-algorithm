#!/usr/bin/env python3
"""Verify the actual downloaded hosted artifact and preserve its substantive bytes.

This does not execute Lean. The original 16-file preflight is left unchanged.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path('/workspace/scratch/7649db1e242c')
REPO = ROOT / 'p196-weights104'
EXEC = REPO / 'proofs/contributions/agent-104/review-agent13-real-weights/execution'
INPUT = ROOT / 'agent104-independent-real-weights-38700059129-1'
ZIP = INPUT.with_suffix('.zip')
DEST = EXEC / 'hosted-38700059129-1'
SOURCE = '122367d4935f0b4cd9e0bee19e4121ec66b3164b'
REVIEW = '39d9f3eb196aae5071b5c48e8a5166dad388ce9d'
FIXTURE = 'ab6768ef000358b5f81c6807db674dc7515819c9'
ZIP_SHA = 'b7e69c40b55ac87bb7580b33df2524b1327995d8e1b9057ace339c3a80985556'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
MODULES = ['LychrelDigitSums', 'Family', 'TargetSafety', 'Counting', 'Weights', 'SqrtBound']
EXPORTS = ['predecessor_le', 'mem_safeFiber_iff', 'full_safe_fiber_finite', 'incoming_nonneg',
           'family_sum_le_incoming', 'finite_family_weight_lower', 'incoming_weight_lower',
           'incoming_weight_ratio', 'no_uniform_multiplier', 'not_exists_uniform_bound',
           'target_size_bound_nat', 'target_size_bound_real', 'family_size_scaled_power',
           'sqrt_scale_lt_family_size', 'incoming_weight_sqrt_lower']


def sha(p):
    with Path(p).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def data(p):
    return json.loads(Path(p).read_text())


def write(p, value):
    Path(p).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def git(commit, path):
    return subprocess.check_output(['git', '-C', str(REPO), 'show', commit + ':' + path])


def check_manifest(base, manifest_name):
    manifest = data(base / manifest_name)
    actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
    assert actual == set(manifest['files']) | {manifest_name}
    for name, expected in manifest['files'].items():
        p = base / name
        assert p.stat().st_size == expected['bytes'] and sha(p) == expected['sha256'], name
    return manifest


def main():
    assert not DEST.exists(), 'Hosted publication already exists; do not overwrite frozen evidence'
    preflight = data(EXEC / 'preflight-manifest.json')
    for name, expected in preflight['files'].items():
        p = EXEC / name
        assert p.stat().st_size == expected['bytes'] and sha(p) == expected['sha256'], name
    assert ZIP.stat().st_size == 5786209 and sha(ZIP) == ZIP_SHA
    actual = {str(p.relative_to(INPUT)) for p in INPUT.rglob('*') if p.is_file()}
    with zipfile.ZipFile(ZIP) as archive:
        members = [i for i in archive.infolist() if not i.is_dir()]
        assert len(members) == len({i.filename for i in members}) == 56
        assert {i.filename for i in members} == actual
        for info in members:
            assert archive.read(info) == (INPUT / info.filename).read_bytes(), info.filename
    outer = check_manifest(INPUT, 'hosted-artifact-inventory.json')
    audit = INPUT / 'independent-audit'
    inner = check_manifest(audit, 'artifact-inventory.json')
    assert outer['review_commit'] == REVIEW and outer['source_commit'] == SOURCE
    assert outer['run_id'] == '38700059129' and outer['run_attempt'] == '1'
    assert outer['checker_status'] == inner['status'] == 'PASS'
    r = data(audit / 'verification.json')
    assert r['status'] == 'PASS' and r['source_commit'] == SOURCE and r['review_commit'] == REVIEW
    assert r['hosted_run']['GITHUB_RUN_ID'] == '38700059129'
    assert r['hosted_run']['GITHUB_RUN_ATTEMPT'] == '1'
    assert r['hosted_run']['GITHUB_SHA'] == REVIEW
    assert r['hosted_run']['GITHUB_REF'] == 'refs/heads/research/agent-104/20261015-real-weights-review'
    assert r['fresh_source_rebuild'] and not r['prior_local_objects_reused']
    assert r['snapshot_initial_object_count'] == 0 and r['snapshot_complete_before_build']
    assert r['local_modules'] == MODULES and set(r['sources']) == set(MODULES)
    assert r['build_workers'] == 1 and r['source_object_compiler_log_stability_checked']
    assert r['compiled_mathlib_cache_reused'] and not r['mathlib_source_rebuild']
    control_paths = {'check.py': 'execution/check.py', 'source-pins.json': 'execution/source-pins.json',
                     'ExactTypes.lean': 'semantic/ExactTypes.lean'}
    review_base = 'proofs/contributions/agent-104/review-agent13-real-weights/'
    for name, rel in control_paths.items():
        assert (audit / 'controls' / name).read_bytes() == git(REVIEW, review_base + rel)
    assert (audit / 'controls/agent104-real-weights-review.yml').read_bytes() == git(REVIEW, '.github/workflows/agent104-real-weights-review.yml')
    pins = data(audit / 'controls/source-pins.json')
    assert pins == data(EXEC / 'source-pins.json') and pins['source_commit'] == SOURCE
    for module, rec in r['sources'].items():
        pin = pins['modules'][module]
        for field in ['path', 'bytes', 'sha256']:
            assert rec[field] == pin[field], (module, field)
        blob = git(SOURCE, rec['path'])
        assert blob == (audit / rec['snapshot']).read_bytes()
        assert blob == (audit / 'original-sources' / rec['path']).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == rec['sha256'] and len(blob) == rec['bytes']
        assert hashlib.sha1(f'blob {len(blob)}\0'.encode() + blob).hexdigest() == rec['git_blob_sha1']
        assert sha(audit / 'project' / (module + '.olean')) == rec['object_sha256']
    assert (audit / 'original-sources/author-check.py').read_bytes() == git(SOURCE, pins['author_checker']['path'])
    assert sha(audit / 'original-sources/author-check.py') == pins['author_checker']['sha256']
    exact = (audit / 'controls/ExactTypes.lean').read_bytes()
    assert exact == git(FIXTURE, review_base + 'semantic/ExactTypes.lean')
    assert exact == (audit / 'project/ExactTypes.lean').read_bytes()
    assert hashlib.sha256(exact).hexdigest() == r['exact_types_sha256'] == '79ff0637667b95ff4b411a6c9ce57880c325769b39fb44285de9fa4e2563200c'
    assert r['exact_types_original_fixture_commit'] == FIXTURE
    compiler = r['compiler']
    assert compiler['archive_sha256'] == '6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe'
    assert compiler['sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
    assert compiler['version'] == 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
    official = data(audit / 'official-archive-members.json')
    assert len(official) == compiler['independently_compared_archive_members'] == 1477
    assert official[compiler['path']] == compiler['sha256']
    collector_path = compiler['prefix'] + '/src/lean/Lean/Util/CollectAxioms.lean'
    assert sha(audit / 'controls/Lean-CollectAxioms.lean') == official[collector_path]
    assert (audit / 'controls/Lean-CollectAxioms.lean').read_bytes() == (ROOT / 'toolchain/lean-4.19.0-linux/src/lean/Lean/Util/CollectAxioms.lean').read_bytes()
    manifest = data(audit / 'mathlib-lake-manifest.json')
    assert sha(audit / 'mathlib-lake-manifest.json') == r['library']['manifest_sha256'] == '5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752'
    assert r['library']['mathlib_commit'] == 'c44e0c8ee63ca166450922a373c7409c5d26b00b'
    packages = {p['name']: p['rev'] for p in manifest['packages']}
    assert packages == r['library']['dependency_commits']
    before = data(audit / 'dependency-object-pins-before.json')
    log = (audit / 'logs/AllCompiledAxioms.log').read_text()
    import_rows = re.findall(r'^AUDIT_IMPORT (\S+) (.+)$', log, re.MULTILINE)
    imported = dict(import_rows)
    assert len(imported) == len(import_rows) and set(imported) == set(r['imported_objects'])
    for module, rec in r['imported_objects'].items():
        assert imported[module] == rec['path']
        if rec['origin'] == 'fresh local source build':
            assert module in [*MODULES, 'ExactTypes']
            obj = audit / 'project' / (module + '.olean')
            assert sha(obj) == rec['sha256'] and obj.stat().st_size == rec['bytes']
        else:
            assert before[rec['path']] == rec['sha256']
            if rec['origin'] == 'verified official Lean archive':
                assert official[rec['path']] == rec['sha256']
            else:
                assert rec['origin'] == 'explicit pinned Mathlib/dependency compiled cache'
                assert rec['source_path'] == module.replace('.', '/') + '.lean'
                assert re.fullmatch('[a-f0-9]{64}', rec['source_sha256'])
                path = rec['path']
                package = re.search(r'/\.lake/packages/([^/]+)/', path)
                expected_commit = packages[package[1]] if package else r['library']['mathlib_commit']
                assert rec['source_commit'] == expected_commit
    commands = r['commands']
    assert len({c['label'] for c in commands}) == len(commands) == 19
    for command in commands:
        assert command['exit_code'] == 0
        assert sha(audit / command['log']) == command['log_sha256']
    for module in [*MODULES, 'ExactTypes']:
        command = next(c for c in commands if c['label'] == module)
        assert command['command'] == [compiler['path'], '-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean']
    audit_command = next(c for c in commands if c['label'] == 'AllCompiledAxioms')
    assert audit_command['command'] == [compiler['path'], '-j1', '-DElab.async=false', 'AllCompiledAxioms.lean']
    assert sha(audit / 'project/AllCompiledAxioms.lean') == r['audit_source_sha256']
    declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$', log, re.MULTILINE)
    declared = {name: module for module, name in declarations}
    assert len(declared) == len(declarations) == r['theorem_count'] == 1144
    printed = {}
    reports = [(n, sorted(a.strip() for a in axes.split(',') if a.strip())) for n, axes in
               re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)]
    reports += [(n, []) for n in re.findall(r"'([^']+)' does not depend on any axioms", log)]
    for name, axioms in reports:
        assert name not in printed and set(axioms) <= ALLOWED, (name, axioms)
        printed[name] = axioms
    assert set(printed) == set(declared) == set(r['theorems'])
    for name in printed:
        assert r['theorems'][name] == {'module': declared[name], 'axioms': printed[name]}
    assert dict(Counter(declared.values())) == r['theorems_per_module']
    unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', log, re.MULTILINE)
    assert [list(x) for x in unsafe] == r['unsafe_implementation_axioms']
    assert len(unsafe) == 13 and not {n for _, n in unsafe}.intersection(a for axes in printed.values() for a in axes)
    expected_exports = {'Agent13SafeWeights.' + n for n in EXPORTS}
    for name in EXPORTS:
        assert declared['Agent13SafeWeights.' + name] in ['Weights', 'SqrtBound']
        assert declared['Agent104.RealWeightsExactTypes.' + name + '_type'] == 'ExactTypes'
    types = re.findall(r'^AUDIT_EXPORT_TYPE (\S+)\n(.*?)\nAUDIT_EXPORT_RAW_TYPE \1\n', log, re.MULTILINE | re.DOTALL)
    raw_names = re.findall(r'^AUDIT_EXPORT_RAW_TYPE (\S+)$', log, re.MULTILINE)
    assert len(types) == len(raw_names) == 15
    assert {n for n, _ in types} == set(raw_names) == expected_exports
    assert set(r['export_axioms']) == expected_exports
    assert not re.search(r'(^|\n).*\berror:', log)
    exclusions = {}
    for module in [*MODULES, 'ExactTypes']:
        source_name = 'independent-audit/project/' + module + '.lean'
        retained = ('independent-audit/controls/ExactTypes.lean' if module == 'ExactTypes'
                    else 'independent-audit/original-sources/' + r['sources'][module]['path'])
        assert (INPUT / source_name).read_bytes() == (INPUT / retained).read_bytes()
        exclusions[source_name] = {'bytes': (INPUT / source_name).stat().st_size, 'sha256': sha(INPUT / source_name),
            'reason': 'Duplicate source bytes; exact original source is retained.', 'recovery': {'kind': 'copy_retained', 'path': retained}}
        object_name = 'independent-audit/project/' + module + '.olean'
        exclusions[object_name] = {'bytes': (INPUT / object_name).stat().st_size, 'sha256': sha(INPUT / object_name),
            'reason': 'Newly compiled object is reproducible build infrastructure; source, command and exact object pin are retained.',
            'recovery': {'kind': 'verified_original_zip_member', 'member': object_name, 'zip_sha256': ZIP_SHA,
                         'rebuild_command': next(c['command'] for c in commands if c['label'] == module)}}
    DEST.mkdir()
    for name in sorted(actual - set(exclusions)):
        target = DEST / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(INPUT / name, target)
        assert sha(target) == sha(INPUT / name)
    write(EXEC / 'artifact-selection.json', {
        'run_id': '38700059129', 'attempt': 1, 'artifact_id': '11955822178', 'zip_bytes': ZIP.stat().st_size,
        'zip_sha256': ZIP_SHA, 'original_file_count': len(actual), 'retained_file_count': len(actual - set(exclusions)),
        'retained_bytes': sum((INPUT / n).stat().st_size for n in actual - set(exclusions)),
        'retained_raw_prefix': DEST.name, 'excluded': exclusions,
        'recovery_command': 'python recover_hosted.py --output /new/empty/recovered --zip /path/to/agent104-independent-real-weights-38700059129-1.zip',
        'source_only_recovery_command': 'python recover_hosted.py --output /new/empty/recovered',
        'all_substantive_logs_preserved_byte_for_byte': True,
        'zip_not_republished': 'The ZIP duplicates retained evidence and excluded reproducible objects; its published hash, byte count, artifact identity and complete member inventories are preserved.'})
    write(EXEC / 'export-types.json', dict(sorted(types)))
    result = {
        'status': 'PASS', 'independent_hosted_execution_verified': True, 'local_real_weight_execution_claimed': False,
        'run_id': '38700059129', 'run_attempt': 1, 'job_id': '116305811381', 'artifact_id': '11955822178',
        'review_commit': REVIEW, 'source_commit': SOURCE, 'source_tree': r['source_tree'], 'fixture_commit': FIXTURE,
        'zip_sha256': ZIP_SHA, 'zip_bytes': ZIP.stat().st_size, 'zip_members_equal_extracted_files': True,
        'all_inner_and_outer_manifest_hashes_verified': True, 'original_artifact_file_count': len(actual),
        'all_19_recorded_commands_exit_zero': True, 'fresh_original_source_module_count': 6,
        'fresh_exact_type_module_count': 1, 'local_object_count': 7,
        'contribution_closure_theorem_count': 1129, 'exact_type_theorem_count': 15, 'total_audited_theorem_count': 1144,
        'private_name_theorem_count': sum(n.startswith('_private') for n in declared),
        'theorems_per_module': r['theorems_per_module'],
        'axiom_set_counts': dict(Counter(';'.join(a) or '(none)' for a in printed.values())),
        'allowed_axioms': sorted(ALLOWED), 'unsafe_implementation_axiom_count': 13,
        'unsafe_implementation_axioms_in_accepted_dependencies': [], 'all_15_exact_types_and_raw_expressions_present': True,
        'compiler': compiler, 'library': r['library'], 'mathlib_source_rebuild_claimed': False,
        'imported_object_counts': dict(Counter(x['origin'] for x in r['imported_objects'].values())),
        'imported_cache_hashes_matched_prebuild_pins': True, 'imported_cache_source_commit_and_hash_records_checked': True,
        'external_cache_bytes_retained_locally': False,
        'checker_report_sha256': sha(audit / 'verification.json'), 'full_axiom_log_sha256': sha(audit / 'logs/AllCompiledAxioms.log'),
        'checker_started_at_utc': r['started_at_utc'], 'checker_finished_at_utc': r['finished_at_utc'],
        'audit_seconds': audit_command['seconds'],
        'preflight_files_unchanged': True, 'additional_Lean_execution_during_acceptance': False,
        'scope': 'All 15 original real-weight exports are accepted with their stated positive/antitone safe-weight hypotheses and width conditions. This is an obstruction to a global incoming-weight bound, not a proof of P196 or decimal Lychrel existence.'}
    write(EXEC / 'acceptance.json', result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
