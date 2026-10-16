#!/usr/bin/env python3
"""独立空目录重建与全量传递公理审计；只读取贡献源码，不执行 Git 写入。"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lean_code(source: str) -> str:
    """去掉嵌套注释、行注释、字符串，避免把文档措辞当代码。"""
    out, pos, depth = [], 0, 0
    while pos < len(source):
        if depth:
            if source.startswith('/-', pos):
                depth += 1
                pos += 2
            elif source.startswith('-/', pos):
                depth -= 1
                pos += 2
            else:
                pos += 1
        elif source.startswith('/-', pos):
            depth = 1
            pos += 2
            out.append(' ')
        elif source.startswith('--', pos):
            end = source.find('\n', pos)
            pos = len(source) if end < 0 else end
            out.append(' ')
        elif source[pos] == '"':
            pos += 1
            while pos < len(source):
                if source[pos] == '\\':
                    pos += 2
                elif source[pos] == '"':
                    pos += 1
                    break
                else:
                    pos += 1
            out.append(' ')
        else:
            out.append(source[pos])
            pos += 1
    if depth:
        raise RuntimeError('未闭合的 Lean 注释')
    return ''.join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--lean', type=Path, default=Path('/workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean'))
    parser.add_argument('--runtime', type=Path, default=Path('/workspace/scratch/94808c4aecb2/agent107-runtime'))
    parser.add_argument('--modules', nargs='+', default=[
        'Agent107TransducerDefs', 'Agent107TransducerPath', 'Agent107TransducerInput',
        'Agent107TransducerTablesData', 'Agent107TransducerTablesChecks',
        'Agent107TransducerTables', 'Agent107TransducerOutput',
        'Agent107TransducerNumeric', 'Agent107TransducerBoundary'])
    args = parser.parse_args()
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    logdir = Path(__file__).resolve().parent / ('clean-rebuild-' + stamp)
    logdir.mkdir()
    build = Path(tempfile.mkdtemp(prefix='reviewer-empty-', dir=args.runtime))
    env = dict(os.environ, LEAN_PATH=str(build))
    manifest = {
        'reviewer': '/root/semantic_review',
        'status': 'IN_PROGRESS',
        'started_utc': stamp,
        'build_dir': str(build),
        'build_dir_initially_empty': not any(build.iterdir()),
        'lean_path': env['LEAN_PATH'],
        'lean_version': subprocess.check_output([str(args.lean), '--version'], text=True).strip(),
        'git_head_at_start': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.repo, text=True).strip(),
        'source_files': [],
        'executions': [],
    }

    def save() -> None:
        (logdir / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    def run(name: str, command: list[str]) -> None:
        start = time.monotonic()
        result = subprocess.run(command, cwd=build, env=env, text=True, capture_output=True)
        (logdir / (name + '.stdout.log')).write_text(result.stdout)
        (logdir / (name + '.stderr.log')).write_text(result.stderr)
        manifest['executions'].append({
            'name': name, 'command': command, 'cwd': str(build),
            'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - start,
            'stdout_log': name + '.stdout.log', 'stderr_log': name + '.stderr.log',
        })
        save()
        print(json.dumps({'stage': name, 'exit_code': result.returncode}, ensure_ascii=False), flush=True)
        if result.returncode:
            raise RuntimeError('编译或审计失败：' + name)

    save()
    try:
        originals = [('Lychrel196Research', args.repo / 'proofs/Lychrel196Research__c696e0ea3db39d92.lean')]
        originals += [(name, args.repo / 'proofs' / (name + '.lean')) for name in args.modules]
        forbidden = re.compile(r'\b(sorry|admit|sorryAx|axiom|native_decide|unsafe|ofReduceBool|ofReduceNat)\b')
        for module, source in originals:
            code = lean_code(source.read_text())
            matches = sorted(set(forbidden.findall(code)))
            if matches:
                raise RuntimeError(f'{source} 含禁止代码标记：{matches}')
            copied = build / (module + '.lean')
            shutil.copy2(source, copied)
            manifest['source_files'].append({
                'module': module,
                'source': str(source.relative_to(args.repo)),
                'sha256': sha(source),
                'copied_sha256': sha(copied),
                'forbidden_code_markers': matches,
            })
        save()
        for module, _ in originals:
            run('build-' + module, [str(args.lean), '--trust=0', '-j1', '-DElab.async=false',
                '-o', str(build / (module + '.olean')), str(build / (module + '.lean'))])
        audit = build / 'IndependentAxiomAudit.lean'
        audit.write_text('import Lean\n' + ''.join('import ' + name + '\n' for name in args.modules) + '''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    let sourceModule : Lean.Name := match env.getModuleIdxFor? name with
      | none => Name.anonymous
      | some idx => env.allImportedModuleNames[idx.toNat]!
    if "Agent107Transducer".isPrefixOf (toString sourceModule) then
      if let .thmInfo _ := info then
        count := count + 1
        logInfo m!"DECLARATION_ORIGIN {sourceModule}: {name}"
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Unapproved axiom: {name} uses {ax}"
  logInfo m!"Audited {count} Agent107Transducer module-origin theorem declarations, including private and generated proof lemmas."
''')
        shutil.copy2(audit, logdir / audit.name)
        run('all-exported-axioms', [str(args.lean), '--trust=0', '-j1', '-DElab.async=false', str(audit)])
        for entry in manifest['source_files']:
            if sha(args.repo / entry['source']) != entry['sha256']:
                raise RuntimeError('重建期间源码发生变化：' + entry['source'])
        manifest['status'] = 'INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS'
        manifest['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save()
        print(json.dumps({'status': manifest['status'], 'evidence_dir': str(logdir)}, ensure_ascii=False), flush=True)
        return 0
    except Exception as error:
        manifest['status'] = 'FAILED'
        manifest['error'] = repr(error)
        save()
        print(json.dumps({'status': manifest['status'], 'error': repr(error), 'evidence_dir': str(logdir)}, ensure_ascii=False), flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
