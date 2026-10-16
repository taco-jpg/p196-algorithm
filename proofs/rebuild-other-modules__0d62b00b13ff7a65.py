#!/usr/bin/env python3
"""Independent source-snapshot build; excludes reviewer's self-authored modules."""
from pathlib import Path
import hashlib, json, os, re, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent.parent
BUILD=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
LEAN=Path('/workspace/scratch/4e3a8a89dfc7/runtime/lean')
MODULES=['OuterBlock','ModulusSplit','PairWeights','PeriodExistence','Lychrel196Research','PalindromeDigits','DigitPools']
assert not BUILD.exists() and not OUT.exists(), 'Fresh directories required'
BUILD.mkdir(parents=True); OUT.mkdir(parents=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
report={'kind':'independent source-snapshot rebuild of other-authored modules','excluded_self_authored':['ModularSpan','ResidueOrbit'],'status':'RUNNING','sources':{},'commands':[]}
for m in MODULES:
 src=ROOT/'proofs/research/Lychrel196Research.lean' if m=='Lychrel196Research' else HERE/(m+'.lean')
 dst=BUILD/(m+'.lean');dst.write_bytes(src.read_bytes())
 report['sources'][m]={'path':str(src),'snapshot':str(dst),'sha256':sha(dst)}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
env=os.environ.copy()
for k in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT']:env.pop(k,None)
env['LEAN_PATH']=str(BUILD)
def run(label,cmd):
 start=time.monotonic()
 with (OUT/(label+'.log')).open('wb') as f:r=subprocess.run(cmd,cwd=BUILD,env=env,stdout=f,stderr=subprocess.STDOUT)
 report['commands'].append({'label':label,'command':cmd,'exit_code':r.returncode,'seconds':time.monotonic()-start,'log_sha256':sha(OUT/(label+'.log'))})
 (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(label,r.returncode,flush=True)
 if r.returncode:raise RuntimeError('Compilation failed: '+label)
 return (OUT/(label+'.log')).read_text()
try:
 run('version',[str(LEAN),'--version'])
 for m in MODULES:run(m,[str(LEAN),'-j1','-DElab.async=false','-o',m+'.olean',m+'.lean'])
 audit='\n'.join('import '+m for m in MODULES)+'\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\nrun_cmd do\n  let env ← getEnv\n  let selected : List String := '+str(MODULES).replace("'",'"')+'\n  for (name, info) in env.constants.toList do\n    if let some idx := env.getModuleIdxFor? name then\n      let mod := env.allImportedModuleNames[idx.toNat]!\n      if selected.contains mod.toString then\n        match info with\n        | .axiomInfo ax =>\n          if ax.isUnsafe then\n            logInfo m!"UNSAFE_COMPILER_AXIOM {mod} {name}"\n          else throwError m!"CUSTOM_AXIOM {mod} {name}"\n        | .thmInfo _ =>\n          logInfo m!"REVIEW_THEOREM {mod} {name}"\n          elabCommand (← `(command| #print axioms $(mkIdent name)))\n        | _ => pure ()\n'
 (BUILD/'Audit.lean').write_text(audit);(OUT/'Audit.lean').write_text(audit)
 logs=run('Audit',[str(LEAN),'-j1','-DElab.async=false','-t0','Audit.lean'])
 inventory=re.findall(r'^REVIEW_THEOREM (\S+) (\S+)$',logs,re.M)
 records={}
 for z in re.finditer(r"^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",logs,re.M):
  vals=sorted(v.strip() for v in (z.group(2) or '').split(',') if v.strip())
  assert set(vals)<={'propext','Classical.choice','Quot.sound'},(z.group(1),vals)
  assert z.group(1) not in records
  records[z.group(1)]=vals
 assert set(records)=={n for _,n in inventory}
 report['theorems']={n:{'module':m,'axioms':records[n]} for m,n in inventory}
 report['theorem_count']=len(records)
 report['axiom_union']=sorted({v for a in records.values() for v in a})
 report['unchanged_sources']=all(sha(Path(d['path']))==d['sha256'] for d in report['sources'].values())
 report['status']='PASS'
except Exception as e:
 report['status']='FAIL';report['error']=str(e)
 raise
finally:
 (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
