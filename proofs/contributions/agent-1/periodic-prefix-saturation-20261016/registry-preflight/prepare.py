#!/usr/bin/env python3
"""Source-only exact registry preflight; never a Lean verification receipt."""
from pathlib import Path
import hashlib,json,re,shutil,sys,time

ROOT=Path('/workspace/p196-agent1-prefix-saturation-20261016')
PROOFS=ROOT/'proofs'
HERE=PROOFS/'contributions/agent-1/periodic-prefix-saturation-20261016/registry-preflight'
REGISTRY=PROOFS/'Agent1PeriodicInitialUnsaturated.registry.json'
NEW=['Agent1PeriodicPrefix','Agent1PeriodicSaturation','Agent1PeriodicInitialUnsaturated']
PRIORS=['Agent1PeriodicReturnClock.registry.json','Agent1PeriodicReturnCore.registry.json','Agent2SaturatedProfile.registry.json']
PROJECT='agent1-periodic-prefix-saturation'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')

def code_only(s):
    # Preserve offsets/newlines while masking nested Lean comments and strings.
    a=list(s);i=0;depth=0;string=False
    while i<len(s):
        if depth:
            if s.startswith('/-',i):a[i:i+2]='  ';depth+=1;i+=2
            elif s.startswith('-/',i):a[i:i+2]='  ';depth-=1;i+=2
            else:
                if s[i]!='\n':a[i]=' '
                i+=1
        elif string:
            if s[i]=='\\':
                a[i]=' ';i+=1
                if i<len(s):a[i]=' ';i+=1
            else:
                if s[i]=='"':string=False
                if s[i]!='\n':a[i]=' '
                i+=1
        elif s.startswith('/-',i):a[i:i+2]='  ';depth=1;i+=2
        elif s.startswith('--',i):
            while i<len(s) and s[i]!='\n':a[i]=' ';i+=1
        elif s[i]=='"':a[i]=' ';string=True;i+=1
        else:i+=1
    assert not depth and not string,'Unterminated comment/string'
    return ''.join(a)

author_checked='--author-checked' in sys.argv[2:]
assert len(sys.argv) in (2,3) and (len(sys.argv)==2 or sys.argv[2]=='--author-checked')
assert all((PROOFS/(mod+'.lean')).is_file() for mod in NEW), 'Await all three actual new sources'
run=HERE/sys.argv[1];assert run.parent==HERE;run.mkdir(parents=True,exist_ok=False)
shutil.copy2(Path(__file__),run/'prepare.py')
started=time.time();prior_sources={};origins=[];duplicates=[]
for name in PRIORS:
    raw=(PROOFS/name).read_bytes();d=json.loads(raw)
    origins.append({'path':'proofs/'+name,'sha256':sha(raw)})
    for project in d['projects'].values():
        for mod,e in project['modules'].items():
            pin={k:e[k] for k in ['path','sha256','git_blob','imports']}
            if mod in prior_sources:
                assert all(prior_sources[mod][k]==pin[k] for k in ['sha256','git_blob','imports']),('Conflicting prior content pins',mod,name)
                assert (ROOT/prior_sources[mod]['path']).read_bytes()==(ROOT/pin['path']).read_bytes(),('Conflicting alias bytes',mod)
                duplicates.append({'module':mod,'registry':'proofs/'+name,'content_identical':True,'selected_path':prior_sources[mod]['path'],'alternate_path':pin['path'],'paths_identical':prior_sources[mod]['path']==pin['path']})
            else:prior_sources[mod]=pin

aliases=[d for d in duplicates if not d['paths_identical']]
baselines=json.loads((HERE/'baseline-readback.json').read_text())
claimraw=(HERE/'agent1-periodic-prefix-saturation-20261016.json').read_bytes();claim=json.loads(claimraw)
for name in NEW:assert 'proofs/'+name+'.lean' in claim['intended_source_files']
assert 'proofs/Agent1PeriodicInitialUnsaturated.registry.json' in claim['intended_source_files']

captures={};modules={};visiting=set();order=[];hits=[]
def visit(mod):
    if any(mod==p or mod.startswith(p+'.') for p in ['Std','Init','Lean']) or mod in modules:return
    assert mod not in visiting,('Import cycle',mod)
    visiting.add(mod)
    path='proofs/'+mod+'.lean' if mod in NEW else prior_sources[mod]['path']
    raw=(ROOT/path).read_bytes();code=code_only(raw.decode());captures[path]=raw
    imports=[]
    for match in re.finditer(r'^\s*import\s+([^\n]+)',code,re.M):imports.extend(match[1].split())
    e={'path':path,'sha256':sha(raw),'git_blob':blob(raw),'imports':imports}
    if mod not in NEW:assert e==prior_sources[mod],('Current source differs from prior pin',mod,e,prior_sources[mod])
    for token in ['sorry','admit','sorryAx','native_decide','axiom','implemented_by','extern','unsafe','ofReduceBool','trustCompiler']:
        for m in re.finditer(r'\b'+re.escape(token)+r'\b',code):
            hits.append({'module':mod,'token':token,'line':code[:m.start()].count('\n')+1})
    for dep in imports:visit(dep)
    visiting.remove(mod);modules[mod]=e;order.append(mod)
visit('Agent1PeriodicInitialUnsaturated')
assert set(NEW)<=set(modules),'A claimed new module is outside actual root closure'
assert not hits,('Disallowed source tokens',hits)

