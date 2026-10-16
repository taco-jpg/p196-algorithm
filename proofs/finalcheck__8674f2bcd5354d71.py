from pathlib import Path
import hashlib, json, os, re, subprocess, time
REPO=Path('/workspace/scratch/50e90e07524e/p196-agent106')
DIR=REPO/'proofs/contributions/agent-106/run-births'
SRC=DIR/'RepeatedBirths.lean'
DEV=DIR/'development/repeated'
LEAN=Path('/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean')
PRELOAD=Path('/workspace/scratch/50e90e07524e/runtime/readlink_self.so')
BASE=REPO/'proofs/research/continuation/LychrelDigitSums.lean'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
env=dict(os.environ, LD_PRELOAD=str(PRELOAD),LEAN_PATH='/workspace/scratch/50e90e07524e/build106')
env.pop('LEAN_SRC_PATH',None)
env.pop('LEAN_SYSROOT',None)
cmd=[str(LEAN),'-j1','-DElab.async=false',str(SRC)]
start=time.monotonic()
proc=subprocess.run(cmd,cwd=REPO,env=env,text=True,capture_output=True)
output=proc.stdout+proc.stderr
(DEV/'finalcheck.log').write_text(output)
expected={'RunBirths.RepeatedBirths.'+n for n in re.findall(r'^theorem ([A-Za-z0-9_]+)',SRC.read_text(),re.M)}
found={}
for n,aa in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output):
 found[n]=[a.strip() for a in aa.split(',') if a.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",output): found[n]=[]
allowed={'propext','Classical.choice','Quot.sound'}
passed=(proc.returncode==0 and set(found)==expected and
 all(set(aa)<=allowed for aa in found.values()) and
 not any(x in output for x in ['error:','sorryAx','Lean.ofReduceBool','Lean.trustCompiler']))
report=dict(status='PASS' if passed else 'FAIL',exit_code=proc.returncode,seconds=time.monotonic()-start,
 source_sha256=sha(SRC),base_source_sha256=sha(BASE),compiler_sha256=sha(LEAN),preload_sha256=sha(PRELOAD),
 command=cmd,version=subprocess.check_output([str(LEAN),'--version'],env=env,text=True).strip(),
 axioms=found,log_sha256=sha(DEV/'finalcheck.log'))
(DEV/'finalcheck.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],len(found),'theorems',report['source_sha256'],round(report['seconds'],2),flush=True)
raise SystemExit(0 if passed else 1)
