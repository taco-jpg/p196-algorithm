#!/usr/bin/env python3
"""Rebuild the affected aggregate and exact endpoint aliases using reviewed objects.
This is deliberately not a second full dependency build.
"""
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,required=True)
parser.add_argument('--review',type=Path,required=True)
parser.add_argument('--scratch',type=Path,required=True)
parser.add_argument('--lean',type=Path,required=True)
a=parser.parse_args()
HERE=Path(__file__).resolve().parent
REMOTE='c0bca37913df5b52963c484ef20cbeb5b3838a32'
TREE='22d91671e98a7c4283ee920470ec249a1c7c6c74'
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
manifest=json.loads((a.review/'manifest.json').read_text())
assert manifest['status']=='PASS' and manifest['fresh_local_objects'] and manifest['sources_unchanged_after_run']
assert len(manifest['sources'])==137 and manifest['theorem_count']==1991
assert all(cmd['exit']==0 for cmd in manifest['commands'])
assert all(set(v)<=ALLOWED for v in manifest['theorem_axioms'].values())
comparison={}
for module,info in manifest['sources'].items():
 current=a.repo/info['source']; snapshot=a.review/'sources'/(module+'.lean')
 assert sha(current)==info['sha256']==sha(snapshot),module
 comparison[module]={'path':info['source'],'review_manifest_sha256':info['sha256'],'current_sha256':sha(current),'review_snapshot_sha256':sha(snapshot),'matches':True}
closure=set()
def add(module):
 if module=='Std' or module in closure:return
 assert module in manifest['sources'],module
 closure.add(module)
 for dep in manifest['sources'][module]['imports']:add(dep)
add('Agent116All')
assert len(closure)==136
save('source-comparison.json',{'status':'PASS','checked_module_count':len(comparison),'review_manifest_sha256':sha(a.review/'manifest.json'),'current_sources_match_reviewed_snapshot':True,'modules':comparison,'aggregate_closure_count':len(closure),'aggregate_closure':sorted(closure),'comparison_scope':'Every source in independent 137-module manifest, including separately selected CanonicalityCounterexample.'})
mapping=json.loads((a.review/'remote_mapping.json').read_text())
assert mapping['status']=='PASS' and mapping['remote_source_commit']==REMOTE and mapping['remote_tree']==TREE and mapping['local_tree']==TREE
observed_tree=subprocess.check_output(['git','rev-parse',REMOTE+'^{tree}'],cwd=a.repo,text=True).strip()
assert observed_tree==TREE
for path,pin in manifest['compiler']['sha256'].items():assert sha(Path(path))==pin,path
assert not os.environ.get('LD_PRELOAD','') and not os.environ.get('LD_LIBRARY_PATH','')
version=subprocess.check_output([str(a.lean),'--version'],text=True).strip()
assert version==manifest['compiler']['version']
a.scratch.mkdir(exist_ok=True)
assert not any(a.scratch.iterdir()),'Use a new or empty scratch directory'
deps=a.scratch/'dependencies';build=a.scratch/'build';deps.mkdir();build.mkdir()
reused={}
for module in sorted(closure-{'Agent116All'}):
 src=a.review/'sources'/(module+'.lean');obj=a.review/'sources'/(module+'.olean')
 assert obj.is_file(),module
 shutil.copyfile(src,deps/src.name);shutil.copyfile(obj,deps/obj.name)
 assert sha(deps/src.name)==manifest['sources'][module]['sha256']
 assert sha(deps/obj.name)==sha(obj)
 reused[module]={'source_sha256':sha(src),'reviewed_object_sha256':sha(obj),'copied_object_sha256':sha(deps/obj.name),'reviewed_object_path':str(obj)}
aggregate=a.repo/manifest['sources']['Agent116All']['source']
shutil.copyfile(aggregate,build/'Agent116All.lean')
shutil.copyfile(HERE/'EndpointAudit.lean',build/'EndpointAudit.lean')
assert not (build/'Agent116All.olean').exists() and not (deps/'Agent116All.olean').exists()
env={**os.environ,'LEAN_PATH':str(build)+':'+str(deps)}
for key in ['LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_PATH']:
 if key!='LEAN_PATH':env.pop(key,None)
