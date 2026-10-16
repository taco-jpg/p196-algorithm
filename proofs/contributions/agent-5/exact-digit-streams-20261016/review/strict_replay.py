#!/usr/bin/env python3
"""Fresh serialized --trust=0 replay of the frozen registry and original audit.

This independent driver does not alter the canonical verifier or any Lean source.
Compiled objects are temporary; source, raw logs, exit codes, and hashes persist.
"""

from pathlib import Path
import argparse
import json
import os
import re
import subprocess
import tempfile
import time

from semantic_inventory import code_only, digest, git_blob


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--audit-source', type=Path, required=True)
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
        'parent_audit_source_copied_unchanged': True,
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
        project_name = 'agent5-exact-digit-streams'
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
        if len(endpoints) != 25 or len(set(endpoints)) != 25:
            return fail('REGISTRY_REJECTED', 'Expected 25 distinct exported endpoints')
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
        if seen != set(modules) or len(order) != 7:
            return fail('REGISTRY_REJECTED', 'Expected one complete seven-module dependency closure')
        receipt['build_order'] = order
        audit_data = args.audit_source.read_bytes()
        audit_text = audit_data.decode()
        checks = re.findall(r'^#check\s+(\S+)\s*$', audit_text, re.M)
        selected = re.search(r'let selected : List String := (\[[^\n]*\])', audit_text)
        if checks != endpoints or selected is None or json.loads(selected.group(1)) != order:
            return fail('AUDIT_SOURCE_MISMATCH', 'Parent audit does not enumerate this exact registry and claim set')
        (source / 'ProjectAudit.lean').write_bytes(audit_data)
        receipt['audit_source'] = {'parent_path': str(args.audit_source.resolve()), 'snapshot_path': 'source/ProjectAudit.lean', 'sha256': digest(audit_data), 'unchanged': True}
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
        with tempfile.TemporaryDirectory(prefix='agent5-digit-review-', dir='/tmp') as temporary:
            compiled = Path(temporary)
            env = os.environ.copy()
            env['LEAN_PATH'] = str(compiled)
            receipt['import_search_path'] = str(compiled)
            receipt['compiled_objects'] = 'Fresh temporary directory, removed after replay; no previously built project oleans are imported.'
            flags = ['--trust=0', '-j1', '-DElab.async=false']
            receipt['compiler_flags'] = flags
            save()
            for module in order:
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
        receipt['status'] = 'PASS_INDEPENDENT_STRICT_REPLAY'
        receipt['exit_code'] = 0
        receipt['finished_at_epoch'] = time.time()
        save()
        files = {}
        for path in sorted(output.rglob('*')):
            if path.is_file() and path.name != 'FILES.json':
                data = path.read_bytes()
                files[str(path.relative_to(output))] = {'bytes': len(data), 'sha256': digest(data)}
        (output / 'FILES.json').write_text(json.dumps(files, indent=2) + '\n')
        print(json.dumps({'status': receipt['status'], 'successful_build_and_audit_commands': len(receipt['commands']), 'full_module_origin_theorems': len(audits), 'fixed_exports': len(endpoints), 'axiom_union': sorted(union)}), flush=True)
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        return fail('REPLAY_INTERRUPTED', type(error).__name__ + ': ' + str(error))


if __name__ == '__main__':
    raise SystemExit(main())
