#!/usr/bin/env python3
"""Literal public prints plus complete new-module theorem/definition axiom audit."""
from pathlib import Path
import hashlib,json,os,re,resource,shutil,subprocess,sys,time

ROOT=Path('/workspace/p196-agent1-width-20261016')
AUTHOR=ROOT/'proofs/contributions/agent-1/periodic-width-projection-20261016/width-path-author'
BUILD=AUTHOR/sys.argv[1]
OUT=AUTHOR/sys.argv[2]
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE='Agent1PeriodicWidthPath'
OUT.mkdir(exist_ok=False)
shutil.copy2(Path(__file__),OUT/'audit-driver.py')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
src=ROOT/'proofs'/(MODULE+'.lean')
assert src.read_bytes()==(BUILD/src.name).read_bytes()
compile_record=json.loads((BUILD/'run.json').read_text())
assert compile_record['exit_code']==0
assert compile_record['source_sha256']==sha(src)
assert compile_record['olean_sha256']==sha(BUILD/(MODULE+'.olean'))
names=['Agent1.Periodic.'+n for n in re.findall(r'^theorem\s+(\w+)',src.read_text(),re.M)]
definitions=['Agent1.Periodic.'+n for n in re.findall(r'^def\s+(\w+)',src.read_text(),re.M)]
assert len(names)==2 and definitions==['Agent1.Periodic.QuotientPath','Agent1.Periodic.quotientClockSum','Agent1.Periodic.quotientDeltaSum']
audit='import Agent1PeriodicWidthPath\nimport Lean\nopen Lean Elab Command\n'
audit+='\n'.join('#check '+name+'\n#print axioms '+name for name in definitions+names)
audit+='''
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicWidthPath" then
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
        | .defnInfo v =>
          if v.safety != .safe then
            if !(["Agent1.Periodic.quotientClockSum._cstage1", "Agent1.Periodic.quotientClockSum._cstage2",
                  "Agent1.Periodic.quotientDeltaSum._cstage1", "Agent1.Periodic.quotientDeltaSum._cstage2"].contains name.toString) then
              throwError m!"NONCOMPILER_NONSAFE_DEFINITION {mod} {name}"
            logInfo m!"COMPILER_IMPLEMENTATION_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_DEFINITION {mod} {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {mod} {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} definitions={defs} union={union}"
'''
(OUT/'WidthPathAudit.lean').write_text(audit)
argv=[str(LEAN),'--trust=0','-j1','-DElab.async=false','WidthPathAudit.lean']
lean_path=compile_record['LEAN_PATH']
record=dict(command=argv,cwd=str(OUT),LEAN_PATH=lean_path,source_sha256=sha(src),
    object_sha256=sha(BUILD/(MODULE+'.olean')),compiler_sha256=sha(LEAN),
    public_theorems=names,public_definitions=definitions,started_at_epoch=time.time(),
    independent_clean_rebuild=False)
(OUT/'run.json').write_text(json.dumps(record,indent=2)+'\n')
cpu=min(os.sched_getaffinity(0))
address_cap=1900*1024*1024
def child_limits():
    resource.setrlimit(resource.RLIMIT_AS,(address_cap,address_cap))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    os.sched_setaffinity(0,{cpu})
record.update(cpu_affinity=[cpu],virtual_address_cap_bytes=address_cap)
start=time.monotonic()
with (OUT/'WidthPathAudit.log').open('w') as log:
    rc=subprocess.run(argv,cwd=OUT,env=dict(os.environ,LEAN_PATH=lean_path),
                      stdout=log,stderr=subprocess.STDOUT,preexec_fn=child_limits).returncode
log=(OUT/'WidthPathAudit.log').read_text()
rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$',log,re.M)
defs=re.findall(r'^AUDIT_DEFINITION (\S+) (\S+) : (.*)$',log,re.M)
implementations=re.findall(r'^COMPILER_IMPLEMENTATION_DEFINITION (\S+) (\S+)$',log,re.M)
totals=re.findall(r'^MODULE_AUDIT theorems=(\d+) definitions=(\d+) union=(.*)$',log,re.M)
printed=re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)",log)
passed=rc==0 and len(totals)==1 and int(totals[0][0])==len(rows) and int(totals[0][1])==len(defs)
passed=passed and set(names)<=set(r[1] for r in rows) and set(names+definitions)==set(printed)
passed=passed and set(definitions)<=set(r[1] for r in defs)
record.update(peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,status='PASS' if passed else 'FAIL',exit_code=rc,seconds=time.monotonic()-start,
    literal_print_count=len(printed),all_new_theorem_count=len(rows),
    all_new_safe_definition_count=len(defs),totals=totals,finished_at_epoch=time.time(),
    compiler_implementation_definitions=implementations,
    audit_source_sha256=sha(OUT/'WidthPathAudit.lean'),audit_log_sha256=sha(OUT/'WidthPathAudit.log'))
(OUT/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if not passed: print(log)
raise SystemExit(0 if passed else 1)
