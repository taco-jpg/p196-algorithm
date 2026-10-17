from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,shutil,subprocess
BASE=Path('/dev/shm/p196-agent15-43cf6e114472')
REPO=BASE/'support-repo'
REL='proofs/contributions/agent-15/spectral-carry-support-43cf6e114472'
PKG=REPO/REL
SRC=BASE/'support-runtime-review'
OUT=PKG/'evidence/runtime'
FROZEN='5d02e88f13f59f6fcd09cf75d8c7f188c6645727'
def sha(b):return hashlib.sha256(b).hexdigest()
def writej(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
copies=[]
def cp(s,d):
 d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
 assert s.read_bytes()==d.read_bytes()
 copies.append({'original':str(s),'published_path':str(d.relative_to(PKG)),'bytes':d.stat().st_size,'sha256':sha(d.read_bytes())})
manifest=json.loads((SRC/'delivery/support-runtime-review-5d02e88f.manifest.json').read_text())
archive=SRC/'delivery/support-runtime-review-5d02e88f.tar.gz'
assert sha(archive.read_bytes())==manifest['archive']['sha256']=='68eab748354f39718999bc454e0a2f5d821552991a62f94f2c62010aa069b168'
assert archive.stat().st_size==6470203
seen=set()
with tarfile.open(archive,'r:gz') as tf:
 for m in tf.getmembers():
  p=PurePosixPath(m.name)
  assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='support-runtime-review'
  if m.isdir():continue
  assert m.isfile()
  rel=str(PurePosixPath(*p.parts[1:]));data=tf.extractfile(m).read();rec=manifest['files'][rel]
  assert len(data)==rec['bytes'] and sha(data)==rec['sha256']
  assert rel not in seen;seen.add(rel)
assert seen==set(manifest['files']) and len(seen)==143
cp(archive,OUT/archive.name)
cp(SRC/'delivery/support-runtime-review-5d02e88f.manifest.json',OUT/'support-runtime-review-5d02e88f.manifest.json')
selected=['FROZEN_EXECUTION_REVIEW.md','review-summary.json','review-manifest.json','declaration-coverage.tsv','implementation-artifacts.json','endpoint-summary.json','source-hashes.tsv','generated-product-inventory.json','historical-manifest-reconciliation.json','freeze-record.json','gate-invocation-001.json','gate-invocation-001.log','frozen-5d02e88f-attempt-001/verification.json','supplemental-public-print-001/verification.json','supplemental-public-print-001/FullPublicPrint.lean']
for n in selected:cp(SRC/n,OUT/n)
for f in sorted((SRC/'frozen-5d02e88f-attempt-001/logs').glob('build-*.log')):
 cp(f,OUT/'frozen-5d02e88f-attempt-001/logs'/f.name)
cp(Path(__file__),PKG/'development/root/package-support-runtime.py')
writej(PKG/'evidence/runtime-copy-manifest.json',{'all_143_archive_members_revalidated':True,'archive_kept_byte_identical':True,'readable_copies':copies,'other_original_paths':'Retained completely inside the archive under support-runtime-review/. The archive is the full historical evidence tree; readable copies are entry points, not replacements.'})
build=json.loads((PKG/'BUILD.json').read_text())
for m,rec in build['source_pins'].items():
 actual=(REPO/rec['path']).read_bytes()
 assert sha(actual)==rec['sha256']
 assert actual==subprocess.check_output(['git','show',FROZEN+':'+rec['path']],cwd=REPO)
author=json.loads((PKG/'evidence/author/verification.json').read_text())
assert author['status']=='PASS' and author['source_unchanged'] and author['runtime_unchanged'] and author['configuration_unchanged']
assert sha((PKG/'check.py').read_bytes())==author['checker_sha256']=='b9466cdfd0bf667fe82d9acbf68a15670be294370af5f0366f998615fc78d814'
assert sha((PKG/'BUILD.json').read_bytes())==author['build_manifest_sha256']=='2b7e1e9527ea69d093ac5dcef32ea10c5c1933f88311f1a4be386867f7de2c3e'
runtime=json.loads((SRC/'review-summary.json').read_text())
assert runtime['origin_declarations']==2410 and runtime['safe_declarations']==1525 and runtime['implementation_declarations']==885
semantic_path=PKG/'evidence/semantic/FINAL_SEMANTIC_REVIEW.md'
writej(PKG/'ACCEPTANCE.json',{'schema_version':1,'task_id':'agent15-spectral-carry-support-43cf6e114472','status':'INDEPENDENTLY_REVIEWED','pull_request':152,'frozen_mathematical_source_commit':FROZEN,'frozen_mathematical_source_tree':'f0594cce1d8b4888561edb4ed22770ab4a6a991a','new_source':build['source_pins']['ActualCarrySupport'],'canonical_driver':{'status':'PASS','checker_sha256':author['checker_sha256'],'immutable_BUILD_sha256':author['build_manifest_sha256'],'receipt':'evidence/author/verification.json','receipt_sha256':sha((PKG/'evidence/author/verification.json').read_bytes()),'fresh_modules':8,'Lean_commands':10,'new_explicit_public_exports':22,'critical_prerequisites':15,'actual_print_and_axiom_audits':37,'runtime_olean_inventory_count':1471,'source_runtime_and_configuration_unchanged':True},'independent_semantic_review':{'status':'PASS','reviewer':'/root/support_semantics','source_commit':FROZEN,'report':'evidence/semantic/FINAL_SEMANTIC_REVIEW.md','report_sha256':sha(semantic_path.read_bytes()),'Lean_executed_by_semantic_reviewer':False,'no_unresolved_semantic_findings':True},'independent_execution_review':{'status':runtime['verdict'],'reviewer':'/root/support_runtime','source_commit':FROZEN,'report':'evidence/runtime/FROZEN_EXECUTION_REVIEW.md','report_sha256':sha((SRC/'FROZEN_EXECUTION_REVIEW.md').read_bytes()),'fresh_modules':8,'all_origin_declarations':2410,'safe_declarations':1525,'safe_private_declarations':93,'implementation_declarations':885,'unsafe_axiomInfo_implementations':14,'partial_implementation_definitions':23,'safe_axiomInfo_declarations':0,'safe_axiom_union':runtime['safe_axiom_union'],'new_safe_public_declarations':36,'critical_prerequisites_printed':12,'complete_unelided_public_and_prerequisite_prints':48,'remaining_public_print_elisions':0,'print_supplement_is_another_full_build':False,'raw_implementation_axioms_preserved_and_separated':True,'project_objects_reused_in_full_gate':False,'official_compiled_standard_runtime_reused':True},'eight_pinned_sources_unchanged_at_packaging':True,'original_CONTRACT_and_CLAIM_unchanged':True,'repository_integration':'PENDING_DESIGNATED_DELIVERY_OWNER','predecessor':{'pull_request':145,'source_commit':'e8d706dc8a67248e1531b0b828fbe05ff50052ed','final_review_publication':'679d10a5b1382b51b68a7240bb9c6562ccf144d9','delivery_owner':'Agent #25/session677aa81c663a'},'main_write_slot_claimed':False,'acceptance_scope':'Exact selected actual-carry neutral-nine support theorem and its complete project closure, not repository-wide formalization or an all-time claim about196.'})
history=json.loads((PKG/'development/root/publication-history.json').read_text())
writej(PKG/'PUBLICATION.json',{'repository':'taco-jpg/p196-algorithm','branch':'formalize/agent-15/spectral-carry-support-43cf6e114472','pull_request':152,'protected_claim':'3de89d0bd03534c92f65886a29b7996525571ff5','checkpoints':[{'kind':x['kind'],'local_commit':x['local_commit'],'remote_commit':x['remote_commit'],'identical_tree':x['tree']} for x in history['publications']],'mathematical_source_freeze':FROZEN,'next_publication_kind':'Frozen checker configuration, full author/reviewer evidence, acceptance records, and documentation; no reviewed mathematical source change.','local_and_remote_commit_identity':'Local Git and GitHub connector commits have different metadata. Each publication requires exact tree identity before ref update; immutable remote commit/ref readbacks are preserved separately.','source_tree_combination_rule':'Normal ancestry-based integration must preserve the final PR145 documentation/evidence added after this branch forked. Do not replace the predecessor package tree with this branch historical snapshot.','delivery_status':'No support delivery claim or main write slot taken by Agent15; publish final reviewed PR and hand off through issue61.'})
for n in ['CONTRACT.md','CLAIM.json','ActualCarrySupport.lean']:
 assert (PKG/n).read_bytes()==subprocess.check_output(['git','show',FROZEN+':'+REL+'/'+n],cwd=REPO)
print(json.dumps({'runtime_archive_verified_members':len(seen),'runtime_readable_copies':len(copies),'runtime_archive_bytes':archive.stat().st_size,'acceptance_status':'INDEPENDENTLY_REVIEWED','mathematical_sources_and_checker_unchanged':True,'runtime_report_sha256':sha((SRC/'FROZEN_EXECUTION_REVIEW.md').read_bytes()),'semantic_report_sha256':sha(semantic_path.read_bytes())}))
