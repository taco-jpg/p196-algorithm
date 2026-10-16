#!/usr/bin/env python3
from pathlib import Path
import json,os,subprocess,time,re,hashlib,sys
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parent
MOD=ROOT/'modules'
run_id=sys.argv[1] if len(sys.argv)>1 else 'default'
if not re.fullmatch(r'[A-Za-z0-9_-]+',run_id): raise SystemExit('invalid run id')
BUILD=ROOT/('build-independent-'+run_id)
LOGS=ROOT/('build-logs-'+run_id)
BUILD.mkdir(exist_ok=False)
LOGS.mkdir(exist_ok=True)
WRAPPER=WORKSPACE/'agent108-runtime/lean-with-mathlib.sh'
env=dict(os.environ,LEAN_PATH=str(BUILD))
order=['LychrelDigitSums','Trace','WholeWord','Safety','Indexing','FiniteWords','FamilyStates','Products','Obstruction','CarryPath']
records=[]
def run(name,args):
    started=time.time()
    p=subprocess.run([str(WRAPPER),*args],cwd=MOD,env=env,text=True,capture_output=True)
    (LOGS/(name+'.stdout.log')).write_text(p.stdout)
    (LOGS/(name+'.stderr.log')).write_text(p.stderr)
    rec={'name':name,'command':[str(WRAPPER),*args],'cwd':str(MOD),'exit_code':p.returncode,'seconds':time.time()-started,'stdout_log':str(LOGS/(name+'.stdout.log')),'stderr_log':str(LOGS/(name+'.stderr.log'))}
    records.append(rec)
    (ROOT/('build-results-'+run_id+'.json')).write_text(json.dumps({'records':records,'all_pass':all(x['exit_code']==0 for x in records),'finished':False},indent=2)+'\n')
    print(json.dumps(rec),flush=True)
    if p.returncode: raise SystemExit(p.returncode)
for name in order:
    run(name,['-o',str(BUILD/(name+'.olean')),name+'.lean'])
names=[]
for module in order[1:]:
    text=(MOD/(module+'.lean')).read_text()
    namespace='Agent13BufferedFamily' if module=='CarryPath' else ('Agent13ProductWeights' if module in ['FiniteWords','FamilyStates','Products','Obstruction'] else 'Agent13FoldedFamily')
    for name in re.findall(r'^(?:noncomputable )?(?:def|theorem|abbrev)\s+([A-Za-z0-9_]+)',text,re.M):
        names.append(namespace+'.'+name)
audit='import Obstruction\nimport CarryPath\n\n'+'\n'.join('#print axioms '+name for name in names)+'\n'
(MOD/'IndependentDependencyAudit.lean').write_text(audit)
run('IndependentDependencyAudit',['IndependentDependencyAudit.lean'])
audit_log=(LOGS/'IndependentDependencyAudit.stdout.log').read_text()
allowed={'propext','Classical.choice','Quot.sound'}
bad=[]
for line in audit_log.splitlines():
    if 'depends on axioms:' in line:
        ax=set(re.search(r'\[(.*)\]',line).group(1).replace(' ','').split(','))-{''}
        if not ax<=allowed: bad.append(line)
results={'records':records,'finished':True,'all_pass':not bad and all(x['exit_code']==0 for x in records),'audited_declarations':len(names),'unexpected_axioms':bad,'modules':order}
(ROOT/('build-results-'+run_id+'.json')).write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'finished':True,'all_pass':results['all_pass'],'audited_declarations':len(names),'unexpected_axioms':bad}),flush=True)
