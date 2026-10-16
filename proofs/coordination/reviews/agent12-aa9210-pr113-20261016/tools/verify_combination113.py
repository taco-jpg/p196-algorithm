#!/usr/bin/env python3
"""Exact PR113 temporary integration tree, preservation, and audit binding.
No checkout, branch/ref update, commit creation, remote write, or Lean execution.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--review-root',type=Path,required=True)
parser.add_argument('--repo',type=Path,required=True)
parser.add_argument('--base',required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--object-directory',type=Path,required=True)
parser.add_argument('--alternate-object-directory',type=Path,required=True)
args=parser.parse_args()
if args.output.exists(): raise SystemExit('Output must not already exist: '+str(args.output))
if re.fullmatch('[0-9a-f]{40}',args.base) is None: raise SystemExit('Base must be a full commit SHA')
ROOT=args.review_root.resolve()
OUT=args.output.resolve()
REPO=args.repo.resolve()
SELECTED=ROOT/'selected-source'
FRESH=ROOT/'fresh-complete-001'
B=args.base
H='cd11afd68833051c81051df22573e8827ab6b671'
D='43259106e755d501ca88819f373e0a6c1bff3f05'
REG='proofs/Agent105InverseBoundaries9df76b.registry.json'
VER='proofs/verify_project__214bf7673efe116b.py'
PROJECT='agent105-inverse-boundaries-9df76b'
ARCHIVE=ROOT.parent/'agent12-review113-evidence.tar.xz'
SEALED_SHA='79c54d861e734b7c305fecb3eb8bfdd5b2b2a94cd4469d6c30df43f8437a7ef9'
ENV_OVERRIDES={'GIT_OBJECT_DIRECTORY':str(args.object_directory.resolve()),
 'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(args.alternate_object_directory.resolve()),
 'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'}
ENV=dict(os.environ,**ENV_OVERRIDES)
COMMANDS=[]

def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def putjson(name,data): (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def demand(condition,message):
 if not condition: raise RuntimeError(message)
def run(label,parts,input_data=None,allowed_exit_codes=(0,)):
 argv=['git','-C',str(REPO),'-c','gc.auto=0','-c','maintenance.auto=false',*parts]
 started=time.monotonic(); p=subprocess.run(argv,input=input_data,capture_output=True,env=ENV)
 n=f'logs/{len(COMMANDS):03d}-{label}'
 (OUT/(n+'.stdout')).write_bytes(p.stdout); (OUT/(n+'.stderr')).write_bytes(p.stderr)
 c={'argv':argv,'environment_overrides':ENV_OVERRIDES,'exit_code':p.returncode,
 'elapsed_seconds':round(time.monotonic()-started,6),'stdout_file':n+'.stdout','stdout_sha256':sha(p.stdout),
 'stderr_file':n+'.stderr','stderr_sha256':sha(p.stderr),'allowed_exit_codes':list(allowed_exit_codes)}
 if input_data is not None: c.update(stdin_bytes=len(input_data),stdin_sha256=sha(input_data),stdin_git_blob=blob(input_data))
 COMMANDS.append(c);putjson('commands.json',COMMANDS)
 demand(p.returncode in allowed_exit_codes,f'Command failed ({p.returncode}): {argv!r}; all output retained.')
 return p.stdout

def tree(label,ref):
 entries={}
 for raw in run(label,['ls-tree','-r','-z',ref]).split(b'\0'):
  if not raw: continue
  info,path=raw.split(b'\t',1);mode,kind,oid=info.decode().split();p=path.decode('utf-8')
  demand(p not in entries,'Duplicate tree path: '+p)
  entries[p]={'mode':mode,'type':kind,'git_object':oid}
 putjson(label+'.json',entries);return entries

def copy_input(src,relative):
 target=OUT/'bound-evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
 return {'path':str(src),'retained_copy':str(target.relative_to(OUT)),'bytes':src.stat().st_size,'sha256':sha(src.read_bytes())}

def main():
 OUT.mkdir(parents=True,exist_ok=False)
 demand(not (OUT/'receipt.json').exists(),'Refusing to overwrite a completed receipt')
 (OUT/'logs').mkdir(exist_ok=False)
 demand(sha(ARCHIVE.read_bytes())==SEALED_SHA,'Initial sealed review archive has changed')
 scope=json.loads((ROOT/'scope-delta.json').read_text());fresh=json.loads((FRESH/'verification.json').read_text())
 review=json.loads((ROOT/'REVIEW_RECEIPT.json').read_text())
 demand(sha((FRESH/'verification.json').read_bytes())=='d3869c4926405e763aeee62f8cd0be7dab1c34067fd7b01d84b2cd6ce5ad0233','Fresh receipt differs from the sealed accepted result')
 demand(scope['status']=='PASS' and scope['head']==H and scope['base']==D,'Wrong approved source scope')
 allowed={r['path']:r for r in scope['files']}
 demand(len(allowed)==65 and all(r['status']=='A' for r in scope['files']),'Scope is not 65 unique additions')
 demand(fresh['status']=='PASS_EXACT_SOURCE_COMPLETE_CLOSURE' and fresh['source_commit']==H,'Fresh audit did not pass exact H')
 putjson('invocation.json',{'argv':sys.argv,'auditor':'Agent #12 /root/review109',
 'base':B,'head':H,'dependency_merge':D,'started_utc':datetime.now(timezone.utc).isoformat(),
 'environment_overrides':ENV_OVERRIDES,'remote_mutations':False,'ref_mutations':False,
 'note':'Only isolated temporary Git objects are written. This checks the fixed requested B, not whether B remains the live main tip.'})
 copy_input(Path('/workspace/scratch/aa9210d02a75/agent12-integration/verify_combination.py'),'reference-helper.py')
 run('git-version',['--version'])
 run('fetch-fixed-base',['-c','fetch.writeCommitGraph=false','fetch','--no-write-fetch-head','--no-tags','origin',B])
 demand(run('resolve-base',['rev-parse',B+'^{commit}']).decode().strip()==B,'Wrong base commit')
 demand(run('resolve-head',['rev-parse',H+'^{commit}']).decode().strip()==H,'Wrong head commit')
 run('head-ancestor',['merge-base','--is-ancestor',H,B],allowed_exit_codes=(0,1))
 contained=COMMANDS[-1]['exit_code']==0
 ancestors=run('merge-bases',['merge-base','--all',B,H]).decode().splitlines()
 base=tree('base-tree',B);head=tree('head-tree',H);dependency=tree('dependency-tree',D)
 # Determine owned scope from the genuine dependency merge, not one arbitrarily selected merge base.
 owned_existing=set(allowed)&set(base)
 demand(owned_existing==set(allowed) if contained else not owned_existing,'Partial or non-ancestral preexisting owned paths require explicit review')
 expected_additions=set() if contained else set(allowed)
 prior_diff={p for p in dependency.keys()|head.keys() if dependency.get(p)!=head.get(p)}
 demand(prior_diff==set(allowed),'Head changes after genuine dependency merge differ from approved 65-path set')
 demand(all(p not in dependency for p in allowed),'Owned scope contains a modification, not solely additions')
 # Populate only isolated object storage using already reviewed, content-addressed bytes.
 source_files=set(allowed)|{x['path'] for x in fresh['sources'].values()}|{REG,VER}
 staged=[]
 for i,path in enumerate(sorted(source_files)):
  data=(SELECTED/path).read_bytes();entry=head[path]
  demand(entry['type']=='blob' and blob(data)==entry['git_object'],'Source bytes do not match H: '+path)
  if path in allowed:
   demand(sha(data)==allowed[path]['sha256'] and len(data)==allowed[path]['bytes'],'Scope manifest mismatch: '+path)
  oid=run('stage-reviewed-blob-'+str(i),['hash-object','-w','--stdin'],data).decode().strip()
  demand(oid==entry['git_object'],'Unexpected staged object for '+path)
  staged.append({'path':path,'git_blob':oid,'sha256':sha(data),'bytes':len(data)})
 putjson('temporary-staged-blobs.json',staged)
 merged=run('merge-tree',['merge-tree','--write-tree',B,H]);(OUT/'merge-tree.stdout').write_bytes(merged)
 lines=merged.decode().splitlines();demand(len(lines)==1 and re.fullmatch('[0-9a-f]{40}',lines[0]) is not None,'Nontrivial merge-tree output requires review')
 T=lines[0];combined=tree('combined-tree',T)
 if contained: demand(combined==base,'Ancestor combination is not exactly the base tree')
 deleted=sorted(base.keys()-combined.keys())
 changed=sorted(p for p in base.keys()&combined.keys() if base[p]!=combined[p])
 added=sorted(combined.keys()-base.keys())
 mismatched=sorted(p for p in allowed if combined.get(p)!=head.get(p))
 inherited=sorted((set(head)-set(allowed))&set(base))
 nonowned_head_missing=sorted((set(head)-set(allowed))-set(base))
 checks={'deleted_base_paths':deleted,'changed_existing_base_paths':changed,
 'unexpected_additions':sorted(set(added)-expected_additions),'missing_owned_additions':sorted(expected_additions-set(added)),
 'owned_paths_not_identical_to_head':mismatched,'nonowned_head_paths_absent_from_base':nonowned_head_missing,
 'effective_additions':added,'all_base_entries_preserved':not deleted and not changed}
 putjson('preservation-checks.json',checks)
 demand(not any([deleted,changed,checks['unexpected_additions'],checks['missing_owned_additions'],mismatched,nonowned_head_missing]),'Combination preservation/scope failure; stop, no waiver')
 putjson('preserved-inherited-head-paths.json',[{'path':p,'base_entry':base[p],
 'head_entry':head[p],'combined_entry':combined[p],'head_equals_base':head[p]==base[p]} for p in inherited])
 inventory=[]
 for i,path in enumerate(added):
  entry=combined[path];data=run('incoming-blob-'+str(i),['cat-file','blob',entry['git_object']])
  demand(data==(SELECTED/path).read_bytes(),'Combined incoming bytes mismatch: '+path)
  inventory.append({'path':path,'base_entry':None,'head_entry':head[path],'combined_entry':entry,
   'bytes':len(data),'sha256':sha(data)})
 putjson('incoming-inventory.json',inventory)
 (OUT/'owned-submitted.patch').write_bytes(run('owned-submitted-patch',['diff','--no-ext-diff','--no-textconv','--binary','--full-index',D,H]))
 (OUT/'effective.patch').write_bytes(run('effective-patch',['diff','--no-ext-diff','--no-textconv','--binary','--full-index',B,T]))
 patches_equal=(OUT/'owned-submitted.patch').read_bytes()==(OUT/'effective.patch').read_bytes()
 if contained: demand((OUT/'effective.patch').stat().st_size==0,'Contained combination has a nonempty effective patch')
 else: demand(patches_equal,'Actual patch differs from owned submitted patch')
 regdata=run('combined-registry',['cat-file','blob',combined[REG]['git_object']]);registry=json.loads(regdata)
 demand(regdata==(SELECTED/REG).read_bytes() and sha(regdata)==fresh['registry_sha256'],'Registry changed')
 project=registry['projects'][PROJECT]
 endpoints=[e for c in registry['claims'] if c['project']==PROJECT for e in c['endpoints']]
 demand(len(endpoints)==38 and endpoints==fresh['endpoints'] and project['roots']==fresh['roots'],'Public exports/roots changed')
 demand(set(project['modules'])==set(fresh['sources']) and len(project['modules'])==9,'Module closure changed')
 closure=[]
 for i,(module,item) in enumerate(project['modules'].items()):
  path=item['path'];compiled=fresh['sources'][module];entry=combined[path]
  data=run('closure-blob-'+str(i),['cat-file','blob',entry['git_object']]);snapshot=(FRESH/compiled['source_snapshot']).read_bytes()
  demand(all(item[k]==compiled[k] for k in ['path','sha256','git_blob','imports']),'Registry/compiled mapping mismatch: '+module)
  demand(data==snapshot==(SELECTED/path).read_bytes(),'Combined/compiled source mismatch: '+module)
  demand(sha(data)==item['sha256'] and blob(data)==item['git_blob'] and head[path]==entry,'Closure identity failure: '+module)
  is_old=path not in allowed
  demand((path in base)==(is_old or contained),'Incorrect inherited/new source classification: '+module)
  if is_old or contained: demand(base[path]==entry,'Existing module changed: '+module)
  closure.append({'module':module,**item,'bytes':len(data),'classification':'preserved inherited source' if is_old else 'new owned source',
   'base_entry':base.get(path),'head_entry':head[path],'combined_entry':entry,'fresh_compiled_snapshot':compiled['source_snapshot'],
   'fresh_snapshot_sha256':sha(snapshot),'exact_compiled_bytes_match':True})
 putjson('closure-binding.json',closure)
 demand(sum(c['classification']=='preserved inherited source' for c in closure)==5,'Expected five inherited sources')
 verifierdata=run('canonical-verifier',['cat-file','blob',combined[VER]['git_object']])
 demand(base[VER]==head[VER]==combined[VER] and verifierdata==(SELECTED/VER).read_bytes(),'Canonical verifier changed')
 demand(sha(verifierdata)=='c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a','Unexpected canonical verifier digest')
 evidence=[]
 for relative in ['REVIEW_RECEIPT.json','SEMANTIC_REVIEW.md','scope-delta.json','source-provenance.json','AUDIT_REPAIR.json','replay-complete.py','auditor-support.py']:
  evidence.append(copy_input(ROOT/relative,relative))
 for p in sorted((FRESH/'source').glob('*.lean')): evidence.append(copy_input(p,str(Path('fresh-complete-001/source')/p.name)))
 evidence.append(copy_input(FRESH/'verification.json','fresh-complete-001/verification.json'))
 for c in fresh['commands']:
  log=FRESH/c['log'];demand(sha(log.read_bytes())==c['log_sha256'],'Fresh command log changed: '+c['label'])
  demand(c['exit_code']==0,'Fresh command did not pass: '+c['label'])
  if c['label'] in fresh['sources'] or c['label']=='CompleteIndependentAudit':
   demand(all(flag in c['argv'] for flag in ['--trust=0','-j1','-DElab.async=false']),'Fresh command missing strict flags')
  evidence.append(copy_input(log,str(Path('fresh-complete-001')/c['log'])))
 demand(sha((ROOT/'replay-complete.py').read_bytes())==fresh['auditor_driver_sha256'],'Fresh driver changed')
 demand(sha((ROOT/'auditor-support.py').read_bytes())==fresh['auditor_support_sha256'],'Fresh audit support changed')
 demand(sha((FRESH/'source/CompleteIndependentAudit.lean').read_bytes())==fresh['audit_source_sha256'],'Fresh audit source changed')
 demand(sha(ARCHIVE.read_bytes())==SEALED_SHA,'First sealed archive changed during combination check')
 putjson('evidence-binding.json',evidence)
 receipt={'schema_version':1,'status':'PASS_ALREADY_CONTAINED_IDENTITY_WITH_FRESH_AUDIT_BINDING' if contained else 'PASS_EXACT_ADDITIVE_COMBINATION_WITH_FRESH_AUDIT_BINDING',
 'auditor':'Agent #12 /root/review109; independent subagent, not a separate account',
 'classification':'ALREADY_CONTAINED_IDENTITY_COMBINATION' if contained else 'NOT_CONTAINED_EXACT_ADDITIVE_COMBINATION',
 'head_is_ancestor_of_base':contained,'ancestry_check_exit_code':0 if contained else 1,
 'checked_at':datetime.now(timezone.utc).isoformat(),'base':B,'head':H,'combined_tree':T,'merge_bases':ancestors,
 'genuine_dependency_merge':D,'base_entry_count':len(base),'head_entry_count':len(head),
 'combined_entry_count':len(combined),'owned_additions_count':len(allowed),'effective_additions_count':len(added),
 'preserved_main_entries_count':len(base),'preserved_inherited_head_paths_count':len(inherited),
 'deleted_count':len(deleted),'changed_existing_count':len(changed),'unexpected_additions_count':len(checks['unexpected_additions']),
 'owned_paths_same_as_head':True,'patch_equals_genuine_dependency_to_head_delta':patches_equal,
 'closure_modules':9,'preserved_inherited_modules':5,'new_modules_in_reviewed_contribution':4,'effective_module_additions':0 if contained else 4,'public_exports':38,
 'registry_path':REG,'registry_sha256':sha(regdata),'canonical_verifier_path':VER,'canonical_verifier_sha256':sha(verifierdata),
 'closure_binding_sha256':sha((OUT/'closure-binding.json').read_bytes()),'fresh_verification_sha256':sha((FRESH/'verification.json').read_bytes()),
 'fresh_lean_execution_in_this_supplement':False,'fresh_lean_execution_reused_from':'fresh-complete-001',
 'reuse_reason':'All nine combined-tree source bytes, registry mapping, roots, imports and 38 endpoints equal the exact fresh compiled and audited snapshots. Canonical verifier remains byte-identical. Complete original command/log hashes are rebound.',
 'fresh_theorem_count':fresh['theorem_count'],'fresh_safe_definition_count':fresh['safe_definition_count'],
 'fresh_axiom_union':fresh['axiom_union_literal'],'first_sealed_archive':str(ARCHIVE),'first_sealed_archive_sha256_before_and_after':SEALED_SHA,
 'remote_mutations':False,'ref_mutations':False,'actual_merge_performed':False,'current_remote_main_freshness_asserted':False,
 'scope_limit':'Acceptance concerns this fixed B/H tree only. Parent must refresh the main tip before any eventual integration; no claim that the repository-wide unrelated proofs were replayed.',
 'helper_sha256':sha(Path(__file__).read_bytes()),'helper_path':str(Path(__file__).resolve())}
 copy_input(Path(__file__),'executed-combination-helper.py')
 putjson('receipt.json',receipt)
 print(json.dumps(receipt,indent=2))

if __name__=='__main__':
 try: main()
 except BaseException as e:
  putjson('failure.json',{'status':'FAILED_STOPPED','exception':repr(e),'traceback':traceback.format_exc(),'commands_completed':len(COMMANDS)})
  raise
