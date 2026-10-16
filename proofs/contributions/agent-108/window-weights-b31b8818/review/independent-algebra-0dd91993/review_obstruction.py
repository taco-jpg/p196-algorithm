#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,os,hashlib,re,time,sys
BASE=Path(__file__).resolve().parent.parent
SOURCE=BASE/'agent108-work/proofs'
OUT=SOURCE/'contributions/agent-108/window-weights-b31b8818/review/independent-algebra-0dd91993'
OUT.mkdir(parents=True,exist_ok=False)
SRC=OUT/'source'
BUILD=OUT/'build'
LOG=OUT/'logs'
for p in [SRC,BUILD,LOG]:p.mkdir()
fixed={'Agent108WindowDefs.lean':'147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0','Agent108WindowObstruction.lean':'0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a'}
for name,digest in fixed.items():
    data=(SOURCE/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==digest,(name,'source hash changed')
    (SRC/name).write_bytes(data)
wrapper=BASE/'agent108-runtime/lean-with-mathlib.sh'
env=dict(os.environ,LEAN_PATH=str(BUILD))
results=[]
def run(name,args):
    t=time.time()
    p=subprocess.run([str(wrapper),'--trust=0',*args],cwd=SRC,env=env,capture_output=True,text=True)
    (LOG/(name+'.stdout.log')).write_text(p.stdout)
    (LOG/(name+'.stderr.log')).write_text(p.stderr)
    rec={'name':name,'command':[str(wrapper),'--trust=0',*args],'cwd':str(SRC),'exit_code':p.returncode,'seconds':time.time()-t}
    results.append(rec)
    (OUT/'build-results.json').write_text(json.dumps({'source_sha256':fixed,'records':results,'finished':False},indent=2)+'\n')
    print(json.dumps(rec),flush=True)
    if p.returncode:raise SystemExit(p.returncode)
for name in fixed:
    run(name,['-o',str(BUILD/(Path(name).stem+'.olean')),name])
decls=[]
for name in fixed:
    text=(SRC/name).read_text()
    for kind,decl in re.findall(r'^(?:noncomputable )?(def|theorem|abbrev)\s+([A-Za-z0-9_]+)',text,re.M):
        decls.append({'module':Path(name).stem,'kind':kind,'name':'Agent108.WindowWeights.'+decl})
audit='import Agent108WindowObstruction\n\n'+'\n'.join('#print axioms '+d['name'] for d in decls)+'\n'
(SRC/'IndependentAlgebraAudit.lean').write_text(audit)
run('audit',['IndependentAlgebraAudit.lean'])
log=(LOG/'audit.stdout.log').read_text()
bad=[]
allowed={'propext','Classical.choice','Quot.sound'}
for line in log.splitlines():
    if 'depends on axioms:' in line:
        found=set(re.search(r'\[(.*)\]',line).group(1).replace(' ','').split(','))-{''}
        if not found<=allowed:bad.append(line)
proof_terms=sum('depends on axioms:' in line or 'does not depend on any axioms' in line for line in log.splitlines())
assert proof_terms==len(decls),(proof_terms,len(decls))
final={'reviewer':'Agent108 claims_inventory','source_sha256':fixed,'records':results,'finished':True,'declarations':decls,'audited_declarations':len(decls),'unexpected_axioms':bad,'all_pass':not bad and all(x['exit_code']==0 for x in results),'scope':'Algebraic conditional interface only. No identification of arbitrary incoming parameter with actual P196 safe incoming operator.'}
(OUT/'build-results.json').write_text(json.dumps(final,indent=2)+'\n')
print(json.dumps({'all_pass':final['all_pass'],'declarations':len(decls),'unexpected_axioms':bad}),flush=True)
raise SystemExit(0 if final['all_pass'] else 1)