commands=[]
for module in ['Agent116All','EndpointAudit']:
 cmd=[str(a.lean),'-j1','-DElab.async=false','-o',module+'.olean',module+'.lean']
 t=time.monotonic()
 proc=subprocess.run(cmd,cwd=build,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=HERE/(module+'.log');log.write_text(proc.stdout)
 commands.append({'module':module,'argv':cmd,'cwd':str(build),'LEAN_PATH':env['LEAN_PATH'],'exit':proc.returncode,'elapsed_seconds':round(time.monotonic()-t,6),'log':log.name,'log_sha256':sha(log)})
 assert proc.returncode==0,proc.stdout
 assert 'sorryAx' not in proc.stdout and 'Lean.ofReduceBool' not in proc.stdout
axioms={}
text=(HERE/'EndpointAudit.log').read_text()
for name,items in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",text):
 axioms[name]=[x.strip() for x in items.split(',') if x.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):axioms[name]=[]
assert len(axioms)==13,len(axioms)
assert all(set(v)<=ALLOWED for v in axioms.values())
for module,info in manifest['sources'].items():assert sha(a.repo/info['source'])==info['sha256']
for module,rec in reused.items():
 assert sha(deps/(module+'.olean'))==rec['copied_object_sha256']
 assert sha(a.review/'sources'/(module+'.olean'))==rec['reviewed_object_sha256']
save('dependency-reuse.json',{'status':'PASS','reused_module_count':len(reused),'fresh_aggregate_count':1,'fresh_audit_count':1,'review_manifest_path':str(a.review/'manifest.json'),'review_manifest_sha256':sha(a.review/'manifest.json'),'modules':reused,'disclosure':'The 135 transitive dependencies are byte-identical copies of the independently freshly rebuilt and axiom-audited objects. This integration run freshly compiles only Agent116All and the exact EndpointAudit aliases. It is not a second 137-module rebuild.'})
report={'status':'PASS','scope':'Affected-root aggregate and exact endpoint integration; explicit dependency reuse','reviewed_remote_math_commit':REMOTE,'reviewed_math_tree':TREE,'observed_remote_tree':observed_tree,'reviewed_local_source_commit':manifest['source_git_head'],'review_full_build':{'module_count':137,'theorem_count':1991,'status':manifest['status'],'manifest_sha256':sha(a.review/'manifest.json')},'accepted_source_comparison_count':len(comparison),'source_sha256':{'Agent116All.lean':sha(aggregate),'EndpointAudit.lean':sha(HERE/'EndpointAudit.lean')},'fresh_object_sha256':{m+'.olean':sha(build/(m+'.olean')) for m in ['Agent116All','EndpointAudit']},'compiler':manifest['compiler'],'inherited_LD_PRELOAD':os.environ.get('LD_PRELOAD',''),'inherited_LD_LIBRARY_PATH':os.environ.get('LD_LIBRARY_PATH',''),'commands':commands,'endpoint_axioms':axioms,'axiom_union':sorted(set().union(*map(set,axioms.values()))),'actual_orbit_scope':'Bounded B,A,C; valid even phase; initial exterior length<=3; both band lengths>=18; exact initial pair-word template. Conclusion: within9 genuine Lychrel196.orbit additions, this specified maximally trimmed exterior coordinate has length>3 and remains the recorded template exterior. No claim of palindrome arrival, escape from all representations, or infinite safe orbit.','all_sources_unchanged_after':True,'all_reused_objects_unchanged_after':True,'runner_sha256':sha(Path(__file__))}
save('verification.json',report)
print(json.dumps({'status':'PASS','compared_sources':137,'reused_dependencies':135,'fresh_modules':['Agent116All','EndpointAudit'],'axiom_union':report['axiom_union']}))
