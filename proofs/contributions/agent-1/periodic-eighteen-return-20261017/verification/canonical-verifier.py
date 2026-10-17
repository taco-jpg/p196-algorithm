#!/usr/bin/env python3
"""Verify every registered accepted project from exact source, without cached objects.

Default mode cannot report repository-wide PASS while the accepted-scope census
is incomplete. --project selects an explicitly scoped build. --check-only checks
source identity/import closure but is not Lean verification. Use a new output
path; prior executions are never overwritten. Standard library only, Lean4.19.0.
The exhaustive module-origin axiom audit is adapted from the inspected Agent104,
Agent111 and Agent103 checkers; original proofs and provenance remain unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = ['propext', 'Classical.choice', 'Quot.sound']
NAME = re.compile(r'[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*\Z')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def code_only(text: str) -> str:
    """Mask nested Lean comments and strings while retaining line positions."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i+2]
        if depth:
            if pair == '/-': depth += 1; out.extend('  '); i += 2
            elif pair == '-/': depth -= 1; out.extend('  '); i += 2
            else: out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif string:
            if text[i] == '\\': out.extend('  '); i += 2
            else: string = text[i] != '"'; out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif pair == '/-': depth = 1; out.extend('  '); i += 2
        elif pair == '--':
            end = text.find('\n', i); end = len(text) if end < 0 else end
            out.extend(' ' * (end-i)); i = end
        elif text[i] == '"': string = True; out.append(' '); i += 1
        else: out.append(text[i]); i += 1
    if depth or string:
        raise ValueError('Unterminated Lean comment or string')
    return ''.join(out)


