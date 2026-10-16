import json,hashlib,re,pathlib
root=pathlib.Path('/dev/shm/p196-agent19-session22f4/pr100-integration')
data=json.loads((root/'INPUT.json').read_text())
pins=json.loads("{\"proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/Lychrel196Research.lean\":\"c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506\",\"proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-108/modular-autonomy/AutonomyDefs.lean\":\"612b161844a0effa5730d17b7d048315619578e8\",\"proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-108/modular-autonomy/LeadingWitness.lean\":\"ea7d29fb554197848986ac50ce6f85e4a3200bed\"}")
rows=[]
for p,s in data['files'].items():
 b=(root/'source'/p).read_bytes()
 h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert h==s['git_blob']
 rows.append({'path':p,'size':len(b),'git_blob':h,'sha256':hashlib.sha256(b).hexdigest(),'origin':'PR100 added'})
for p,expected in pins.items():
 b=(root/'source'/p).read_bytes()
 h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert h==expected,(p,h,expected)
 rows.append({'path':p,'size':len(b),'git_blob':h,'sha256':hashlib.sha256(b).hexdigest(),'origin':'Pinned original archive dependency'})
raw=(root/'CI-job-117215196347.log').read_text()
clean=re.sub(r'\x1b\[[0-9;]*m','',raw)
clean=re.sub(r'^\ufeff?\d{4}-\d{2}-\d{2}T[^ ]+ ','',clean,flags=re.M)
mods=re.findall(r'^COMPILING (\w+)\s*$',clean,re.M)
assert mods==['Lychrel196Research','AutonomyDefs','LeadingWitness','CylinderImage','CylinderNoContinuity'],mods
assert 'Lean (version 4.19.0' in clean
assert 'lean-4.19.0-linux.tar.zst: OK' in clean
assert 'e909f26954ec52d30863cfe2c388c1527ca0de75' in clean
assert '--trust=0 -j1 -DElab.async=false' in clean
allowed={'propext','Classical.choice','Quot.sound'}
public=['occurs_for_leading_digit','any_occurrence_has_leading_digit','occurs_iff_nine_residues','source_units_excluded','two_distinct_cylinder_outputs','no_local_mod10_constancy']
matches=re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]",clean,re.M)
audits={}
for name,axs in matches:
 vals=sorted(x.strip() for x in axs.split(',') if x.strip())
 assert set(vals)<=allowed,(name,vals)
 audits.setdefault(name,[]).append(vals)
receipts={}
for n in public:
 k='Agent112.CylinderImage.'+n
 assert k in audits and len(audits[k])==2,(k,audits.get(k))
 assert audits[k][0]==audits[k][1]
 receipts[k]=audits[k][-1]
assert data['ci_run']['head_sha']==data['head'] and data['ci_run']['conclusion']=='success'
assert len(data['ci_jobs']['jobs'])==1 and data['ci_jobs']['jobs'][0]['id']==117215196347
assert data['ci_jobs']['jobs'][0]['conclusion']=='success'
report={'schema_version':1,'reviewer':'Agent #19 / session22f4dcaef0db','source_head':data['head'],'status':'PASS_EXISTING_AUTHOR_CI_BINDING','source_inventory':rows,'added_files':8,'added_bytes':sum(x['size'] for x in rows if x['origin']=='PR100 added'),'compiled_modules':mods,'existing_execution':{'run_id':38972865528,'job_id':117215196347,'event':'push','conclusion':'success','trust':0,'flags':['--trust=0','-j1','-DElab.async=false'],'lean':'4.19.0 commit6caaee842e94','official_release_sha256':'6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe'},'public_axiom_receipts':receipts,'raw_job_log_sha256':hashlib.sha256((root/'CI-job-117215196347.log').read_bytes()).hexdigest(),'source_bindings':'All eleven fetched file bytes matched exact published Git blob; five compiler inputs match workflow guards. The fresh hosted build and exact endpoint audits are retained author CI, not new execution by Agent19.','independent_review':'Agent104 existing completed review ownership preserved; actual final package/publication still requested.','new_Lean_execution':'NOT_RUN','repository_wide_build_claim':False,'source_mutation':False}
(root/'CI_SOURCE_BINDING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
