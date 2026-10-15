#!/usr/bin/env python3
"""Fresh-source Lean rebuild and exhaustive local-module theorem axiom audit."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, shlex, shutil, subprocess, sys, time, uuid
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--lean-root', type=Path, required=True)
p.add_argument('--build-root', type=Path, required=True)
p.add_argument('--phase', required=True)
p.add_argument('--modules', nargs='+', required=True)
p.add_argument('--preload', type=Path)
p.add_argument('--timeout', type=int, default=1200)
a = p.parse_args()
repo, lean_root = a.repo.resolve(), a.lean_root.resolve()
contrib = repo / 'proofs/contributions/agent-108/modular-autonomy'
review = contrib / 'review/clean'
review.mkdir(parents=True, exist_ok=True)
assert all(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', x) for x in a.modules)
assert re.fullmatch(r'[A-Za-z0-9_-]+', a.phase)
a.build_root.mkdir(parents=True, exist_ok=True)
run_id = a.phase + '-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
run = a.build_root.resolve() / run_id
src, logs = run / 'src', run / 'logs'
src.mkdir(parents=True, exist_ok=False)
logs.mkdir()
report = review / run_id
report.mkdir(exist_ok=False)
m = {'run_id':run_id, 'phase':a.phase, 'status':'running', 'repository':str(repo),
     'build_directory':str(run), 'modules':a.modules, 'source_snapshot_sha256':{},
     'source_live_sha256_after':{}, 'commands':[], 'toolchain_sha256_before':{},
     'toolchain_sha256_after':{}, 'preexisting_olean_count':len(list(run.rglob('*.olean'))),
     'axiom_allowlist':['propext','Classical.choice','Quot.sound'],
     'trust_note':('Official Lean with explicit readlink self-path compatibility adapter.' if a.preload
                   else 'Unadapted official Lean execution; no LD_PRELOAD.')}

def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def save():
    (run/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    shutil.copy2(run/'manifest.json',report/'manifest.json')

files = {'Lychrel196Research':repo/'proofs/research/Lychrel196Research.lean'}
files.update({name:contrib/(name+'.lean') for name in a.modules})
for name,path in files.items():
    data=path.read_bytes()
    (src/(name+'.lean')).write_bytes(data)
    m['source_snapshot_sha256'][str(path.relative_to(repo))]=hashlib.sha256(data).hexdigest()
m['lean_toolchain_file']=(repo/'proofs/research/lean-toolchain').read_text().strip()
m['lean_toolchain_sha256']=sha(repo/'proofs/research/lean-toolchain')
tool_files=['bin/lean','lib/lean/libleanshared.so','lib/lean/libleanshared_1.so',
            'lib/lean/libInit_shared.so','lib/lean/Init.olean','lib/lean/Std.olean']
for rel in tool_files: m['toolchain_sha256_before'][rel]=sha(lean_root/rel)
m['script_sha256']=sha(Path(__file__))
if a.preload:
    a.preload=a.preload.resolve()
    m['adapter']={'path':str(a.preload),'sha256':sha(a.preload)}
    adapter_source=a.preload.parent/'proc_self_readlink.c'
    if adapter_source.is_file():
        m['adapter']['source_sha256']=sha(adapter_source)
        shutil.copy2(adapter_source,report/adapter_source.name)
env=dict(os.environ)
env['LEAN_PATH']=str(src)
for key in ['LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD']: env.pop(key,None)
if a.preload: env['LD_PRELOAD']=str(a.preload)
m['environment_overrides']={'LEAN_PATH':env['LEAN_PATH'],'LD_PRELOAD':env.get('LD_PRELOAD')}
lean=str(lean_root/'bin/lean')

def execute(label,args):
    rec={'label':label,'argv':args,'cwd':str(src),'command':shlex.join(args),
         'started_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
    start=time.monotonic()
    try:
        cp=subprocess.run(args,cwd=src,env=env,text=True,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=a.timeout)
        output,code=cp.stdout,cp.returncode
    except subprocess.TimeoutExpired as e:
        output=e.stdout or ''
        if isinstance(output,bytes): output=output.decode(errors='replace')
        output+='\nTIMEOUT\n'; code=124
    log=logs/(label+'.log')
    log.write_text(output); shutil.copy2(log,report/log.name)
    rec.update(exit_code=code,elapsed_seconds=round(time.monotonic()-start,3),
               full_log=log.name,full_log_sha256=sha(log))
    m['commands'].append(rec); save()
    print(f'{label}: exit={code}, elapsed={rec["elapsed_seconds"]}s',flush=True)
    if code: raise RuntimeError(f'{label} failed; see {log}')
    return output

try:
    version=execute('00-version',[lean,'--version'])
    if 'version 4.19.0,' not in version: raise RuntimeError('Unexpected Lean version')
    for i,name in enumerate(files,1):
        execute(f'{i:02d}-compile-{name}',[lean,'-o',name+'.olean',name+'.lean'])
        if not (src/(name+'.olean')).is_file(): raise RuntimeError('Missing output: '+name)
    imports='\n'.join('import '+name for name in a.modules)
    wanted='#['+', '.join('`'+name for name in files)+']'
    discovery=imports+'\nimport Lean\n\nopen Lean Elab Command\n\nrun_cmd do\n'
    discovery+=f'  let wanted : Array Name := {wanted}\n'
    discovery+='''  let env ← getEnv
  for (name, info) in env.constants do
    if let some idx := env.getModuleIdxFor? name then
      let moduleName := env.header.moduleNames[idx.toNat]!
      if wanted.contains moduleName then
        match info with
        | .axiomInfo _ =>
          throwError "Unexpected locally declared axiom: {name}"
        | .thmInfo _ =>
          let visibility := if isPrivateName name then "private" else "exported"
          liftIO <| IO.println s!"THEOREM|{moduleName}|{name}|{visibility}"
          let axioms ← collectAxioms name
          let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
          for ax in axioms do
            unless allowed.contains ax do
              throwError "Forbidden axiom {ax} in {name}"
          liftIO <| IO.println s!"AXIOMS|{name}|{axioms}"
        | _ => pure ()
'''
    (src/'DiscoverExports.lean').write_text(discovery)
    shutil.copy2(src/'DiscoverExports.lean',report/'DiscoverExports.lean')
    discovered=execute('90-discover-and-validate-axioms',[lean,'DiscoverExports.lean'])
    declarations=[]; axiom_sets={}
    for line in discovered.splitlines():
        if line.startswith('THEOREM|'):
            _,mod,name,visibility=line.split('|')
            declarations.append({'module':mod,'name':name,'visibility':visibility})
        elif line.startswith('AXIOMS|'):
            _,name,values=line.split('|',2); axiom_sets[name]=values
    declarations.sort(key=lambda d:(d['module'],d['name']))
    if not declarations: raise RuntimeError('No theorems discovered; refusing empty audit')
    exported=[d for d in declarations if d['visibility']=='exported']
    contribution=[d for d in exported if d['module'] in a.modules]
    if not contribution: raise RuntimeError('No exported contribution theorems discovered')
    m['exported_contribution_theorems']=contribution
    m['all_local_theorems']=declarations
    m['axiom_sets']=axiom_sets
    audit=imports+'\n\n'+'\n'.join('#print axioms '+d['name'] for d in exported)+'\n'
    (src/'PrintAxioms.lean').write_text(audit)
    shutil.copy2(src/'PrintAxioms.lean',report/'PrintAxioms.lean')
    printed=execute('91-print-axioms-all-exports',[lean,'PrintAxioms.lean'])
    actual=re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)",printed,re.M)
    expected=[d['name'] for d in exported]
    if actual!=expected: raise RuntimeError('Printed audit does not exactly match export inventory')
    m['exported_theorem_count']=len(exported)
    m['exported_contribution_theorem_count']=len(contribution)
    m['exported_dependency_theorem_count']=len(exported)-len(contribution)
    m['status']='passed'
except Exception as e:
    m['status']='failed'; m['failure']=str(e)
finally:
    for rel in tool_files: m['toolchain_sha256_after'][rel]=sha(lean_root/rel)
    m['toolchain_unchanged']=m['toolchain_sha256_before']==m['toolchain_sha256_after']
    for name,path in files.items(): m['source_live_sha256_after'][str(path.relative_to(repo))]=sha(path)
    m['sources_unchanged_during_run']=m['source_snapshot_sha256']==m['source_live_sha256_after']
    if not m['toolchain_unchanged'] or not m['sources_unchanged_during_run']:
        m['status']='failed'; m['failure']='Toolchain or source changed during audit'
    m['compiled_olean_sha256']={p.name:sha(p) for p in sorted(src.glob('*.olean'))}
    m['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat(); save()
    latest={'run_id':run_id,'status':m['status'],'report_directory':str(report),'build_directory':str(run)}
    (review/('latest-'+a.phase+'.json')).write_text(json.dumps(latest,indent=2)+'\n')
    print(json.dumps({**latest,'failure':m.get('failure'),
                     'contribution_theorems':m.get('exported_contribution_theorem_count')},indent=2),flush=True)
sys.exit(0 if m['status']=='passed' else 1)
