#!/usr/bin/env python3
"""Census and audit every theorem constant in the review's Agent109/Agent121 namespaces.
Run after rebuild.py; verify source/object hashes before importing them.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    args=ap.parse_args()
    run=args.run.resolve(); lean=args.lean.resolve(); build=run/'build'; logs=run/'logs'
    d=json.loads((run/'result.json').read_text())
    if d['status']!='PASS' or sha(lean)!=d['lean_sha256']:
        raise RuntimeError('Successful pinned build required')
    for entry in d['sources']:
        if sha(build/(entry['module']+'.lean'))!=entry['sha256']:
            raise RuntimeError('Input source changed since build')
    for entry in d['project_objects']:
        if sha(build/entry['file'])!=entry['sha256']:
            raise RuntimeError('Project object changed since build')
    if sha(build/'Agent121ScopeRegression.lean')!=d['review_source_sha256']:
        raise RuntimeError('Review source changed since build')
    src=Path(__file__).parent/'Agent121DeclarationCensus.lean'
    shutil.copyfile(src,build/src.name)
    env=os.environ.copy(); env['LEAN_PATH']=str(build)
    commands=[]
    def execute(module: str) -> str:
        argv=[str(lean),'-j1','-DElab.async=false',module+'.lean']
        p=subprocess.run(argv,cwd=build,env=env,text=True,capture_output=True,timeout=120)
        text=p.stdout+p.stderr
        (logs/(module+'.log')).write_text(text)
        commands.append({'argv':argv,'exit_code':p.returncode,'log':'logs/'+module+'.log',
                         'log_sha256':sha(logs/(module+'.log'))})
        if p.returncode: raise RuntimeError(module+' failed; see retained log')
        return text
    census=execute('Agent121DeclarationCensus')
    targets=sorted(set(re.findall(r'AGENT121_THEOREM (\S+)',census)))
    if not set(d['axiom_targets'])<=set(targets):
        raise RuntimeError('Missing source theorem in the loaded environment')
    for name in targets:
        if not re.fullmatch(r"[A-Za-z0-9_'.]+",name):
            raise RuntimeError('Unexpected identifier syntax; refuse to generate a command')
    audit='import Agent121ScopeRegression\n\n'+'\n'.join('#print axioms '+n for n in targets)+'\n'
    (build/'Agent121EnvironmentAxioms.lean').write_text(audit)
    (run/'Agent121EnvironmentAxioms.lean').write_text(audit)
    text=execute('Agent121EnvironmentAxioms')
    reports=re.findall(r"'([^\n]+)'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",text)
    ax={}
    for n,msg,a in reports:
        ax[n]=[] if msg.startswith('does not') else [s.strip() for s in a.split(',') if s.strip()]
    if set(ax)!=set(targets): raise RuntimeError('Incomplete environment axiom audit')
    for n,a in ax.items():
        if not set(a)<={'propext','Classical.choice','Quot.sound'}:
            raise RuntimeError('Excluded dependency: '+n+': '+str(a))
    result={'agent':121,'status':'PASS','commands':commands,'source_theorems':len(d['axiom_targets']),
            'environment_theorems_including_generated_helpers':len(targets),
            'source_targets_all_present':True,'axioms_by_theorem':ax,
            'census_source_sha256':sha(src),'main_build_result_sha256':sha(run/'result.json')}
    (run/'environment-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(targets)} environment theorem constants; {len(d["axiom_targets"])} source-declared review targets')
if __name__=='__main__': main()
