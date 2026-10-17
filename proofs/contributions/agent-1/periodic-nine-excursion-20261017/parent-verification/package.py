#!/usr/bin/env python3
"""Validate and package completed canonical evidence; never execute Lean."""
from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
ORIGINAL=Path('/workspace/p196-agent1-session-20261016/nine-excursion-parent-clean-001')
CONSOLE=ORIGINAL.with_name(ORIGINAL.name+'.console.log')
COMMIT='ee58c494d1021aa27ff71ef75653b962cf6a2006'
PROJECT='agent1-periodic-nine-excursion'
REGISTRY='proofs/Agent1PeriodicNinesExcursion.registry.json'
CHECKER='proofs/verify_project__214bf7673efe116b.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
published=lambda p:subprocess.check_output(['git','show',COMMIT+':'+p],cwd=ROOT)
manifest_bytes=(ORIGINAL/'FILES.json').read_bytes()
manifest=json.loads(manifest_bytes)
report_bytes=(ORIGINAL/'verification.json').read_bytes()
report=json.loads(report_bytes);project=report['projects'][PROJECT]
assert report['status']==project['status']=='PASS'
assert report['source_commit']==COMMIT and report['source_tree_clean'] is True
assert set(report['projects'])=={PROJECT}
for path,entry in manifest.items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    assert Path(path).suffix in ['.lean','.log','.json']
    raw=(ORIGINAL/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
module_count=len(project['sources']);commands=project['commands'];command_count=len(commands)
assert len(project['build_order'])==module_count
assert command_count==module_count+1
assert [c['label'] for c in commands]==project['build_order']+['ProjectAudit']
assert all(c['exit_code']==0 for c in commands)
for c in commands:
    assert not any(x.startswith('--trust') for x in c['argv'])
    assert '-j1' in c['argv'] and '-DElab.async=false' in c['argv']
    assert sha((ORIGINAL/c['log']).read_bytes())==c['log_sha256']
log=(ORIGINAL/PROJECT/'logs/ProjectAudit.log').read_text()
rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)\s*:\s*\[([^\]]*)\]',log,re.M)
assert len(rows)==project['theorem_count']
assert len({name for mod,name,axs in rows})==len(rows)
summary=re.search(r'FULL_MODULE_AUDIT theorems=(\d+) union=\[([^\]]*)\]',log)
assert summary and int(summary[1])==len(rows)
union=sorted({a.strip() for mod,name,axs in rows for a in axs.split(',') if a.strip()})
allowed={'propext','Classical.choice','Quot.sound'}
assert set(union)<=allowed
assert '['+', '.join(union)+']'==project['axiom_union']
assert set(a.strip() for a in summary[2].split(',') if a.strip())==set(union)
console_bytes=CONSOLE.read_bytes();console_lines=console_bytes.decode().splitlines()
assert console_lines==[PROJECT+' '+c['label']+' exit=0' for c in commands]
registry=(ROOT/REGISTRY).read_bytes();checker=(ROOT/CHECKER).read_bytes()
assert registry==published(REGISTRY) and checker==published(CHECKER)
assert sha(registry)==report['registry_sha256']=='f169295f2aa28b7f433cf8512a128644b7f28d85628f17b38a137e15b29e4a9e'
assert sha(checker)=='c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
reg=json.loads(registry);registered=reg['projects'][PROJECT]['modules']
assert set(project['sources'])==set(project['build_order'])==set(registered)
assert project['endpoints']==[e for c in reg['claims'] if c['project']==PROJECT for e in c['endpoints']]
assert 'version 4.19.0' in report['compiler']['version']
assert report['compiler']['files']['/workspace/p196-tools/lean-4.19.0-linux/bin/lean']=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
for path,digest in report['compiler']['files'].items():assert sha(Path(path).read_bytes())==digest,path
pins=[]
for name,entry in project['sources'].items():
    raw=(ROOT/entry['path']).read_bytes();built=(ORIGINAL/PROJECT/'source'/(name+'.lean')).read_bytes()
    pin=registered[name]
    assert raw==built==published(entry['path'])
    assert sha(raw)==entry['sha256']==entry['build_sha256']==pin['sha256']
    assert entry['path']==pin['path'] and entry['imports']==pin['imports'] and entry['adapter'] is None
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert blob==pin['git_blob']
    pins.append({'module':name,'path':entry['path'],'sha256':sha(raw),'git_blob':blob,'published_current_compiled_registry_bytes_equal':True})
