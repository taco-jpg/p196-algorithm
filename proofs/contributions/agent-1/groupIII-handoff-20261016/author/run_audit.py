from pathlib import Path
import hashlib, json, re, subprocess, time

ROOT = Path('/workspace/p196-agent1-handoff-20261016')
BUILD = Path('/workspace/p196-agent1-session-20261016/handoff-author-build')
OUT = ROOT/'proofs/contributions/agent-1/groupIII-handoff-20261016/author/audit-001'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
ENV = {'PATH':str(LEAN.parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LEAN_PATH':str(BUILD)}
OUT.mkdir(exist_ok=False)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
modules = ['Agent1GroupIIIHandoff','Agent1GroupIIIHandoffNumeric']
names = []
sources = {}
for mod in modules:
    src = ROOT/'proofs'/(mod+'.lean')
    assert src.read_bytes() == (BUILD/(mod+'.lean')).read_bytes()
    sources[mod] = {'source_sha256':sha(src),'object_sha256':sha(BUILD/(mod+'.olean'))}
    names += ['P196.Agent1.GroupIIIHandoff.'+name for name in re.findall(r'^theorem\s+(\w+)',src.read_text(),re.M)]
audit = 'import Agent1GroupIIIHandoffNumeric\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
audit += '\n'.join('#check '+name+'\n#print axioms '+name for name in names)
audit += '''
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let selected : List String := ["Agent1GroupIIIHandoff", "Agent1GroupIIIHandoffNumeric"]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"MODULE_AUDIT theorems={count} union={union}"
'''
(BUILD/'AuthorAudit.lean').write_text(audit)
(OUT/'AuthorAudit.lean').write_text(audit)
argv = [str(LEAN),'--trust=0','-j1','-DElab.async=false','AuthorAudit.lean']
t = time.monotonic()
with (OUT/'AuthorAudit.log').open('wb') as stream:
    rc = subprocess.run(argv,cwd=BUILD,env=ENV,stdout=stream,stderr=subprocess.STDOUT,timeout=300).returncode
log = (OUT/'AuthorAudit.log').read_text()
rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : (.*)$',log,re.M)
totals = re.findall(r'^MODULE_AUDIT theorems=(\d+) union=(.*)$',log,re.M)
printed = re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)",log)
status = 'PASS' if rc == 0 and len(totals)==1 and int(totals[0][0])==len(rows) and set(names)<=set(r[1] for r in rows) and set(names)==set(printed) else 'FAIL'
record = {'status':status,'exit_code':rc,'argv':argv,'cwd':str(BUILD),'environment':ENV,'seconds':time.monotonic()-t,'compiler_sha256':sha(LEAN),'source_objects':sources,'public_endpoints':names,'literal_print_count':len(printed),'all_new_theorem_count':len(rows),'totals':totals,'audit_source_sha256':sha(OUT/'AuthorAudit.lean'),'audit_log_sha256':sha(OUT/'AuthorAudit.log'),'independent_clean_rebuild':False}
(OUT/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
raise SystemExit(0 if status == 'PASS' else 1)
