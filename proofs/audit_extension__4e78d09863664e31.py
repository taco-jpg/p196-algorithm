#!/usr/bin/env python3
"""Audit one new source module on a previously independently rebuilt core."""
import argparse,datetime as dt,hashlib,json,os,re,shlex,shutil,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--core-manifest',type=Path,required=True)
p.add_argument('--module',required=True)
a=p.parse_args()
assert re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',a.module)
core=json.loads(a.core_manifest.read_text())
assert core['status']=='passed'
repo=Path(core['repository']); run=Path(core['build_directory']); src=run/'src'
review=repo/'proofs/contributions/agent-108/modular-autonomy/review/clean'
report=review/(core['run_id']+'-extension-'+a.module)
report.mkdir(exist_ok=False)
source=repo/'proofs/contributions/agent-108/modular-autonomy'/(a.module+'.lean')
def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for name,digest in core['compiled_olean_sha256'].items():assert sha(src/name)==digest
for rel,digest in core['source_snapshot_sha256'].items():assert sha(repo/rel)==digest
m={'status':'running','module':a.module,'core_manifest':str(a.core_manifest.resolve()),
   'core_manifest_sha256':sha(a.core_manifest),'core_run_id':core['run_id'],
   'build_directory':str(run),'core_olean_sha256_before':core['compiled_olean_sha256'],
   'source_sha256_before':sha(source),'commands':[],'axiom_allowlist':core['axiom_allowlist'],
   'toolchain_sha256_before':core['toolchain_sha256_after'],'trust_note':core['trust_note'],
   'script_sha256':sha(Path(__file__))}
shutil.copy2(Path(__file__),report/'audit_extension.py')
shutil.copy2(source,src/(a.module+'.lean'))
shutil.copy2(source,report/(a.module+'.lean'))
env=dict(os.environ)
for key in ['LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD']:env.pop(key,None)
env['LEAN_PATH']=str(src)
if core['environment_overrides']['LD_PRELOAD']:env['LD_PRELOAD']=core['environment_overrides']['LD_PRELOAD']
m['environment_overrides']={'LEAN_PATH':str(src),'LD_PRELOAD':env.get('LD_PRELOAD')}
lean=core['commands'][0]['argv'][0]
lean_root=Path(lean).parent.parent
for rel,digest in m['toolchain_sha256_before'].items():assert sha(lean_root/rel)==digest

def save():(report/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def execute(label,args):
    start=time.monotonic()
    cp=subprocess.run(args,cwd=src,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    log=report/(label+'.log');log.write_text(cp.stdout)
    m['commands'].append({'label':label,'argv':args,'command':shlex.join(args),'cwd':str(src),
      'exit_code':cp.returncode,'elapsed_seconds':round(time.monotonic()-start,3),
      'full_log':log.name,'full_log_sha256':sha(log)})
    save();print(label,'exit='+str(cp.returncode),flush=True)
    if cp.returncode:raise RuntimeError(label+' failed')
    return cp.stdout
try:
    execute('01-compile-'+a.module,[lean,'-o',a.module+'.olean',a.module+'.lean'])
    discovery=(src/'DiscoverExports.lean').read_text()
    discovery='import '+a.module+'\n'+discovery
    discovery=re.sub(r'  let wanted : Array Name := .*','  let wanted : Array Name := #[`'+a.module+']',discovery)
    (src/'DiscoverExtension.lean').write_text(discovery)
    shutil.copy2(src/'DiscoverExtension.lean',report/'DiscoverExtension.lean')
    output=execute('02-discover-and-validate-axioms',[lean,'DiscoverExtension.lean'])
    theorems=[];axioms={};unsafe=[]
    for line in output.splitlines():
        if line.startswith('THEOREM|'):
            _,mod,name,visibility=line.split('|');theorems.append({'module':mod,'name':name,'visibility':visibility})
        elif line.startswith('AXIOMS|'):
            _,name,values=line.split('|',2);axioms[name]=values
        elif line.startswith('UNSAFE_COMPILER_DECL|'):unsafe.append(line)
    theorems.sort(key=lambda x:x['name'])
    exported=[d for d in theorems if d['visibility']=='exported']
    declared=['ModularAutonomy.'+name for name in re.findall(r'^theorem\s+([^\s(:]+)',source.read_text(),re.M)]
    assert declared and all(name in [d['name'] for d in exported] for name in declared)
    audit='import '+a.module+'\n\n'+'\n'.join('#print axioms '+d['name'] for d in exported)+'\n'
    (src/'PrintExtensionAxioms.lean').write_text(audit)
    shutil.copy2(src/'PrintExtensionAxioms.lean',report/'PrintExtensionAxioms.lean')
    printed=execute('03-print-axioms-all-exports',[lean,'PrintExtensionAxioms.lean'])
    actual=re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)",printed,re.M)
    assert actual==[d['name'] for d in exported]
    m.update(status='passed',all_local_theorems=theorems,exported_theorem_count=len(exported),
             source_declared_theorems=declared,source_declared_theorem_count=len(declared),
             axiom_sets=axioms,unsafe_compiler_declarations=unsafe)
except Exception as e:m.update(status='failed',failure=str(e))
finally:
    m['source_sha256_after']=sha(source)
    m['core_olean_sha256_after']={name:sha(src/name) for name in core['compiled_olean_sha256']}
    m['core_oleans_unchanged']=m['core_olean_sha256_before']==m['core_olean_sha256_after']
    m['toolchain_sha256_after']={rel:sha(lean_root/rel) for rel in m['toolchain_sha256_before']}
    m['toolchain_unchanged']=m['toolchain_sha256_before']==m['toolchain_sha256_after']
    m['source_unchanged']=m['source_sha256_before']==m['source_sha256_after']
    m['compiled_extension_olean_sha256']=sha(src/(a.module+'.olean')) if (src/(a.module+'.olean')).exists() else None
    m['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    if not all(m[k] for k in ['core_oleans_unchanged','toolchain_unchanged','source_unchanged']):m.update(status='failed',failure='Input mutated during audit')
    save();print(json.dumps({'status':m['status'],'report_directory':str(report),'source_theorems':m.get('source_declared_theorem_count'),'exported_theorems':m.get('exported_theorem_count'),'failure':m.get('failure')},indent=2),flush=True)
sys.exit(0 if m['status']=='passed' else 1)
