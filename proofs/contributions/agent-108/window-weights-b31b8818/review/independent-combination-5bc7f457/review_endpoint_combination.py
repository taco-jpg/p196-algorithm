#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,os,hashlib,re,time
BASE=Path(__file__).resolve().parent.parent
SOURCE=BASE/'agent108-work/proofs'
OUT=SOURCE/'contributions/agent-108/window-weights-b31b8818/review/independent-combination-5bc7f457'
OUT.mkdir(parents=True,exist_ok=False)
SRC=OUT/'source';BUILD=OUT/'build';LOG=OUT/'logs'
for p in [SRC,BUILD,LOG]:p.mkdir()
fixed={
 'Agent108WindowDefs.lean':'147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0',
 'Agent108WindowProducts.lean':'2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584',
 'Agent108WindowWeights.lean':'5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae',
 'Agent108WindowEndpoints.lean':'ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22',
 'Agent108WindowEndpointWeights.lean':'21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1'
}
source_paths={name:str(SOURCE/name) for name in fixed}
for name,digest in fixed.items():
    data=Path(source_paths[name]).read_bytes()
    assert hashlib.sha256(data).hexdigest()==digest,(name,'source hash changed')
    (SRC/name).write_bytes(data)
wrapper=BASE/'agent108-runtime/lean-with-mathlib.sh'
env=dict(os.environ,LEAN_PATH=str(BUILD))
results=[]
def run(name,args):
    t=time.time()
    p=subprocess.run([str(wrapper),'--trust=0',*args],cwd=SRC,env=env,capture_output=True,text=True)
    (LOG/(name+'.stdout.log')).write_text(p.stdout);(LOG/(name+'.stderr.log')).write_text(p.stderr)
    rec={'name':name,'command':[str(wrapper),'--trust=0',*args],'cwd':str(SRC),'exit_code':p.returncode,'seconds':time.time()-t}
    results.append(rec)
    (OUT/'build-results.json').write_text(json.dumps({'source_sha256':fixed,'records':results,'finished':False},indent=2)+'\n')
    print(json.dumps(rec),flush=True)
    if p.returncode:raise SystemExit(p.returncode)
for name in fixed:run(name,['-o',str(BUILD/(Path(name).stem+'.olean')),name])
decls=[]
for name in fixed:
    text=(SRC/name).read_text()
    for kind,decl in re.findall(r'^(?:noncomputable )?(def|theorem|abbrev)\s+([A-Za-z0-9_]+)',text,re.M):
        decls.append({'module':Path(name).stem,'kind':kind,'name':'Agent108.WindowWeights.'+decl})
audit='import Agent108WindowEndpointWeights\n\n'+'\n'.join('#print axioms '+d['name'] for d in decls)+'\n'
(SRC/'IndependentEndpointAudit.lean').write_text(audit)
run('audit',['IndependentEndpointAudit.lean'])
log=(LOG/'audit.stdout.log').read_text()
bad=[];allowed={'propext','Classical.choice','Quot.sound'}
for line in log.splitlines():
    if 'depends on axioms:' in line:
        found=set(re.search(r'\[(.*)\]',line).group(1).replace(' ','').split(','))-{''}
        if not found<=allowed:bad.append(line)
prints=sum('depends on axioms:' in line or 'does not depend on any axioms' in line for line in log.splitlines())
assert prints==len(decls),(prints,len(decls))
final={'reviewer':'Agent108 claims_inventory','source_sha256':fixed,'source_paths':source_paths,'records':results,'finished':True,'declarations':decls,'audited_declarations':len(decls),'unexpected_axioms':bad,'all_pass':not bad and all(x['exit_code']==0 for x in results),'scope':'Literal endpoint-window decomposition and positive legal-window endpoint constants. No all-U/target global family ratio or actual arithmetic family is proved by this endpoint package.'}
(OUT/'build-results.json').write_text(json.dumps(final,indent=2)+'\n')
print(json.dumps({'all_pass':final['all_pass'],'declarations':len(decls),'unexpected_axioms':bad}),flush=True)
raise SystemExit(0 if final['all_pass'] else 1)
