from pathlib import Path, PurePosixPath
import hashlib,json,shutil,tarfile,subprocess
BASE=Path('/dev/shm/p196-agent15-43cf6e114472')
REPO=BASE/'repo'
REL='proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472'
PKG=REPO/REL
FROZEN='e8d706dc8a67248e1531b0b828fbe05ff50052ed'
NAMES=['SpectralWeights','BinaryCode','ChargeSymmetry','SourceFormula','ChargeControls']
def sha(b): return hashlib.sha256(b).hexdigest()
def writej(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def verify_source():
 for n in [*[x+'.lean' for x in NAMES],'check.py']:
  assert (PKG/n).read_bytes()==subprocess.check_output(['git','show',FROZEN+':'+REL+'/'+n],cwd=REPO),n
verify_source()
ops=PKG/'development/root';ops.mkdir(parents=True,exist_ok=True)
writej(ops/'review-packaging-failures.json',[
 {'attempt':1,'operation':'Copy runtime archive records into readable review tree','exit_code':1,'diagnostic':'ValueError: Non-file archive member','cause':'The initial script rejected the valid first directory member runtime-review.','effects':'Only an empty destination directory was created. No source, checker, review or documentation changed.','resolution':'Accept safe directories, copy regular files, reject links and unsafe paths; retain original archive.'},
 {'attempt':2,'operation':'Submit packaging script through orchestration','executed':False,'diagnostic':'SyntaxError: Unexpected string','cause':'Incorrect quoting in the submitted JavaScript string.','effects':'Orchestrator rejected the script before execution; no filesystem mutation.','resolution':'Use a quoted shell heredoc and raw JavaScript string.'}
])
shutil.copyfile(Path(__file__),ops/'package-charge-reviews.py')
ind=PKG/'evidence/independent';runt=ind/'runtime';sem=ind/'semantic'
archive=BASE/'runtime-review/delivery/runtime-review-e8d706dc.tar.gz'
assert sha(archive.read_bytes())=='b5d335c483e4b94ac573f4d00f047cc2cfa4303864469620cd1c20c8ead2b261'
copied=[];objects=[]
with tarfile.open(archive,'r:gz') as tf:
 for m in tf.getmembers():
  p=PurePosixPath(m.name)
  assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='runtime-review',m.name
  if m.isdir(): continue
  assert m.isfile(),m.name
  rel=Path(*p.parts[1:]);data=tf.extractfile(m).read()
  rec={'path':str(rel),'bytes':len(data),'sha256':sha(data)}
  if rel.suffix in {'.olean','.ilean'}:
   objects.append(rec);continue
  dest=runt/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);copied.append(rec)
