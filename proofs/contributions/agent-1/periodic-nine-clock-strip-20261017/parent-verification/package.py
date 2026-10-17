#!/usr/bin/env python3
"""Package two completed parent runs without executing Lean or changing inputs."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = Path('/workspace/p196-agent1-session-20261016')
COMMIT = '26af0f094c8e55639253c99df83c44dc21959de7'
PROJECT = 'agent1-periodic-nine-clock-strip'
BAD_PROJECT = 'agent1-periodic-nine-sharp-excursion'
REGISTRY = 'proofs/Agent1PeriodicNinesSharpExcursion.registry.json'
CHECKER = 'proofs/verify_project__214bf7673efe116b.py'
LEAN = '/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
CHECK_IN = 'https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6228712115'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda p, v: p.write_text(json.dumps(v, indent=2)+'\n')
published = lambda p: subprocess.check_output(['git', 'show', COMMIT+':'+p], cwd=ROOT)

registry = (ROOT/REGISTRY).read_bytes()
checker = (ROOT/CHECKER).read_bytes()
assert registry == published(REGISTRY) and checker == published(CHECKER)
assert sha(registry) == 'c2ad34d000178a35563cb5a7f7a94ad51a8f3637cfa325a1c9c9fb0af61de7a4'
assert sha(checker) == 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
reg = json.loads(registry)
assert PROJECT in reg['projects'] and BAD_PROJECT not in reg['projects']
runs = []
for number in ['001', '002']:
    original = BASE/('nine-sharp-parent-clean-'+number)
    manifest_bytes = (original/'FILES.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    report_bytes = (original/'verification.json').read_bytes()
    report = json.loads(report_bytes)
    console_bytes = original.with_name(original.name+'.console.log').read_bytes()
    for path, entry in manifest.items():
        assert not Path(path).is_absolute() and '..' not in Path(path).parts
        assert Path(path).suffix in ['.lean', '.log', '.json', '.txt']
        raw = (original/path).read_bytes()
        assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], path
    assert report['source_commit'] == COMMIT
    assert report['registry_sha256'] == sha(registry)
    assert report['source_tree_clean'] is True
    runs.append(dict(number=number, original=original, manifest_bytes=manifest_bytes,
        manifest=manifest, report_bytes=report_bytes, report=report, console_bytes=console_bytes))

failed, passed = runs
failure = failed['report']
assert failure['status'] == 'FAIL' and failure['error'] == 'Unknown project requested'
assert failure['projects'] == {} and 'compiler' not in failure
assert set(failed['manifest']) == {'failure.txt', 'verification.json'}
assert {p.name for p in failed['original'].iterdir()} == {'failure.txt', 'verification.json', 'FILES.json'}
assert failed['console_bytes'] == b'FAIL: Unknown project requested\n'
assert 'ValueError: Unknown project requested' in (failed['original']/'failure.txt').read_text()
# Confirm that the recorded error precedes even the compiler-version invocation.
checker_text = checker.decode()
assert checker_text.index("raise ValueError('Unknown project requested')") < checker_text.index("version = subprocess.check_output([str(lean), '--version']")

report = passed['report']
assert report['status'] == 'PASS' and set(report['projects']) == {PROJECT}
project = report['projects'][PROJECT]
assert project['status'] == 'PASS'
registered = reg['projects'][PROJECT]['modules']
assert set(project['sources']) == set(project['build_order']) == set(registered)
modules = len(project['sources'])
commands = project['commands']
assert len(commands) == modules+1
assert [c['label'] for c in commands] == project['build_order']+['ProjectAudit']
for command in commands:
    assert command['exit_code'] == 0 and command['argv'][0] == LEAN
    assert '-j1' in command['argv'] and '-DElab.async=false' in command['argv']
    assert not any(arg.startswith('--trust') for arg in command['argv'])
    assert sha((passed['original']/command['log']).read_bytes()) == command['log_sha256']
assert passed['console_bytes'].decode().splitlines() == [PROJECT+' '+c['label']+' exit=0' for c in commands]
audit = (passed['original']/PROJECT/'logs/ProjectAudit.log').read_text()
rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+)\s*:\s*\[([^\]]*)\]', audit, re.M)
assert len(rows) == project['theorem_count'] and len({name for mod, name, axs in rows}) == len(rows)
assert all(mod in registered for mod, name, axs in rows)
summary = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=\[([^\]]*)\]', audit, re.M)
assert len(summary) == 1 and int(summary[0][0]) == len(rows)
union = sorted({a.strip() for mod, name, axs in rows for a in axs.split(',') if a.strip()})
assert set(union) <= {'propext', 'Classical.choice', 'Quot.sound'}
assert set(a.strip() for a in summary[0][1].split(',') if a.strip()) == set(union)
assert '['+', '.join(union)+']' == project['axiom_union']
unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit, re.M)
assert [list(row) for row in unsafe] == project['unsafe_implementation_axioms']
assert project['endpoints'] == [e for c in reg['claims'] if c['project'] == PROJECT for e in c['endpoints']]
assert re.search(r'version 4\.19\.0,.*commit 6caaee842e94, Release', report['compiler']['version'])
assert report['compiler']['files'][LEAN] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
for path, digest in report['compiler']['files'].items():
    assert sha(Path(path).read_bytes()) == digest, path

pins = []
for module, entry in project['sources'].items():
    raw = (ROOT/entry['path']).read_bytes()
    built = (passed['original']/PROJECT/'source'/(module+'.lean')).read_bytes()
    pin = registered[module]
    assert raw == built == published(entry['path'])
    assert sha(raw) == entry['sha256'] == entry['build_sha256'] == pin['sha256']
    assert entry['path'] == pin['path'] and entry['imports'] == pin['imports'] and entry['adapter'] is None
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob == pin['git_blob']
    pins.append({'module': module, 'path': entry['path'], 'sha256': sha(raw), 'git_blob': blob,
                 'published_current_compiled_registry_bytes_equal': True})
expected = {PROJECT+'/source/'+module+'.lean' for module in project['build_order']}
expected |= {c['log'] for c in commands} | {PROJECT+'/source/ProjectAudit.lean', 'verification.json'}
assert set(passed['manifest']) == expected
source_count = sum(Path(p).suffix == '.lean' for p in passed['manifest'])
log_count = sum(Path(p).suffix == '.log' for p in passed['manifest'])
assert source_count == log_count == len(commands)

# Only manifested text payloads are copied; compiled objects remain outside Git.
run_receipts = []
launches = []
for run, selected_project, exit_code, session in [(failed, BAD_PROJECT, 1, None), (passed, PROJECT, 0, 14025)]:
    dest = HERE/('parent-clean-'+run['number'])
    dest.mkdir(exist_ok=False)
    for path in run['manifest']:
        target = dest/path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(run['original']/path, target)
    (dest/'FILES.json').write_bytes(run['manifest_bytes'])
    (HERE/('parent-clean-'+run['number']+'.console.log')).write_bytes(run['console_bytes'])
    launches.append({'attempt': run['number'], 'evidence_kind': 'Root executor confirmation supplied in this packaging assignment',
        'argv': ['python3', CHECKER, '--lean', LEAN, '--output', str(run['original']), '--project', selected_project, '--registry', REGISTRY],
        'cwd': str(ROOT), 'tool_session_id': session, 'actual_exit_code': exit_code,
        'session_note': 'Root supplied actual session 14025.' if session else 'No session identifier supplied for the immediate failed launch; none inferred.',
        'per_lean_argv_source': 'parent-clean-'+run['number']+'/verification.json' if session else None})
    run_receipts.append({'attempt': run['number'], 'status': run['report']['status'], 'actual_exit_code': exit_code,
        'project_argument': selected_project, 'original_output': str(run['original']),
        'original_manifest_entries': len(run['manifest']), 'original_manifest_sha256': sha(run['manifest_bytes']),
        'original_report_sha256': sha(run['report_bytes']), 'original_console_sha256': sha(run['console_bytes']),
        'elapsed_seconds': run['report']['finished_at_epoch']-run['report']['started_at_epoch'],
        'all_original_manifest_members_and_manifest_preserved_unchanged': True})

(HERE/'registry.json').write_bytes(registry)
(HERE/'canonical-verifier.py').write_bytes(checker)
dump(HERE/'parent-launch.json', {'execution_owner': 'Agent #1 root', 'packager_reran_commands': False, 'launches': launches})
dump(HERE/'publication-source-receipt.json', {'status': 'PASS_SOURCE_IDENTITY', 'published_source_commit': COMMIT,
    'module_count': modules, 'registry_path': REGISTRY, 'registry_sha256': sha(registry),
    'checker_path': CHECKER, 'checker_sha256': sha(checker), 'sources': pins, 'lean_executed_by_packager': False})
elapsed = report['finished_at_epoch']-report['started_at_epoch']
dump(HERE/'parent-result-addendum.json', {'status': 'PASS_PRESERVED_PARENT_RUN_WITH_PRIOR_CONFIGURATION_FAILURE',
    'original_source_commit': COMMIT, 'original_source_tree_clean': True,
    'clean_field_limit': 'Canonical verifier checks tracked files and excludes untracked files; both original reports remain unchanged.',
    'runs': run_receipts,
    'failure_classification': 'Attempt001 rejected an unknown project argument before any Lean invocation, including --version. It is a configuration failure, not a failed mathematical proof check.',
    'failed_report_mode_field_limit': 'mathematical_proof_check=true records requested mode; projects is empty and no Lean was invoked.',
    'modules': modules, 'commands': len(commands), 'all_command_exits_zero': True,
    'theorem_constants': project['theorem_count'], 'theorem_axiom_union': union,
    'public_endpoints': project['endpoints'], 'separate_unsafe_implementation_axioms': len(unsafe),
    'safe_definition_audit_claimed_here': False, 'explicit_trust_zero': False,
    'flags_limit': 'Actual canonical argv lack explicit --trust=0. No trust default is inferred; this is not relabeled as the separate strict independent review.',
    'all_source_and_registry_bytes_match_published_commit': True, 'original_files_changed': False,
    'lean_rerun_by_packager': False, 'packager': 'Agent #1 specialist control_review',
    'packager_role': 'Continuing root-assigned registry/evidence support: packages root execution, authors no mathematics, claims no independent execution or final mathematical review.',
    'existing_attributed_registry_check_in': CHECK_IN, 'independent_final_review_owner': 'Agent #1 specialist center_review_resume',
    'packaging_driver_sha256': sha(Path(__file__).read_bytes())})
(HERE/'README.md').write_text(f'''# Preserved parent canonical sharp-excursion verification

Agent #1 root executed both runs. Specialist control_review validated and packaged the completed evidence under the continuing registry/evidence assignment. The packager authored no mathematics, ran no Lean, and claims no independent execution or final mathematical review; that separate review belongs to center_review_resume.

Attempt001 selected the unregistered project `{BAD_PROJECT}` and exited 1 with `Unknown project requested`. It stopped before any Lean invocation, including compiler-version checks. Its original report, traceback, FILES.json and console are preserved unchanged. The original report's mathematical_proof_check=true records requested mode; its projects object is empty. This is a configuration failure, not a failed Lean proof.

Attempt002 corrected the project argument to `{PROJECT}` with no source or registry changes. The actual report records PASS for {modules} modules and ProjectAudit: {len(commands)} commands, all exit zero, and {project['theorem_count']:,} module-origin theorem constants. The axiom union is {', '.join(union)}. The report separately inventories {len(unsafe)} inherited generated unsafe implementation axioms, which are not accepted theorem dependencies. No separate safe-definition audit is claimed here. All {len(project['endpoints'])} registry endpoints are retained. Root's actual session was 14025, exit zero; report elapsed time was {elapsed} seconds.

Both reports identify source commit {COMMIT} and registry SHA256 {sha(registry)}. All {modules} compiled source snapshots match current source, the published commit, and registry SHA256/Git-blob pins. Both original source_tree_clean=true fields are retained; the checker examines tracked files and excludes untracked files. Historical pending text in the frozen registry remains unchanged.

Every actual Lean argv is retained in parent-clean-002/verification.json. Commands use -j1 -DElab.async=false and lack explicit --trust=0. No trust default is inferred, and the run is not relabeled as the separate strict review. Official Lean 4.19.0 version/compiler/library hashes are preserved and matched against current files. parent-launch.json preserves root's confirmed outer Python argv and exits; no session identifier was supplied for the immediate failed launch, so none is invented.

The {len(failed['manifest'])} original failed-run manifest members and {len(passed['manifest'])} successful-run members are copied unchanged, together with each original FILES.json and both consoles. The successful payload includes {source_count} source snapshots, {log_count} logs and its report. Compiled objects remain outside the package. registry.json and canonical-verifier.py are exact published snapshots. Original external evidence remains untouched.

publication-source-receipt.json records all source comparisons; parent-result-addendum.json records both outcomes and limits. package.py is the executed packaging helper, adapted from the exact prior excursion helper identified in helper-provenance.json. No additional issue history was copied; this continues the attributed registry/evidence role in issue61 comment6228712115.

PACKAGE-FILES.json covers every package file except itself and frozen-receipt.json. The frozen receipt binds the full manifest and receipts. This is the scoped sharp-excursion project check, not a repository-wide result or a conclusion about196. No source or Git state was modified by the packager.
''')

# Recheck original and copied evidence before sealing the finite package.
for run in runs:
    dest = HERE/('parent-clean-'+run['number'])
    for base in [run['original'], dest]:
        assert (base/'FILES.json').read_bytes() == run['manifest_bytes']
        assert (base/'verification.json').read_bytes() == run['report_bytes']
        for path, entry in run['manifest'].items():
            raw = (base/path).read_bytes()
            assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256']
    assert run['original'].with_name(run['original'].name+'.console.log').read_bytes() == run['console_bytes']
    assert (HERE/('parent-clean-'+run['number']+'.console.log')).read_bytes() == run['console_bytes']
package = {}
for path in sorted(HERE.rglob('*')):
    if path.is_file() and path.name not in ['PACKAGE-FILES.json', 'frozen-receipt.json']:
        assert path.suffix not in ['.olean', '.ilean', '.pyc']
        package[str(path.relative_to(HERE))] = {'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())}
dump(HERE/'PACKAGE-FILES.json', package)
for path, entry in package.items():
    raw = (HERE/path).read_bytes()
    assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256']
dump(HERE/'frozen-receipt.json', {'status': 'SEALED', 'packager': 'Agent #1 specialist control_review',
    'execution_owner': 'Agent #1 root', 'published_source_commit': COMMIT, 'registry_sha256': sha(registry),
    'lean_rerun_by_packager': False, 'payload_file_count': len(package), 'total_file_count': len(package)+2,
    'manifest_file': 'PACKAGE-FILES.json', 'manifest_sha256': sha((HERE/'PACKAGE-FILES.json').read_bytes()),
    'result_receipt_sha256': sha((HERE/'parent-result-addendum.json').read_bytes()),
    'source_receipt_sha256': sha((HERE/'publication-source-receipt.json').read_bytes()),
    'manifest_scope': 'All package files except this frozen receipt and PACKAGE-FILES.json; seal hash separately reported.',
    'compiled_objects_packaged': False, 'runs': run_receipts, 'failed_attempt_lean_invocations': 0,
    'actual_successful_root_session': 14025, 'actual_successful_root_exit_code': 0,
    'modules': modules, 'commands': len(commands), 'theorem_constants': project['theorem_count'],
    'explicit_trust_zero_in_actual_commands': False})
print(json.dumps({'status': 'SEALED', 'modules': modules, 'commands': len(commands),
    'theorems': project['theorem_count'], 'original_manifest_entries': [len(r['manifest']) for r in runs],
    'package_entries': len(package), 'package_manifest_sha256': sha((HERE/'PACKAGE-FILES.json').read_bytes()),
    'seal_sha256': sha((HERE/'frozen-receipt.json').read_bytes()), 'total_file_count': len(package)+2}, indent=2))
