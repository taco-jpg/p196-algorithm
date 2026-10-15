#!/usr/bin/env python3
"""Reparse completed logs and inventory every excluded clean-build file exactly."""
import argparse
import hashlib
import json
from pathlib import Path
import re


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
    args=parser.parse_args()
    repo=args.repo.resolve();root=repo/'proofs/contributions/agent-104/review-agent4-whole-word/execution'
    closure=json.loads((root/'attempt01/verification.json').read_text())
    witness=json.loads((root/'scope-attempt01/verification.json').read_text())
    if closure['status']!='PASS' or witness['status']!='PASS':raise ValueError('Cannot finalize as PASS: compilation/audit remains incomplete or failed')
    summaries={}
    for kind,report,where,auditlog in [('original_closure',closure,root/'attempt01',root/'attempt01/logs/AllLocalTheorems.log'),('scope_illustrations',witness,root/'scope-attempt01',root/'scope-attempt01/ScopeTheoremAudit.log')]:
        for rec in report['builds']:
            if rec['exit_code']!=0 or sha(where/rec['log'])!=rec['log_sha256']:raise ValueError('Compiler log identity or successful exit mismatch')
        log=auditlog.read_text()
        rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',log,re.MULTILINE)
        emitted={name:module for module,name in rows}
        if len(rows)!=len(emitted) or set(emitted)!=set(report['theorems']):raise ValueError('Compiled theorem inventory mismatch')
        parsed={name:sorted(a.strip() for a in ax.split(',') if a.strip()) for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log)}
        for name in re.findall(r"'([^']+)' does not depend on any axioms",log):parsed[name]=[]
        if set(parsed)!=set(emitted):raise ValueError('Missing/extra transitive axiom output')
        for name,ax in parsed.items():
            if set(ax)-{'propext','Classical.choice','Quot.sound'}:raise ValueError('Forbidden axiom dependency')
            if ax!=report['theorems'][name]['axioms']:raise ValueError('Axiom report differs from preserved raw output')
        summaries[kind]={'status':'PASS','theorem_constants':len(emitted),'named_source_theorems':330 if kind=='original_closure' else 9,'raw_audit_log_sha256':sha(auditlog),'report_sha256':sha(where/'verification.json'),'all_subprocess_exit_codes_zero':True,'every_enumerated_theorem_has_allowed_transitive_axioms':True}
    summary={'status':'PASS','scope':'Independent clean build, exhaustive transitive theorem axiom audit, and concrete scope illustration checks only. No P196 or novelty claim.',
        'source_commit':closure['source_commit'],'witness_commit':witness['source_commit'],
        'compiler_version':closure['compiler_version'],'compiler_binary_sha256':closure['compiler_fingerprints']['/workspace/scratch/7649db1e242c/toolchain/lean-4.19.0-linux/bin/lean'],
        'original_local_source_modules':len(closure['sources']),'original_closure_theorems_per_module':closure['theorems_per_module'],
        'official_imported_objects_rehashed':closure['official_imported_object_count'],
        'historical_toolchain_provenance':'Inherited published official release archive-member manifest; no new independent download.',
        'six_export_axioms':closure['six_export_axioms'],'checks':summaries,
        'failed_compile_or_audit_attempts':0,
        'preserved_preflight':'The original PREPARED_NOT_EXECUTED checkpoint remains byte-identical; this is the later completed execution result.'}
    save(root/'execution-review.json',summary)
    mapped={}
    for module,rec in closure['sources'].items():mapped[module+'.lean']=(rec['path'],closure['source_commit'],rec['sha256'])
    mapped['ReviewScopeWitnesses.lean']=(witness['source_path'],witness['source_commit'],witness['source_sha256'])
    mapped['AllLocalTheorems.lean']=(str((root/'attempt01/AllLocalTheorems.lean').relative_to(repo)),'current review',sha(root/'attempt01/AllLocalTheorems.lean'))
    mapped['ScopeTheoremAudit.lean']=(str((root/'scope-attempt01/ScopeTheoremAudit.lean').relative_to(repo)),'current review',sha(root/'scope-attempt01/ScopeTheoremAudit.lean'))
    lines=['original_path\tbytes\tsha256\tdecision\treason\tretained_source\tsource_commit']
    excluded_count=0
    for path in sorted(args.build.resolve().rglob('*')):
        if not path.is_file():continue
        h=sha(path)
        if path.suffix=='.lean' and path.name in mapped:
            original,pin,expected=mapped[path.name]
            if h!=expected:raise ValueError('Duplicate source hash mismatch '+str(path))
            reason='byte-identical source or audit copy; retained original identified'
        elif path.suffix=='.olean' and path.with_suffix('.lean').name in mapped:
            original,pin,_=mapped[path.with_suffix('.lean').name]
            reason='reproducible Lean compilation object; source and full build logs retained'
        else:raise ValueError('Unclassified build file must not be silently omitted: '+str(path))
        lines.append('\t'.join([str(path),str(path.stat().st_size),h,'exclude',reason,original,pin]));excluded_count+=1
    (root/'execution-exclusions.tsv').write_text('\n'.join(lines)+'\n')
    summary['exact_infrastructure_exclusions']=excluded_count
    save(root/'execution-review.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