ind.mkdir(parents=True,exist_ok=True)
shutil.copyfile(archive,ind/archive.name)
shutil.copyfile(BASE/'runtime-review/delivery/package-manifest.json',ind/'runtime-archive-manifest.json')
semfiles=[]
for f in sorted((BASE/'semantic-review').rglob('*')):
 if f.is_dir(): continue
 assert f.is_file() and not f.is_symlink(),str(f)
 rel=f.relative_to(BASE/'semantic-review');dest=sem/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
 semfiles.append({'path':str(rel),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
assert sha((runt/'FROZEN_REVIEW.md').read_bytes())=='88d76f25613603ff4780bcc62f0a2fe26491c2e7aac47849d3e3aaa7f7c0dc25'
assert sha((sem/'FINAL_SEMANTIC_REVIEW.md').read_bytes())=='fd6d2769a200e8849873679acd851c672837297a49f15b765f1b1eed9f5f4879'
writej(ind/'COPY_MANIFEST.json',{'frozen_source_commit':FROZEN,'runtime_readable_records':copied,'runtime_compiled_objects_preserved_in_archive_only':objects,'semantic_records':semfiles,'complete_runtime_archive':{'path':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes())},'all_copied_records_byte_identical':True,'no_Lean_source_or_checker_changed':True})
readme=(PKG/'README.md').read_text()
old='Status: **LEAN_CHECKED**. A complete fresh author build and public axiom audit passed. Frozen-source independent semantic review, independent full-closure rebuild and repository integration are pending at this source checkpoint.'
new='Status: **INDEPENDENTLY_REVIEWED**. Genuine nonauthor semantic review and independent full-closure rebuilding both passed on frozen source '+FROZEN+'. All five mathematical modules and the canonical checker remain byte-identical to that commit. Repository integration remains pending with the designated integration owner.'
assert old in readme;readme=readme.replace(old,new)
readme=readme.replace('Its public export scan is supplemented by a separate nonauthor module-origin audit before final acceptance.','Its public export scan has been supplemented by the completed independent nonauthor module-origin audit described below.')
old='Five baseline/fixture compiler objects were removed only after their hashes were recorded; this did not change the source or proof acceptance policy.'
new='A historical cleanup receipt reported removing five regenerable baseline/fixture compiler objects after recording their hashes. A later approved filesystem read found all five original paths present with matching hashes and timestamps; the reason for the different observations is unknown. Both observations are retained in evidence/independent/runtime/cleanup-observation-correction.json. No lasting deletion or space recovery is asserted. The accepted fresh build did not import any of those objects.'
assert old in readme;readme=readme.replace(old,new)
readme=readme.replace('Genuine nonauthor ownership and runtime specialists perform the semantic and execution reviews.','Genuine nonauthor ownership and runtime specialists completed the semantic and execution reviews.')
section='''## Completed independent acceptance

The [semantic review](evidence/independent/semantic/FINAL_SEMANTIC_REVIEW.md) by the genuine nonauthor ownership_scout checks the exact original parity sums, all quantifiers, full-word conventions, and the literal source-sum adapters. Its verdict is PASS with no semantic blocker. Its finite Python design comparisons are diagnostics, not the universal proof. This reviewer did not execute Lean.

The [execution review](evidence/independent/runtime/FROZEN_REVIEW.md) by the genuine nonauthor runtime_scout rebuilt all five project modules from committed sources using official Lean 4.19.0 with --trust=0 -j1 -DElab.async=false. It reused no previous project objects. The prebuilt official Lean/Init/Std runtime is explicitly pinned and was not rebuilt.

The independent gate printed all 69 explicit public declarations and their axioms. It separately enumerated and issued #print axioms for all 174 declarations originating in the five modules: 123 safe declarations, including 14 private safe declarations, plus 51 generated compiler implementation declarations. All safe declarations depend only on propext, Classical.choice, Quot.sound, or none. All 51 generated implementation declarations have empty axiom lists. No project mathematical axiom was introduced.

Complete original review logs, failed infrastructure attempts, source snapshots, audit code, compiler hashes, exact public signatures and inventories are preserved in the readable review trees and the [unchanged runtime archive](evidence/independent/runtime-review-e8d706dc.tar.gz). COPY_MANIFEST.json records every copied file and the compiled objects retained inside that archive.

[BUILD_REGISTRY.json](BUILD_REGISTRY.json) is scoped integration metadata for this five-module project. It does not declare repository-wide coverage or replace the actual strict checker and independent gate. [COVERAGE.json](COVERAGE.json) updates the inspected claim ledger while retaining explicit census gaps; earlier census states remain in the development archive and Git history. [PUBLICATION.json](PUBLICATION.json) records the exact local/remote commit-tree correspondence.

'''
readme=readme.replace('## Scope, provenance and status\n',section+'## Scope, provenance and status\n')
(PKG/'README.md').write_text(readme)
build=json.loads((PKG/'BUILD.json').read_text());build['status']='INDEPENDENTLY_REVIEWED';build['frozen_source_commit']=FROZEN
build['independent_review']={'semantic':{'status':'PASS','reviewer':'/root/ownership_scout','report':'evidence/independent/semantic/FINAL_SEMANTIC_REVIEW.md'},'execution':{'status':'ACCEPT_EXACT_US_CHARGE_TARGET','reviewer':'/root/runtime_scout','report':'evidence/independent/runtime/FROZEN_REVIEW.md','project_modules_rebuilt':5,'explicit_public_exports':69,'origin_declarations':174,'safe_declarations':123,'safe_private_declarations':14,'compiler_implementation_declarations':51,'official_standard_runtime_rebuilt':False}}
writej(PKG/'BUILD.json',build)
mods={}
for n in NAMES:
 data=(PKG/(n+'.lean')).read_bytes()
 mods[n]={'path':REL+'/'+n+'.lean','sha256':sha(data),'git_blob':hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest(),'imports':[l[7:].strip() for l in data.decode().splitlines() if l.startswith('import ')]}
writej(PKG/'BUILD_REGISTRY.json',{'schema_version':1,'toolchain':{'release':'leanprover/lean4:v4.19.0','compiler_commit':'6caaee842e94','allowed_axioms':['propext','Classical.choice','Quot.sound'],'strict_flags':['--trust=0','-j1','-DElab.async=false']},'catalogue_complete':False,'catalogue_blockers':['This contribution is not a completed repository-wide accepted-source census.','Main integration and shared registry reconciliation remain assigned to the integration owner.'],'projects':{'agent15-spectral-carry-charge':{'scope':'Exact original integer U/S charge of full binary outgoing words: zero iff reversal, with literal odd/even source-sum bridges.','status':'INDEPENDENTLY_REVIEWED','frozen_source_commit':FROZEN,'roots':['ChargeControls'],'modules':mods,'acceptance_checker':REL+'/check.py','independent_review':REL+'/evidence/independent/runtime/FROZEN_REVIEW.md'}},'claims':[{'id':'A15-SPEC-002','project':'agent15-spectral-carry-charge','status':'INDEPENDENTLY_REVIEWED','endpoints':['P196.Agent15.SpectralCarry.carryCharge_zero_iff','P196.Agent15.SpectralCarry.odd_source_charge_zero_iff','P196.Agent15.SpectralCarry.even_source_charge_zero_iff','P196.Agent15.SpectralCarry.sumFirst_eq_range_sum']}],'integration_note':'The shared verify_project runner was not executed for this contribution. This compatible registry is metadata; strict acceptance rests on the actual canonical check.py run and independent full-origin gate. No shared registry was modified.'})
coverage=json.loads(Path('/workspace/scratch/43cf6e114472/scout/coverage.json').read_text())
coverage['agent']='Agent 15 / coverage_scout census with attributed root status reconciliation'
coverage['verification_level']='Per-claim status: A15-SPEC-002 independently reviewed; corpus incomplete.'
coverage['inventory_complete']=False;coverage['formalization_complete']=False
for c in coverage['claims']:
 if c['id']=='A15-SPEC-002':
  c.update({'disposition':'INDEPENDENTLY_REVIEWED','verification_status':'PASS exact semantic review and independent fresh five-module trust=0 build; all 174 origin declarations audited.','accepted_lean_identifiers':['P196.Agent15.SpectralCarry.carryCharge_zero_iff','P196.Agent15.SpectralCarry.odd_source_charge_zero_iff','P196.Agent15.SpectralCarry.even_source_charge_zero_iff'],'owning_agent':'Agent 15','task_id':'agent15-spectral-carry-charge-43cf6e114472','contribution_branch':'formalize/agent-15/spectral-carry-charge-43cf6e114472','frozen_source_commit':FROZEN,'pull_request':145,'remaining_obligations':['Repository integration and shared accepted-registry reconciliation by the designated integration owner.'],'next_action':'Hand reviewed PR #145 to the integration owner; preserve exact source and both reviews.'})
 if c['id']=='A15-SPEC-007':
  c.update({'disposition':'ACTIVE_FORMALIZATION','verification_status':'Owned by Agent 14; this ledger does not certify the separate proof.','owning_agent':'Agent 14','task_id':'agent14-carryfree-residue-saturation-20261016','claim_commit':'bdfdc25c3158b81e6c6e40109886cdf80c744e57','task_blob':'8912d279695f7f298e0b1bcde5e612660e13ae5f','next_action':'Do not duplicate the protected Agent 14 carryfree saturation scope.'})
 if c['id']=='A15-SPEC-010':
  c.update({'disposition':'ACTIVE_FORMALIZATION','verification_status':'Protected contract and checked source published; independent support reviews in progress.','owning_agent':'Agent 15','task_id':'agent15-spectral-carry-support-43cf6e114472','contribution_branch':'formalize/agent-15/spectral-carry-support-43cf6e114472','claim_commit':'3de89d0bd03534c92f65886a29b7996525571ff5','frozen_source_commit':'5d02e88f13f59f6fcd09cf75d8c7f188c6645727','next_action':'Complete canonical driver and both independent reviews of the exact eight-module actual-carry closure.'})
coverage['recommended_next_action']='Integrate reviewed A15-SPEC-002 through its owner and complete protected A15-SPEC-010; retain census gaps and recheck coordination before another claim.'
coverage['status_reconciliation']={'source_commit':FROZEN,'original_census_unchanged_in':'evidence/development-evidence.tar.gz','review_reports':['evidence/independent/semantic/FINAL_SEMANTIC_REVIEW.md','evidence/independent/runtime/FROZEN_REVIEW.md'],'repository_wide_completion':False}
writej(PKG/'COVERAGE.json',coverage)
writej(PKG/'PUBLICATION.json',{'repository':'taco-jpg/p196-algorithm','branch':'formalize/agent-15/spectral-carry-charge-43cf6e114472','pull_request':145,'checkpoints':[{'kind':'protected_contract','local_commit':'135de23538cc85bcdac0b8dfe2f30c5c8d9b0e2c','remote_commit':'11327eb55b30df752e4c3fe7cb337a2d0a22f2bf','identical_tree':'91e201931cc97ef13f2691cf79e0f06ff4faa2c2'},{'kind':'complete_checked_source_and_author_evidence','local_commit':'449c2deaed4dbd098280ea097bc6faba9485c392','remote_commit':FROZEN,'identical_tree':'2d447634e0ff42b4275d34bfb169101bba0ed130'}],'source_freeze':{'remote_commit':FROZEN,'mathematical_modules_unchanged':NAMES,'canonical_checker_unchanged':True},'current_checkpoint_kind':'Independent review evidence and status metadata only; exact local/remote tree checked before publication.','git_transport':'Local commits use the workspace Git identity. Authorized GitHub connector commits have different IDs, mapped by identical tree IDs. No local commit is claimed to be remote.','main_write_slot_claimed':False,'repository_integration':'Pending designated integration owner.'})
verify_source()
print(json.dumps({'status':'PACKAGED','runtime_readable_files':len(copied),'runtime_objects_in_archive':len(objects),'semantic_files':len(semfiles),'archive_bytes':archive.stat().st_size,'frozen_sources_and_checker_unchanged':True}))
