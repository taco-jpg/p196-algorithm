#!/usr/bin/env python3
"""Independent sequential clean-source rebuild and compiled-environment audit.

The author's check.py is not imported or invoked. This driver snapshots its
resolved source closure before compiling, uses one worker, and requires actual
#print axioms output for every theorem found in each local compiled module.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def code_only(text):
    out, i, depth = [], 0, 0
    while i < len(text):
        pair = text[i:i+2]
        if pair == '/-' and (depth or True):
            depth += 1; out += '  '; i += 2
        elif depth and pair == '-/':
            depth -= 1; out += '  '; i += 2
        elif depth:
            out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif pair == '--':
            j = text.find('\n',i)
            if j == -1: j = len(text)
            out += ' '*(j-i); i = j
        elif text[i] == '"':
            out.append(' '); i += 1
            while i < len(text):
                ch = text[i]; out.append('\n' if ch == '\n' else ' '); i += 1
                if ch == '\\' and i < len(text): out.append(' '); i += 1
                elif ch == '"': break
        else:
            out.append(text[i]); i += 1
    assert depth == 0
    return ''.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build',type=Path,required=True)
    parser.add_argument('--lean',type=Path,required=True)
    parser.add_argument('modules',nargs='+')
    args = parser.parse_args()
    build = args.build.resolve(); build.mkdir(parents=True,exist_ok=False)
    src = build/'sources'; src.mkdir()
    logs = build/'logs'; logs.mkdir()
    result = {'status':'IN_PROGRESS','evidence_kind':'actual independent clean execution',
              'sources':{},'commands':[],'selected':args.modules,
              'source_git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
              'runner_sha256':digest(Path(__file__)), 'fresh_local_objects':True,
              'author_checker_invoked':False}
    manifest = build/'manifest.json'
    def save(): manifest.write_text(json.dumps(result,indent=2)+'\n')
    save()
    env = dict(os.environ)
    for k in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT'): env.pop(k,None)
    env['LEAN_PATH'] = str(src)
    def run(label,cmd):
        start=time.monotonic()
        proc=subprocess.run(cmd,cwd=src,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log=logs/(label+'.log');log.write_text(proc.stdout)
        result['commands'].append({'label':label,'argv':cmd,'exit':proc.returncode,
                                   'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(build)),
                                   'sha256':digest(log)})
        save();print(label,proc.returncode,round(time.monotonic()-start,2),flush=True)
        if proc.returncode: raise RuntimeError('nonzero '+label)
        return proc.stdout
    try:
        lean=str(args.lean.resolve())
        version=run('version',[lean,'--version']).strip()
        assert 'version 4.19.0' in version and '6caaee842e94' in version,version
        prefix=Path(run('prefix',[lean,'--print-prefix']).strip())
        compiler=[args.lean.resolve(),prefix/'bin/lean']
        compiler += list(args.lean.resolve().parent.glob('readlink_self.*'))
        result['compiler']={'version':version,'prefix':str(prefix),
                            'sha256':{str(p):digest(p) for p in compiler if p.is_file()}}
        dirs=[REPO/'proofs/research/continuation',
              REPO/'proofs/contributions/2026-10-15-agent8-complementary-bulk',
              REPO/'proofs/contributions/agent-109/template-step-bridge',
              REPO/'proofs/contributions/agent-109/template-return-certificate',
              REPO/'proofs/contributions/agent-109/outer-projection-bridge',
              REPO/'proofs/contributions/agent-109/outer-projection-bridge/agent7-deps',
              HERE.parent/'certificate-exterior',HERE.parent/'cap3-kernel',HERE]
        sources={}
        for d in dirs:
            for p in d.glob('*.lean'):
                if p.stem in sources and sources[p.stem] != p:
                    raise RuntimeError('ambiguous '+p.stem)
                sources[p.stem]=p
        ordered=[];visiting=set()
        def visit(mod):
            if mod in ordered:return
            if mod not in sources:
                assert (prefix/'lib/lean'/(mod.replace('.','/')+'.olean')).exists(),mod
                return
            assert mod not in visiting,mod
            visiting.add(mod)
            p=sources[mod];text=p.read_text(); code=code_only(text)
            bad=re.findall(r'\b(?:sorry|admit|axiom|native_decide|sorryAx|implemented_by|extern)\b',code)
            assert not bad,(mod,bad)
            imports=[]
            for line in code.splitlines():
                if line.strip().startswith('import '):imports+=line.split()[1:]
            for dep in imports:visit(dep)
            (src/(mod+'.lean')).write_text(text)
            result['sources'][mod]={'source':str(p.relative_to(REPO)),'sha256':digest(p),'imports':imports}
            visiting.remove(mod);ordered.append(mod)
        for mod in args.modules:visit(mod)
        result['order']=ordered;save()
        for mod in ordered:
            run(mod,[lean,'-j1','-DElab.async=false','-o',mod+'.olean',mod+'.lean'])
        audit='\n'.join('import '+m for m in args.modules)+'\nimport Lean\n'
        audit+='''open Lean Elab Command
set_option maxHeartbeats 0
set_option maxRecDepth 100000
run_cmd do
  let env ← getEnv
  let localModules : List String := '''+json.dumps(ordered)+'''
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[index.toNat]!
      if localModules.contains mod.toString then
        match info with
        | .thmInfo _ =>
          logInfo m!"REVIEW_DECL {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .axiomInfo v =>
          if !v.isUnsafe then throwError m!"Custom axiom: {name}"
        | _ => pure ()
'''
        (src/'ReviewAudit.lean').write_text(audit)
        output=run('ReviewAudit',[lean,'-j1','-DElab.async=false','ReviewAudit.lean'])
        names=[];axioms={}
        for line in output.splitlines():
            if line.startswith('REVIEW_DECL '):names.append(line[len('REVIEW_DECL '):])
            if " depends on axioms: [" in line:
                name, ax=line.rsplit(' depends on axioms: [',1)
                axioms[name[1:-1]]=[x.strip() for x in ax.rstrip(']').split(',') if x.strip()]
            elif line.endswith(' does not depend on any axioms'):
                name=line[:-len(' does not depend on any axioms')]
                axioms[name[1:-1]]=[]
        assert len(set(names))==len(names) and set(names)==set(axioms),(len(names),len(axioms))
        allowed={'propext','Classical.choice','Quot.sound'}
        assert all(set(v)<=allowed for v in axioms.values()),axioms
        result['theorem_axioms']=axioms; result['theorem_count']=len(names)
        result['sources_unchanged_after_run']=all(digest(REPO/r['source'])==r['sha256'] for r in result['sources'].values())
        result['status']='PASS';save()
        print('PASS',len(ordered),'modules;',len(names),'theorems',flush=True)
    except Exception as e:
        result['status']='FAIL';result['error']=str(e);save();raise


if __name__=='__main__':main()
