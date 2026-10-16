#!/usr/bin/env python3
"""Independent byte/provenance audit of PR99 retained Lean evidence; does not run Lean."""
from pathlib import Path
from collections import Counter
import hashlib, importlib.util, json, re, subprocess, sys
R=Path(__file__).resolve().parent
TREE=R/'tree'
P=TREE/'proofs/contributions/agent-9/digit-sum-interval-counts-20261016'
E=R/'retained-evidence'
C=E/'review/horizon-safety/full-closure'
RUN=C/'runs/full-closure-001'
H='d81784d62b399775982084a54313b6df1695b2c4'
B='5ff4f607535587d572fbc9e95ba9501d1fbe5fc5'
M='fe65cf5b1219fdd9bdd1f77d1c43c0cb53adc019'
A={'propext','Classical.choice','Quot.sound'}
def sha(data): return hashlib.sha256(data).hexdigest()
def write(path,value): path.write_text(json.dumps(value,indent=2)+'\n')
report={'auditor':'Agent #11 session046f9285a650 /root/review99','kind':'Independent retained-evidence byte/provenance and source audit, not fresh Lean execution','head':H,'base':B,'merge_tree':M,'command':[sys.executable,str(Path(__file__).resolve())],'status':'RUNNING'}
try:
    # The entire verifier was manually inspected before importing its pure audit generator.
    checker=P/'review/horizon-safety/full-closure/verify_closure.py'
    spec=importlib.util.spec_from_file_location('pr99reviewed_checker',checker); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    v=json.loads((RUN/'verification.json').read_text()); registry=json.loads((C/'source-registry.json').read_text())
    assert sha(checker.read_bytes())==v['workflow_sha256']
    assert checker.read_bytes()==(C/'verify_closure.py').read_bytes()
    for source in [P/'review/horizon-safety/full-closure/source-registry.json',RUN/'source-manifest.json']:
        assert source.read_bytes()==(C/'source-registry.json').read_bytes()
        assert sha(source.read_bytes())==v['manifest_sha256']
    assert v['status']=='PASS_SELECTED_SOURCE_CLOSURE' and v['lean_trust_level']==0 and v['precompile_object_count']==0
    assert v['output_directory_created_new'] and v['all_selected_sources_unchanged'] and v['compiler_snapshot_unchanged']
    rows=[]
    imports={}
    for name,record in registry['modules'].items():
        source=({'repository':TREE,'package':P}[record['base']])/record['path'];data=source.read_bytes(); copied=RUN/'source'/(name+'.lean')
        assert data==copied.read_bytes() and sha(data)==record['sha256']==v['sources'][name]['build_sha256']
        assert hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==record['git_blob']
        code=mod.code_only(data.decode()); assert not mod.BANNED.search(code)
        stronger=re.findall(r'(?<![\w\x27])(?:unsafe|partial|implemented_by|extern|csimp|trustCompiler|ofReduceNat|ofReduceBool|run_meta|run_cmd|elab|macro|axiom|sorryAx|native_decide|skipKernelTC)(?![\w\x27])',code)
        assert not stronger,(name,stronger)
        deps=[x for line in re.findall(r'^\s*import\s+([^\n]+)',code,re.M) for x in line.split()]
        assert deps==record['imports']; imports[name]=deps
        provenance=record.get('historical_provenance')
        if provenance:
            actual=subprocess.check_output(['git','show',provenance['commit']+':'+provenance['path']],cwd=TREE)
            assert actual==data
        rows.append({'module':name,'sha256':sha(data),'git_blob':record['git_blob'],'imports':deps,'forbidden_code_tokens':[]})
    visited=[]
    def visit(name):
        if name in visited or name not in imports:return
        for child in imports[name]:visit(child)
        visited.append(name)
    for root in registry['roots']:visit(root)
    assert visited==v['build_order'] and set(visited)==set(registry['modules'])
    generated=mod.audit_source(registry['roots'],visited,registry['endpoints'])
    assert generated.encode()==(RUN/'source/IntervalClosureAudit.lean').read_bytes()
    assert sha(generated.encode())==v['audit_source_sha256']
    commands=[]
    for c in v['commands']:
        log=RUN/c['log'];data=log.read_bytes(); assert sha(data)==c['log_sha256'] and c['exit_code']==0
        if c['label'] in visited+['IntervalClosureAudit']:
            assert all(flag in c['argv'] for flag in ['--trust=0','-j1','-DElab.async=false'])
        commands.append({'label':c['label'],'exit_code':c['exit_code'],'log':c['log'],'sha256':sha(data),'argv':c['argv']})
    log=(RUN/'logs/IntervalClosureAudit.log').read_text()
    thms=re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$',log,re.M)
    defs=re.findall(r'^AUDIT_DEFINITION (\S+) (\S+) : \[([^\]]*)\]$',log,re.M)
    assert len(thms)==1451 and len(defs)==178
    assert len({x[1] for x in thms})==len(thms) and len({x[1] for x in defs})==len(defs)
    union=set()
    for origin,name,axioms in thms+defs:
        assert origin in registry['modules']; ax={x.strip() for x in axioms.split(',') if x.strip()}; assert ax<=A;(union.update(ax))
    assert union==A
    assert dict(Counter(x[0] for x in thms))==v['theorems_by_module']
    assert dict(Counter(x[0] for x in defs))==v['safe_definitions_by_module']
    assert not re.search(r'CUSTOM_AXIOM|DISALLOWED_|sorryAx|Lean\.ofReduceBool|Lean\.ofReduceNat',log)
    public=[]
    for name in registry['new_modules']:
        code=mod.code_only((P/(name+'.lean')).read_text())
        for kind,short in re.findall(r'^\s*(def|theorem|lemma|opaque|axiom)\s+(\w+)',code,re.M):
            full='P196.Agent9.IntervalCounts.'+short
            matching=[x for x in thms+defs if x[0]==name and x[1]==full];assert len(matching)==1
            public.append({'module':name,'kind':kind,'name':full,'axioms':matching[0][2]})
    assert len(public)==8
    # Verify the author and independent manifests against extracted original bytes.
    sums=[]
    for manifest in [E/'MANIFEST.sha256',E/'review/horizon-safety/SHA256SUMS',C/'SHA256SUMS']:
        checked=0
        for line in manifest.read_text().splitlines():
            if not line.strip():continue
            expected,name=line.split(maxsplit=1);name=name.lstrip('* '); path=manifest.parent/name
            assert path.is_file(),(manifest,name)
            assert sha(path.read_bytes())==expected,(manifest,name);checked+=1
        sums.append({'manifest':str(manifest.relative_to(R)),'files_checked':checked})
    # Author output includes the separate public audit module (no new mathematical declarations).
    av=json.loads((E/'development/full-001/summary.json').read_text())
    for c in av['commands']:
        assert c['exit_code']==0
        for stream in ['stdout','stderr']:
            assert sha((E/'development/full-001'/c[stream+'_file']).read_bytes())==c[stream+'_sha256']
    assert (E/'Agent9IntervalCountsAudit.lean').read_bytes()==(P/'Agent9IntervalCountsAudit.lean').read_bytes()
    assert (E/'development/full-001/new-source-snapshot/Agent9IntervalCountsAudit.lean').read_bytes()==(P/'Agent9IntervalCountsAudit.lean').read_bytes()
    # Retained failed attempt must remain failed; it is not part of an accepted proof chain.
    failed=json.loads((C/'runs/numeric-boundaries-001/verification.json').read_text())
    passed=json.loads((C/'runs/numeric-boundaries-002/verification.json').read_text())
    assert failed['status']=='FAIL' and failed['exit_code']==1
    assert passed['status']=='PASS' and passed['exit_code']==0
    for label, rec in [('numeric-boundaries-001',failed),('numeric-boundaries-002',passed)]:
        d=C/'runs'/label
        assert sha((d/'Agent9DigitSumIndependentReview.lean').read_bytes())==rec['source_sha256']
        for stream in ['stdout','stderr']:
            assert sha((d/(stream+'.log')).read_bytes())==rec[stream+'_sha256']
        assert rec['closure_verification_sha256']==sha((RUN/'verification.json').read_bytes())
    assert 'sorryAx' in (C/'runs/numeric-boundaries-001/stdout.log').read_text()
    assert all(set(axioms)<=A for axioms in passed['printed_axioms'].values())
    assert 'sorryAx' not in (C/'runs/numeric-boundaries-002/stdout.log').read_text()
    notes=subprocess.check_output(['git','show','2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5:proofs/research/continuation/strengthening_notes.txt'],cwd=TREE)
    assert notes==(C/'strengthening_notes.source.txt').read_bytes()
    assert sha(notes)=='15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f'
    report['written_source_sha256']=sha(notes)
    report['numeric_boundary_records']={'failed':failed,'passed':passed}
    oldroot=Path(v['compiler']['runtime_root']);newroot=Path('/workspace/scratch/8b5152316f75/runtime-agent1/toolchain/lean-4.19.0-linux')
    runtime=[]
    for old,digest in v['compiler']['files'].items():
        relative=Path(old).relative_to(oldroot);current=newroot/relative
        assert current.is_file() and sha(current.read_bytes())==digest
        runtime.append({'relative_path':str(relative),'sha256':digest})
    report.update(status='PASS_RETAINED_EVIDENCE_VALIDATED',fresh_lean_build='NOT_RUN_RUNTIME_UNAVAILABLE',retained_executor=v['auditor'],retained_started_epoch=v['started_epoch'],retained_finished_epoch=v['finished_epoch'],source_rows=rows,commands=commands,retained_verification_sha256=sha((RUN/'verification.json').read_bytes()),retained_audit_log_sha256=sha(log.encode()),workflow_sha256=v['workflow_sha256'],registry_sha256=v['manifest_sha256'],audited_theorems=len(thms),audited_safe_definitions=len(defs),public_declarations=public,axiom_union=sorted(union),unsafe_implementation_axioms=len(v['unsafe_implementation_constants']),unsafe_implementation_definitions=len(v['unsafe_implementation_definitions']),manifest_checks=sums,runtime_files_compared=runtime,runtime_scope='Eight recorded runtime files match. This is not complete transitive standard-library binary authentication or a fresh runtime execution.',repository_wide_pass=False)
except BaseException as error:
    report.update(status='FAIL',error=repr(error));write(R/'retained-evidence-validation.json',report);raise
write(R/'retained-evidence-validation.json',report)
print(json.dumps({k:report[k] for k in ['status','fresh_lean_build','retained_executor','audited_theorems','audited_safe_definitions','axiom_union','unsafe_implementation_axioms','unsafe_implementation_definitions','workflow_sha256','registry_sha256','retained_verification_sha256','retained_audit_log_sha256','manifest_checks']},indent=2))
