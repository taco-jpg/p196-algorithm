#!/usr/bin/env python3
"""Preserve each strict author increment; reuse explicit pinned dependency objects."""
from pathlib import Path
import hashlib,json,os,re,resource,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
MODULE='Agent1PeriodicCenterNormalPath'
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
BASE=Path('/workspace/p196-agent1-session-20261016/nine-center-normal-author-build')
PRIOR=[(Path('/workspace/p196-agent1-session-20261016/nine-cycle-parent-clean-001'),'agent1-periodic-nine-cycle')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def limits():resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
source_commit_before_increment=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
name=sys.argv[1];attempt=HERE/name;attempt.mkdir(exist_ok=False);build=BASE/name;build.mkdir(parents=True,exist_ok=False)
shutil.copyfile(__file__,attempt/'run.py')
for f in [ROOT/'proofs'/(MODULE+'.lean'),HERE/'NormalAudit.lean']:
 shutil.copyfile(f,attempt/f.name);shutil.copyfile(f,build/f.name)
records={}
for f in ['Agent1PeriodicNinesCycle.registry.json']:
 registry=json.loads((ROOT/'proofs'/f).read_text())
 for project in registry['projects'].values():
  for mod,rec in project['modules'].items():
   if mod in records:assert records[mod]==rec,mod
   records[mod]=rec
imports=[l.split()[1] for l in (attempt/(MODULE+'.lean')).read_text().splitlines() if l.startswith('import ')]
needed=[]
def visit(mod):
 if mod in needed or mod=='Std' or mod.startswith('Lean'):return
 for dep in records[mod]['imports']:visit(dep)
 needed.append(mod)
for mod in imports:visit(mod)
(attempt/'dependency-sources').mkdir()
deps=[]
for mod in needed:
 rec=records[mod];orig=ROOT/rec['path'];assert sha(orig)==rec['sha256'],mod
 run,proj=next((r,p) for r,p in PRIOR if (r/p/'source'/(mod+'.olean')).is_file())
 src=run/proj/'source'/(mod+'.lean');obj=src.with_suffix('.olean');report=json.loads((run/'verification.json').read_text());entry=report['projects'][proj]['sources'][mod]
 assert src.read_bytes()==orig.read_bytes() and sha(src)==entry['sha256']==entry['build_sha256'],mod
 for f in [src,obj]:shutil.copyfile(f,build/f.name)
 shutil.copyfile(src,attempt/'dependency-sources'/src.name)
 deps.append({'module':mod,'registry_path':rec['path'],'source_sha256':sha(src),'object_sha256':sha(obj),'reused_source':str(src),'reused_object':str(obj),'copied_source':str(build/src.name),'copied_object':str(build/obj.name),'prior_report':str(run/'verification.json'),'prior_report_sha256':sha(run/'verification.json'),'prior_source_commit':report['source_commit'],'prior_command':next(c for c in report['projects'][proj]['commands'] if c['label']==mod),'copy_hashes_equal':sha(build/obj.name)==sha(obj)})
dump(attempt/'dependencies.json',deps)
env=os.environ.copy();env['LEAN_PATH']=str(build)
version=subprocess.check_output([str(LEAN),'--version'],text=True);assert 'version 4.19.0' in version and '6caaee842e94' in version
(attempt/'lean-version.txt').write_text(version)
dump(attempt/'compiler.json',{'version':version.strip(),'files':{str(p):sha(p) for p in [LEAN,*sorted((LEAN.parents[1]/'lib/lean').glob('*.so'))]}})
commands=[]
def run(label,args):
 start=time.monotonic()
 with (attempt/(label+'.log')).open('w') as log:r=subprocess.run(args,cwd=build,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600,preexec_fn=limits)
 commands.append({'label':label,'argv':args,'cwd':str(build),'LEAN_PATH':env['LEAN_PATH'],'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,'address_space_limit_bytes':4*1024**3,'log_sha256':sha(attempt/(label+'.log'))})
 dump(attempt/'commands.json',commands);print((attempt/(label+'.log')).read_text(),end='',flush=True);return r.returncode
flags=[str(LEAN),'--trust=0','-j1','-DElab.async=false']
code=run('compile',flags+['-o',MODULE+'.olean',MODULE+'.lean'])
if code==0:code=run('audit',flags+['NormalAudit.lean'])
audit=(attempt/'audit.log').read_text() if (attempt/'audit.log').exists() else ''
dump(attempt/'result.json',{'status':'PASS' if code==0 else 'FAIL','exit_code':code,'source_sha256':sha(attempt/(MODULE+'.lean')),'audit_source_sha256':sha(attempt/'NormalAudit.lean'),'dependency_count':len(deps),'dependency_objects_reused':True,'fresh_full_closure':False,'explicit_trust_zero':True,'source_commit_before_increment':source_commit_before_increment,'theorem_count':len(re.findall(r'^AUDIT_THEOREM ',audit,re.M)),'safe_definition_count':len(re.findall(r'^AUDIT_SAFE_DEFINITION ',audit,re.M)),'runtime_count':len(re.findall(r'^GENERATED_RUNTIME ',audit,re.M)),'compiled_object_path':str(build/(MODULE+'.olean')) if (build/(MODULE+'.olean')).exists() else None,'compiled_object_sha256':sha(build/(MODULE+'.olean')) if (build/(MODULE+'.olean')).exists() else None})
sys.exit(code)
