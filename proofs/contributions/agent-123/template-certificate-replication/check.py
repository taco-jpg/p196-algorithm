#!/usr/bin/env python3
"""Agent #123: pinned, isolated replication of the complementary-template chain.

Usage: python3 check.py REPO_ROOT LEAN_BIN EVIDENCE_DIR --pins module-pins.json
The evidence directory must not exist. No source, Git ref, or claim is modified.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, pathlib, re, subprocess, time

MODULES = {
 'LychrelDigitSums': 'proofs/research/continuation/LychrelDigitSums.lean',
 'PeriodObstructions': 'proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean',
 'TemplateStep': 'proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean',
 'ActualWordBridge': 'proofs/contributions/2026-10-15-agent8-complementary-bulk/ActualWordBridge.lean',
 'Compat': 'proofs/contributions/agent-109/template-step-bridge/Compat.lean',
 'ReturnCertificate': 'proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean',
 'CertCompat': 'proofs/contributions/agent-109/template-return-certificate/CertCompat.lean',
 'NoPalStep': 'proofs/contributions/agent-109/template-step-safety/NoPalStep.lean',
 'NoPalCompat': 'proofs/contributions/agent-109/template-step-safety/NoPalCompat.lean',
 'IntegerEndpoints': 'proofs/contributions/agent-109/template-step-bridge/IntegerEndpoints.lean',
}
ALLOWED = {'propext','Classical.choice','Quot.sound'}

def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def put(path: pathlib.Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('repo_root', type=pathlib.Path)
    p.add_argument('lean_bin', type=pathlib.Path)
    p.add_argument('evidence_dir', type=pathlib.Path)
    p.add_argument('--pins', type=pathlib.Path, required=True)
    a=p.parse_args()
    root=a.repo_root.resolve(); lean=a.lean_bin.resolve(); out=a.evidence_dir.resolve()
    if out.exists(): raise SystemExit('Evidence directory must be new; no cleanup is performed.')
    out.mkdir(parents=True); build=out/'clean-build'; build.mkdir(); logs=out/'logs'; logs.mkdir()
    report={'agent':123,'status':'RUNNING','scope':'unpublished replication; no new theorem or remote claim',
            'source_commit':'eec3d5f3646cab50abad6e610ea19626cd249070',
            'commands':[], 'source_pins':{}, 'axiom_policy':sorted(ALLOWED)}
    put(out/'verification.json',report)
    env=dict(os.environ, LEAN_PATH=str(build))
    def run(label: str, args: list[str]) -> str:
        start=time.monotonic()
        proc=subprocess.run(args,cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log=logs/(label+'.log'); log.write_text(proc.stdout)
        row={'label':label,'argv':args,'cwd':str(build),'returncode':proc.returncode,
             'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(out)),'sha256':sha(log)}
        report['commands'].append(row); put(out/'verification.json', report)
        print(json.dumps({k:row[k] for k in ('label','returncode','seconds')}),flush=True)
        if proc.returncode: raise RuntimeError(f'{label} failed; see {log}')
        return proc.stdout
    try:
        version=run('version',[str(lean),'--version']).strip()
        if '4.19.0' not in version or '6caaee842e94' not in version:
            raise RuntimeError('Unexpected Lean version')
        report['compiler']={'version':version,'executable_sha256':sha(lean)}
        required=json.loads(a.pins.read_text()) if a.pins else None
        for mod,path in MODULES.items():
            src=root/path; data=src.read_bytes()
            pin={'path':path,'bytes':len(data),'sha256':sha(src),
                 'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
            if required is not None and pin != required[mod]: raise RuntimeError(f'Pin mismatch: {mod}')
            report['source_pins'][mod]=pin
            (build/(mod+'.lean')).write_bytes(data)
        put(out/'module-pins.json',report['source_pins'])
        for mod in MODULES:
            imports=re.findall(r'^import\s+([^\n]+)',(build/(mod+'.lean')).read_text(),re.M)
            for line in imports:
                for dep in line.split():
                    if dep not in MODULES and dep not in ('Std','Lean','Init'):
                        raise RuntimeError(f'Unpinned local import {dep} in {mod}')
            run(mod,[str(lean),'-j1','-DElab.async=false','-o',mod+'.olean',mod+'.lean'])
            report['source_pins'][mod]['object_sha256']=sha(build/(mod+'.olean'))
        names=', '.join(json.dumps(x) for x in MODULES)
        audit='\n'.join('import '+m for m in MODULES)+'''\nimport Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ['''+names+''']
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
'''
        (build/'AllTheoremAxioms.lean').write_text(audit)
        (out/'AllTheoremAxioms.lean').write_text(audit)
        output=run('all-theorem-axioms',[str(lean),'-j1','-DElab.async=false','AllTheoremAxioms.lean'])
        declarations=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',output,re.M)
        owners={name:mod for mod,name in declarations}
        audited={name:sorted(x.strip() for x in xs.split(',') if x.strip())
                 for name,xs in re.findall(r"^'([^\n]*)' depends on axioms:\s*\[([^\]]*)\]",output,re.M)}
        for name in re.findall(r"^'([^\n]*)' does not depend on any axioms",output,re.M): audited[name]=[]
        if not owners or len(owners)!=len(declarations) or set(owners)!=set(audited):
            raise RuntimeError('Incomplete or duplicated theorem inventory')
        bad={n:v for n,v in audited.items() if not set(v)<=ALLOWED}
        if bad: raise RuntimeError(f'Excluded axioms: {bad}')
        report['axioms']={'theorems':len(owners),'per_module':dict(collections.Counter(owners.values())),
                          'union':sorted(set().union(*map(set,audited.values()))),
                          'unsafe_implementation_declarations':re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM .+$',output,re.M)}
        put(out/'theorem-axioms.json',[{'name':n,'module':owners[n],'axioms':audited[n]} for n in sorted(owners)])
        endpoints='''import CertCompat
import NoPalCompat
import IntegerEndpoints
set_option pp.universes true
#print Agent109.Cert.check
#print Agent109.Cert.LocalOK
#print Agent109.Cert.Admissible0
#print Agent109.Cert.certificate_sound
#print Agent109.Cert.template_realized
#print Agent109.CertCompat.certificate_existence_lychrel
#print Agent109.NoPal.not_stepPal
#print Agent109.NoPalCompat.lychrel_template_orbit_safe
#print Lychrel196.reverse10
#print Lychrel196.Palindrome
#print Lychrel196.step
#print Lychrel196.orbit
#print Lychrel196.IsLychrel
#print Lychrel196.DecimalLychrelExistence
'''
        (build/'EndpointTypes.lean').write_text(endpoints); (out/'EndpointTypes.lean').write_text(endpoints)
        run('endpoint-types',[str(lean),'-j1','-DElab.async=false','EndpointTypes.lean'])
        for mod,path in MODULES.items():
            if sha(root/path)!=report['source_pins'][mod]['sha256']:
                raise RuntimeError('Source changed during execution')
        report['status']='PASS'
    except BaseException as e:
        report['status']='FAIL'; report['error']=str(e); raise
    finally:
        put(out/'verification.json',report)

if __name__=='__main__': main()
