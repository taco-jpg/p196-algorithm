#!/usr/bin/env python3
"""Compile two frozen raw-prefix modules against an attributed author baseline.

Thirteen dependency objects are inherited and source/hash checked. Only the two
new modules are freshly compiled. The final audit covers all fifteen origins.
This is not a fresh full dependency rebuild.
"""

from pathlib import Path
import argparse
import json
import os
import re
import subprocess
import tempfile
import time
import shutil
import sys

sys.dont_write_bytecode = True

from source_identity import code_only, digest, git_blob


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--audit-source', type=Path, required=True)
    parser.add_argument('--author-stage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('--output must be a fresh, nonexistent directory')
    repo = args.repo.resolve()
    lean = args.lean.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True)
    source = output / 'source'
    logs = output / 'logs'
    source.mkdir()
    logs.mkdir()
    receipt = {
        'schema_version': 1,
        'status': 'STARTED',
        'actual_executor': 'Agent #5 /root/semantic_review',
        'independent_of_theorem_authorship': True,
        'authored_any_reviewed_theorem': False,
        'execution_mode': 'Supported require_escalated tool execution after ordinary sandbox application-location preflight failure',
        'toolchain': None,
        'trust_level': 0,
        'serialized': True,
        'canonical_verifier_modified': False,
        'input_audit_source_copied_unchanged': True,
        'audit_template_body': 'Canonical module-origin axiom audit body, unchanged; selected fifteen modules and six new exports come from the reviewer registry',
        'is_fresh_full_dependency_rebuild': False,
        'freshly_compiled_modules': ['RawPrefixStreams', 'OrdinaryStreamStep'],
        'inherited_dependencies': 'Nine published coordinate objects inherited by the author plus four arithmetic dependencies compiled by runtime sibling; this reviewer rebuilds neither group here',
        'sources': {},
        'preflight_commands': [],
        'commands': [],
        'audit': {},
        'repository_wide_pass': False,
        'started_at_epoch': time.time(),
    }

    def save():
        (output / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')

    def fail(status, explanation, code=1):
        receipt.update(status=status, explanation=explanation, exit_code=code, finished_at_epoch=time.time())
        save()
        print(json.dumps({'status': status, 'explanation': explanation, 'exit_code': code}), flush=True)
        return code

    def run(label, command, env=None, is_preflight=False, timeout=300):
        start = time.monotonic()
        log = logs / (label + '.log')
        with log.open('wb') as stream:
            try:
                result = subprocess.run(command, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        record = {
            'label': label, 'argv': command, 'exit_code': code,
            'elapsed_seconds': round(time.monotonic() - start, 6),
            'log': str(log.relative_to(output)), 'log_sha256': digest(log.read_bytes()),
        }
        receipt['preflight_commands' if is_preflight else 'commands'].append(record)
        save()
        print(json.dumps({'module': label, 'exit_code': code, 'elapsed_seconds': record['elapsed_seconds']}), flush=True)
        return code, log.read_text()

    save()
    try:
        registry_data = args.registry.read_bytes()
        registry = json.loads(registry_data)
        project_name = 'agent5-ordinary-stream-prefix'
        project = registry['projects'][project_name]
        modules = project['modules']
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        if set(registry['toolchain']['allowed_axioms']) != allowed:
            return fail('REGISTRY_REJECTED', 'Unexpected axiom allowlist')
        receipt['registry'] = {'input_path': str(args.registry.resolve()), 'sha256': digest(registry_data), 'snapshot_path': 'registry.json'}
        (output / 'registry.json').write_bytes(registry_data)
        receipt['scope'] = project['scope']
        receipt['repository_head_at_snapshot'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
        receipt['source_identity_note'] = 'Registry hashes and the copied source bytes identify this review. Repository HEAD metadata alone does not assert that all reviewed files were tracked in that commit.'
        endpoints = [endpoint for claim in registry['claims'] if claim['project'] == project_name for endpoint in claim['endpoints']]
        if len(endpoints) != 6 or len(set(endpoints)) != 6:
            return fail('REGISTRY_REJECTED', 'Expected six distinct new exported endpoints')
        receipt['expected_exports'] = endpoints
        for module, expected in modules.items():
            data = (repo / expected['path']).read_bytes()
            if digest(data) != expected['sha256'] or git_blob(data) != expected['git_blob']:
                return fail('SOURCE_HASH_MISMATCH', expected['path'])
            if expected.get('adapter'):
                return fail('REGISTRY_REJECTED', 'No source adapters are allowed in this independent exact-source replay')
            code = code_only(data.decode())
            forbidden = re.findall(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe)\b', code)
            if forbidden:
                return fail('FORBIDDEN_SOURCE_TOKEN', module + ': ' + ','.join(sorted(set(forbidden))))
            imports = [part for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for part in line.split()]
            if imports != expected['imports']:
                return fail('IMPORT_MISMATCH', module)
            target = source / (module + '.lean')
            target.write_bytes(data)
            receipt['sources'][module] = {**expected, 'snapshot_path': str(target.relative_to(output)), 'snapshot_sha256': digest(data)}
        order, active, seen = [], set(), set()

        def visit(module):
            if module not in modules:
                if module.split('.')[0] not in {'Init', 'Std', 'Lean'}:
                    raise ValueError('Unregistered external import: ' + module)
                return
            if module in active:
                raise ValueError('Import cycle: ' + module)
            if module in seen:
                return
            active.add(module)
            for dependency in modules[module]['imports']:
                visit(dependency)
            active.remove(module)
            seen.add(module)
            order.append(module)

        for root in project['roots']:
            visit(root)
        if seen != set(modules) or len(order) != 15:
            return fail('REGISTRY_REJECTED', 'Expected one complete fifteen-module dependency closure')
        receipt['build_order'] = order
        audit_data = args.audit_source.read_bytes()
        audit_text = audit_data.decode()
        checks = re.findall(r'^#check\s+(\S+)\s*$', audit_text, re.M)
        selected = re.search(r'let selected : List String := (\[[^\n]*\])', audit_text)
        if checks != endpoints or selected is None or json.loads(selected.group(1)) != order:
            return fail('AUDIT_SOURCE_MISMATCH', 'Audit does not enumerate this exact registry and claim set')
        (source / 'ProjectAudit.lean').write_bytes(audit_data)
        receipt['audit_source'] = {'input_path': str(args.audit_source.resolve()), 'snapshot_path': 'source/ProjectAudit.lean', 'sha256': digest(audit_data), 'unchanged': True}
        save()
        code, version = run('CompilerVersion', [str(lean), '--version'], is_preflight=True, timeout=30)
        if code or 'version 4.19.0' not in version or 'commit 6caaee842e94, Release' not in version:
            return fail('COMPILER_PREFLIGHT_FAILED', 'Official compiler version preflight did not succeed')
        code, prefix = run('CompilerPrefix', [str(lean), '--print-prefix'], is_preflight=True, timeout=30)
        if code:
            return fail('COMPILER_PREFLIGHT_FAILED', 'Compiler prefix preflight did not succeed')
        runtime = Path(prefix.strip()).resolve()
        binaries = [lean, *sorted((runtime / 'lib/lean').glob('*.so'))]
        receipt['toolchain'] = {'version': version.strip(), 'runtime_prefix': str(runtime), 'files': {str(path): digest(path.read_bytes()) for path in binaries}}
        if receipt['toolchain']['files'][str(lean)] != '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':
            return fail('COMPILER_HASH_MISMATCH', 'Compiler binary differs from the canonical replay')
        baseline_names, new_names = order[:-2], order[-2:]
        if len(baseline_names) != 13 or new_names != ['RawPrefixStreams', 'OrdinaryStreamStep']:
            return fail('REGISTRY_REJECTED', 'Unexpected inherited/new module partition')
        author_stage = args.author_stage.resolve()
        inheritance_path = author_stage / 'inherited-artifacts.json'
        baseline_path = author_stage / 'baseline.json'
        inheritance_data, baseline_data = inheritance_path.read_bytes(), baseline_path.read_bytes()
        inheritance, baseline = json.loads(inheritance_data), json.loads(baseline_data)
        inherited_records = {r['module']: r for r in inheritance['modules'] + inheritance['new_arithmetic_dependencies']}
        arithmetic_runs = {r['module']: r for r in baseline['runs']}
        if set(inherited_records) != set(baseline_names) or len(inheritance['modules']) != 9 or len(arithmetic_runs) != 4:
            return fail('BASELINE_EVIDENCE_REJECTED', 'Unexpected author baseline module coverage')
        if baseline['flags'] != ['--trust=0', '-j1', '-DElab.async=false'] or any(r['exit_code'] != 0 for r in arithmetic_runs.values()):
            return fail('BASELINE_EVIDENCE_REJECTED', 'Author arithmetic baseline did not pass strict checking')
        provenance = output / 'provenance'
        provenance.mkdir()
        (provenance / 'author-inherited-artifacts.json').write_bytes(inheritance_data)
        (provenance / 'author-baseline.json').write_bytes(baseline_data)
        receipt['author_baseline_receipts'] = {
            'inheritance': {'input_path': str(inheritance_path), 'sha256': digest(inheritance_data), 'snapshot_path': 'provenance/author-inherited-artifacts.json'},
            'arithmetic_build': {'input_path': str(baseline_path), 'sha256': digest(baseline_data), 'snapshot_path': 'provenance/author-baseline.json', 'actual_executor': 'Agent #5 runtime sibling /root/lean_runtime', 'not_executed_by_this_reviewer': True},
        }
        receipt['inherited_objects'] = {}
        for module in baseline_names:
            expected = modules[module]
            record = inherited_records[module]
            stage_source = author_stage / (module + '.lean')
            stage_object = author_stage / (module + '.olean')
            if record['source_sha256'] != expected['sha256'] or record['git_blob'] != expected['git_blob'] or record['repository_source'] != expected['path'] or digest(stage_source.read_bytes()) != expected['sha256']:
                return fail('BASELINE_SOURCE_MISMATCH', module)
            object_hash = digest(stage_object.read_bytes())
            if 'olean_sha256' in record and object_hash != record['olean_sha256']:
                return fail('BASELINE_OBJECT_MISMATCH', module)
            if module in arithmetic_runs:
                prior = arithmetic_runs[module]
                if prior['source_sha256'] != expected['sha256']:
                    return fail('BASELINE_SOURCE_MISMATCH', module)
                prior_log = (author_stage / prior['log']).read_bytes()
                if digest(prior_log) != prior['log_sha256']:
                    return fail('BASELINE_LOG_MISMATCH', module)
                (provenance / (module + '-author.log')).write_bytes(prior_log)
            receipt['inherited_objects'][module] = {'source_path': str(stage_source), 'source_sha256': expected['sha256'], 'olean_path': str(stage_object), 'olean_sha256_at_import': object_hash, 'preexisting_author_olean_hash_verified': 'olean_sha256' in record, 'provenance': 'Published coordinate dependency inherited by author' if module not in arithmetic_runs else 'Arithmetic module compiled by runtime sibling in author baseline'}
        with tempfile.TemporaryDirectory(prefix='agent5-raw-prefix-review-', dir='/tmp') as temporary:
            compiled = Path(temporary)
            env = os.environ.copy()
            env['LEAN_PATH'] = str(compiled)
            receipt['import_search_path'] = str(compiled)
            receipt['compiled_objects'] = 'Private temporary directory, removed after replay; thirteen attributed dependency oleans are copied in and two new modules are compiled freshly.'
            for module in baseline_names:
                target = compiled / (module + '.olean')
                shutil.copyfile(author_stage / (module + '.olean'), target)
                if digest(target.read_bytes()) != receipt['inherited_objects'][module]['olean_sha256_at_import']:
                    return fail('BASELINE_OBJECT_COPY_MISMATCH', module)
            flags = ['--trust=0', '-j1', '-DElab.async=false']
            receipt['compiler_flags'] = flags
            save()
            for module in new_names:
                command = [str(lean), *flags, '-o', str(compiled / (module + '.olean')), module + '.lean']
                code, _ = run(module, command, env=env)
                if code:
                    return fail('STRICT_LEAN_BUILD_FAILED', 'Module ' + module + ' failed; see preserved raw log')
            code, audit_log = run('ProjectAudit', [str(lean), *flags, 'ProjectAudit.lean'], env=env)
            if code:
                return fail('STRICT_AUDIT_FAILED', 'Exhaustive module-origin audit failed; see preserved raw log')
        summaries = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$', audit_log, re.M)
        declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$', audit_log, re.M)
        if len(summaries) != 1 or len(declarations) != int(summaries[0][0]):
            return fail('INCOMPLETE_AXIOM_AUDIT', 'Audit summary and declaration count differ')
        names = [name for _, name, _ in declarations]
        if len(set(names)) != len(names) or not set(endpoints) <= set(names):
            return fail('INCOMPLETE_AXIOM_AUDIT', 'Missing exports or duplicate declarations')
        audits = []
        union = set()
        for module, name, axes in declarations:
            axiom_list = [axiom.strip() for axiom in axes.split(',') if axiom.strip()]
            if module not in modules or not set(axiom_list) <= allowed:
                return fail('DISALLOWED_AXIOMS', name)
            union.update(axiom_list)
            audits.append({'module': module, 'name': name, 'axioms': axiom_list, 'fixed_export': name in endpoints})
        if re.search(r'CUSTOM_AXIOM|DISALLOWED_AXIOMS|sorryAx', audit_log):
            return fail('AXIOM_AUDIT_REJECTED', 'Forbidden diagnostic in audit output')
        receipt['audit'] = {
            'full_module_origin_theorems': len(audits),
            'fixed_exports_checked': len(endpoints),
            'axiom_union': sorted(union),
            'all_axioms_permitted': True,
            'unsafe_implementation_axioms': re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit_log, re.M),
            'declarations': audits,
        }
        for module, record in receipt['sources'].items():
            if digest((repo / record['path']).read_bytes()) != record['sha256']:
                return fail('LIVE_SOURCE_CHANGED_DURING_REVIEW', module)
        receipt['live_source_hashes_unchanged_at_completion'] = True
        receipt['status'] = 'PASS_INDEPENDENT_TWO_MODULE_REPLAY_WITH_INHERITED_BASELINE'
        receipt['exit_code'] = 0
        receipt['finished_at_epoch'] = time.time()
        save()
        files = {}
        for path in sorted(output.rglob('*')):
            if path.is_file() and path.name != 'FILES.json':
                data = path.read_bytes()
                files[str(path.relative_to(output))] = {'bytes': len(data), 'sha256': digest(data)}
        (output / 'FILES.json').write_text(json.dumps(files, indent=2) + '\n')
        print(json.dumps({'status': receipt['status'], 'successful_build_and_audit_commands': len(receipt['commands']), 'fresh_module_count': len(new_names), 'inherited_module_count': len(baseline_names), 'full_module_origin_theorems': len(audits), 'fixed_exports': len(endpoints), 'axiom_union': sorted(union)}), flush=True)
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        return fail('REPLAY_INTERRUPTED', type(error).__name__ + ': ' + str(error))


if __name__ == '__main__':
    raise SystemExit(main())
