#!/usr/bin/env python3
"""Fresh pinned closure build; audit adapted from retained repository verifier.

Authorized review claim: 3b2c5a05ca25b173aacdd080123ddd43f6282e7d.
Published isolated repair head: 50ce06bcdfec473f0e1348123d2f17e5b854fd2b. Every run gets a new directory.
No generated object is read from the author's build or the checkout.
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import runpy
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[4]
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
PINS = REVIEW/'source-pins.json'
VERIFIER = ROOT/'proofs/verify_project__214bf7673efe116b.py'
CODE_ONLY = runpy.run_path(str(VERIFIER))['code_only']
ORDER = ['LychrelDigitSums', 'SafeDelay', 'DecimalSafeRuns', 'DecimalDelayBridge',
         'PairDelayBridge', 'DelayedOverlapGate', 'Agent114ShortRFirst11']
ROOT_MODULE = 'Agent114ShortRFirst11'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    label = sys.argv[1]
    if not re.fullmatch(r'[A-Za-z0-9_-]+', label):
        raise ValueError('Invalid run label')
    out = REVIEW/label
    out.mkdir(exist_ok=False)
    src = out/'source'
    logs = out/'logs'
    src.mkdir()
    logs.mkdir()
    env = {'PATH':str(LEAN.parent)+':/usr/bin:/bin', 'LANG':'C.UTF-8', 'LEAN_PATH':str(src)}
    report = {'status':'RUNNING', 'started_epoch':time.time(), 'source_snapshot':{},
              'commands':[], 'module_order':ORDER, 'environment':env,
              'scanner_source':str(VERIFIER), 'scanner_sha256':sha(VERIFIER.read_bytes()),
              'runner_sha256':sha(Path(__file__).read_bytes())}

    def save():
        (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')

    def command(label, argv):
        start = time.monotonic()
        log = logs/(label+'.log')
        with log.open('wb') as stream:
            try:
                rc = subprocess.run(argv, cwd=src, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=600).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        report['commands'].append({'label':label, 'argv':argv, 'exit_code':rc,
                                   'seconds':round(time.monotonic()-start,6),
                                   'log_sha256':sha(log.read_bytes())})
        save()
        print(label, 'exit='+str(rc), flush=True)
        if rc:
            raise RuntimeError('Failed '+label+'; see retained log')
        return log.read_text()

    try:
        version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
        if not re.search(r'version 4\.19\.0,.*commit 6caaee842e94, Release', version):
            raise ValueError('Wrong pinned compiler: '+version)
        runtime = Path(subprocess.check_output([str(LEAN), '--print-prefix'], text=True).strip())
        compiler_files = [LEAN, *sorted((runtime/'lib/lean').glob('*.so'))]
        report['compiler'] = {'version':version, 'files':{str(p):sha(p.read_bytes()) for p in compiler_files}}
        pinned = json.loads(PINS.read_text())
        report['pins_sha256'] = sha(PINS.read_bytes())
        report['source_commit'] = '50ce06bcdfec473f0e1348123d2f17e5b854fd2b'
        report['review_claim_commit'] = '3b2c5a05ca25b173aacdd080123ddd43f6282e7d'
        originals, endpoints = {}, []
        for name in ORDER:
            pin = pinned[name]
            path = ROOT/pin['source']
            raw = path.read_bytes()
            digest = sha(raw)
            blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if name in pinned and (digest != pin['sha256'] or blob != pin['git_blob']):
                raise ValueError('Pinned source changed: '+name)
            code = CODE_ONLY(raw.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code):
                raise ValueError('Forbidden source token: '+name)
            imports = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for d in line.split()]
            for dep in imports:
                if dep in ORDER and ORDER.index(dep) >= ORDER.index(name):
                    raise ValueError('Unexpected dependency order: '+name+' '+dep)
                if dep not in ORDER:
                    if dep.split('.')[0] not in {'Init','Std','Lean'} or not (runtime/'lib/lean'/(dep.replace('.','/')+'.olean')).is_file():
                        raise ValueError('Unregistered import: '+dep)
            if name == ROOT_MODULE:
                namespaces = re.findall(r'^namespace\s+(\S+)', code, re.M)
                if namespaces != ['Agent114.ShortR']:
                    raise ValueError('Inspect changed namespace layout before audit: '+str(namespaces))
                endpoints += ['Agent114.ShortR.'+x for x in re.findall(r'^theorem\s+([\w\x27]+)', code, re.M)]
            originals[name] = (path, raw)
            (src/(name+'.lean')).write_bytes(raw)
            report['source_snapshot'][name] = {'source':str(path), 'sha256':digest, 'git_blob':blob, 'imports':imports}
        if not endpoints:
            raise ValueError('No new public theorem endpoints')
        # Confirm exact reachability from the frozen repaired root.
        reached = set()
        def visit(name):
            if name in reached:
                return
            reached.add(name)
            for dep in report['source_snapshot'][name]['imports']:
                if dep in ORDER:
                    visit(dep)
        visit(ROOT_MODULE)
        if reached != set(ORDER):
            raise ValueError('Selected modules are not exactly the new roots import closure')
        report['public_new_endpoints'] = endpoints
        save()
        for name in ORDER:
            command(name, [str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',name+'.olean',name+'.lean'])
        audit = 'import Agent114ShortRFirst11\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
        audit += '\n'.join('#check @'+name+'\n#print axioms '+name for name in endpoints)
        audit += '\nrun_cmd do\n  let env ← getEnv\n  let selected : List String := '+json.dumps(ORDER)+'''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut safeDefs := 0
  let mut safeOpaques := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .defnInfo v =>
          if v.safety != .safe then logInfo m!"NON_SAFE_DEFINITION {mod} {name} {repr v.safety}"
        | .opaqueInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_OPAQUE {mod} {name}"
        | _ => pure ()
        let kind : Option String := match info with
          | .thmInfo _ => some "THEOREM"
          | .defnInfo v => if v.safety == .safe then some "SAFE_DEFINITION" else none
          | .opaqueInfo v => if !v.isUnsafe then some "SAFE_OPAQUE" else none
          | _ => none
        if let some kind := kind then
          if kind == "THEOREM" then count := count + 1
          else if kind == "SAFE_DEFINITION" then safeDefs := safeDefs + 1
          else safeOpaques := safeOpaques + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {kind} {mod} {name} : {axl}"
          logInfo m!"AUDIT_{kind} {mod} {name} : {axl}"
  logInfo m!"SAFE_DEFINITION_AUDIT definitions={safeDefs} opaque={safeOpaques}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
'''
        (src/'IndependentAudit.lean').write_text(audit)
        audit_log = command('IndependentAudit', [str(LEAN),'--trust=0','-j1','-DElab.async=false','IndependentAudit.lean'])
        totals = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$', audit_log, re.M)
        rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$', audit_log, re.M)
        if len(totals) != 1 or int(totals[0][0]) != len(rows) or not rows or len({r[1] for r in rows}) != len(rows):
            raise ValueError('Incomplete or duplicate audit')
        if not set(endpoints) <= {r[1] for r in rows}:
            raise ValueError('Public endpoint absent from module-origin audit')
        safe_totals = re.findall(r'^SAFE_DEFINITION_AUDIT definitions=(\d+) opaque=(\d+)$', audit_log, re.M)
        safe_rows = re.findall(r'^AUDIT_SAFE_DEFINITION (\S+) (\S+) : (.*)$', audit_log, re.M)
        opaque_rows = re.findall(r'^AUDIT_SAFE_OPAQUE (\S+) (\S+) : (.*)$', audit_log, re.M)
        if len(safe_totals) != 1 or int(safe_totals[0][0]) != len(safe_rows) or int(safe_totals[0][1]) != len(opaque_rows):
            raise ValueError('Incomplete safe definition audit')
        if len({row[1] for row in rows + safe_rows + opaque_rows}) != len(rows + safe_rows + opaque_rows):
            raise ValueError('Duplicate theorem/definition audit entries')
        report['safe_definition_count'] = len(safe_rows)
        report['safe_definition_count_by_module'] = dict(collections.Counter(row[0] for row in safe_rows))
        report['safe_opaque_count'] = len(opaque_rows)
        report['safe_opaque_count_by_module'] = dict(collections.Counter(row[0] for row in opaque_rows))
        report['non_safe_definitions'] = re.findall(r'^NON_SAFE_DEFINITION (\S+) (\S+) (.*)$', audit_log, re.M)
        report['unsafe_opaques'] = re.findall(r'^UNSAFE_OPAQUE (\S+) (\S+)$', audit_log, re.M)
        report['theorem_count'] = len(rows)
        report['theorem_count_by_module'] = dict(collections.Counter(row[0] for row in rows))
        report['axiom_union'] = totals[0][1]
        report['unsafe_implementation_axioms'] = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit_log, re.M)
        for name, (path, raw) in originals.items():
            if path.read_bytes() != raw or (src/(name+'.lean')).read_bytes() != raw:
                raise ValueError('Source changed during run: '+name)
        for path, digest in report['compiler']['files'].items():
            if sha(Path(path).read_bytes()) != digest:
                raise ValueError('Compiler changed during run')
        report['status'] = 'PASS_INDEPENDENT_FRESH_BUILD_AND_AXIOM_AUDIT'
        return 0
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = str(exc)
        (out/'failure.txt').write_text(traceback.format_exc())
        print('FAIL', str(exc), flush=True)
        return 1
    finally:
        report['finished_epoch'] = time.time()
        save()
        inventory = {str(p.relative_to(out)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
                     for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'FILES.json'}
        (out/'FILES.json').write_text(json.dumps(inventory, indent=2)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