expected_files={PROJECT+'/source/'+name+'.lean' for name in project['build_order']}
expected_files|={c['log'] for c in commands}|{PROJECT+'/source/ProjectAudit.lean','verification.json'}
assert set(manifest)==expected_files
source_count=sum(Path(p).suffix=='.lean' for p in manifest)
log_count=sum(Path(p).suffix=='.log' for p in manifest)
assert source_count==log_count==command_count
# Only the original manifest's text payload is copied. Objects stay outside Git.
dest=HERE/'parent-clean-001';dest.mkdir(exist_ok=False)
for path in manifest:
    target=dest/path;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ORIGINAL/path,target);assert target.read_bytes()==(ORIGINAL/path).read_bytes()
(dest/'FILES.json').write_bytes(manifest_bytes)
(HERE/'parent-console.log').write_bytes(console_bytes)
(HERE/'registry.json').write_bytes(registry)
(HERE/'canonical-verifier.py').write_bytes(checker)
dump(HERE/'publication-source-receipt.json',{'status':'PASS_SOURCE_IDENTITY','published_source_commit':COMMIT,'module_count':module_count,'registry_path':REGISTRY,'registry_sha256':sha(registry),'checker_path':CHECKER,'checker_sha256':sha(checker),'sources':pins,'lean_executed_by_packager':False})
dump(HERE/'parent-launch.json',{'evidence_kind':'Root executor confirmation supplied in this packaging assignment','argv':['python3',CHECKER,'--lean','/workspace/p196-tools/lean-4.19.0-linux/bin/lean','--output',str(ORIGINAL),'--project',PROJECT,'--registry',REGISTRY],'cwd':str(ROOT),'tool_session_id':21466,'actual_exit_code':0,'per_lean_argv_source':'parent-clean-001/verification.json','confirmation':'Root explicitly supplied this actual launch argv and session exit. Specialist control_review packaged the already completed run without re-executing it.'})
elapsed=report['finished_at_epoch']-report['started_at_epoch']
addendum={'status':'PASS_PRESERVED_PARENT_RUN','original_source_commit':COMMIT,'original_source_tree_clean':report['source_tree_clean'],'clean_field_limit':'Canonical verifier checks tracked files and excludes untracked files. The original report is unchanged.','all_source_and_registry_bytes_match_published_commit':True,'modules':module_count,'commands':command_count,'all_command_exits_zero':True,'theorem_constants':project['theorem_count'],'theorem_axiom_union':union,'public_endpoints':project['endpoints'],'separate_unsafe_implementation_axioms':len(project['unsafe_implementation_axioms']),'safe_definition_audit_claimed_here':False,'explicit_trust_zero':False,'flags_limit':'The actual canonical argv lacks --trust=0. No trust default is inferred; this run is not relabeled as the separate strict independent review.','original_started_at_epoch':report['started_at_epoch'],'original_finished_at_epoch':report['finished_at_epoch'],'elapsed_seconds':elapsed,'original_manifest_entries':len(manifest),'original_manifest_sha256':sha(manifest_bytes),'original_report_sha256':sha(report_bytes),'original_console_sha256':sha(console_bytes),'packaging_driver_sha256':sha(Path(__file__).read_bytes()),'original_files_changed':False,'lean_rerun_by_packager':False,'packager':'Agent #1 specialist control_review','packager_role':'Continuing root-assigned registry/evidence support; packages root execution, authors no math, claims no independent execution or final mathematical review.','existing_attributed_registry_check_in':'https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6228610542','independent_final_review_owner':'Agent #1 specialist center_review_resume'}
dump(HERE/'parent-result-addendum.json',addendum)
(HERE/'README.md').write_text(f'''# Preserved parent canonical nine-excursion verification

This package preserves the completed run executed by Agent #1 root. Specialist control_review validated and packaged stored evidence under the continuing registry/evidence assignment. The packager authored no mathematical source, ran no Lean, and claims no independent execution or final mathematical review. That separate review belongs to center_review_resume.

The original report records PASS for {module_count} modules and ProjectAudit: {command_count} commands, all exit zero, and {project['theorem_count']:,} module-origin theorem constants. The theorem axiom union is {', '.join(union)}. It separately inventories {len(project['unsafe_implementation_axioms'])} inherited generated unsafe implementation axioms, which are not accepted theorem dependencies. This canonical receipt makes no separate safe-definition audit claim. All {len(project['endpoints'])} registry endpoints are retained.

Source commit: {COMMIT}. Registry SHA256: {sha(registry)}. All {module_count} compiled source snapshots match current source, the exact published commit, and registry SHA256/Git-blob pins. The report's original source_tree_clean=true is retained; that checker examines tracked files and excludes untracked files. The registry's historical fresh-review-pending text remains unchanged.

Every actual Lean argv is retained in parent-clean-001/verification.json. The commands use -j1 -DElab.async=false and lack explicit --trust=0. No compiler trust default is inferred, and the canonical run is not relabeled as the separate strict review. Official Lean 4.19.0 version/compiler/library hashes are preserved and matched against the current files. Elapsed report time: {elapsed} seconds.

parent-launch.json records root's confirmed top-level Python argv, working directory, executor session 21466 and actual exit zero. That outer launch is root-provided executor evidence; child argv, exits and log hashes come directly from the unchanged original report. parent-console.log is a byte-identical copy of the original console output.

All {len(manifest)} original manifest members are copied unchanged into parent-clean-001/, together with the untouched original FILES.json. They comprise {source_count} Lean source snapshots including ProjectAudit, {log_count} logs and the report. Compiled objects are excluded. registry.json and canonical-verifier.py are exact published snapshots. The original output, report, logs and manifest remain untouched.

publication-source-receipt.json records all source comparisons; parent-result-addendum.json records the preserved result and limits. package.py contains the executed packaging logic, with the prior center package identified in helper-provenance.json. No additional issue history was copied: this continues the attributed registry/evidence role from issue61 comment6228610542.

PACKAGE-FILES.json hashes every package file except itself and frozen-receipt.json; the latter binds that complete manifest and both receipts. This is only the recorded excursion project check. It supplies no actual cycle, unrestricted no-return theorem, repository-wide build, or conclusion about196. No source or Git state was modified by the packager.
''')
# Recheck original and copied evidence before sealing.
assert (ORIGINAL/'FILES.json').read_bytes()==manifest_bytes and (ORIGINAL/'verification.json').read_bytes()==report_bytes
for path,entry in manifest.items():
    for base in [ORIGINAL,dest]:
        raw=(base/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
assert (dest/'FILES.json').read_bytes()==manifest_bytes
package={}
for path in sorted(HERE.rglob('*')):
    if path.is_file() and path.name not in ['PACKAGE-FILES.json','frozen-receipt.json']:
        assert path.suffix not in ['.olean','.ilean','.pyc']
        package[str(path.relative_to(HERE))]={'bytes':path.stat().st_size,'sha256':sha(path.read_bytes())}
dump(HERE/'PACKAGE-FILES.json',package)
for path,entry in package.items():
    raw=(HERE/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
dump(HERE/'frozen-receipt.json',{'status':'SEALED','packager':'Agent #1 specialist control_review','execution_owner':'Agent #1 root','published_source_commit':COMMIT,'lean_rerun_by_packager':False,'payload_file_count':len(package),'total_file_count':len(package)+2,'manifest_file':'PACKAGE-FILES.json','manifest_sha256':sha((HERE/'PACKAGE-FILES.json').read_bytes()),'result_receipt_sha256':sha((HERE/'parent-result-addendum.json').read_bytes()),'source_receipt_sha256':sha((HERE/'publication-source-receipt.json').read_bytes()),'manifest_scope':'All package files except this frozen receipt and PACKAGE-FILES.json; seal hash separately reported.','compiled_objects_packaged':False,'original_manifest_entries':len(manifest),'original_manifest_sha256':sha(manifest_bytes),'original_report_sha256':sha(report_bytes),'actual_root_session':21466,'actual_root_exit_code':0,'explicit_trust_zero_in_actual_commands':False})
print(json.dumps({'status':'SEALED','modules':module_count,'commands':command_count,'theorems':project['theorem_count'],'original_manifest_entries':len(manifest),'package_entries':len(package),'package_manifest_sha256':sha((HERE/'PACKAGE-FILES.json').read_bytes()),'seal_sha256':sha((HERE/'frozen-receipt.json').read_bytes()),'total_file_count':len(package)+2},indent=2))