def local_path(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Unsafe path: ' + relative)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--project', action='append', default=[])
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--registry', type=Path, default=ROOT / 'proofs/ACCEPTED_BUILD.json')
    args = parser.parse_args()
    out, lean = args.output.resolve(), args.lean.resolve()
    out.mkdir(parents=True, exist_ok=False)
    report = {'agent': 'Agent #1', 'status': 'RUNNING', 'projects': {},
              'mathematical_proof_check': not args.check_only,
              'repository_wide_pass': False, 'started_at_epoch': time.time()}
    def save():
        (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    try:
        registry_bytes = args.registry.read_bytes()
        registry = json.loads(registry_bytes)
        if registry['schema_version'] != 1 or registry['toolchain']['allowed_axioms'] != ALLOWED:
            raise ValueError('Unsupported registry schema or axiom-policy change')
        report['registry_sha256'] = digest(registry_bytes)
        report['source_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        report['source_tree_clean'] = not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT)
        if registry['catalogue_complete'] and registry['catalogue_blockers']:
            raise ValueError('Complete catalogue cannot retain unresolved blockers')
        report['catalogue_complete'] = registry['catalogue_complete']
        report['catalogue_blockers'] = registry['catalogue_blockers']
        selected = args.project or list(registry['projects'])
        if not selected or len(set(selected)) != len(selected):
            raise ValueError('Empty or repeated project selection')
        if set(selected) - registry['projects'].keys():
            raise ValueError('Unknown project requested')
        version = subprocess.check_output([str(lean), '--version'], text=True).strip()
        if not re.search(r'version 4\.19\.0,.*commit 6caaee842e94, Release', version):
            raise ValueError('Incorrect official Lean toolchain: ' + version)
        runtime = Path(subprocess.check_output([str(lean), '--print-prefix'], text=True).strip()).resolve()
        compiler_files = [lean, runtime / 'bin/lean', *sorted((runtime / 'lib/lean').glob('*.so'))]
        report['compiler'] = {'version': version, 'files': {str(p): digest(p.read_bytes()) for p in compiler_files}}
        for project in selected:
            if not NAME.fullmatch(project.replace('-', '_')):
                raise ValueError('Invalid project identifier')
            spec = registry['projects'][project]
            folder = out / project; folder.mkdir(); source = folder / 'source'; source.mkdir(); logs = folder / 'logs'; logs.mkdir()
            pr = {'status': 'RUNNING', 'scope': spec['scope'], 'sources': {}, 'commands': [], 'roots': spec['roots']}
            report['projects'][project] = pr
            records, originals, compiled, imports = spec['modules'], {}, {}, {}
            for module, rec in records.items():
                if not NAME.fullmatch(module): raise ValueError('Invalid module name')
                path = local_path(ROOT, rec['path']); data = path.read_bytes()
                if digest(data) != rec['sha256']: raise ValueError('Source hash mismatch: ' + rec['path'])
                git_blob = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
                if git_blob != rec['git_blob']: raise ValueError('Git blob mismatch: ' + rec['path'])
                originals[module] = data
            for module, rec in records.items():
                data = originals[module]
                if rec.get('adapter'):
                    adapter = rec['adapter']; target = adapter['container_module']
                    if adapter['kind'] != 'verified_embedded_foundation' or target == module:
                        raise ValueError('Unsupported foundation adapter')
                    container = originals[target]
                    if digest(container) != adapter['container_source_sha256'] or digest(data) != adapter['original_source_sha256']:
                        raise ValueError('Adapter source pins changed')
                    small, big = data.splitlines(keepends=True), container.splitlines(keepends=True)
                    offset, count = adapter['embedded_start_line_1_based']-1, adapter['embedded_line_count']
                    if small[0] != b'import Std\n' or big[0] != b'import Std\n' or count != len(small)-1 or big[offset:offset+count] != small[1:]:
                        raise ValueError('Foundation byte containment failed')
                    data = ('/- Generated compatibility import; original foundation bytes remain retained and are verified in full inside the canonical module. -/\nimport ' + target + '\n').encode()
                code = code_only(data.decode())
                if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code):
                    raise ValueError('Forbidden source token in ' + module)
                deps = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for d in line.split()]
                if deps != rec['imports'] or any(not NAME.fullmatch(d) for d in deps):
                    raise ValueError('Import registry mismatch: ' + module)
                for dep in deps:
                    if dep not in records:
                        if dep.split('.')[0] not in {'Init', 'Std', 'Lean'} or not (runtime / 'lib/lean' / (dep.replace('.', '/')+'.olean')).is_file():
                            raise ValueError('Unregistered or unavailable import: ' + dep)
                compiled[module], imports[module] = data, deps
                dest = source / (module.replace('.', '/')+'.lean'); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
                pr['sources'][module] = {'path': rec['path'], 'sha256': rec['sha256'], 'build_sha256': digest(data), 'imports': deps, 'adapter': rec.get('adapter')}
            order, active, seen = [], set(), set()
            def visit(module):
                if module not in records: return
                if module in active: raise ValueError('Import cycle: ' + module)
                if module in seen: return
                active.add(module)
                for dep in imports[module]: visit(dep)
                active.remove(module); seen.add(module); order.append(module)
            for root in spec['roots']:
                if root not in records: raise ValueError('Missing root ' + root)
                visit(root)
            if seen != set(records): raise ValueError('Registry includes modules outside selected root closure')
            pr['build_order'] = order; save()
            env = {'PATH': str(lean.parent)+':/usr/bin:/bin', 'HOME': str(folder), 'LANG': 'C.UTF-8', 'LEAN_PATH': str(source)}
            def run(label, command):
                start = time.monotonic(); log = logs / (label+'.log')
                with log.open('wb') as stream:
                    try: rc = subprocess.run(command, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800).returncode
                    except subprocess.TimeoutExpired: rc = 124
                pr['commands'].append({'label': label, 'argv': command, 'exit_code': rc, 'elapsed_seconds': round(time.monotonic()-start,6), 'log': str(log.relative_to(out)), 'log_sha256': digest(log.read_bytes())}); save()
                print(project, label, 'exit='+str(rc), flush=True)
                if rc: raise RuntimeError('Failed '+project+'/'+label+'; see retained log')
                return log.read_text()
            if args.check_only:
                pr['status'] = 'SOURCE_AND_IMPORT_CHECK_ONLY'; save(); continue
            for module in order:
                relative = module.replace('.', '/')
                run(module, [str(lean), '-j1', '-DElab.async=false', '-o', relative+'.olean', relative+'.lean'])
            endpoints = [e for c in registry['claims'] if c['project'] == project for e in c.get('endpoints', [])]
            if not endpoints or any(not NAME.fullmatch(e) for e in endpoints): raise ValueError('Missing or invalid claim endpoints')
            audit = '\n'.join('import '+m for m in spec['roots'])+'\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'+ '\n'.join('#check '+e for e in endpoints)+'\nrun_cmd do\n  let env ← getEnv\n  let selected : List String := '+json.dumps(order)+'''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
'''
            (source / 'ProjectAudit.lean').write_text(audit)
            audit_log = run('ProjectAudit', [str(lean), '-j1', '-DElab.async=false', 'ProjectAudit.lean'])
            matches = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$', audit_log, re.M)
            declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$', audit_log, re.M)
            if len(matches) != 1 or int(matches[0][0]) != len(declarations) or not declarations or len({x[1] for x in declarations}) != len(declarations):
                raise ValueError('Missing, duplicate or incomplete module audit')
            pr['theorem_count'] = len(declarations); pr['axiom_union'] = matches[0][1]; pr['endpoints'] = endpoints
            pr['unsafe_implementation_axioms'] = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit_log, re.M)
            for module, rec in records.items():
                if local_path(ROOT, rec['path']).read_bytes() != originals[module]: raise ValueError('Source changed during verification')
                if (source / (module.replace('.', '/')+'.lean')).read_bytes() != compiled[module]: raise ValueError('Build snapshot changed')
            pr['status'] = 'PASS'; save()
        for path, h in report['compiler']['files'].items():
            if digest(Path(path).read_bytes()) != h: raise ValueError('Compiler changed during verification')
        if args.check_only: report['status'] = 'SOURCE_AND_IMPORT_CHECK_ONLY'
        elif not args.project and not registry['catalogue_complete']: report['status'] = 'BLOCKED_INCOMPLETE_ACCEPTED_CATALOGUE'
        else:
            report['status'] = 'PASS'; report['repository_wide_pass'] = not args.project and registry['catalogue_complete']
        return 2 if not args.project and not registry['catalogue_complete'] else 0
    except Exception as error:
        report['status'] = 'FAIL'; report['error'] = str(error)
        (out / 'failure.txt').write_text(traceback.format_exc())
        print('FAIL:', error, flush=True)
        return 1
    finally:
        report['finished_at_epoch'] = time.time(); save()
        files = {str(p.relative_to(out)): {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
                 for p in sorted(out.rglob('*')) if p.is_file() and p.suffix != '.olean' and p.name != 'FILES.json'}
        (out / 'FILES.json').write_text(json.dumps(files, indent=2)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
