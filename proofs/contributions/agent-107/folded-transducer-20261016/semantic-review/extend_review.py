#!/usr/bin/env python3
"""向同一次空目录独立重建追加已冻结模块，保留全部先前记录与审计日志。"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
from rebuild_review import lean_code, sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--lean', type=Path, default=Path('/workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean'))
    parser.add_argument('--modules', nargs='+', required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    logdir, build = args.manifest.parent.resolve(), Path(manifest['build_dir'])
    env = dict(os.environ, LEAN_PATH=str(build))
    assert manifest['build_dir_initially_empty'] is True
    assert manifest['status'] == 'INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS'
    assert subprocess.check_output([str(args.lean), '--version'], text=True).strip() == manifest['lean_version']
    for entry in manifest['source_files']:
        source, copy = args.repo / entry['source'], build / (entry['module'] + '.lean')
        assert sha(source) == sha(copy) == entry['sha256'] == entry['copied_sha256'], entry['source']
        assert (build / (entry['module'] + '.olean')).is_file()
        assert any(run['name'] == 'build-' + entry['module'] and run['exit_code'] == 0 for run in manifest['executions'])
    known = {entry['module'] for entry in manifest['source_files']}
    assert not known.intersection(args.modules), '已经核验的模块不能被静默覆盖'
    assert len(args.modules) == len(set(args.modules))
    iteration = 1 + len(manifest.setdefault('extensions', []))
    manifest['extensions'].append({
        'iteration': iteration, 'modules': args.modules,
        'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.repo, text=True).strip(),
        'previous_verified_sources_checked_unchanged': True,
    })

    def save():
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    def run(name, command):
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
        print(json.dumps({'stage': name, 'exit_code': result.returncode}), flush=True)
        if result.returncode:
            raise RuntimeError('编译或审计失败：' + name)

    try:
        manifest['status'] = 'IN_PROGRESS_EXTENSION'
        save()
        forbidden = re.compile(r'\b(sorry|admit|sorryAx|axiom|native_decide|unsafe|ofReduceBool|ofReduceNat)\b')
        for module in args.modules:
            source, copy = args.repo / 'proofs' / (module + '.lean'), build / (module + '.lean')
            matches = sorted(set(forbidden.findall(lean_code(source.read_text()))))
            assert not matches, (source, matches)
            assert not copy.exists() and not copy.with_suffix('.olean').exists(), module
            shutil.copy2(source, copy)
            manifest['source_files'].append({
                'module': module, 'source': str(source.relative_to(args.repo)),
                'sha256': sha(source), 'copied_sha256': sha(copy),
                'forbidden_code_markers': matches,
            })
        save()
        for module in args.modules:
            run('build-' + module, [str(args.lean), '--trust=0', '-j1', '-DElab.async=false',
                '-o', str(build / (module + '.olean')), str(build / (module + '.lean'))])
        modules = [entry['module'] for entry in manifest['source_files'] if entry['module'] != 'Lychrel196Research']
        audit_name = 'IndependentAxiomAudit_extension_' + str(iteration)
        audit = build / (audit_name + '.lean')
        audit.write_text('import Lean\n' + ''.join('import ' + module + '\n' for module in modules) + '''
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
        run('all-exported-axioms-extension-' + str(iteration), [str(args.lean), '--trust=0', '-j1', '-DElab.async=false', str(audit)])
        for entry in manifest['source_files']:
            assert sha(args.repo / entry['source']) == entry['sha256'], entry['source']
        manifest['status'] = 'INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS'
        manifest['extensions'][-1]['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        manifest['finished_utc'] = manifest['extensions'][-1]['finished_utc']
        save()
        print(json.dumps({'status': manifest['status'], 'evidence_dir': str(logdir)}), flush=True)
        return 0
    except Exception as error:
        manifest['status'] = 'FAILED_EXTENSION'
        manifest['error'] = repr(error)
        save()
        print(json.dumps({'status': manifest['status'], 'error': repr(error)}, ensure_ascii=False), flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
