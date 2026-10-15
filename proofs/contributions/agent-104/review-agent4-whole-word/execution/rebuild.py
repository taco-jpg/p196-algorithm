#!/usr/bin/env python3
"""Fresh, commit-pinned Agent 4 whole-word bridge build and transitive axiom audit.

Preparation performs no compiler invocation. After the coordinator grants a slot,
--execute performs a single-worker rebuild, then enumerates every local theorem
constant from Lean's imported environment and applies official #print axioms.
All five local sources are extracted afresh from the immutable Git commit. Local
objects are never reused. Historical official-toolchain provenance is explicitly
inherited; imported official objects are rehashed against that published manifest.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

PIN = '4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7'
MODULES = {
    'LychrelDigitSums': 'proofs/research/continuation/LychrelDigitSums.lean',
    'PrefixModel': 'proofs/agent4/prefix_growth/PrefixModel.lean',
    'SaturationCertificate': 'proofs/agent4/prefix_growth/SaturationCertificate.lean',
    'SaturationTheorem': 'proofs/agent4/prefix_growth/SaturationTheorem.lean',
    'WholeWordBridge': 'proofs/agent4/prefix_growth/integration/WholeWordBridge.lean',
}
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
EXPECTED_EXPORTS = {
    'nextColumns_prefix3', 'iterPairs_width_ge', 'actual_width_overflow_identity',
    'iterPairs_prefix_evolution', 'actual_saturated_prefix_return',
    'numeric_saturated_prefix_obstruction',
}
INHERITED = 'proofs/contributions/agent-104/seven-column-kernel/review-final-clean/preflight-01'
FORBIDDEN = re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|newaxiom|native_decide|sorryAx|ofReduceBool|ofReduceNat|unsafe|implemented_by|extern|run_cmd|elab|macro|initialize|unsafeCast)\b(?![\w'])|#(?:eval|reduce)|debug\.skipKernelTC")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def code_only(text):
    """Mask nested comments and strings, retaining exact line positions."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i+2]
        if depth:
            if pair == '/-': depth += 1; out.extend('  '); i += 2
            elif pair == '-/': depth -= 1; out.extend('  '); i += 2
            else: out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif string:
            if text[i] == '\\': out.extend('  '); i += 2
            else: string = text[i] != '"'; out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif pair == '/-': depth = 1; out.extend('  '); i += 2
        elif pair == '--':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out.extend(' ' * (end-i)); i = end
        elif text[i] == '"': string = True; out.append(' '); i += 1
        else: out.append(text[i]); i += 1
    if depth or string: raise ValueError('Unterminated source comment/string')
    return ''.join(out)


