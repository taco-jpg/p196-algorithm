#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, os, re, subprocess, time

ROOT = Path('/workspace/p196-agent1-validity-20261016')
BUILD = Path('/workspace/p196-agent1-session-20261016/periodic-positive-author-build')
OUT = ROOT/'proofs/contributions/agent-1/periodic-validity-20261016/positive-author/audit-001'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE = 'Agent1PeriodicPositivity'
OUT.mkdir(exist_ok=False)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
src = ROOT/'proofs'/(MODULE+'.lean')
assert src.read_bytes() == (BUILD/src.name).read_bytes()
names = ['Agent1.Periodic.'+n for n in re.findall(r'^theorem\s+(\w+)', src.read_text(), re.M)]
audit = 'import Agent1PeriodicPositivity\nimport Lean\nopen Lean Elab Command\n'
audit += '\n'.join('#check '+name+'\n#print axioms '+name for name in names)
audit += '''
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicPositivity" then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} union={union}"
'''
(BUILD/'PositiveAudit.lean').write_text(audit)
(OUT/'PositiveAudit.lean').write_text(audit)
argv = [str(LEAN),'--trust=0','-j1','-DElab.async=false','PositiveAudit.lean']
started = time.monotonic()
with (OUT/'PositiveAudit.log').open('w') as stream:
    rc = subprocess.run(argv, cwd=BUILD, env=dict(os.environ, LEAN_PATH=str(BUILD)),
                        stdout=stream, stderr=subprocess.STDOUT).returncode
log = (OUT/'PositiveAudit.log').read_text()
rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$', log, re.M)
totals = re.findall(r'^MODULE_AUDIT theorems=(\d+) union=(.*)$', log, re.M)
printed = re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)", log)
passed = rc == 0 and len(totals) == 1 and int(totals[0][0]) == len(rows)
passed = passed and set(names) <= set(r[1] for r in rows) and set(names) == set(printed)
record = dict(status='PASS' if passed else 'FAIL', exit_code=rc, command=argv,
              cwd=str(BUILD), LEAN_PATH=str(BUILD), seconds=time.monotonic()-started,
              source_sha256=sha(src), object_sha256=sha(BUILD/(MODULE+'.olean')),
              compiler_sha256=sha(LEAN), public_endpoints=names, literal_print_count=len(printed),
              all_new_theorem_count=len(rows), totals=totals,
              audit_source_sha256=sha(OUT/'PositiveAudit.lean'), audit_log_sha256=sha(OUT/'PositiveAudit.log'),
              independent_clean_rebuild=False)
(OUT/'run.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
raise SystemExit(0 if passed else 1)
