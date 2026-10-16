#!/usr/bin/env python3
"""After the merged checker exits, obtain an independent inventory and finalize.

This waits without running a compiler. Its single inventory compiler starts
only after the original full build/audit has completely released its slot.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

WORK = Path('/workspace/scratch/7649db1e242c/build104-integrated')
SNAPSHOT = WORK / 'rebuild/snapshot'


def main():
    while True:
        try:
            invocation = json.loads((WORK / 'invocation.json').read_text())
        except (OSError, json.JSONDecodeError):
            time.sleep(2)
            continue
        if 'checker_exit_code' in invocation:
            break
        if invocation.get('status') == 'FAIL':
            raise RuntimeError(invocation)
        time.sleep(2)
    if invocation['checker_exit_code'] != 0:
        raise RuntimeError('Original checker failed; no acceptance attempted')
    report = json.loads((WORK / 'rebuild/verification.json').read_text())
    assert report['status'] == 'PASS'
    selected = ', '.join(json.dumps(m) for m in report['build_order'])
    source = '''import Conclusion739
import TerminalObstruction
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [''' + selected + ''']
  let mut names : Array (String × String) := #[]
  let mut privateCount : Nat := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .thmInfo _ =>
          names := names.push (mod.toString, name.toString)
          if name.toString.startsWith "_private." then
            privateCount := privateCount + 1
        | _ => pure ()
  logInfo m!"INVENTORY_TOTAL_THEOREMS {names.size}"
  logInfo m!"INVENTORY_PRIVATE_NAME_THEOREMS {privateCount}"
  for mod in selected do
    let count := (names.filter (fun pair => pair.1 == mod)).size
    logInfo m!"INVENTORY_MODULE {mod} {count}"
'''
    (WORK / 'InventoryOnly.lean').write_text(source)
    (SNAPSHOT / 'InventoryOnly.lean').write_text(source)
    env = dict(os.environ)
    for key in ('LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT'):
        env.pop(key, None)
    env['LEAN_PATH'] = str(SNAPSHOT)
    command = ['/workspace/scratch/7649db1e242c/toolchain/lean', '-j1', '-DElab.async=false', 'InventoryOnly.lean']
    started = time.monotonic()
    print('Original full checker PASS; starting post-build inventory-only cross-check.', flush=True)
    with (WORK / 'inventory-only.log').open('w') as out:
        proc = subprocess.Popen(command, cwd=SNAPSHOT, env=env, stdout=out, stderr=subprocess.STDOUT)
        _, status, usage = os.wait4(proc.pid, 0)
        proc.returncode = os.waitstatus_to_exitcode(status)
    result = {
        'command': command, 'cwd': str(SNAPSHOT), 'exit_code': proc.returncode,
        'seconds': time.monotonic() - started,
        'user_cpu_seconds': usage.ru_utime, 'system_cpu_seconds': usage.ru_stime,
        'maximum_resident_set_kib': usage.ru_maxrss,
        'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
        'log_sha256': hashlib.sha256((WORK / 'inventory-only.log').read_bytes()).hexdigest(),
        'scope': 'Independent inventory only after full checker completion; no theorem axiom gate replaced or weakened.',
        'finished_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    (WORK / 'inventory-only.json').write_text(json.dumps(result, indent=2) + '\n')
    assert proc.returncode == 0, result
    with (WORK / 'finalization-output.log').open('w') as out:
        final = subprocess.run(['python', str(WORK / 'independent_finalize.py')], stdout=out, stderr=subprocess.STDOUT)
    print(f'Independent merged finalization exit: {final.returncode}', flush=True)
    if final.returncode:
        print((WORK / 'finalization-output.log').read_text(), flush=True)
        raise RuntimeError('Final acceptance failed; preserve all diagnostics')


if __name__ == '__main__':
    main()
