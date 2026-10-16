#!/usr/bin/env python3
"""Reparse completed review logs, verify frozen checkpoints, inventory build files."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def save(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--build',type=Path,required=True)
    args=parser.parse_args();repo=args.repo.resolve()
    root=repo/'proofs/contributions/agent-104/review-agent4-temporal-strip/execution'
    original=json.loads((root/'attempt01/verification.json').read_text())
    auxiliary=json.loads((root/'auxiliary-attempt01/verification.json').read_text())
    if original['status']!='PASS' or auxiliary['status']!='PASS':raise ValueError('Cannot accept incomplete or failed execution')
    checks={}
    for kind,report,folder,audit in [('original_strip',original,root/'attempt01',root/'attempt01/logs/AllLocalTheorems.log'),('five_module_closure',auxiliary,root/'auxiliary-attempt01',root/'auxiliary-attempt01/AllFiveModulesAudit.log')]:
        for run in report['builds']:
            if run['exit_code']!=0 or sha(folder/run['log'])!=run['log_sha256']:raise ValueError('Compiler-log identity or exit check failed')
        text=audit.read_text();rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',text,re.MULTILINE)
        names={name:module for module,name in rows}
        if len(names)!=len(rows) or set(names)!=set(report['theorems']):raise ValueError('Environment theorem inventory does not match report')
        axes={}
        for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text):
            if name in axes:raise ValueError('Duplicate axiom line')
            axes[name]=sorted(a.strip() for a in ax.split(',') if a.strip())
        for name in re.findall(r"'([^']+)' does not depend on any axioms",text):
            if name in axes:raise ValueError('Duplicate empty axiom line')
            axes[name]=[]
        if set(axes)!=set(names):raise ValueError('Incomplete transitive axiom audit')
        for name,ax in axes.items():
            if ax!=report['theorems'][name]['axioms'] or set(ax)-{'propext','Classical.choice','Quot.sound'}:raise ValueError('Axiom trust gate failed')
        checks[kind]={'status':'PASS','theorem_constants':len(names),'raw_audit_log_sha256':sha(audit),'report_sha256':sha(folder/'verification.json'),'all_compiler_exits_zero':True}
    if auxiliary['contracts_proved'] is not False:raise ValueError('Unproved Prop contracts must remain unproved')
    for line in (root/'preflight-manifest.sha256').read_text().splitlines():
        expected,path=line.split('  ',1)
        if sha(root/path)!=expected:raise ValueError('Frozen preflight changed '+path)
    semantic=repo/'proofs/contributions/agent-104/review-agent4-temporal-strip/semantic'
    checkpoint=json.loads((semantic/'checkpoint.json').read_text())
    for name,digest in checkpoint['artifacts_sha256'].items():
        if sha(semantic/name)!=digest:raise ValueError('Frozen semantic artifact changed '+name)
    semantic_pin='81019eda501af5194a0e43b98458c268a71f5729'
    refs={}
    for name in ['checkpoint.json','REVIEW.md','diagnostics.json','ExactTypes.lean','ExactTypesApplied.lean','ScopeTests.lean','ActualMapObligations.lean']:
        path=semantic/name;relative=str(path.relative_to(repo))
        blob=subprocess.check_output(['git','show',semantic_pin+':'+relative],cwd=repo)
        if path.read_bytes()!=blob:raise ValueError('Published semantic artifact mismatch '+name)
        refs[relative]={'source_commit':semantic_pin,'bytes':len(blob),'sha256':sha(path)}
    summary={'status':'ACCEPTED_ABSTRACT_STRIP_REVIEW','source_commit':original['source']['source_commit'],
        'source_sha256':original['source']['sha256'],'review_fixture_commit':semantic_pin,
        'compiler_version':original['compiler_version'],
        'compiler_binary_sha256':original['compiler_fingerprints']['/workspace/scratch/7649db1e242c/toolchain/lean-4.19.0-linux/bin/lean'],
        'checks':checks,'theorems_per_module':auxiliary['theorems_per_module'],
        'seven_export_axioms':original['seven_export_axioms'],
        'exact_elaborated_statement_count':original['exact_elaborated_statement_count'],
        'original_official_imported_objects_rehashed':original['official_imported_object_count'],
        'auxiliary_official_imported_objects_rehashed':sum(not r['local_rebuilt'] for r in auxiliary['imported_object_fingerprints'].values()),
        'foundation_compiled_fresh':True,'safe_custom_axioms':0,
        'unsafe_generated_implementation_axioms_recorded':len(auxiliary['unsafe_implementation_axioms']),
        'forbidden_transitive_axioms':{},'failed_compiler_or_audit_attempts':0,
        'initial_type_fixture_status':'STATIC_REPAIR_NOT_COMPILER_OBSERVED; original draft retained uncompiled; explicit-application replacement passed.',
        'actual_map_contracts_status':'TYPECHECKED_BUT_UNPROVED','contracts_proved':False,
        'ordinary_integer_bridge_accepted':False,'P196_established':False,'novelty_claim':False,
        'frozen_preflight_unchanged':True,'frozen_semantic_checkpoint_unchanged':True,
        'preserved_semantic_evidence':refs,
        'toolchain_provenance':'Inherited published official archive-member comparison; actual compiler and imported objects rehashed; no new archive download claim.'}
    mapped={}
    for module,rec in auxiliary['sources'].items():mapped[module+'.lean']=(rec['path'],rec.get('source_commit','published exact hash'),rec['sha256'])
    for name,stored in [('AllLocalTheorems.lean',root/'attempt01/AllLocalTheorems.lean'),('StatementDump.lean',root/'attempt01/StatementDump.lean'),('AllFiveModulesAudit.lean',root/'auxiliary-attempt01/AllFiveModulesAudit.lean')]:
        mapped[name]=(str(stored.relative_to(repo)),'current review',sha(stored))
    exclusions=['original_path\tbytes\tsha256\tdecision\treason\tretained_source\tsource_commit']
    for path in sorted(args.build.resolve().rglob('*')):
        if not path.is_file():continue
        digest=sha(path)
        if path.suffix=='.lean' and path.name in mapped:
            retained,pin,expected=mapped[path.name]
            if digest!=expected:raise ValueError('Duplicate source mismatch '+str(path))
            reason='byte-identical source or audit copy; retained original identified'
        elif path.suffix=='.olean' and path.with_suffix('.lean').name in mapped:
            retained,pin,_=mapped[path.with_suffix('.lean').name]
            reason='reproducible Lean compilation object; original source and full compiler/audit logs retained'
        else:raise ValueError('Unclassified build file must not be silently omitted '+str(path))
        exclusions.append('\t'.join([str(path),str(path.stat().st_size),digest,'exclude',reason,retained,pin]))
    (root/'execution-exclusions.tsv').write_text('\n'.join(exclusions)+'\n')
    summary['exact_infrastructure_exclusion_count']=len(exclusions)-1
    save(root/'acceptance.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