def audit_source():
    module_strings = ', '.join(json.dumps(m) for m in MODULES)
    return '''import WholeWordBridge
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := [''' + module_strings + ''']
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--execute', action='store_true')
    ap.add_argument('--slot-authorization', default='')
    args = ap.parse_args()
    repo, build, evidence = (getattr(args, key).resolve() for key in ('repo','build','evidence'))
    evidence.mkdir(parents=True, exist_ok=True)
    snapshot = build/'snapshot'
    snapshot.mkdir(parents=True, exist_ok=True)
    if any(snapshot.glob('*.olean')):
        raise ValueError('Build has pre-existing local objects; use a new build directory and retain this attempt')
    source_pins = {}
    trust_hits = []
    for module, rel in MODULES.items():
        blob = subprocess.check_output(['git','show',PIN+':'+rel], cwd=repo)
        dest = snapshot/(module+'.lean')
        if dest.exists() and dest.read_bytes() != blob:
            raise ValueError('Existing source differs: '+module)
        dest.write_bytes(blob)
        source = code_only(blob.decode())
        imports = []
        for clause in re.findall(r'^\s*import\s+(.+)$', source, re.MULTILINE):
            imports += clause.split()
        for m in FORBIDDEN.finditer(source):
            trust_hits.append({'module':module,'line':source.count('\n',0,m.start())+1,'token':m.group()})
        source_pins[module] = {'path':rel, 'bytes':len(blob), 'sha256':digest(dest),
            'git_blob_sha1':hashlib.sha1(f'blob {len(blob)}\0'.encode()+blob).hexdigest(),
            'imports':imports, 'explicit_theorems':len(re.findall(r'^\s*(?:private\s+)?theorem\s+',source,re.MULTILINE))}
    nonlocal_imports = sorted({i for rec in source_pins.values() for i in rec['imports']} - set(MODULES))
    if nonlocal_imports != ['Lean.Elab.Tactic.Omega','Std']:
        raise ValueError('Unexpected import closure: '+str(nonlocal_imports))
    write_json(evidence/'source-pins.json',{'source_commit':PIN,'modules':source_pins,'outside_repository_build':str(build)})
    official_pins_path = repo/INHERITED/'official-archive-member-pins.json'
    inherited_preflight_path = repo/INHERITED/'independent-preflight.json'
    inherited = json.loads(inherited_preflight_path.read_text())
    official_pins = json.loads(official_pins_path.read_text())
    tc = args.lean.resolve().parent
    prefix = tc/'lean-4.19.0-linux'
    preflight = {'status':'PREPARED_NOT_EXECUTED','source_commit':PIN,
        'source_modules':len(MODULES),'source_bytes':sum(r['bytes'] for r in source_pins.values()),
        'source_explicit_theorems':sum(r['explicit_theorems'] for r in source_pins.values()),
        'source_trust_escape_scan':trust_hits,'nonlocal_direct_imports':nonlocal_imports,
        'historical_toolchain_provenance':'Inherited previously published official Lean 4.19.0 archive comparison; no new download claimed.',
        'inherited_evidence':{
            str(official_pins_path.relative_to(repo)):digest(official_pins_path),
            str(inherited_preflight_path.relative_to(repo)):digest(inherited_preflight_path)},
        'official_archive_sha256':inherited['official_archive_sha256'],
        'official_archive_member_count':len(official_pins),
        'inherited_LD_PRELOAD':os.environ.get('LD_PRELOAD',''),
        'inherited_LD_LIBRARY_PATH':os.environ.get('LD_LIBRARY_PATH',''),
        'runner_sha256':digest(__file__), 'build_dir':str(build),
        'compiler_started':False}
    if trust_hits: raise ValueError('Excluded source trust dependencies: '+str(trust_hits))
    for key in ('LD_PRELOAD','LD_LIBRARY_PATH'):
        if os.environ.get(key): raise ValueError('Unreviewed inherited '+key)
    write_json(evidence/'preflight.json',preflight)
    (evidence/'AllLocalTheorems.lean').write_text(audit_source())
    if not args.execute:
        print(json.dumps(preflight,indent=2)); return 0
    if not args.slot_authorization:
        raise ValueError('Execution requires recorded coordinator authorization')
    logdir = evidence/'logs'
    logdir.mkdir(exist_ok=False)
    report = {'status':'IN_PROGRESS','source_commit':PIN,'slot_authorization':args.slot_authorization,
        'runner_sha256':digest(__file__),'fresh_local_source_rebuild':True,'reused_local_objects':False,
        'local_build_workers':1,'compiler_threads':1,'asynchronous_elaboration':False,
        'memory_cap':None,'timeout':None,'allowed_axioms':sorted(ALLOWED),'builds':[],
        'sources':source_pins,'source_build_order':list(MODULES),
        'audit_scope':'Every local theorem constant, including generated/private constants, and its transitive axioms.',
        'claim_scope':'Build/reproducibility audit only; no P196, novel theorem, or witness claim.'}
    report_file = evidence/'verification.json'
    write_json(report_file,report)
    env=dict(os.environ)
    for key in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH'):
        env.pop(key,None)
    env['LEAN_PATH']=str(snapshot)
    report['compiler_environment']={k:env.get(k,'') for k in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH')}
    def run(label, command):
        log=logdir/(label+'.log')
        start=time.monotonic()
        with log.open('w') as stream:
            proc=subprocess.Popen(command,cwd=snapshot,env=env,stdout=stream,stderr=subprocess.STDOUT)
            _,status,usage=os.wait4(proc.pid,0)
            proc.returncode=os.waitstatus_to_exitcode(status)
        rec={'label':label,'command':command,'cwd':str(snapshot),'exit_code':proc.returncode,
             'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(evidence)),
             'log_sha256':digest(log),'resources':{k:getattr(usage,k) for k in ('ru_utime','ru_stime','ru_maxrss','ru_minflt','ru_majflt','ru_nswap')}}
        report['builds'].append(rec); write_json(report_file,report)
        print(json.dumps(rec),flush=True)
        if proc.returncode: raise ValueError(f'{label}: compiler exited {proc.returncode}')
        return log.read_text()
    try:
        version=run('version',[str(args.lean),'--version']).strip()
        if version != 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)':
            raise ValueError('Unexpected compiler version: '+version)
        actual_prefix=Path(run('prefix',[str(args.lean),'--print-prefix']).strip()).resolve()
        if actual_prefix != prefix: raise ValueError('Unexpected installation prefix')
        compiler_paths=[args.lean.resolve(),prefix/'bin/lean',tc/'proc-self-compat.c',tc/'proc-self-compat.so',prefix/'src/lean/Lean/Util/CollectAxioms.lean']
        compiler_paths += sorted((prefix/'lib/lean').glob('*.so'))
        report['compiler_fingerprints']={str(p):digest(p) for p in compiler_paths}
        for p in compiler_paths:
            if p.is_relative_to(prefix) and str(p.relative_to(prefix)) in official_pins:
                if digest(p)!=official_pins[str(p.relative_to(prefix))]: raise ValueError('Official toolchain hash mismatch '+str(p))
            elif str(p) in inherited['support_file_pins']:
                if digest(p)!=inherited['support_file_pins'][str(p)]: raise ValueError('Inherited support hash mismatch '+str(p))
            else: raise ValueError('Unpinned compiler component '+str(p))
        report['compiler_version']=version
        report['inherited_toolchain_manifest_sha256']=digest(official_pins_path)
        write_json(report_file,report)
        for module in MODULES:
            run(module,[str(args.lean),'-j1','-DElab.async=false','-o',module+'.olean',module+'.lean'])
            source_pins[module]['object_sha256']=digest(snapshot/(module+'.olean'))
            write_json(report_file,report)
        audit_path=snapshot/'AllLocalTheorems.lean'
        audit_path.write_text(audit_source())
        report['audit_source_sha256']=digest(audit_path)
        output=run('AllLocalTheorems',[str(args.lean),'-j1','-DElab.async=false',audit_path.name])
        declarations=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',output,re.MULTILINE)
        names={n:m for m,n in declarations}
        if len(names)!=len(declarations) or not names: raise ValueError('Empty/duplicate environment theorem enumeration')
        audits={}
        for n,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output):
            if n in audits: raise ValueError('Duplicate axiom record '+n)
            audits[n]=sorted(a.strip() for a in ax.split(',') if a.strip())
        for n in re.findall(r"'([^']+)' does not depend on any axioms",output):
            if n in audits: raise ValueError('Duplicate empty axiom record '+n)
            audits[n]=[]
        if set(audits)!=set(names): raise ValueError('Incomplete theorem axiom audit')
        forbidden={n:a for n,a in audits.items() if set(a)-ALLOWED}
        report['forbidden_transitive_axioms']=forbidden
        if forbidden: raise ValueError('Disallowed transitive axiom dependencies')
        report['theorems']={n:{'module':names[n],'axioms':audits[n]} for n in sorted(names)}
        report['theorem_count']=len(names)
        report['theorems_per_module']={m:sum(v==m for v in names.values()) for m in MODULES}
        exports={n for n,m in names.items() if m=='WholeWordBridge'}
        expected={'P196.Agent4.WholeWord.'+n for n in EXPECTED_EXPORTS}
        if not expected<=exports: raise ValueError('Missing WholeWordBridge export')
        report['six_export_axioms']={n:audits[n] for n in sorted(expected)}
        report['unsafe_implementation_axioms']=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$',output,re.MULTILINE)
        report['imported_object_fingerprints']={}
        for module in sorted(set(re.findall(r'^AUDIT_IMPORT (\S+)$',output,re.MULTILINE))):
            relative=module.replace('.','/')+'.olean'
            p=snapshot/relative if module in MODULES else prefix/'lib/lean'/relative
            h=digest(p)
            rec={'path':str(p),'sha256':h,'local_rebuilt':module in MODULES}
            if module not in MODULES:
                key='lib/lean/'+relative
                if key not in official_pins or h != official_pins[key]: raise ValueError('Official imported object mismatch '+module)
                rec['official_archive_manifest_match']=True
            report['imported_object_fingerprints'][module]=rec
        for module,rec in source_pins.items():
            if digest(snapshot/(module+'.lean')) != rec['sha256']: raise ValueError('Snapshot changed '+module)
            blob=subprocess.check_output(['git','show',PIN+':'+rec['path']],cwd=repo)
            if hashlib.sha256(blob).hexdigest()!=rec['sha256']: raise ValueError('Pinned source mismatch '+module)
        for p,h in report['compiler_fingerprints'].items():
            if digest(p)!=h: raise ValueError('Compiler changed during build')
        report['snapshot_and_pinned_sources_unchanged_at_completion']=True
        report['official_imported_object_count']=sum(not r['local_rebuilt'] for r in report['imported_object_fingerprints'].values())
        report['status']='PASS'
        write_json(report_file,report)
        print(f"PASS: {len(MODULES)} fresh source modules, {len(names)} transitive theorem audits",flush=True)
        return 0
    except Exception as exc:
        report['status']='FAIL'; report['failure']=str(exc); write_json(report_file,report)
        print('FAIL: '+str(exc),flush=True)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
