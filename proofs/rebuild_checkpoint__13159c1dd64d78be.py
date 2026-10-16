#!/usr/bin/env python3
"""Agent 121 independent checkpoint-01 rebuild, from exact author-pinned sources.
No Git operations. The output directory must not exist. No old project objects.
"""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
BASE_SOURCES=[
 ('TemplateStep','proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean'),
 ('ReturnCertificate','proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean'),
 ('OuterFinite','proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean'),
 ('OuterBounds','proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterBounds.lean'),
 ('OuterBridge','proofs/contributions/agent-109/outer-projection-bridge/OuterBridge.lean')]
SNAPSHOTS=['ExteriorNormalization','CertificateRealization']
AUTHOR_COMMIT='72c3879b11b722e8701789bd4e2b75b202d8b137'
def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    for x in ['repo','lean','output']:ap.add_argument('--'+x,type=Path,required=True)
    a=ap.parse_args();repo=a.repo.resolve();lean=a.lean.resolve();out=a.output.resolve();here=Path(__file__).parent.resolve()
    out.mkdir(parents=True,exist_ok=False);build=out/'build';build.mkdir();logs=out/'logs';logs.mkdir()
    pins=json.loads((here/'checkpoint-pins.json').read_text())
    env=os.environ.copy();env['LEAN_PATH']=str(build)
    ver=subprocess.run([str(lean),'--version'],capture_output=True,text=True,check=True).stdout.strip()
    if '4.19.0' not in ver or '6caaee842e94' not in ver:raise RuntimeError('Wrong Lean toolchain')
    report={'agent':121,'reviewed_agent':116,'mode':'NONEXCLUSIVE_INDEPENDENT_CHECKPOINT_REPLICATION',
        'author_commit':AUTHOR_COMMIT,'main_source_commit':'eec3d5f3646cab50abad6e610ea19626cd249070',
        'started_at':datetime.now(timezone.utc).isoformat(),'lean_version':ver,'lean_sha256':sha(lean),
        'sources':[],'commands':[],'fresh_build_directory':str(build),'status':'RUNNING'}
    def save(): (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    def run(module:str,output:bool=False):
        argv=[str(lean),'-j1','-DElab.async=false']
        if output:argv+=['-o',module+'.olean']
        argv+=[module+'.lean'];t=time.monotonic()
        with (logs/(module+'.log')).open('w') as f:
            p=subprocess.run(argv,cwd=build,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
        report['commands'].append({'module':module,'argv':argv,'exit_code':p.returncode,
            'seconds':round(time.monotonic()-t,3),'log':'logs/'+module+'.log','log_sha256':sha(logs/(module+'.log'))})
        save();print(f'{module}: exit={p.returncode} ({time.monotonic()-t:.3f}s)',flush=True)
        if p.returncode:raise RuntimeError(module+' failed; see log')
    try:
        sources=[(n,repo/path,path) for n,path in BASE_SOURCES]+[(n,here/'upstream-snapshot'/(n+'.lean'),'upstream-snapshot/'+n+'.lean') for n in SNAPSHOTS]
        for n,src,path in sources:
            if sha(src)!=pins[n]:raise RuntimeError('Author pin mismatch: '+n)
            report['sources'].append({'module':n,'path':path,'sha256':sha(src),'bytes':src.stat().st_size})
            shutil.copyfile(src,build/(n+'.lean'))
        for n in ['Agent121CertificateContracts','Agent121CheckpointCensus','Agent121CheckpointAxioms']:
            shutil.copyfile(here/(n+'.lean'),build/(n+'.lean'))
        report['contract_source_sha256']=sha(here/'Agent121CertificateContracts.lean');save()
        for n,_,_ in sources:run(n,True)
        run('Agent121CertificateContracts',True)
        run('Agent121CheckpointCensus')
        targets=sorted(set(re.findall(r'AGENT121_THEOREM (\S+)',(logs/'Agent121CheckpointCensus.log').read_text())))
        if not targets:raise RuntimeError('Empty theorem census')
        shutil.copyfile(here/'Agent121CheckpointAxioms.lean',out/'Agent121CheckpointAxioms.lean')
        run('Agent121CheckpointAxioms')
        text=(logs/'Agent121CheckpointAxioms.log').read_text()
        matches=re.findall(r"'([^\n]+)'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",text)
        ax={}
        for n,msg,t in matches:
            ax[n]=[] if msg.startswith('does not') else [x.strip() for x in t.split(',') if x.strip()]
        if set(ax)!=set(targets):raise RuntimeError('Incomplete axiom coverage: '+str(set(targets)-set(ax)))
        for n,axs in ax.items():
            if not set(axs)<={'propext','Classical.choice','Quot.sound'}:raise RuntimeError('Excluded axioms: '+n+str(axs))
        report['axioms_by_theorem']=ax;report['audited_count']=len(ax)
        report['unsafe_implementation_placeholders']=sorted(set(re.findall(r'AGENT121_UNSAFE_IMPL (\S+)',text)))
        report['unsafe_implementation_note']='Compiler-generated unsafe implementation placeholders are logged, not used as theorem assumptions. All theorem transitive axiom lists must independently stay within the three standard axioms.'
        report['all_author_pins_match']=True
        report['objects']=[{'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(build.glob('*.olean'))]
        report['status']='PASS'
    except BaseException as exc:
        report['status']='FAIL';report['error']=str(exc);raise
    finally:
        report['finished_at']=datetime.now(timezone.utc).isoformat();save()
    print(f'PASS: checkpoint-01 + review contracts, {len(ax)} theorem constants',flush=True)
if __name__=='__main__':main()
