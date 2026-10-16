#!/usr/bin/env python3
"""Agent 121: fresh merged-source replication. No network or Git writes.
Usage: rebuild.py --repo ROOT --lean /path/to/lean --output NEW_DIR
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path
from datetime import datetime, timezone
SOURCES = [
 ('TemplateStep', 'proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean'),
 ('LychrelDigitSums', 'proofs/research/continuation/LychrelDigitSums.lean'),
 ('PeriodObstructions', 'proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean'),
 ('Compat', 'proofs/contributions/agent-109/template-step-bridge/Compat.lean'),
 ('ReturnCertificate', 'proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean'),
 ('NoPalStep', 'proofs/contributions/agent-109/template-step-safety/NoPalStep.lean'),
 ('NoPalCompat', 'proofs/contributions/agent-109/template-step-safety/NoPalCompat.lean')]
PIN = 'eec3d5f3646cab50abad6e610ea19626cd249070'
ALLOWED = {'propext','Classical.choice','Quot.sound'}
def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
def names(text: str) -> list[str]:
    stack, result = [], []
    for line in text.splitlines():
        if re.match(r'^section(?:\s|$)',line):
            raise RuntimeError('Unsupported section nesting: stop to avoid incomplete census')
        m=re.match(r'^namespace (\S+)',line)
        if m: stack.append(m[1]); continue
        if re.match(r'^end(?:\s+(\S+))?\s*$',line):
            if not stack: raise RuntimeError('Unmatched end')
            stack.pop(); continue
        m=re.match(r'^theorem\s+(\S+)',line)
        if m: result.append('.'.join(stack+[m[1]]))
    if stack: raise RuntimeError('Unclosed namespace')
    return result

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    for x in ['repo','lean','output']: ap.add_argument('--'+x,type=Path,required=True)
    args=ap.parse_args(); repo=args.repo.resolve(); lean=args.lean.resolve(); out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    build=out/'build'; build.mkdir(); logs=out/'logs'; logs.mkdir()
    env=os.environ.copy(); env['LEAN_PATH']=str(build)
    v=subprocess.run([str(lean),'--version'],capture_output=True,text=True,check=True).stdout.strip()
    if '4.19.0' not in v or '6caaee842e94' not in v: raise RuntimeError('Toolchain mismatch: '+v)
    report={'agent':121,'mode':'NONEXCLUSIVE_MERGED_SOURCE_REPLICATION','base_commit':PIN,
        'started_at':datetime.now(timezone.utc).isoformat(),'lean_version':v,'lean_sha256':sha(lean),
        'fresh_build_directory':str(build),'sources':[],'commands':[],'status':'RUNNING'}
    def save(): (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    def run(label,argv):
        t=time.monotonic()
        with (logs/(label+'.log')).open('w') as f:
            p=subprocess.run(argv,cwd=build,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600)
        report['commands'].append({'label':label,'argv':argv,'exit_code':p.returncode,
            'seconds':round(time.monotonic()-t,3),'log':'logs/'+label+'.log','log_sha256':sha(logs/(label+'.log'))})
        save(); print(f'{label}: exit={p.returncode} ({time.monotonic()-t:.3f}s)',flush=True)
        if p.returncode: raise RuntimeError(label+' failed, see log')
    try:
        targets=[]
        pins=json.loads((Path(__file__).parent/'source-pins.json').read_text())
        expected={r['path']:r for r in pins['sources']}
        if pins['base_commit']!=PIN: raise RuntimeError('Commit pin mismatch')
        for module,path in SOURCES:
            src=repo/path
            if sha(src)!=expected[path]['sha256'] or src.stat().st_size!=expected[path]['bytes']:
                raise RuntimeError('Source pin mismatch: '+path)
            report['sources'].append({'module':module,'path':path,'sha256':sha(src),'bytes':src.stat().st_size})
            shutil.copyfile(src,build/(module+'.lean'))
            if module not in {'LychrelDigitSums','PeriodObstructions'}: targets.extend(names(src.read_text()))
        review_src=Path(__file__).parent/'Agent121ScopeRegression.lean'
        shutil.copyfile(review_src,build/'Agent121ScopeRegression.lean')
        targets.extend(names(review_src.read_text()))
        report['review_source_sha256']=sha(review_src)
        report['axiom_targets']=targets; save()
        audit='import Agent121ScopeRegression\n\n/- Agent 121: explicit transitive axiom census. -/\n'
        audit+='\n'.join('#print axioms '+n for n in targets)+'\n'
        (build/'Agent121AxiomAudit.lean').write_text(audit); (out/'Agent121AxiomAudit.lean').write_text(audit)
        for module,path in SOURCES: run(module,[str(lean),'-j1','-DElab.async=false','-o',module+'.olean',module+'.lean'])
        run('Agent121ScopeRegression',[str(lean),'-j1','-DElab.async=false','-o','Agent121ScopeRegression.olean','Agent121ScopeRegression.lean'])
        run('Agent121AxiomAudit',[str(lean),'-j1','-DElab.async=false','Agent121AxiomAudit.lean'])
        text=(logs/'Agent121AxiomAudit.log').read_text()
        matches=re.findall(r"'([^\n]+)'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",text)
        audited={}
        for n,msg,ax in matches:
            axioms=[] if msg.startswith('does not') else [x.strip() for x in ax.split(',') if x.strip()]
            if not set(axioms)<=ALLOWED: raise RuntimeError(f'Excluded axioms: {n}: {axioms}')
            audited[n]=axioms
        if set(audited)!=set(targets): raise RuntimeError('Incomplete audit coverage: '+str(set(targets)-set(audited)))
        report['axioms_by_theorem']=audited; report['audited_count']=len(audited)
        report['project_objects']=[{'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(build.glob('*.olean'))]
        report['status']='PASS'
    except BaseException as exc:
        report['status']='FAIL'; report['error']=str(exc); raise
    finally:
        report['finished_at']=datetime.now(timezone.utc).isoformat(); save()
    print(f'PASS: {len(audited)} explicit transitive axiom reports',flush=True)
if __name__=='__main__': main()
