#!/usr/bin/env python3
"""Reviewer-owned sequential, clean-source build and exhaustive public axiom audit.

This does not call the author's build.sh or reuse any project .olean file.
Invoke with --help for relocation options; source commit is deliberately pinned.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

SOURCE_COMMIT = 'b2374410d427beb78fc601ee81cf15e34a1ac934'
AGENT7_COMMIT = 'da4a1799b74b98b4199cdb224ea7a694b2657651'
PACKAGE = 'proofs/contributions/agent-109/outer-projection-bridge'
INPUTS = [
    ('TemplateStep', 'proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean'),
    ('LychrelDigitSums', 'proofs/research/continuation/LychrelDigitSums.lean'),
    ('PeriodObstructions', 'proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean'),
    ('Compat', 'proofs/contributions/agent-109/template-step-bridge/Compat.lean'),
    ('ReturnCertificate', 'proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean'),
    ('OuterFinite', PACKAGE + '/agent7-deps/OuterFinite.lean'),
    ('OuterBounds', PACKAGE + '/agent7-deps/OuterBounds.lean'),
    ('OuterBridge', PACKAGE + '/OuterBridge.lean'),
    ('OuterCompat', PACKAGE + '/OuterCompat.lean'),
]
AUDIT_MODULES = {'OuterFinite', 'OuterBounds', 'OuterBridge', 'OuterCompat'}
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def code_only(source):
    """Erase nested Lean comments and strings, keeping offsets and newlines."""
    out = []
    i = depth = 0
    quoted = False
    while i < len(source):
        pair = source[i:i + 2]
        if depth:
            if pair == '/-':
                depth += 1
                out.extend('  ')
                i += 2
            elif pair == '-/':
                depth -= 1
                out.extend('  ')
                i += 2
            else:
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif quoted:
            if source[i] == '\\' and i + 1 < len(source):
                out.extend('  ')
                i += 2
            else:
                if source[i] == '"':
                    quoted = False
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif pair == '/-':
            depth = 1
            out.extend('  ')
            i += 2
        elif pair == '--':
            end = source.find('\n', i)
            end = len(source) if end < 0 else end
            out.extend(' ' * (end - i))
            i = end
        elif source[i] == '"':
            quoted = True
            out.append(' ')
            i += 1
        else:
            out.append(source[i])
            i += 1
    if depth or quoted:
        raise RuntimeError('Unclosed Lean comment/string in scanner input')
    return ''.join(out)


def exported_theorems(clean):
    """All target modules have one explicit namespace; fail on new forms."""
    namespaces = re.findall(r'^namespace\s+(\S+)\s*$', clean, re.M)
    if len(namespaces) != 1:
        raise RuntimeError('Target declaration structure requires manual parser update')
    names = []
    private = []
    declaration = re.compile(r'^\s*(?:(private|protected)\s+)?(?:theorem|lemma)\s+([\w\u0080-\uffff\'.]+)', re.M)
    for match in declaration.finditer(clean):
        full = namespaces[0] + '.' + match.group(2)
        (private if match.group(1) == 'private' else names).append(full)
    all_decl_tokens = re.findall(r'\b(?:theorem|lemma)\s+', clean)
    if len(all_decl_tokens) != len(names) + len(private):
        raise RuntimeError('Unparsed theorem/lemma declaration requires manual audit')
    if len(set(names)) != len(names):
        raise RuntimeError('Duplicate exported names')
    return names, private


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('/workspace/scratch/64704429df15/review109-source107'))
    p.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--scratch', type=Path, default=Path('/workspace/scratch/64704429df15'))
    p.add_argument('--lean', type=Path, default=Path('/workspace/scratch/64704429df15/env107/lean'))
    p.add_argument('--native-lean', type=Path, default=Path('/workspace/scratch/64704429df15/toolchain/lean-4.19.0-linux/bin/lean'))
    p.add_argument('--shim', type=Path, default=Path('/workspace/scratch/64704429df15/env107/readlink_self.so'))
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    build = Path(tempfile.mkdtemp(prefix='agent107-outer109-clean-', dir=args.scratch))
    evidence = args.output / build.name
    evidence.mkdir()
    report = {'status': 'RUNNING', 'source_commit': SOURCE_COMMIT,
              'source_checkout': str(args.source), 'fresh_build_directory': str(build),
              'harness_sha256': digest(Path(__file__).read_bytes()),
              'author_build_script_executed': False, 'project_olean_reused': False,
              'lean_processes_parallel': False, 'commands': [], 'sources': [],
              'target_theorems': [], 'private_helpers': [], 'provenance': []}
    manifest = evidence / 'manifest.json'

    def save():
        manifest.write_text(json.dumps(report, indent=2) + '\n')

    def command(argv, cwd, label, env=None):
        started = time.monotonic()
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
        stdout_path = evidence / (label + '.stdout.log')
        stderr_path = evidence / (label + '.stderr.log')
        stdout_path.write_bytes(result.stdout)
        stderr_path.write_bytes(result.stderr)
        report['commands'].append({'label': label, 'argv': [str(a) for a in argv],
            'cwd': str(cwd), 'exit_code': result.returncode,
            'elapsed_seconds': round(time.monotonic() - started, 3),
            'stdout_log': stdout_path.name, 'stdout_sha256': digest(result.stdout),
            'stderr_log': stderr_path.name, 'stderr_sha256': digest(result.stderr)})
        save()
        if result.returncode:
            raise RuntimeError(label + ' failed with exit ' + str(result.returncode))
        return result.stdout

    try:
        head = command(['git', 'rev-parse', 'HEAD'], args.source, 'head-before').decode().strip()
        if head != SOURCE_COMMIT:
            raise RuntimeError('Source checkout differs from authorized commit')
        dirty = command(['git', 'status', '--porcelain=v1', '--untracked-files=all'], args.source, 'status-before')
        if dirty:
            raise RuntimeError('Source checkout not clean before execution')
        env = dict(os.environ)
        env.pop('LEAN_SYSROOT', None)
        env.update(LEAN_PATH=str(build), LD_PRELOAD='')
        report['environment_overrides'] = {'LEAN_PATH': str(build), 'LD_PRELOAD': '', 'LEAN_SYSROOT': 'unset'}
        report['compiler'] = {'wrapper': str(args.lean), 'wrapper_sha256': digest(args.lean.read_bytes()),
            'native_binary': str(args.native_lean), 'native_binary_sha256': digest(args.native_lean.read_bytes()),
            'readlink_shim': str(args.shim), 'readlink_shim_sha256': digest(args.shim.read_bytes())}
        version = command([str(args.lean), '--version'], build, 'lean-version', env).decode().strip()
        report['compiler']['version'] = version
        if '4.19.0' not in version or '6caaee842e94' not in version:
            raise RuntimeError('Unexpected Lean version')
        if report['compiler']['native_binary_sha256'] != '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':
            raise RuntimeError('Unexpected native Lean binary digest')
        if report['compiler']['readlink_shim_sha256'] != '100718efe84a5c605d4752eadf9d9f6b14f38d5adbc82ce00407d378f4d9973d':
            raise RuntimeError('Unexpected readlink-only shim digest')
        std = args.native_lean.parent.parent / 'lib/lean/Std.olean'
        report['compiler']['Std_olean_sha256'] = digest(std.read_bytes())
        available = {'Std'}
        for module, relpath in INPUTS:
            source = args.source / relpath
            data = source.read_bytes()
            committed = command(['git', 'show', SOURCE_COMMIT + ':' + relpath], args.source, 'source-commit-' + module)
            if committed != data:
                raise RuntimeError('Working source differs from commit: ' + module)
            snapshot = build / (module + '.lean')
            snapshot.write_bytes(data)
            clean = code_only(data.decode())
            excluded = sorted(set(re.findall(r'\b(?:sorry|admit|native_decide|ofReduceBool|axiom|implemented_by|unsafe|extern)\b|debug\.skipKernelTC', clean)))
            imports = [dep for line in clean.splitlines() if line.startswith('import ') for dep in line.split()[1:]]
            if any(dep not in available for dep in imports):
                raise RuntimeError('Unresolved import or wrong order: ' + module)
            available.add(module)
            item = {'module': module, 'repository_path': relpath, 'sha256': digest(data),
                    'commit_bytes_match': True, 'imports': imports, 'excluded_code_tokens': excluded}
            report['sources'].append(item)
            if excluded:
                raise RuntimeError('Excluded proof/trust token in ' + module + ': ' + repr(excluded))
            if module in AUDIT_MODULES:
                names, private = exported_theorems(clean)
                item['exported_theorems'] = names
                item['private_helpers'] = private
                report['target_theorems'].extend(names)
                report['private_helpers'].extend(private)
            if module in {'OuterFinite', 'OuterBounds'}:
                historical = command(['git', 'show', AGENT7_COMMIT + ':proofs/agent7/' + module + '.lean'], args.source, 'agent7-original-' + module)
                report['provenance'].append({'module': module, 'original_commit': AGENT7_COMMIT,
                    'original_path': 'proofs/agent7/' + module + '.lean',
                    'original_sha256': digest(historical), 'copy_sha256': digest(data), 'byte_identical': historical == data})
                if historical != data:
                    raise RuntimeError('Agent7 dependency differs from pinned original: ' + module)
        save()
        for module, _ in INPUTS:
            print('START', module, flush=True)
            argv = [str(args.lean), '-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean']
            command(argv, build, 'compile-' + module, env)
            report['sources'][[m for m, _ in INPUTS].index(module)]['olean_sha256'] = digest((build / (module + '.olean')).read_bytes())
            print('PASS', module, flush=True)
            save()
        audit = '\n'.join('import ' + module for module, _ in INPUTS if module in AUDIT_MODULES) + '\n\n'
        audit += '\n'.join('#print axioms ' + name for name in report['target_theorems']) + '\n'
        (build / 'IndependentOuterAxioms.lean').write_text(audit)
        (evidence / 'IndependentOuterAxioms.lean').write_text(audit)
        print('START IndependentOuterAxioms', len(report['target_theorems']), 'public theorems', flush=True)
        output = command([str(args.lean), '-j1', '-DElab.async=false', 'IndependentOuterAxioms.lean'], build, 'audit-all-exported', env).decode()
        profiles = {}
        for name in report['target_theorems']:
            if "'" + name + "' does not depend on any axioms" in output:
                profiles[name] = []
                continue
            match = re.search(re.escape("'" + name + "' depends on axioms: [") + r'([^\]]*)\]', output)
            if not match:
                raise RuntimeError('Missing axiom report for ' + name)
            profiles[name] = sorted(x.strip() for x in match.group(1).split(',') if x.strip())
        union = set(a for axioms in profiles.values() for a in axioms)
        report['axiom_reports'] = profiles
        report['axiom_union'] = sorted(union)
        report['unexpected_axioms'] = sorted(union - ALLOWED_AXIOMS)
        if report['unexpected_axioms']:
            raise RuntimeError('Unexpected axiom dependencies')
        for item in report['sources']:
            item['unchanged_after_execution'] = (digest((args.source / item['repository_path']).read_bytes())
                == item['sha256'] == digest((build / (item['module'] + '.lean')).read_bytes()))
            if not item['unchanged_after_execution']:
                raise RuntimeError('Source or snapshot changed during run')
        endhead = command(['git', 'rev-parse', 'HEAD'], args.source, 'head-after').decode().strip()
        endstatus = command(['git', 'status', '--porcelain=v1', '--untracked-files=all'], args.source, 'status-after')
        if endhead != SOURCE_COMMIT or endstatus:
            raise RuntimeError('Source checkout changed during run')
        report['source_checkout_clean_before_and_after'] = True
        report['status'] = 'PASS'
        save()
        print('PASS', manifest, flush=True)
    except Exception as exc:
        report['status'] = 'FAIL'
        report['unresolved_obligation'] = str(exc)
        save()
        print('FAIL', exc, manifest, flush=True)
        raise


if __name__ == '__main__':
    main()