endpoints={};declarations={}
for mod in NEW:
    raw=captures[modules[mod]['path']];code=code_only(raw.decode())
    assert re.findall(r'^namespace\s+([^\n]+)',code,re.M)==['Agent1.Periodic']
    endpoints[mod]=['Agent1.Periodic.'+n for n in re.findall(r'^theorem\s+(\w+)',code,re.M)]
    declarations[mod]=[{'kind':k,'name':'Agent1.Periodic.'+n} for k,n in re.findall(r'^(theorem|def|abbrev|structure)\s+(\w+)',code,re.M)]
    assert endpoints[mod],('No actual public theorem found',mod)
    (run/(mod+'.lean')).write_bytes(raw)

scope=('Necessary actual three-column projection of the original maximal period-four quotient, followed by reuse of the existing checked saturated eight-state prefix profile. '
       'For positive complete-tuple returns from period [14,14,4,4], derive strict unsaturation and positive gain G with clock=8G, signed shift=G, and 16G<N<=32G, hence N>=17. '
       'No generic saturation/profile reproof, odd-control balance, arbitrary graph realization, safety closure, saved outside-17/8 witness rejection, cycle existence or 196 conclusion.')
registry={'schema_version':1,'catalogue_complete':False,
    'catalogue_blockers':[f'Scoped {len(modules)}-module contribution registry; not a repository-wide accepted catalogue.',
        'PROVISIONAL source-only snapshot: all three author freezes/audits and complete combined fresh verification remain pending.'],
    'toolchain':{'version':'4.19.0','commit':'6caaee842e94','allowed_axioms':['propext','Classical.choice','Quot.sound']},
    'projects':{PROJECT:{'scope':scope,'roots':['Agent1PeriodicInitialUnsaturated'],'modules':modules}},
    'claims':[{'id':'A1-PERIODIC-PREFIX-SATURATION-'+mod.removeprefix('Agent1Periodic').upper(),'project':PROJECT,'endpoints':eps} for mod,eps in endpoints.items()],
    'source_baseline':baselines['combined']['resolved']['sha'],
    'prior_clock_source':baselines['clock']['resolved']['sha'],
    'merged_dependency_source':baselines['return_core']['resolved']['sha'],
    'source_pin_origins':origins,'logical_alias_resolution':aliases,
    'accepted_global_registry_modified':False,'verification_status':'PROVISIONAL_SOURCE_PREFLIGHT_ONLY',
    'metadata_validation':{'exact_actual_import_dfs':True,'module_count':len(modules),'new_module_count':len(NEW),
        'new_public_theorem_count':sum(map(len,endpoints.values())),'matching_duplicate_prior_pins':len(duplicates),
        'source_tokens_checked':['sorry','admit','sorryAx','native_decide','axiom','implemented_by','extern','unsafe','ofReduceBool','trustCompiler'],
        'source_token_hits':hits,'lean_execution_performed_by_this_preflight':False,
        'claim_commit':'8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2','claim_git_blob':blob(claimraw),'claim_sha256':sha(claimraw)}}
if author_checked:
    freeze_raw=(HERE/'author-confirmation.json').read_bytes()
    freeze=json.loads(freeze_raw)
    assert freeze['all_three_author_confirmations_received'] is True
    assert freeze['all_three_compiles']=='PASS' and freeze['all_three_new_module_audits']=='PASS'
    for mod,pin in freeze['frozen_sources'].items():assert modules[mod]['sha256']==pin
    assert set(freeze['frozen_sources'])==set(NEW)
    for receipt in freeze['author_receipts']:
        assert sha((ROOT/receipt['path']).read_bytes())==receipt['sha256']
    registry['catalogue_blockers'][1]='All three new modules have completed strict author compilation and full new-module audits. Complete parent and independent fresh combined verification remain pending.'
    if freeze.get('published_foundation_commit'):
        registry['published_combined_foundation']=freeze['published_foundation_commit']
    registry['verification_status']='FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING'
    registry['author_verification']={'all_three_new_module_compiles':'PASS',
        'all_three_new_module_origin_audits':'PASS','fresh_combined_verification':'PENDING',
        'evidence_path':str((HERE/'author-confirmation.json').relative_to(ROOT)),
        'evidence_sha256':sha(freeze_raw),'qualification':'Receipts inspected and exact author confirmations retained; this metadata run executes no Lean.'}
    (run/'author-confirmation.json').write_bytes(freeze_raw)
assert all((ROOT/path).read_bytes()==raw for path,raw in captures.items()),'Sources changed during preflight'
save(run/'registry.json',registry);shutil.copy2(run/'registry.json',REGISTRY)
report={'status':'SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN' if author_checked else 'SOURCE_PREFLIGHT_PASS_PROVISIONAL','started_at_epoch':started,'finished_at_epoch':time.time(),
    'command':['python3',str(Path(__file__))]+sys.argv[1:],'cwd':str(Path.cwd()),
    'script_sha256':sha(Path(__file__).read_bytes()),'registry_sha256':sha(REGISTRY.read_bytes()),
    'module_count':len(modules),'exact_dfs_order':order,'new_public_theorems':endpoints,
    'new_public_declarations':declarations,'duplicate_prior_pin_matches':duplicates,
    'alias_resolution':aliases,'source_scan_hits':hits,'source_snapshots_stable_during_run':True,
    'qualification':'Source metadata only. No Lean build or axiom audit executed; no publication or accepted global registry mutation.'}
save(run/'report.json',report)
print(json.dumps({k:report[k] for k in ['status','registry_sha256','module_count','new_public_theorems','source_scan_hits']},indent=2))
